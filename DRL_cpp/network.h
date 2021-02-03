/*
	This file contains a neural network module for us to
	define our actor and critic networks in PPO.
*/

#pragma once

#include <torch/torch.h>
#include <math.h>

struct NN_modelImpl : public torch::nn::Module 
{
	/*
		A standard in_dim-64-64-out_dim Feed Forward Neural Network.
		
		Parameter : n_in, n_out, parameters of NN_net
		
		Returns : None
		
	*/

	torch::nn::Linear ac1_, ac2_, ac3_,
					  cr1_, cr2_, cr3_, cr_val_;

	torch::Tensor mu_, log_std_;

	torch::Tensor val_;
	
	NN_modelImpl(int64_t n_in, int64_t n_out, double std)
		:
			// Construct and register two Linear submodules.
			
			//actor
			ac1_(torch::nn::Linear(n_in, 64)),
			ac2_(torch::nn::Linear(64, 64)),
			ac3_(torch::nn::Linear(64, n_out)),
			mu_(torch::full(n_out, 0.)),
			log_std_(torch::full(n_out, std)),
			
			// Critic
			cr1_(torch::nn::Linear(n_in, 64)),
			cr2_(torch::nn::Linear(64, 64)),
			cr3_(torch::nn::Linear(64, n_out)),
			cr_val_(torch::nn::Linear(n_out, 1)) 
			{
				
				//actor
				register_module("ac1", ac1_);
				register_module("ac2", ac2_);
				register_module("ac3", ac3_);
				register_parameter("log_std", log_std_);

				//critic
				register_module("cr1", cr1_);
				register_module("cr2", cr2_);
				register_module("cr3", cr3_);
				register_module("cr3", cr_val_);
				
  			}
	
    torch::Tensor forward(torch::Tensor obs) {

		//actor
    	mu_ = torch::relu(ac1_->forward(obs));
    	mu_ = torch::relu(ac2_->forward(mu_));
    	mu_ = torch::tanh(ac3_->forward(mu_));

		//critic
		val_ = torch::relu(cr1_->forward(obs));
        val_ = torch::relu(cr2_->forward(val_));
        val_ = torch::tanh(cr3_->forward(val_));
        val_ = cr_val_->forward(val_);

		// returning values of actor and critic
		//BECAUSE : while training sample(Exploration) and while testing mean value
		if (this->is_training()) 
        {
            torch::NoGradGuard no_grad;

            torch::Tensor action = at::normal(mu_, log_std_.exp().expand_as(mu_));
            return std::make_tuple(action, val_);  
        }
        else 
        {
            return std::make_tuple(mu_, val_);  
        }
    }

	 void normal(double mu, double std) 
    {
        torch::NoGradGuard no_grad;

        for (auto& p: this->parameters()) 
        {
            p.normal_(mu,std);
        }         
    }

    auto entropy() -> torch::Tensor
    {
        // Differential entropy of normal distribution. For reference https://pytorch.org/docs/stable/_modules/torch/distributions/normal.html#Normal
        return 0.5 + 0.5*log(2*M_PI) + log_std_;
    }

    auto log_prob(torch::Tensor action) -> torch::Tensor
    {
        // Logarithmic probability of taken action, given the current distribution.
        torch::Tensor var = (log_std_+log_std_).exp();

        return -((action - mu_)*(action - mu_))/(2*var) - log_std_ - log(sqrt(2*M_PI));
    }
};

TORCH_MODULE(NN_model);
