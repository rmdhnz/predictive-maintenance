#!/usr/bin/env python3

import torch
import torch.nn as nn
import sys
import os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from utils.MotorFaultNN import MotorFaultNN
from model.DataTestModel import DataTestModel
from utils.Utilities import Utilities
import pandas as pd

model = MotorFaultNN(input_dim=4, output_dim=3)
model.load_state_dict(torch.load("model-nn/1_model_training_time_domain.pth"))
model.eval()

tes_model = DataTestModel()
data = tes_model.select("time", "current", "percent_load").panda()
# data = tes_model.findAll().panda()
df_data = Utilities.fft_current_db_by_load(data)
df_data = df_data.dropna()
df_data = df_data.apply(pd.to_numeric, errors="coerce")


Xtensor = torch.tensor(df_data.values.astype(np.float32))

with torch.no_grad():
    output = model(Xtensor)
    pred_label = min(output.argmax(dim=1))

print(f"Prediksi kerusakan label : {pred_label}")
