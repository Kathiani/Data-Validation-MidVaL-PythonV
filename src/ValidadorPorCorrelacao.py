import numpy as np
import time
import pandas as pd
import os
from src.CalculadoraDeMetricas import computa_metricas
from src.CalculadoraDeMetricas import computa_media_metricas

def calculate_correlation(data1, data2):
    correlation_matrix = np.corrcoef(data1, data2)
    return correlation_matrix[0, 1]  # Retorna apenas o coeficiente de correlação


def salvar_em_arquivo(sensor_data, data, outliers, caminho_arquivo):
    # Avaliando
    labels = sensor_data.iloc[:, 1].values
    comparacao = []

    for true, pred in zip(labels, outliers):
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
        'Predição': ['P-correto' if pred == 1 else 'P-incorreto' for pred in outliers],
        'Avaliação': comparacao
    })

    # Salvando o DataFrame como CSV
    df.to_csv(caminho_arquivo, index=False)
    #print(f"resultados salvos em {caminho_arquivo}")

def startcalculocorrelacao(n_sensores, tecnica):
    tiposensor = 'temperatura'
    tipo_erro = ['LossAccuracy', 'Drift', 'Noise', 'Bias', 'Freezing']
    lotes = ['L1', 'L2']
    limiar = 3

    # Carregar os L1-10pt do sensor 1
    correlations = []

    for nlote in lotes:
        for n in tipo_erro:
            grupo_execucao = f'{tecnica}-{n}-{nlote}'
            caminho_arquivo = f'resultados/{tecnica}/{n}/{nlote}/{grupo_execucao}/'
            os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)  # Criar diretório para salvar numa primeira execução

            for i in range(1, n_sensores + 1):

                sensor_name = f'/home/kathiani/midval/dados/{tiposensor}/{nlote}/{n}-{tiposensor}{i}.csv'

                sensor_data = pd.read_csv(sensor_name)

                # Supondo que a coluna de interesse seja a primeira coluna
                data = sensor_data.iloc[:, 0].values

                start_time = time.time()

                # Calcular a correlação entre o sensor i e os demais sensores
                for j in range(1, n_sensores + 1):
                    if i!=j:
                        proximo_sensor = pd.read_csv(f'/home/kathiani/midval/dados/{tiposensor}/{nlote}/{n}-{tiposensor}{j}.csv')
                        data_proximo_sensor =  proximo_sensor.iloc[:, 0].values
                        correlation = calculate_correlation(data, data_proximo_sensor)
                        correlations.append((j, correlation))
                    #else:
                        #correlations.append((j, 0))


                correlations.sort(key=lambda x: x[1], reverse=True)

                best_sensor_id = correlations[0][0]
                best_sensor_data = pd.read_csv(f'/home/kathiani/midval/dados/{tiposensor}/{nlote}/{n}-{tiposensor}{best_sensor_id}.csv')
                best_sensor_data = best_sensor_data.iloc[:, 0].values

                outliers = [None] * (len(data))

                for k in range(0, len(data)):
                    value_sensor = data[k]  # verificando se esta dentro dos limiares
                    if abs(value_sensor - best_sensor_data[k]) >= limiar:
                          outliers[k] = -1
                    else:
                          outliers[k] = 1

                end_time = time.time()
                tempoprocessamento_atual = end_time - start_time

                caminho_nome_arquivo = f'{caminho_arquivo}/{grupo_execucao}-{tiposensor}-{i}.csv'

                salvar_em_arquivo(sensor_data, data, outliers, caminho_nome_arquivo)
                computa_metricas(caminho_nome_arquivo)  # Computa e armazena F1-Score para o sensor atual
                computa_media_metricas(caminho_nome_arquivo, grupo_execucao, tempoprocessamento_atual, i)