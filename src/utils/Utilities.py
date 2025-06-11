from datetime import datetime
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt


class Utilities:

    @staticmethod
    def time_to_seconds(t_str):
        t = datetime.strptime(t_str, "%M:%S.%f")
        return t.minute * 60 + t.second + t.microsecond / 1e6

    @staticmethod
    def fft_current_by_load(data, status):
        time_seconds = data["time"].apply(Utilities.time_to_seconds)
        time_seconds = time_seconds - time_seconds.iloc[0]
        data["time_sec"] = time_seconds
        loads = data["load"].unique()
        result_list = []

        for load in loads:
            df_load = data[data["load"] == load].copy()
            t = df_load["time_sec"].values
            i = df_load["current"].values
            # Sampling frequency
            dt = np.mean(np.diff(t))
            fs = 1 / dt
            N = len(i)

            # FFT
            Y = np.fft.fft(i)
            P2 = np.abs(Y / N)
            P1 = P2[: N // 2 + 1]
            P1[1:-1] = 2 * P1[1:-1]

            f = fs * np.arange(0, N // 2 + 1) / N
            df_result = pd.DataFrame(
                {
                    "frequency": f,
                    "current_magnitude": P1,
                    "load": load,
                    "status": status,
                }
            )
            result_list.append(df_result)
        return pd.concat(result_list, ignore_index=True)

    @staticmethod
    def fft_current_db_by_load(data, status, reference=None):
        time_seconds = data["time"].apply(Utilities.time_to_seconds)
        time_seconds = time_seconds - time_seconds.iloc[0]
        data = data.copy()
        data["time_sec"] = time_seconds

        loads = data["load"].unique()
        result_list = []

        all_amplitudes = []

        for load in loads:
            df_load = data[data["load"] == load].copy()
            t = df_load["time_sec"].values
            i = df_load["current"].values

            dt = np.mean(np.diff(t))
            fs = 1 / dt
            N = len(i)

            Y = np.fft.fft(i)
            P2 = np.abs(Y / N)
            P1 = P2[: N // 2 + 1]
            P1[1:-1] = 2 * P1[1:-1]

            all_amplitudes.append(P1)
            all_amplitudes_concat = np.concatenate(all_amplitudes)
        if reference is None:
            reference = np.max(all_amplitudes_concat)

        # Sekarang buat hasil dB per load
        for idx, load in enumerate(loads):
            amplitudes = all_amplitudes[idx]
            t_len = len(amplitudes)
            df_load = data[data["load"] == load].copy()
            t = df_load["time_sec"].values
            dt = np.mean(np.diff(t))
            fs = 1 / dt
            N = len(df_load)

            f = fs * np.arange(0, N // 2 + 1) / N

            mag_db = 20 * np.log10(
                amplitudes / reference + 1e-12
            )  # +1e-12 untuk menghindari log(0)

            df_result = pd.DataFrame(
                {"frequency": f, "magnitude_db": mag_db, "load": load, "status": status}
            )

            # Opsional: cari peak frekuensi
            peaks, _ = find_peaks(
                mag_db, height=-60
            )  # threshold -60 dB bisa disesuaikan
            df_result["is_peak"] = False
            df_result.loc[peaks, "is_peak"] = True

            result_list.append(df_result)

        result_df = pd.concat(result_list, ignore_index=True)
        return result_df

    @staticmethod
    def classify_rotor_condition(db_value):
        if db_value > 60:
            return ("Excellent", "None")
        elif 54 <= db_value <= 60:
            return ("Good", "None")
        elif 48 <= db_value < 54:
            return ("Moderate", "Trend")
        elif 42 <= db_value < 48:
            return (
                "Rotor Fracture or High Resistance Joint",
                "Increase Test Intervals and Trend",
            )
        elif 36 <= db_value < 42:
            return (
                "Two or more bars cracked or broken",
                "Confirm with motor circuit analysis",
            )
        elif 30 <= db_value < 36:
            return ("Multiple cracked or broken bars and end ring problems", "Overhaul")
        else:
            return (
                "Multiple broken rotor bars and other severe rotor problems",
                "Overhaul or Replace",
            )

    @staticmethod
    def plot_by_load(
        data: pd.DataFrame,
        title,
        xlabel,
        ylabel,
        xlim=None,
        ylim=None,
        peaks=False,
    ):
        for load in data["load"].unique():
            df_load = data[data["load"] == load]
            plt.plot(
                df_load["frequency"],
                df_load["current_magnitude"],
                label=f"Load {load}%",
            )
            if peaks:
                peak = df_load[df_load["is_peak"]]
                plt.scatter(peak["frequency"], peak["magnitude_db"], color="red")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True)
        plt.legend()
        plt.xlim(xlim)
        plt.ylim(ylim)
        plt.show()
