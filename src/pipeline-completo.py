import random
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

# Simulação de dados de sensores de temperatura
def simulate_sensor_data(num_samples):
    sensor_data = []
    for i in range(num_samples):
        if i == 2 or i == 6 or i == 9:  # Introduzindo anomalias nas amostras 2, 6 e 9
            temperature = random.uniform(50.0, 60.0)  # Temperatura anômala entre 50.0°C e 60.0°C
        else:
            temperature = random.uniform(40.0, 41.0)  # Temperatura normal entre 40.0°C e 41.0°C

        sensor_data.append({'timestamp': pd.Timestamp.now(), 'temperature': temperature})
        time.sleep(2)  # Espera 2 segundos entre cada amostra

    return pd.DataFrame(sensor_data)

# Pré-processamento: Limpeza de dados
def validate_numeric(data):
    data['temperature'] = pd.to_numeric(data['temperature'], errors='coerce')
    return data.dropna(subset=['temperature'])

def validate_range(data, min_temp=-50, max_temp=50):
    return data[(data['temperature'] >= min_temp) & (data['temperature'] <= max_temp)]

def validate_time(data, time_interval=2):
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data = data.sort_values('timestamp')
    data['time_diff'] = data['timestamp'].diff().dt.total_seconds().fillna(time_interval)
    return data[data['time_diff'] <= time_interval * 1.5]

def moving_average(data, window_size=3):
    return data['temperature'].rolling(window=window_size).mean()

def weighted_moving_average(data, window_size=3):
    weights = np.arange(1, window_size + 1)
    return data['temperature'].rolling(window_size).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

def detect_outliers_weighted_avg(data, window_size=3, threshold=0.5):
    data['weighted_avg'] = weighted_moving_average(data, window_size)
    data['is_outlier_weighted_avg'] = abs(data['temperature'] - data['weighted_avg']) > threshold
    print(data)
    return data

def detect_outliers_moving_avg(data, window_size=3, threshold=2.5):
    data['moving_avg'] = moving_average(data, window_size)
    data['is_outlier_moving_avg'] = abs(data['temperature'] - data['moving_avg']) > threshold
    return data

def validate_by_historical_avg(data, historical_data, threshold=2.5):
    historical_mean = historical_data['temperature'].mean()
    historical_std = historical_data['temperature'].std()
    data['is_outlier_context'] = abs(data['temperature'] - historical_mean) > (threshold * historical_std)
    return data

# Coleta de dados
sensor_data = simulate_sensor_data(10)
print("Dados de sensores de temperatura coletados:")
print(sensor_data)

# Limpeza de dados
sensor_data = validate_numeric(sensor_data)
sensor_data = validate_range(sensor_data)
sensor_data = validate_time(sensor_data)

# Detecção de Outliers
sensor_data = detect_outliers_moving_avg(sensor_data)
sensor_data = detect_outliers_weighted_avg(sensor_data)

print("\nDados com detecção de anomalias:")
print(sensor_data[['timestamp', 'temperature', 'is_outlier_moving_avg', 'is_outlier_weighted_avg']])

# Validação Contextual (usando dados históricos simulados)
historical_data = simulate_sensor_data(15)  # Dados históricos simulados
sensor_data = validate_by_historical_avg(sensor_data, historical_data)

print("\nDados após validação contextual:")
print(sensor_data)

# Visualização simples (requer matplotlib)
plt.figure(figsize=(10, 6))
plt.plot(sensor_data['timestamp'], sensor_data['temperature'], marker='o', linestyle='-', color='b', label='Temperatura')
plt.title('Leituras de Temperatura dos Sensores')
plt.xlabel('Timestamp')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
