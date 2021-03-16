"""
	This file contains a neural network module for us to
	define our actor and critic networks in PPO.

	called in main.py
"""

import torch
from torch import nn
import torch.nn.functional as F


class FCCA(nn.Module):
    """
        A standard in_dim-64-64-out_dim Feed Forward Neural Network for policy model(Actor).
    """

    def __init__(self, input_dim, hidden_dims=(64, 64), activation_fc=F.relu):
        """
        The output layer dimensions are 2 neurons. 1st neuron in output layer represents mean value
        and 2nd neuron in output layer represents std value.

        Args:
            input_dim: input dimensions are equal to number of pressure sensors
                        sensors -> p values of patches at surface of cylinder.
            hidden_dims: 64x64
            activation_fc: neuron activation function = relu -> torch,nn.functional.F.relu
        """
        super(FCCA, self).__init__()
        # activation function for neurons
        self.activation_fc = activation_fc

        # size of mean and std value
        self.env_min = 1
        self.env_max = 1

        # input layer declaration
        self.input_layer = nn.Linear(input_dim[0], hidden_dims[0])

        # hidden layer declaration
        self.hidden_layers = nn.ModuleList()
        for i in range(len(hidden_dims) - 1):
            hidden_layer = nn.Linear(hidden_dims[i], hidden_dims[i + 1])
            self.hidden_layers.append(hidden_layer)

        # output layer containing mean and std of an action
        self.output_layer_mean = nn.Linear(hidden_dims[-1], self.env_max)
        self.output_layer_log_std = nn.Linear(hidden_dims[-1], self.env_max)

    def forward(self, states):
        """
        Feed forwarding in NN net

        Args:
            states: array or tensor containing value of pressure of patches at the surface of cylinder
                    must be (n_sensors x 1) dimensions.

        Returns:
            x_mean: mean value from 1st neuron of output layer, mean value of taken action.
            x_std: std value from 2nd neuron of output layer, std value of taken action.

        """
        # convert input data into tensor if not
        x = self._format(states)

        # feed forwards to layers
        x = self.activation_fc(self.input_layer(x))
        for hidden_layer in self.hidden_layers:
            x = self.activation_fc(hidden_layer(x))
        x_mean = self.output_layer_mean(x)
        x_log_std = self.output_layer_log_std(x)

        return x_mean, x_log_std

    @torch.jit.export
    def _format(self, states):
        """
        Class method to convert an input array to a tensor for ease of feed forward and back propagation

        Args:
            states: the array which need to convert in a tensor

        Returns:
            x: converted tensor

        """
        x = states
        if not isinstance(x, torch.Tensor):
            x = torch.tensor(x, dtype=torch.float32)
            if len(x.size()) == 1:
                x = x.unsqueeze(0)
        return x

    @torch.jit.ignore
    def get_predictions(self, states, actions):
        """
        To compute log probability of taken action and entropy of taken action from the distribution.

        Args:
            states: input array, pressure array
            actions: action array

        Returns: tensors of log probability and tensor of entropy

        """
        # get action and state tensors
        states, actions = self._format(states), self._format(actions)
        # get mean and std of action for the supplied state
        mean_ac, std_ac = self.forward(states)
        mean_ac = mean_ac.squeeze()
        std_ac = std_ac.squeeze()
        # get distribution from mean and std by feed forward
        dist = torch.distributions.Normal(mean_ac, std_ac.exp())
        # compute log probabilities and entropy
        logpas = dist.log_prob(actions)
        entropies = dist.entropy()

        return logpas, entropies


class FCV(nn.Module):
    """
        A standard in_dim-64-64-out_dim Feed Forward Neural Network for value model(Critic).
    """

    def __init__(self, input_dim, hidden_dims=(64, 64), activation_fc=F.relu):
        """
        The output layer dimensions are 1 neuron. The neuron in output layer represents value of the state.

        Args:
            input_dim: input dimensions are equal to number of pressure sensors
                        sensors -> p values of patches at surface of cylinder.
            hidden_dims: 64x64
            activation_fc: neuron activation function = relu -> torch,nn.functional.F.relu
        """
        super(FCV, self).__init__()
        # activation function for neurons
        self.activation_fc = activation_fc

        # input layer declaration
        self.input_layer = nn.Linear(input_dim[0], hidden_dims[0])

        # hidden layer declaration
        self.hidden_layers = nn.ModuleList()
        for i in range(len(hidden_dims) - 1):
            hidden_layer = nn.Linear(hidden_dims[i], hidden_dims[i + 1])
            self.hidden_layers.append(hidden_layer)

        # output layer containing neuron represent V_pi
        self.output_layer = nn.Linear(hidden_dims[-1], 1)

    def _format(self, states):
        """
        Class method to convert an input array to a tensor for ease of feed forward and back propagation

        Args:
            the array which need to convert in a tensor

        Returns:
            x: converted tensor

        """
        x = states
        if not isinstance(x, torch.Tensor):
            x = torch.tensor(x, dtype=torch.float32)
            if len(x.size()) == 1:
                x = x.unsqueeze(0)
        return x

    def forward(self, states):
        """
         Feed forwarding in NN net.

        Args:
            states: array or tensor containing value of pressure of patches at the surface of cylinder
                    must be (n_sensors x 1) dimensions.

        Returns: Tensor of an state value(value is pi_theta)

        """
        # convert input data into tensor if not
        x = self._format(states)

        # feed forwards to layers
        x = self.activation_fc(self.input_layer(x))
        for hidden_layer in self.hidden_layers:
            x = self.activation_fc(hidden_layer(x))
        return self.output_layer(x).squeeze()
