import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import time
import os
from src.ComputaMetricas import startmetricas


def salvar_infos_em_arquivo(sensor_data, data, forecasts, caminho_arquivo):

    # Avaliando verdadeiros positivos
    labels = sensor_data.iloc[:, 1].values
    comparacao = []

    for true, pred in zip(labels, forecasts):
        if true == 'correto' and pred == 1:
            comparacao.append('VP')
        elif true == 'incorreto' and pred == 1:
            comparacao.append('FN')
        elif true == 'correto' and pred == -1:
            comparacao.append('FP')
        elif true == 'incorreto' and pred == -1:
            comparacao.append('VN')
        else:
            comparacao.append('Análise incorreta!')


    # Criar DataFrame para salvar os valores e previsões
    df = pd.DataFrame({
        'Dado': data.flatten(),
        'Label': sensor_data.iloc[:, 1].values,
        'Predição': ['P-correto' if pred == 1 else 'P-incorreto' for pred in forecasts],
        'Avaliação': comparacao
    })

    # Salvando o DataFrame como CSV
    df.to_csv(caminho_arquivo, index=False)
    print(f"resultados salvos em {caminho_arquivo}")


def startisolationforest(n_sensores, nomesensor, tecnica):
    start_time = time.time()

    for i in range(1, n_sensores + 1):
        sensor_name = f'dados/{nomesensor}{i}.csv'

        # Carregar dados do arquivo CSV
        sensor_data = pd.read_csv(sensor_name)

        # Supondo que a coluna de interesse seja a primeira coluna
        temperatures = sensor_data.iloc[:, 0].values

        # Reshape dos dados para ajuste do modelo
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

        # Rotular dados como 'correto' ou 'incorreto' baseado nas previsões (-1 = anomalia, 1 = normal)
        nomearquivo = f'ResultadosIsolation-{nomesensor}{i}.csv'
        caminho_arquivo = f'resultados/{tecnica}/{nomearquivo}'
        if not os.path.exists(caminho_arquivo):
            os.makedirs(caminho_arquivo)

        salvar_infos_em_arquivo(sensor_data, temperatures, iso_preds,  caminho_arquivo)
        startmetricas(caminho_arquivo)



