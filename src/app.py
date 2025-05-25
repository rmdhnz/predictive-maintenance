#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from src.utils.time_to_freq import arus_to_frekuensi
# ----- 1. Generate data dummy dan simpan ke CSV -----

def app() : 
  fs = 1000       # Sampling frequency 1000 Hz
  t = np.linspace(0, 1, fs, endpoint=False)  # 1 detik data

  # Sinyal arus motor normal: frekuensi utama 50 Hz
  current_normal = 10 + 2 * np.sin(2*np.pi*50*t) + 0.5*np.random.randn(fs)

  # Sinyal arus motor rusak: frekuensi utama 50 Hz + harmonik 150 Hz (kerusakan)
  current_faulty = 10 + 2 * np.sin(2*np.pi*50*t) + 1.5 * np.sin(2*np.pi*150*t) + 0.5*np.random.randn(fs)

  # Gabungkan jadi dataset (label: 0 normal, 1 rusak)
  data_list = []
  for i in range(100):  # 100 sample normal
      noise = 0.2 * np.random.randn(fs)
      data_list.append({'time': t, 'current': current_normal + noise, 'label': 0})
  for i in range(100):  # 100 sample rusak
      noise = 0.2 * np.random.randn(fs)
      data_list.append({'time': t, 'current': current_faulty + noise, 'label': 1})

  # Karena dataframe tidak bisa simpan array di kolom, kita simpan per sample sebagai file CSV terpisah atau numpy
  # Untuk contoh sederhana kita skip simpan file dan proses langsung di memory

  # ----- 2. Fungsi FFT & ekstrak fitur -----

  def extract_features(signal, fs):
      N = len(signal)
      fft_vals = np.fft.fft(signal)
      fft_freq = np.fft.fftfreq(N, 1/fs)
      
      # Ambil magnitudo spektrum untuk frekuensi positif saja
      pos_mask = fft_freq >= 0
      freqs = fft_freq[pos_mask]
      mags = np.abs(fft_vals[pos_mask]) * 2 / N  # normalisasi
      
      # Ekstrak amplitudo di frekuensi utama dan harmonik penting
      def get_amplitude_at(freq):
          idx = np.argmin(np.abs(freqs - freq))
          return mags[idx]
      
      features = [
          get_amplitude_at(50),    # frek utama
          get_amplitude_at(150),   # harmonik 3x
          get_amplitude_at(250),   # harmonik 5x
          np.mean(mags),           # rata-rata amplitudo spektrum
          np.std(mags),            # std deviasi spektrum
      ]
      return features

  # ----- 3. Buat dataset fitur dan label -----

  X = []
  y = []

  for sample in data_list:
      feats = extract_features(sample['current'], fs)
      X.append(feats)
      y.append(sample['label'])

  X = np.array(X)
  y = np.array(y)

  # ----- 4. Split data, scaling dan training NN -----

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

  scaler = StandardScaler()
  X_train_scaled = scaler.fit_transform(X_train)
  X_test_scaled = scaler.transform(X_test)

  mlp = MLPClassifier(hidden_layer_sizes=(50,), max_iter=500, random_state=42)
  mlp.fit(X_train_scaled, y_train)

  # ----- 5. Evaluasi -----

  y_pred = mlp.predict(X_test_scaled)
  print(classification_report(y_test, y_pred))

  # ----- 6. Visualisasi contoh sinyal dan spektrum -----

  plt.figure(figsize=(12,5))

  plt.subplot(1,2,1)
  plt.plot(t, current_normal)
  plt.title('Sinyal Arus Motor Normal')
  plt.xlabel('Waktu (detik)')
  plt.ylabel('Arus (A)')

  plt.subplot(1,2,2)
  plt.plot(t, current_faulty)
  plt.title('Sinyal Arus Motor Rusak')
  plt.xlabel('Waktu (detik)')
  plt.ylabel('Arus (A)')

  plt.tight_layout()
  plt.show()
