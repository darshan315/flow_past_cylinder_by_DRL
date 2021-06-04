#!/usr/bin/python3

import torch

torch.set_default_tensor_type(torch.DoubleTensor)


class TestPolicy(torch.nn.Module):
    def __init__(self, n_inputs, neurons_per_layer):
        super(TestPolicy, self).__init__()
        self.linear_0 = torch.nn.Linear(n_inputs, neurons_per_layer)
        self.linear_1 = torch.nn.Linear(neurons_per_layer, neurons_per_layer)
        self.linear_2 = torch.nn.Linear(neurons_per_layer, 2)

    def forward(self, x):
        x = torch.nn.functional.relu(self.linear_0(x))
        x = torch.nn.functional.relu(self.linear_1(x))
        return self.linear_2(x)


scripted = torch.jit.script(TestPolicy(54, 20))
scripted.save("policy.pt")
policy = torch.jit.load("policy.pt")
example = torch.ones((2, 54))
output = policy(example)
print(output)

