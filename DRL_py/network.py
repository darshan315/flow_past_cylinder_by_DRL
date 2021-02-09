"""
	This file contains a neural network module for us to
	define our actor and critic networks in PPO.
"""

import torch
from torch import nn
import torch.nn.functional as F
import numpy as np


class FCCA(nn.Module):
	"""
		A standard in_dim-64-64-out_dim Feed Forward Neural Network for Actor.
		Init and methods input : in_dim, out_dim, states
	"""
	def __init__(self, input_dim, output_dim, hidden_dims=(64, 64), activation_fc=F.relu):
		super(FCCA, self).__init__()
		self.activation_fc = activation_fc

		self.input_layer = nn.Linear(input_dim[0], hidden_dims[0])
		self.hidden_layers = nn.ModuleList()
		for i in range(len(hidden_dims) - 1):
			hidden_layer = nn.Linear(hidden_dims[i], hidden_dims[i + 1])
			self.hidden_layers.append(hidden_layer)
		self.output_layer = nn.Linear(hidden_dims[-1], output_dim)

		device = "cpu"
		if torch.cuda.is_available():
			device = "cuda:0"
		self.device = torch.device(device)
		self.to(self.device)

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
		return self.output_layer(x)

	def np_pass(self, states):
		logits = self.forward(states)
		np_logits = logits.detach().cpu().numpy()
		dist = torch.distributions.Categorical(logits=logits)
		actions = dist.sample()
		np_actions = actions.detach().cpu().numpy()
		logpas = dist.log_prob(actions)
		np_logpas = logpas.detach().cpu().numpy()
		is_exploratory = np_actions != np.argmax(np_logits, axis=1)
		return np_actions, np_logpas, is_exploratory

	def select_action(self, states):
		logits = self.forward(states)
		dist = torch.distributions.Categorical(logits=logits)
		action = dist.sample()
		return action.detach().cpu().item()

	def get_predictions(self, states, actions):
		states, actions = self._format(states), self._format(actions)
		logits = self.forward(states)
		dist = torch.distributions.Categorical(logits=logits)
		logpas = dist.log_prob(actions)
		entropies = dist.entropy()
		return logpas, entropies

	def select_greedy_action(self, states):
		logits = self.forward(states)
		return np.argmax(logits.detach().squeeze().cpu().numpy())


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

		device = "cpu"
		if torch.cuda.is_available():
			device = "cuda:0"
		self.device = torch.device(device)
		self.to(self.device)

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
