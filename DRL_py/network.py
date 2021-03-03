"""
	This file contains a neural network module for us to
	define our actor and critic networks in PPO.
"""

import torch
from torch import nn
import torch.nn.functional as F
import numpy as np


class FCCA(nn.Module):

    def __init__(self, input_dim, output_dim, hidden_dims=(64, 64), activation_fc=F.relu):
        super(FCCA, self).__init__()
        self.activation_fc = activation_fc
        self.env_min = 1
        self.env_max = 1

        self.input_layer = nn.Linear(input_dim[0], hidden_dims[0])
        self.hidden_layers = nn.ModuleList()
        for i in range(len(hidden_dims) - 1):
            hidden_layer = nn.Linear(hidden_dims[i], hidden_dims[i + 1])
            self.hidden_layers.append(hidden_layer)
        self.output_layer_mean = nn.Linear(hidden_dims[-1], self.env_max)
        self.output_layer_log_std = nn.Linear(hidden_dims[-1], self.env_max)

    def forward(self, states):
        x = self._format(states)
        x = self.activation_fc(self.input_layer(x))
        for hidden_layer in self.hidden_layers:
            x = self.activation_fc(hidden_layer(x))
        x_mean = self.output_layer_mean(x)
        x_log_std = self.output_layer_log_std(x)

        return x_mean, x_log_std

    @torch.jit.export
    def _format(self, states):
        x = states
        if not isinstance(x, torch.Tensor):
            x = torch.tensor(x, device=self.device, dtype=torch.float32)
            if len(x.size()) == 1:
                x = x.unsqueeze(0)
        return x

    @torch.jit.ignore
    def get_predictions(self, states, actions):
        states, actions = self._format(states), self._format(actions)
        mean_ac, std_ac = self.forward(states)
        dist = torch.distributions.Normal(mean_ac, std_ac.exp())
        logpas = dist.log_prob(actions)
        entropies = dist.entropy()
        return logpas, entropies

    @torch.jit.ignore
    def select_greedy_action(self, states):
        mean_ac, std_ac = self.forward(states)
        return np.argmax(mean_ac.detach().squeeze().cpu().numpy())


class FCV(nn.Module):
    """
        A standard in_dim-64-64-out_dim Feed Forward Neural Network for Critic.
        Init and methods input : in_dim, out_dim, states
    """

    def __init__(self, input_dim, hidden_dims=(32, 32), activation_fc=F.relu):
        super(FCV, self).__init__()
        self.activation_fc = activation_fc

        self.input_layer = nn.Linear(input_dim[0], hidden_dims[0])
        self.hidden_layers = nn.ModuleList()
        for i in range(len(hidden_dims) - 1):
            hidden_layer = nn.Linear(hidden_dims[i], hidden_dims[i + 1])
            self.hidden_layers.append(hidden_layer)
        self.output_layer = nn.Linear(hidden_dims[-1], 1)

    def _format(self, states):
        x = states
        if not isinstance(x, torch.Tensor):
            x = torch.tensor(x, device=self.device, dtype=torch.float32)
            if len(x.size()) == 1:
                x = x.unsqueeze(0)
        return x

    def forward(self, states):
        x = self._format(states)
        x = self.activation_fc(self.input_layer(x))
        for hidden_layer in self.hidden_layers:
            x = self.activation_fc(hidden_layer(x))
        return self.output_layer(x).squeeze()
