from model.MotorModel import MotorModel
from model.MotorBRB3mm import MotorBRB3mm
from model.MotorBRB7mm import MotorBRB7mm
from model.TesMotor import TesMotor
from model.TesMotorBRB3 import TesMotorBRB3
from model.TesMotorBRB7 import TesMotorBRB7
from model.TesMotorBRB37 import TesMotorBRB37
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.Utilities import Utilities

data_prediksi = pd.read_csv("hasil_prediksi.csv")
model_data = TesMotorBRB3()
data_asli = model_data.findAll().panda()
label_prediksi = data_prediksi["predicted_label_id"].values
label_asli = data_asli["label_id"].values
x = range(len(label_asli))
# Buat plot
plt.figure(figsize=(12, 5))
plt.scatter(x,label_asli, label='Label Asli', color='blue', marker='o', s=30)
plt.scatter(x,label_prediksi, label='Label Prediksi', color='red', marker='x', s=30)

plt.title("Perbandingan Label Asli vs Prediksi")
plt.xlabel("Index Sampel")
plt.ylabel("Label ID")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()