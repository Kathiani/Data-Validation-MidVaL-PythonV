import numpy as np
import time
import os

#Localização e capability (filtro nos dados da Interscity)
def load_sensor_data(filename):
    return np.loadtxt(filename, delimiter=',')


def calculate_correlation(data1, data2):
    correlation_matrix = np.corrcoef(data1, data2)
    return correlation_matrix[0, 1]  # Retorna apenas o coeficiente de correlação

def salvar_infos_em_arquivo(sensorname, correlations, processing_time, valor, valorcomparado, fault, filename):
    pasta_resultados = 'resultados'
    if not os.path.exists(pasta_resultados):
        os.makedirs(pasta_resultados)

    # Caminho completo para o arquivo dentro da pasta 'resultados'
    caminho_arquivo = os.path.join(pasta_resultados, filename)

    with open(caminho_arquivo, 'a') as file:
        max_sensor_id, max_correlation = max(correlations, key=lambda x: x[1])

        # Escreva o sensor com a maior correlação
        file.write(f"\n\nSensor Analisado = {str(sensorname)}\n")
        file.write(f"Id Sensor correlato é {max_sensor_id} com Máxima Correlação = {max_correlation:.4f}\n")
        file.write(f"Tempo de processamento = {processing_time:.4f}\n")
        file.write(f"Valor Analisado = {str(valor)}\n")
        file.write(f"Valor Comparado = {str(valorcomparado)}\n")
        file.write(f"Erro identificado = {str(fault)}\n")

def startrankeamento():
    start_time = time.time()
    limiar = 3

    # Carregar os dados do sensor 1
    sensor_name =  'sensor_data1.csv'
    sensor_data1 = load_sensor_data(sensor_name)
    num_sensors = 10  # Número total de sensores
    correlations = []

    # Calcular a correlação entre o sensor 1 e os demais sensores
    for i in range(2, num_sensors + 1):
        sensor_data = load_sensor_data(f'sensor_data{i}.csv')
        correlation = calculate_correlation(sensor_data1, sensor_data)
        correlations.append((i, correlation))

    # Ordenar as correlações em ordem decrescente
    correlations.sort(key=lambda x: x[1], reverse=True)
    best_sensor_id = correlations[0][0]
    best_sensor_data = load_sensor_data(f'sensor_data{best_sensor_id}.csv')

    first_value_sensor1 = sensor_data1[0] #considerando a última leitura realizada
    first_value_best_sensor = best_sensor_data[0] #obtendo a última leitura realizada

    if abs(first_value_sensor1 - first_value_best_sensor) >=limiar:
        error = "Verdadeiro"
    else:
        error = "Falso"

    end_time = time.time()
    processing_time = end_time - start_time

    salvar_infos_em_arquivo(sensor_name, correlations, processing_time, first_value_sensor1, first_value_best_sensor, error, 'resultados-Correlacao.txt')

    return error