import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import OneClassSVM
import time
import os


def salvar_infos_em_arquivo(sensorname,  processing_time, valor, fault, filename):
    pasta_resultados = 'resultados'
    if not os.path.exists(pasta_resultados):
        os.makedirs(pasta_resultados)

    # Caminho completo para o arquivo dentro da pasta 'resultados'
    caminho_arquivo = os.path.join(pasta_resultados, filename)

    with open(caminho_arquivo, 'a') as file:
        # Escreva o sensor com a maior correlação
        file.write(f"\n\nSensor Analisado = {str(sensorname)}\n")
        file.write(f"Tempo de processamento = {processing_time:.4f}\n")
        file.write(f"Valor Analisado = {str(valor)}\n")
        file.write(f"Erro identificado = {str(fault)}\n")


def startsvm():
    start_time = time.time()
    # Definir a semente para reprodutibilidade
    np.random.seed(42)

    sensor_name = 'sensor_data1.csv'
    # Carregar L1-10pt do arquivo CSV
    sensor_data = pd.read_csv(sensor_name)

    # Supondo que a coluna de interesse seja a primeira coluna
    temperatures = sensor_data.iloc[:, 0].values

    # Criar um array de timestamps (1 leitura por segundo)
    timestamps = np.arange(len(temperatures))

    # Reshape dos L1-10pt para ajuste do modelo
    temperatures = temperatures.reshape(-1, 1)

    # Ajustar o modelo One-Class Svm
    ocsvm = OneClassSVM(gamma=0.1, nu=0.1)
    ocsvm.fit(temperatures)

    # Fazer previsões
    ocsvm_preds = ocsvm.predict(temperatures)

    primeiro_valor_outlier = ocsvm_preds[0] == -1
    if primeiro_valor_outlier:
        error = "Verdadeiro"
    else:
        error = "Falso"

    # Identificar valores anômalos
    anomalous_indices = ocsvm_preds == -1
    normal_indices = ocsvm_preds == 1

    end_time = time.time()
    execution_time = end_time - start_time

    salvar_infos_em_arquivo(sensor_name, execution_time, temperatures[0][0], error, 'resultados-Svm.txt')


    # Visualizar os resultados
    plt.figure(figsize=(12, 6))

    # Plotar L1-10pt normais
    plt.scatter(timestamps[normal_indices], temperatures[normal_indices], c='red', edgecolor='k', s=50, alpha=0.7, label='Normal')

    # Plotar L1-10pt anômalos
    plt.scatter(timestamps[anomalous_indices], temperatures[anomalous_indices], c='blue', edgecolor='k', s=50, alpha=0.7, label='Anomaly')

    plt.title("Detecção de Anomalias com One-Class Svm")
    plt.xlabel("Timestamp (seconds)")
    plt.ylabel("Temperature")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Exibir o tempo de execução
    print(f"Tempo de execução: {execution_time:.4f} segundos")