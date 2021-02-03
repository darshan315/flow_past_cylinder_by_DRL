#pragma once

#include <iostream>
#include <torch/torch.h>
#include <random>
#include "network.h"

// Random engine for shuffling memory.
std::random_device rd;
std::mt19937 re(rd());
std::uniform_int_distribution<> dist(-5, 5);

class PPO
{			/*
				This is the PPO class we will use as our model in main.py
			
				Initializes the PPO model, including hyperparameters.
			
					Parameters:
						policy_class - the policy class to use for our actor/critic networks.
						env - the environment to train on.
						hyperparameters - all extra arguments passed into PPO that should be hyperparameters.
					Returns:
						None
			*/
public:	

	//classes definations

	static auto learn_agent( NN_model& nn_ac,
						TestEnvironment& env,
						hyperparameters& hyp,
						torch::optim::Optimizer& opt,
						std::ofstream& out ); -> void;

	static auto PPO::update( NN_model& nn_ac,
							torch::Tensor& states,
							torch::Tensor& actions,
							torch::Tensor& log_probs,
							torch::Tensor& returns,
							torch::Tensor& advantages, 
							torch::optim::Optimizer& opt, 
							hyperparameters& hyp ) -> void;

	static auto PPO::act_in_env_update( NN_model& nn_ac,
					 	  		 TestEnvironment& env,
								 hyperparameters& hyp,
								 int *bfs,
								 double avg_reward,
								 torch::optim::Optimizer& opt,
						  		 std::ofstream& out,
								 int cout_train );

	static auto PPO::returns( std::vector<torch::Tensor>& rewards,
				  			  std::vector<torch::Tensor>& dones,
				  			  std::vector<torch::Tensor>& values,
				  			  double gamma,
				  			  double lambda ) -> std::vector<torch::Tensor>;
	
};

	
auto PPO::act_in_env_update(NN_model& nn_ac,
					 TestEnvironment& env,
					 hyperparameters& hyp,
					 int *bfs,
					 double avg_reward,
					 torch::optim::Optimizer& opt,
					 std::ofstream& out,
					 int cout_train)
	{

		// SARS sampling
		std::vector<torch::Tensor> states;
		std::vector<torch::Tensor> actions;
		std::vector<torch::Tensor> rewards;
		std::vector<torch::Tensor> dones;

		// characteristcs of SARS
		std::vector<torch::Tensor> log_probs;
		std::vector<torch::Tensor> returns;
		std::vector<torch::Tensor> values;

		for(int t_epl = 0; t_epl < hyp.total_t_batch; t_epl++) 
		{
			// get initial state
			states.push_back(env.State());

			// feed forward in NN to get action and values
			auto av = nn_ac->forward(states[*bfs]);

			// save the values of NN
			actions.push_back(std::get<0>(av));
			values.push_back(std::get<1>(av));
			log_probs.push_back(nn_ac->log_prob(actions[*bfs]));

			// extracting action values to apply act in evn
			double x_act = actions[*bfs][0][0].item<double>();
			double y_act = actions[*bfs][0][1].item<double>();

			// acting in env ang getting next state, status
			auto sd = env.Act(x_act, y_act);

			// New state.
			rewards.push_back(env.Reward(std::get<1>(sd)));
			dones.push_back(std::get<2>(sd));

			// avaraging the rewards
			avg_reward += rewards[*bfs][0][0].item<double>()/hyp.total_t_batch;

			//output log in cmd
			out << cout_train << ", " << env.pos_(0) << ", " << env.pos_(1) << ", " << env.goal_(0) << ", " << env.goal_(1) << ", " << RESETTING << "\n";


			if (dones[*bfs][0][0].item<double>() == 1.) 
            {
                // Set new goal.
                double x_new = double(dist(re)); 
                double y_new = double(dist(re));
                env.SetGoal(x_new, y_new);

                // Reset the position of the agent.
                env.Reset();

                // episode, agent_x, agent_y, goal_x, goal_y, STATUS=(PLAYING, WON, LOST, RESETTING)
                out << cout_train << ", " << env.pos_(0) << ", " << env.pos_(1) << ", " << env.goal_(0) << ", " << env.goal_(1) << ", " << RESETTING << "\n";
            }

			*bfs+=1;

			if (*bfs%hyp.epl == 0)
            {
				printf("Updating the network.\n");
                values.push_back(std::get<1>(nn_ac->forward(states[*bfs-1])));

                returns = PPO::returns(rewards, dones, values, hyp.gamma, hyp.lambda);

                torch::Tensor t_log_probs = torch::cat(log_probs).detach();
                torch::Tensor t_returns = torch::cat(returns).detach();
                torch::Tensor t_values = torch::cat(values).detach();
                torch::Tensor t_states = torch::cat(states);
                torch::Tensor t_actions = torch::cat(actions);
                torch::Tensor t_advantages = t_returns - t_values.slice(0, 0, hyp.epl);

                PPO::update(nn_ac, t_states, t_actions, t_log_probs, t_returns, t_advantages, opt, hyp);
            
                *bfs = 0;

                states.clear();
                actions.clear();
                rewards.clear();
                dones.clear();

                log_probs.clear();
                returns.clear();
                values.clear();
            }
		}

		return avg_reward;
	}


