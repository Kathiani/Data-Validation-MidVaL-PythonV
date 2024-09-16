import numpy as np
import matplotlib.pyplot as plt
import time
import os

def salvar_infos_em_arquivo(processing_time, nome_sensor, valor, fault, filename):
    pasta_resultados = 'resultados'
    if not os.path.exists(pasta_resultados):
        os.makedirs(pasta_resultados)

    # Caminho completo para o arquivo dentro da pasta 'resultados'
    caminho_arquivo = os.path.join(pasta_resultados, filename)

    with open(caminho_arquivo, 'a') as file:
        file.write("\n")
        file.write(f"Sensor Analisado = {str(nome_sensor)}\n")
        file.write(f"Valor Analisado = {str(valor)}\n")
        file.write(f"Tempo de processamento = {processing_time:.4f}\n")
        file.write(f"Erro identificado = {str(fault)}\n")

def load_sensor_data(filename):
    return np.loadtxt(filename, delimiter=',')

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

def detect_outliers_moving_mean(data, window_size):
    moving_means = moving_average(data, window_size)
    moving_stds = [np.std(data[i:i + window_size]) for i in range(len(data) - window_size + 1)]
    outliers = []

    for i in range(len(moving_means)):
        if np.abs(data[i + window_size - 1] - moving_means[i]) > moving_stds[i]:
            outliers.append((i + window_size - 1, data[i + window_size - 1]))

    return outliers, moving_means, moving_stds

def startmediamovel():
    # Medir o tempo de execução
    start_time = time.time()

    nome_do_sensor = 'sensor_data1.csv'

    # Carregar os dados dos sensores
    sensor_data1 = load_sensor_data(nome_do_sensor)

    # Definir o tamanho da janela para a média móvel
    window_size = 20

    # Detectar outliers usando média móvel
    outliers1, moving_means1, moving_stds1 = detect_outliers_moving_mean(sensor_data1, window_size)

    # Verificar se o valor na primeira posição foi considerado um outlier
    first_value_outlier = any(outlier[0] == 0 for outlier in outliers1) #se o valor na primeiro for igual a zero representa um outlier

    # Medir o tempo de execução
    end_time = time.time()
    processing_time = end_time - start_time

    # Salvar informações no arquivo
    salvar_infos_em_arquivo(processing_time, nome_do_sensor, sensor_data1[0], first_value_outlier, 'resultados-MediaMovel.txt')

    # Visualizar resultados para sensor 1
    plt.figure(figsize=(12, 6))
    plt.plot(sensor_data1, label='Sensor Data 1')
    plt.plot(range(window_size - 1, len(sensor_data1)), moving_means1, color='green', linestyle='--',
             label='Moving Mean 1')

    for outlier in outliers1:
        plt.scatter(outlier[0], outlier[1], color='red', marker='x', s=100, label='Outlier 1')

    plt.title('Outlier Detection using Moving Mean and Standard Deviation (Sensor 1)')
    plt.xlabel('Index')
    plt.ylabel('Temperature')
    plt.legend(loc='best')
    plt.show()

    print("Outliers detected in sensor data 1 at indices:")
    print(outliers1)

