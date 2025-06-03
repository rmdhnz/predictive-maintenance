#!/usr/bin/env python3

from model.MotorModel import MotorModel
from model.MotorBRB3mm import MotorBRB3mm
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
from core.Autoencoder import Autoencoder
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import time
from datetime import datetime
from utils.Utilities import Utilities


def app():
    start_time = time.time()
    motor_model = MotorBRB3mm("motor_brb_current_3mm")
    data = motor_model.findAll(panda=True)
    df_data = Utilities.fft_current_by_load(data)

    for load in df_data["load"].unique():
        df_plot = df_data[df_data["load"] == load]
        plt.plot(
            df_plot["frequency"], df_plot["current_magnitude"], label=f"Load {load}%"
        )

    plt.xlabel("Frekuensi (Hz)")
    plt.ylabel("Magnitudo FFT")
    plt.title("Spektrum Frekuensi Arus per Beban")
    plt.legend()
    plt.grid()
    plt.show()

    fft_db_df = Utilities.fft_current_db_by_load(data)
    for load in fft_db_df["load"].unique():
        df_load = fft_db_df[fft_db_df["load"] == load]
        plt.plot(df_load["frequency"], df_load["magnitude_db"], label=f"Load {load}%")

        # Tandai peak
        peaks = df_load[df_load["is_peak"]]
        plt.scatter(peaks["frequency"], peaks["magnitude_db"], color="red")
    plt.xlabel("Frekuensi (Hz)")
    plt.ylabel("Magnitudo (dB)")
    plt.title("Spektrum Frekuensi Arus Motor Induksi (dB)")
    plt.legend()
    plt.grid()
    plt.xlim(0, 100)
    plt.show()
