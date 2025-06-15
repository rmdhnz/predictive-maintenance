import torch
import torch.nn as nn


class MotorFaultNN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(MotorFaultNN, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim),
        )

    def forward(self, x):
        return self.model(x)
