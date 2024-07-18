import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from pydlm import dlm, trend, seasonality
import matplotlib.pyplot as plt

# Passo 1: Gerar dados simulados de temperatura
np.random.seed(42)
n = 1000
time = np.arange(n)
temperature = 20 + 2 * np.sin(2 * np.pi * time / 100) + np.random.normal(0, 1, n)

# Introduzir algumas anomalias
temperature[::50] = temperature[::50] + np.random.normal(10, 5, n // 50)

df = pd.DataFrame({'time': time, 'temperature': temperature})

# Passo 2: Aplicar Isolation Forest para detecção inicial de anomalias
model = IsolationForest(contamination=0.05)
df['anomaly'] = model.fit_predict(df[['temperature']])
df['anomaly'] = df['anomaly'].apply(lambda x: True if x == -1 else False)

# Filtrar os dados removendo anomalias
df_cleaned = df[df['anomaly'] == False]

# Passo 3: Aplicar Filtros de Kalman para estimativas em tempo real
temperature_dlm = dlm(df_cleaned['temperature']) + trend(degree=1, name='lineTrend') + seasonality(period=24, name='24hourSeason', keep=True)
temperature_dlm.fit()

# Prever os próximos valores
predictions = temperature_dlm.predictN(N=1, date=df_cleaned.index[-1])[0]
df_cleaned['predicted'] = np.append(np.full(len(df_cleaned) - 1, np.nan), predictions)

# Definir limites dinâmicos usando uma janela deslizante (rolling window)
window_size = 50
df_cleaned['rolling_mean'] = df_cleaned['temperature'].rolling(window=window_size).mean()
df_cleaned['rolling_std'] = df_cleaned['temperature'].rolling(window=window_size).std()
df_cleaned['upper_limit'] = df_cleaned['rolling_mean'] + 3 * df_cleaned['rolling_std']
df_cleaned['lower_limit'] = df_cleaned['rolling_mean'] - 3 * df_cleaned['rolling_std']

# Detecção de anomalias em tempo real
df_cleaned['real_time_anomaly'] = (df_cleaned['temperature'] > df_cleaned['upper_limit']) | (df_cleaned['temperature'] < df_cleaned['lower_limit'])

# Passo 4: Salvar os resultados em uma planilha Excel
df_cleaned.to_excel('temperature_analysis.xlsx', index=False)

# Plotar os dados
plt.figure(figsize=(14, 7))
plt.plot(df['time'], df['temperature'], label='Temperatura Original')
plt.plot(df_cleaned['time'], df_cleaned['predicted'], label='Temperatura Predita', linestyle='--')
plt.fill_between(df_cleaned['time'], df_cleaned['upper_limit'], df_cleaned['lower_limit'], color='gray', alpha=0.2, label='Limites de Confiança')
plt.scatter(df_cleaned[df_cleaned['real_time_anomaly']]['time'], df_cleaned[df_cleaned['real_time_anomaly']]['temperature'], color='red', label='Anomalias em Tempo Real')
plt.legend()
plt.xlabel('Tempo')
plt.ylabel('Temperatura')
plt.title('Detecção e Previsão de Temperatura com Limites Dinâmicos')
plt.show()
