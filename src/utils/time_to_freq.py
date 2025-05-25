#!/usr/bin/env python3
import numpy as np
import pandas as pd

def arus_to_frekuensi(csv_file, col_current='current', col_time='time'):
    df = pd.read_csv(csv_file)

    current = df[col_current].values
    time = df[col_time].values


    dt = np.mean(np.diff(time))
    fs = 1.0 / dt

    N = len(current)
    fft_vals = np.fft.fft(current)
    fft_freqs = np.fft.fftfreq(N, d=dt)
    mask = fft_freqs >= 0
    freqs = fft_freqs[mask]
    magnitudes = np.abs(fft_vals[mask]) * 2 / N 

    return freqs, magnitudes
