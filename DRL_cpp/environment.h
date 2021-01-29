#include <iostream>
#include <tuple>

class ENV
{
public:
	uint obs_dim = 10; //env.observation_space;	// .size(0)
	uint act_dim = 1; //env.action_space;			// .size(0)
	uint crit_dim = 1;
    
    std::tuple<torch::Tensor, torch::Tensor> get_action(){
        torch::Tensor a;

        // Multivariate Normal Distribution
        // Example : a = random from [a-0.1a, a+0.1a]

        torch::Tensor log_prob;
        return {a, log_prob};
    }

    auto get_obs() -> torch::Tensor
    {
        torch::Tensor obs;
        return obs;
    }


    std::tuple<torch::Tensor, torch::Tensor, torch::Tensor> step(){
        torch::Tensor rew;
        torch::Tensor done;
        torch::Tensor n_obs;
        return {rew, n_obs, done};
    }

};