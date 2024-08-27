import numpy as np
import matplotlib.pyplot as plt

# Função para carregar os dados do sensor
def load_sensor_data(filename):
    return np.loadtxt(filename, delimiter=',')

# Função para identificar tendências (subidas e descidas) usando a derivada
def identify_trends(data):
    derivative = np.diff(data)  # Calcula a derivada do sinal
    down_trend = derivative < 0  # Identifica descidas (derivada negativa)
    up_trend = derivative > 0    # Identifica subidas (derivada positiva)

    # Identificar descidas e subidas consecutivas de 5 ou mais valores
    consecutive_downs = []
    consecutive_ups = []

    # Identificar descidas consecutivas
    count = 0
    for i in range(len(down_trend)):
        if down_trend[i]:
            count += 1
            if count >= 5:
                # Marca os últimos 5 pontos e continua marcando enquanto a descida continua
                consecutive_downs.extend(range(i - count + 1, i + 1))
        else:
            count = 0

    # Identificar subidas consecutivas
    count = 0
    for i in range(len(up_trend)):
        if up_trend[i]:
            count += 1
            if count >= 5:
                # Marca os últimos 5 pontos e continua marcando enquanto a subida continua
                consecutive_ups.extend(range(i - count + 1, i + 1))
        else:
            count = 0

    return consecutive_downs, consecutive_ups

if __name__ == "__main__":
    # Carregar os dados do sensor
    sensor_data1 = load_sensor_data('sensor_data2.csv')

    # Identificar descidas e subidas consecutivas
    consecutive_downs, consecutive_ups = identify_trends(sensor_data1)

    # Plotar o sinal original e as tendências
    plt.figure(figsize=(12, 6))
    plt.plot(sensor_data1, label='Sensor Data 2', color='blue')

    # Marcar descidas consecutivas com setas vermelhas para baixo
    plt.scatter(consecutive_downs, sensor_data1[consecutive_downs], color='red', label='Descidas Consecutivas', marker='v')

    # Marcar subidas consecutivas com setas verdes para cima
    plt.scatter(consecutive_ups, sensor_data1[consecutive_ups], color='green', label='Subidas Consecutivas', marker='^')

    plt.title('Detecção de Tendências Consecutivas de 5 ou Mais Valores (Sensor Data 1)')
    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.legend()
    plt.show()
