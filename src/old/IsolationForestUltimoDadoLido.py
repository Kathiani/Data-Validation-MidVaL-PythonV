import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import time
import os

def salvar_infos_em_arquivo(processing_time, fault, sensor_name, value, forecast, filename):
    pasta_resultados = 'resultados-series normais'
    if not os.path.exists(pasta_resultados):
        os.makedirs(pasta_resultados)

    # Caminho completo para o arquivo dentro da pasta 'resultados-series normais'
    caminho_arquivo = os.path.join(pasta_resultados, filename)

    with open(caminho_arquivo, 'a') as file:
        file.write("\n\n")
        file.write(f"Sensor Analisado = {str(sensor_name)}\n")
        file.write(f"Valor Analisado = {str(value)}\n")
        file.write(f"Resultado da Análise = {str(forecast)}\n")
        file.write(f"Tempo de processamento = {processing_time:.4f}\n")
        file.write(f"Erro identificado = {str(fault)}\n")

def startisolationforest():
    start_time = time.time()
    sensor_name = 'data/pessoas1.csv'
    # Carregar L1-10pt do arquivo CSV
    sensor_data = pd.read_csv(sensor_name)

    # Supondo que a coluna de interesse seja a primeira coluna
    temperatures = sensor_data.iloc[:, 0].values

    # Criar um array de timestamps (1 leitura por segundo)
    timestamps = np.arange(len(temperatures))

    # Reshape dos L1-10pt para ajuste do modelo
    temperatures = temperatures.reshape(-1, 1)

    # Definir os parâmetros para o modelo Isolation Forest
    params = {
        'n_estimators': 100,
        'max_samples': 'auto',
        'contamination': 0.1,
        'max_features': 1.0,
        'random_state': 42
    }

    # Ajustar o modelo
    iso_forest = IsolationForest(**params)
    iso_forest.fit(temperatures)
    iso_preds = iso_forest.predict(temperatures)

    end_time = time.time()
    processing_time = end_time - start_time

    if iso_preds[0] == -1:
        error = "Verdadeiro"
    else:
        error = "Falso"

    salvar_infos_em_arquivo(processing_time, error, sensor_name, temperatures[0][0], iso_preds[0], 'resultados-series normais-UltimoDado.txt')

    # Visualizar os resultados-series normais
    plt.figure(figsize=(12, 6))
    plt.title(f"Isolation Forest com parâmetros: {params}")
    scatter = plt.scatter(np.arange(len(temperatures)), temperatures, c=iso_preds, cmap='coolwarm', s=100, edgecolor='k')

    # Adicionar números aos pontos
    for i, txt in enumerate(temperatures):
        plt.annotate(f'{txt[0]:.1f}', (i, temperatures[i]), textcoords="offset points", xytext=(0, 10), ha='center')

    # Adicionar barra de cores
    plt.colorbar(scatter, label="Anomaly Score")

    plt.xlabel("Index")
    plt.ylabel("Temperature")
    plt.tight_layout()
    plt.show()

    # Exibir os resultados-series normais
    print(f"Parâmetros: {params}")
    print("Isolation Forest Predictions:", iso_preds)

    return error

