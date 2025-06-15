#!/usr/bin/env python3

from model.MotorModel import MotorModel
from model.MotorBRB3mm import MotorBRB3mm
from model.MotorBRB7mm import MotorBRB7mm
import matplotlib.pyplot as plt
import time
from utils.Utilities import Utilities
import pandas as pd


def app():
    start_time = time.time()
    motor_model = MotorModel()
    exit()
    motor_brb_3 = MotorBRB3mm("motor_brb_current_3mm")
    motor_brb_7 = MotorBRB7mm("motor_brb_current_7mm")
    data_normal = motor_model.findAll(panda=True)
    data_brb_3mm = motor_brb_3.findAll(panda=True)
    data_brb_7mm = motor_brb_7.findAll(panda=True)
    df_normal = Utilities.fft_current_db_by_load(data_normal, status=0)
    df_brb_3mm = Utilities.fft_current_db_by_load(data_brb_3mm, status=1)
    df_brb_7mm = Utilities.fft_current_db_by_load(data_brb_7mm, status=2)
    # df_data = pd.concat([df_normal, df_brb_3mm, df_brb_7mm], ignore_index=True)
    df_data = df_normal
    plt.figure(figsize=(10, 6))
    for i, load in enumerate(df_data["load"].unique(), start=1):
        df_load = df_data[df_data["load"] == load]
        plt.subplot(3, 1, i)
        plt.plot(df_load["frequency"], df_load["magnitude_db"], label=f"Load {load}%")
        plt.xlabel("Frekuensi")
        plt.ylabel("Magnitude")
        plt.title(f"Spektrum Frekuensi arus - Load {load}%")
        plt.grid(True)
        plt.xlim(45, 55)
        plt.legend()
    plt.tight_layout()
    plt.show()

    exit()
    fft_db_df = Utilities.fft_current_db_by_load(data, label=0)
    print(fft_db_df)
    plt.figure(figsize=(10, 6))
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
    plt.xlim(40, 60)
    plt.ylim(-70, 0)
    plt.show()