auto PPO::returns(std::vector<torch::Tensor>& rewards,
				  std::vector<torch::Tensor>& dones,
				  std::vector<torch::Tensor>& values,
				  double gamma,
				  double lambda) -> std::vector<torch::Tensor>
	{
		// Compute the returns.
		torch::Tensor gae = torch::zeros({1}, torch::kFloat64);
		
		std::vector<torch::Tensor> returns(rewards.size(), torch::zeros({1}, torch::kFloat64));

		for (uint i=rewards.size();i-- >0;) // inverse for loops over unsigned: https://stackoverflow.com/questions/665745/whats-the-best-way-to-do-a-reverse-for-loop-with-an-unsigned-index/665773
		{
			// Advantage.
			auto delta = rewards[i] + gamma*values[i+1]*(1-dones[i]) - values[i];
			gae = delta + gamma*lambda*(1-dones[i])*gae;

			returns[i] = gae + values[i];
		}

    	return returns;
	}

auto PPO::update( NN_model& nn_ac,
                  		 torch::Tensor& states,
                 		 torch::Tensor& actions,
                 		 torch::Tensor& log_probs,
                 		 torch::Tensor& returns,
                		 torch::Tensor& advantages, 
                 		 torch::optim::Optimizer& opt, 
                 		 hyperparameters& hyp ) -> void
{
    for (uint n=0;n<hyp.n_update_per_iteration;n++)
    {
        // Generate random indices.
        torch::Tensor cpy_sta = torch::zeros({hyp.mini_batch_size, states.size(1)}, states.type());
        torch::Tensor cpy_act = torch::zeros({hyp.mini_batch_size, actions.size(1)}, actions.type());
        torch::Tensor cpy_log = torch::zeros({hyp.mini_batch_size, log_probs.size(1)}, log_probs.type());
        torch::Tensor cpy_ret = torch::zeros({hyp.mini_batch_size, returns.size(1)}, returns.type());
        torch::Tensor cpy_adv = torch::zeros({hyp.mini_batch_size, advantages.size(1)}, advantages.type());

		/*
		 Here sampling the minibatch from the whole data set
		 */

        for (uint b=0;b<hyp.mini_batch_size;b++) {
            uint idx = std::uniform_int_distribution<uint>(0, hyp.epl-1)(re);
            cpy_sta[b] = states[idx];
            cpy_act[b] = actions[idx];
            cpy_log[b] = log_probs[idx];
            cpy_ret[b] = returns[idx];
            cpy_adv[b] = advantages[idx];
        }

        auto av = nn_ac->forward(cpy_sta); // action value pairs
        auto action = std::get<0>(av);
        auto entropy = nn_ac->entropy().mean();
        auto new_log_prob = nn_ac->log_prob(cpy_act);

        auto old_log_prob = cpy_log;
        auto ratio = (new_log_prob - old_log_prob).exp();
        auto surr1 = ratio*cpy_adv;
        auto surr2 = torch::clamp(ratio, 1. - hyp.clip_param, 1. + hyp.clip_param)*cpy_adv;

        auto val = std::get<1>(av);
        auto actor_loss = -torch::min(surr1, surr2).mean();
        auto critic_loss = (cpy_ret-val).pow(2).mean();

        auto loss = 0.5*critic_loss+actor_loss-hyp.beta*entropy;

        opt.zero_grad();
        loss.backward();
        opt.step();
    }
}
auto PPO::learn_agent( NN_model& nn_ac, 
					   TestEnvironment& env, 
					   hyperparameters& hyp,
					   torch::optim::Optimizer& opt,
					   std::ofstream& out)
	{
		int bfs = 0;
		double best_avg_reward = 0.;
    	double avg_reward = 0.;

		for (int t_train = 1; t_train < hyp.total_t_train; t_train++) {			// step 2

			printf("epoch %u/%u\n", t_train, hyp.total_t_train);

			//getting batch infos			 										// step 3
			auto avg_reward_n = PPO::act_in_env_update(nn_ac, env, hyp, &bfs, avg_reward, opt, out, t_train);

			// Save the best net.
			if (avg_reward_n > best_avg_reward) {

				best_avg_reward = avg_reward_n;
				printf("Best average reward: %f\n", best_avg_reward);
				torch::save(nn_ac, "best_model.pt");
			}

			avg_reward = 0.;

			// Reset at the end of an epoch.
			double x_new = double(dist(re)); 
			double y_new = double(dist(re));
			env.SetGoal(x_new, y_new);

			// Reset the position of the agent.
			env.Reset();

			// episode, agent_x, agent_y, goal_x, goal_y, STATUS=(PLAYING, WON, LOST, RESETTING)
			out << t_train << ", " << env.pos_(0) << ", " << env.pos_(1) << ", " << env.goal_(0) << ", " << env.goal_(1) << ", " << RESETTING << "\n";
		}

		out.close();
	
	}

