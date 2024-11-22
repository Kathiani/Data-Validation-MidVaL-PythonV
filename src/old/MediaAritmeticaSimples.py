import numpy as np
import matplotlib.pyplot as plt
import time

def load_sensor_data(filename):
    return np.loadtxt(filename, delimiter=',')

def detect_outliers_mean(data):
    mean = np.mean(data)
    std_dev = np.std(data)
    outliers = [(i, val) for i, val in enumerate(data) if np.abs(val - mean) >  std_dev]
    return outliers

if __name__ == "__main__":
    # Medir o tempo de execução
    start_time = time.time()

    # Carregar os L1-10pt dos sensores
    sensor_data1 = load_sensor_data('../../dados/L1-10pt/sets/sensor_data1.csv')

      # Detectar outliers
    outliers1 = detect_outliers_mean(sensor_data1)

    # Medir o tempo de execução
    end_time = time.time()
    execution_time = end_time - start_time

    # Visualizar resultados-series normais para sensor 1
    plt.figure(figsize=(12, 6))
    plt.plot(sensor_data1, label='Sensor Data 1')
    plt.axhline(np.mean(sensor_data1), color='green', linestyle='--', label='Mean 1')
    plt.axhline(np.mean(sensor_data1) +  np.std(sensor_data1), color='orange', linestyle='--', label='Upper Bound 1')
    plt.axhline(np.mean(sensor_data1) -  np.std(sensor_data1), color='orange', linestyle='--', label='Lower Bound 1')

    for outlier in outliers1:
        plt.scatter(outlier[0], outlier[1], color='red', marker='x', s=100, label='Outlier 1')

    plt.title('Outlier Detection using Mean and Standard Deviation (Sensor 1)')
    plt.xlabel('Index')
    plt.ylabel('Temperature')
    plt.legend(loc='best')
    plt.show()

    print("Outliers detected in sensor data 1 at indices:")
    print(outliers1)


    # Exibir o tempo de execução
    print(f"Tempo de execução: {execution_time:.4f} segundos")
