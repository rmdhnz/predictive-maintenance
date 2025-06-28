from datetime import datetime
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt


class Utilities:

    @staticmethod
    @staticmethod
    def plot_time_domain(data: pd.DataFrame, subplot=False):
        data["time_sec"] = pd.to_timedelta("00:" + data["time"]).dt.total_seconds()
        plt.figure(figsize=(10, 6))
        if subplot:
            for i, load in enumerate(data["percent_load"].unique()):
                df_load = data[data["percent_load"] == load]
                plt.subplot(3, 1, i + 1)
                plt.plot(df_load["time_sec"], df_load["current"], label=f"Load {load}%")
                plt.xlabel("Time")
                plt.ylabel("Current")
                plt.title("Grafik Domain Waktu")
                plt.grid(True)
                plt.legend()
        else:
            for load in data["percent_load"].unique():
                # Filter data untuk load tertentu
                df_load = data[data["percent_load"] == load]

                # Plot current vs time untuk load tertentu dalam satu grafik
                plt.plot(
                    df_load["time_sec"],
                    df_load["current"],
                    label=f"Load {load}%",
                    color=(
                        "tab:blue"
                        if load == 0
                        else "tab:green" if load == 50 else "tab:red"
                    ),
                )

            # Set labels dan judul
            plt.xlabel("Time (s)")
            plt.ylabel("Current (A)")
            plt.title("Current vs Time for Different Load Percentages")
            plt.grid(True)
            plt.legend()

        plt.tight_layout()
        plt.show()

    @staticmethod
    def time_to_seconds(t_str):
        t = datetime.strptime(t_str, "%M:%S.%f")
        return t.minute * 60 + t.second + t.microsecond / 1e6

    @staticmethod
    def fft_current_by_load(data: pd.DataFrame, label):
        time_seconds = data["time"].apply(Utilities.time_to_seconds) #ambil data waktu dan masukkan ke time_to_seconds
        time_seconds = time_seconds - time_seconds.iloc[0]
        data["time_sec"] = time_seconds
        loads = data["percent_load"].unique()
        result_list = []

        for load in loads:
            df_load = data[data["percent_load"] == load].copy()
            df_load = df_load.sort_values(by="time_sec")
            t = df_load["time_sec"].values
            i = df_load["current"].values
            # Sampling frequency
            dt = np.mean(np.diff(t))
            if dt <= 0:
                raise ValueError(
                    "Sampling interval (dt) is not positive! Check time order."
                )
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
                    "percent_load": load,
                    "label": label,
                }
            )
            result_list.append(df_result)
        return pd.concat(result_list, ignore_index=True)

    @staticmethod
    def fft_current_db_by_load(data, label=None, reference=None):
        time_seconds = data["time"].apply(Utilities.time_to_seconds)
        time_seconds = time_seconds - time_seconds.iloc[0]
        data = data.copy()
        data["time_sec"] = time_seconds

        loads = data["percent_load"].unique()
        result_list = []

        all_amplitudes = []

        for load in loads:
            df_load = data[data["percent_load"] == load].copy()
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
            df_load = data[data["percent_load"] == load].copy()
            t = df_load["time_sec"].values
            dt = np.mean(np.diff(t))
            fs = 1 / dt
            N = len(df_load)

            f = fs * np.arange(0, N // 2 + 1) / N

            mag_db = 20 * np.log10(
                amplitudes / reference + 1e-12
            )  # +1e-12 untuk menghindari log(0)

            df_result = pd.DataFrame(
                {
                    "frequency": f,
                    "magnitude_db": mag_db,
                    "percent_load": load,
                    "label": label,
                }
            )

            if label is None:
                df_result.drop("label", axis=1, inplace=True)

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
    def add_time_sec(data: pd.DataFrame, replace=False):
        time_normal = data["time"].apply(Utilities.time_to_seconds)
        time_normal = time_normal - time_normal.iloc[0]
        data = data.copy()
        data["time_sec"] = time_normal
        if replace:
            data.drop(columns=["time"], inplace=True)
            return data
        return data
    
    @staticmethod
    def sideband_freq(Nr):
        f_fund =50
        k = 1
        Ns = 1500
        s = (Ns - Nr) / Ns
        f1 = (1 - 2*k*s) * f_fund   # lower side-band
        f2 = (1 + 2*k*s) * f_fund   # upper side-band
        return s, (f1, f2)
    
    @staticmethod
    def amplitude_at(freq_vector, mag_db_vector, target_freq, tol=0.2):
        idx = np.argmin(np.abs(freq_vector - target_freq))
        if abs(freq_vector[idx] - target_freq) <= tol:
            return mag_db_vector[idx]
        else:
            return np.nan 
        
    @staticmethod     
    def sideband_amplitudes(Nr_dict,freq, mag_db, load_percent):
        _, (f1, f2) = Utilities.sideband_freq(Nr_dict[load_percent])
        amp1 = Utilities.amplitude_at(freq, mag_db, f1)
        amp2 = Utilities.amplitude_at(freq, mag_db, f2)
        return pd.Series({
            "load_%": load_percent,
            "f_lower": f1,  "amp_lower": amp1,
            "f_upper": f2,  "amp_upper": amp2
        })

