import pandas as pd
import time
import random
# Função para calcular a média móvel
def moving_average(data, window_size):
    return data['temperature'].rolling(window=window_size).mean()

# Função para detectar outliers utilizando a média móvel
def detect_outliers_moving_avg(data, window_size=3, threshold=2.5):
    data['moving_avg'] = moving_average(data, window_size)
    data['is_outlier_moving_avg'] = abs(data['temperature'] - data['moving_avg']) > threshold
    return data

# Simulação de leituras de temperatura a cada 2 segundos
def simulate_sensor_data(num_samples):
    sensor_data = []
    for i in range(num_samples):
        if i == 3 or i == 7 or i == 9:  # Introduzindo anomalias nas amostras 3, 7 e 9
            temperature = 50.0 + 10 * random.random()  # Temperatura anômala entre 50.0°C e 60.0°C
        else:
            temperature = 40.0 + random.random()  # Temperatura normal entre 40.0°C e 41.0°C

        sensor_data.append({'timestamp': pd.Timestamp.now(), 'temperature': temperature})
        time.sleep(2)  # Espera 2 segundos entre cada amostra

    return pd.DataFrame(sensor_data)

# Geração de dados de temperatura a cada 2 segundos
sensor_data = simulate_sensor_data(10)
print("Dados de sensores de temperatura coletados:")
print(sensor_data)

# Detecta outliers utilizando média móvel
sensor_data = detect_outliers_moving_avg(sensor_data)

# Printa todos os dados com a detecção de outliers
print("\nDados com detecção de anomalias:")
print(sensor_data[['timestamp', 'temperature', 'moving_avg', 'is_outlier_moving_avg']])
