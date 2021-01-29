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

	torch::nn::Linear fc1{nullptr}, fc2{nullptr}, fc3{nullptr};
	
	NN_modelImpl(int64_t n_in, int64_t n_out) {
    // Construct and register two Linear submodules.
    fc1 = register_module("fc1", torch::nn::Linear(n_in, 64));
    fc2 = register_module("fc2", torch::nn::Linear(64, 64));
    fc3 = register_module("fc3", torch::nn::Linear(64, n_out));
  }
	
    torch::Tensor forward(torch::Tensor obs) {
    	obs = torch::relu(fc1->forward(obs));
    	obs = torch::relu(fc2->forward(obs));
    	obs = fc3->forward(obs);
    	return obs;
  }
  
};

TORCH_MODULE(NN_model);
