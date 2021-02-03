#include <torch/torch.h>
#include <iostream>
#include <list>
#include <tuple>
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

			// for acting in env and sampling batches of episodes
			int total_t_batch = 10000;         
			int total_t_train = 15;

			int epl = 2048;					   
			int buffer_setting = 0;						 
			int n_update_per_iteration = 5;        
			
			// for PPO updates
			int mini_batch_size = 512;

			double clip_param = 0.2;
			double gamma = .99;	
			double lambda = .95;
			double beta;

	};
