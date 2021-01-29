/*
	The file contains the PPO class to train with.
*/

#include <fstream>
#include <Eigen/Core>
#include <torch/torch.h>
#include <random>

#include <iostream>
#include <list>
#include <tuple>
#include "network.h"
#include "environment.h"

//#include "ProximalPolicyOptimization.h"
//#include "TestEnvironment.h"

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
			
	ENV env;
	uint obs_dim = env.obs_dim; //env.observation_space;	// .size(0)
	uint act_dim = env.act_dim; //env.action_space;			// .size(0)
	uint crit_dim = env.crit_dim;

	NN_model actor(uint obs_dim, uint act_dim);
	NN_model critic(uint obs_dim, uint crit_dim);   // output represent only value of state
	
auto learn(int64_t total_t_train) 
{

	 for (int t_train = 0; t_train < total_t_train; total_t_train++) {
   		//body
    }
}

struct hyperparameters
{
			/*
				Initialize default and custom values for hyperparameters
					Parameters:
						hyperparameters - the extra arguments included when creating the PPO model, 
						should only include hyperparameters defined below with custom values.
					Return:
						None
			*/
	public:
		int total_t_batch = 4800;          // timesteps per batch
    	int total_t_episode = 1600;        // timesteps per episode
};


auto PPO::rollout()
{
	hyperparameters hyparam;

	std::vector<torch::Tensor> batch_obs;
	std::vector<torch::Tensor> batch_acts;
	std::vector<torch::Tensor> batch_log_probs;
	std::vector<std::vector<torch::Tensor>> batch_rews;
	std::vector<torch::Tensor> batch_rtgs;
	std::vector<torch::Tensor> batch_lens;
	torch::Tensor ep_length = torch::zeros({1}, torch::kF64);

	for(int t_batch = 0; t_batch < hyparam.total_t_batch; hyparam.total_t_batch++) {
		
		auto obs = env.get_obs();		// vector of obs
		bool done = false;
		
		std::vector<torch::Tensor> ep_rews;

		for(int t_episode = 0; t_episode < hyparam.total_t_episode; hyparam.total_t_episode++) {

			// getting initial obs
			batch_obs.push_back(obs);
			
			// |s -> a -> ns -> r -> done|
			// (1). action and log probability (2). rewards, new_obs, done
			auto action = env.get_action();
			auto feedback = env.step();

			// collecting into batches (~replay buffer if saved)
			ep_rews.push_back(std::get<0>(feedback));
    		batch_acts.push_back(std::get<0>(action));
    		batch_log_probs.push_back(std::get<1>(action)); 
			
			if (done) {
				ep_length[0] = t_episode+1;
				break;
			}
			
			ep_length[0] = t_episode+1;

		}
		
		
		//collect the batch-length
		batch_lens.push_back(ep_length);
		batch_rews.push_back(ep_rews);
	}
}


auto PPO::returns(std::vector<torch::Tensor>& rewards, 
				  std::vector<torch::Tensor>& done, 
				  std::vector<torch::Tensor>& vals, 
				  double gamma, 
				  double lambda) -> std::vector<torch::Tensor>
{
    // Compute the returns.
    torch::Tensor gae = torch::zeros({1}, torch::kFloat64);
    std::vector<torch::Tensor> returns(rewards.size(), torch::zeros({1}, torch::kFloat64));

    for (uint i=rewards.size();i-- >0;) // inverse for loops over unsigned: https://stackoverflow.com/questions/665745/whats-the-best-way-to-do-a-reverse-for-loop-with-an-unsigned-index/665773
    {
        // Advantage.
        auto delta = rewards[i] + gamma*vals[i+1]*(1-dones[i]) - vals[i];
        gae = delta + gamma*lambda*(1-dones[i])*gae;

        returns[i] = gae + vals[i];
    }

    return returns;
}

};
