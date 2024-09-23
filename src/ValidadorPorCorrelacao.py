import numpy as np
import time
import pandas as pd
from src.CalculadoraDeMetricas import startmetricas
from src.CalculadoraDeMetricas import comparemetricas


def calculate_correlation(data1, data2):
    correlation_matrix = np.corrcoef(data1, data2)
    return correlation_matrix[0, 1]  # Retorna apenas o coeficiente de correlação


def salvar_infos_em_arquivo(sensor_data, data, outliers, caminho_arquivo):
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

def startcalculocorrelacao(n_sensores, nomesensor, tecnica):
    start_time = time.time()
    limiar = 3

    # Carregar os dados do sensor 1
    correlations = []

    for i in range(1, n_sensores + 1):
        sensor_name = f'dados/{nomesensor}{i}.csv'
        #print(sensor_name)

        # Carregar dados do arquivo CSV
        sensor_data = pd.read_csv(sensor_name)

        # Supondo que a coluna de interesse seja a primeira coluna
        data = sensor_data.iloc[:, 0].values


        # Calcular a correlação entre o sensor i e os demais sensores
        for j in range(1, n_sensores + 1):
            if i!=j:
                proximo_sensor = pd.read_csv(f'dados/{nomesensor}{j}.csv')
                data_proximo_sensor =  proximo_sensor.iloc[:, 0].values
                correlation = calculate_correlation(data, data_proximo_sensor)
                correlations.append((j, correlation))
            #else:
                #correlations.append((j, 0))


        correlations.sort(key=lambda x: x[1], reverse=True)
        #print(correlations)

        best_sensor_id = correlations[0][0]
        #print(best_sensor_id)
        best_sensor_data = pd.read_csv(f'dados/{nomesensor}{best_sensor_id}.csv')
        best_sensor_data = best_sensor_data.iloc[:, 0].values

        #best_sensor_data = best_sensor_data.reshape(-1, 1)
        #first_value_best_sensor = best_sensor_data[0]  # obtendo a última leitura realizada do sensor mais correlato

        outliers = [None] * (len(data))

        for k in range(0, len(data)):
            value_sensor = data[k]  # fazer a leitura do último dado lido
            if abs(value_sensor - best_sensor_data[k]) >= limiar:
                  outliers[k] = -1
            else:
                  outliers[k] = 1

        nomearquivo = f'ResultadosDiversidade-{nomesensor}{i}.csv'
        caminho_arquivo = f'resultados/{tecnica}/{nomearquivo}'

        # Corrigir a criação de diretórios
        #dir_path = os.path.dirname(caminho_arquivo)
        #if not os.path.exists(dir_path):
            #os.makedirs(dir_path)



        salvar_infos_em_arquivo(sensor_data, data, outliers, caminho_arquivo)
        startmetricas(caminho_arquivo, tecnica)

    comparemetricas(caminho_arquivo, tecnica)