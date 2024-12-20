import numpy as np
import time
import pandas as pd
import os
from src.CalculadoraDeMetricas import computa_Fmeasure
from src.CalculadoraDeMetricas import computa_media_Fmeasure




def calculate_correlation(data1, data2):
    correlation_matrix = np.corrcoef(data1, data2)
    return correlation_matrix[0, 1]  # Retorna apenas o coeficiente de correlação


def salvar_predicoes_avaliacoes(sensor_data, outliers, caminho_arquivo):
    # Avaliando
    labels = sensor_data.iloc[:, 1].values
    comparacao = []

    for true, pred in zip(labels, outliers):  # Ponto de vista de detecção de erros
        if true == 'correto' and pred == -1:
            comparacao.append('FN')
        elif true == 'incorreto' and pred == 1:
            comparacao.append('FP')
        elif true == 'correto' and pred == 1:
            comparacao.append('VN')
        elif true == 'incorreto' and pred == -1:
            comparacao.append('VP')
        else:
            comparacao.append('Análise incorreta!')

    # Criar DataFrame para salvar os valores e previsões
    df = pd.DataFrame({
        'Dado': sensor_data.iloc[:, 0].values,
        'Label': sensor_data.iloc[:, 1].values,
        'Predição': ['P-correto' if pred == 1 else 'P-incorreto' for pred in outliers],
        'Avaliação': comparacao
    })

    # Salvando o DataFrame como CSV
    df.to_csv(caminho_arquivo, index=False)
    #print(f"resultados-series normais salvos em {caminho_arquivo}")

def startcalculocorrelacaot(n_sensores, tecnica, pasta_dadoscorretos, pasta_dadosincorretos, pasta_resultados, pasta_resumo, tipo_sensor):
    tipo_erro = ['LossAccuracy', 'Noise', 'Bias', 'Freezing']
    #tipo_erro = ['Noise', 'Bias']
    lotes = ['L1', 'L2']
    limiar = 3

    # Carregar os L1-10pt do sensor 1
    correlations = []

    for nlote in lotes:
        for n in tipo_erro:
            grupo_execucao = f'{tecnica}-{n}-{nlote}'
            caminho_resultados = f'{pasta_resultados}/{tecnica}/{n}/{nlote}/'
            os.makedirs(os.path.dirname(caminho_resultados),
                        exist_ok=True)  # Criar diretório para salvar numa primeira execução

            for i in range(1, n_sensores + 1):

                        sensor_name = f'{pasta_dadosincorretos}/{nlote}/{n}-{tipo_sensor}{i}.csv'

                        sensor_data = pd.read_csv(sensor_name)

                        # Supondo que a coluna de interesse seja a primeira coluna
                        data = sensor_data.iloc[:, 0].values

                        start_time = time.time()

                        # Calcular a correlação entre o sensor i e os demais sensores

                        for j in range(1, n_sensores + 1):
                            if i!=j:
                                next_sensor = pd.read_csv(f'{pasta_dadoscorretos}/{nlote}/{tipo_sensor}{i}.csv')
                                data_next_sensor =  next_sensor.iloc[:, 0].values
                                correlation = calculate_correlation(data, data_next_sensor)
                                correlations.append((j, correlation))

                        correlations.sort(key=lambda x: x[1], reverse=True)

                        best_sensor_id = correlations[0][0]
                        best_sensor_data = pd.read_csv(f'{pasta_dadoscorretos}/{nlote}/{tipo_sensor}{best_sensor_id}.csv') #Carregando dados do sensor de índice com maior correlação
                        best_sensor_data = best_sensor_data.iloc[:, 0].values





                        #print(f"Melhor Id:{correlations[0][0]}")  # Carrega o índice do sensor com maior correlação
                        #print(data)
                        #print(best_sensor_data)

                        outliers = [None] * (len(data))

                        for k in range(0, len(data)):
                            value_sensor = data[k]
                            if abs(value_sensor - best_sensor_data[k]) >= limiar: # verificação de limiar
                                  outliers[k] = -1
                            else:
                                  outliers[k] = 1



                        #print(outliers)

                        end_time = time.time()
                        tempoprocessamento_atual = end_time - start_time

                        #Caminho para salvar os resultados-series normais do algoritmo para as leituras
                        caminho_nome_arquivo = f'{caminho_resultados}/{grupo_execucao}-{tipo_sensor}-{i}.csv'

                        salvar_predicoes_avaliacoes(sensor_data, outliers, caminho_nome_arquivo)  # Computa e armazena predições para as leituras do sensor atua
                        computa_Fmeasure(caminho_nome_arquivo, pasta_resumo, grupo_execucao, i, tempoprocessamento_atual)

