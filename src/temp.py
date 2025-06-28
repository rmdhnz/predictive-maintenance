
from model.MotorModel import MotorModel
from model.MotorBRB3mm import MotorBRB3mm
from model.MotorBRB7mm import MotorBRB7mm
from model.TesMotor import TesMotor
from model.TesMotorBRB3 import TesMotorBRB3
from model.TesMotorBRB7 import TesMotorBRB7
from model.TesMotorBRB37 import TesMotorBRB37
from model.TesMotorBRB77 import TesMotorBRB77
from model.MotorModel import MotorModel
import matplotlib.pyplot as plt
import time
from utils.Utilities import Utilities
import pandas as pd

def block_average(series:pd.DataFrame,n) : 
    temp = len(series) - (len(series)%n)
    return series.iloc[:temp].to_numpy().reshape(-1,n).mean(axis=1)

def app():
    motor_model = TesMotorBRB3()
    data_normal = motor_model.findAll().panda()
    # data_normal["time_sec"] = pd.to_timedelta("00:" + data_normal["time"]).dt.total_seconds()
    df_data = Utilities.fft_current_by_load(data_normal,label=1)
    print(df_data)
    plt.figure(figsize=(10, 6))
    for i, load in enumerate(df_data["percent_load"].unique(), start=1):
        df_load = df_data[df_data["percent_load"] == load]
        plt.subplot(3, 1, i)
        plt.plot(df_load["frequency"], df_load["current_magnitude"], label=f"percent_load {load}%")
        plt.xlabel("time")
        plt.ylabel("current")
        plt.title(f"Spektrum Frekuensi arus - Load {load}%")
        plt.grid(True)
        plt.xlim(0, 100)
        # plt.ylim(-70,0)
        plt.legend()
    plt.tight_layout()
    plt.show()

    fft_db_df = Utilities.fft_current_db_by_load(data_normal, label=0,reference=1)
    plt.figure(figsize=(10, 6))
    for i, load in enumerate(fft_db_df["percent_load"].unique(), start=1):
        df_load = fft_db_df[fft_db_df["percent_load"] == load]
        plt.subplot(3, 1, i)
        plt.plot(df_load["frequency"], df_load["magnitude_db"], label=f"percent_load {load}%")
        plt.xlabel("Frekuensi")
        plt.ylabel("magnitude dB")
        plt.title(f"Spektrum Frekuensi arus - Load {load}%")
        plt.grid(True)
        plt.xlim(0, 100)
        # plt.ylim(-70,0)
        plt.legend()
    plt.tight_layout()
    plt.show()


app()