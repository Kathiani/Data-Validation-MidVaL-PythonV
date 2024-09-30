import os
import numpy as np
import matplotlib.pyplot as plt
from PIL.ImageCms import isIntentSupported
from scipy.interpolate import interp1d
import random

def generate_sensor_data(num_sensors):
    # Configurações para os dados
    #np.random.seed(10)
    indices_erroneos =  5


    for i in range(1, num_sensors + 1):
        # Simular dados normais com variação dependente do sensor
        normal_temperatures = np.random.normal(loc=300, scale=0.5, size=10)  # Dados normais
        normal_temperatures = np.round(normal_temperatures).astype(int)  # Arredondar

        # Selecionar num_pontos_drift índices aleatórios da sequência para aplicar drift
        indices_anomalos = random.sample(range(len(normal_temperatures)), indices_erroneos)

        # Aplicar drift nos dados normais
        erroneous_data = drift(normal_temperatures, indices_anomalos)
        #erroneous_data = bias(normal_temperatures, indices_anomalos)
        #erroneous_data = freezing(normal_temperatures, indices_anomalos)
        #erroneous_data = loss_accuracy(normal_temperatures, indices_anomalos)
        #erroneous_data = noise(normal_temperatures, indices_anomalos)


        # Criar rótulos iniciais como 'correto'
        labels = ['correto'] * len(normal_temperatures)  # Para o tamanho correto
        for idx in indices_anomalos:
            labels[idx] = 'incorreto'  # Atualiza para 'incorreto' onde for anômalo

        # Combinar temperaturas e rótulos
        labeled_data = np.column_stack((erroneous_data, labels))

        pasta_dados = 'dados'
        if not os.path.exists(pasta_dados):
            os.makedirs(pasta_dados)

        # Caminho completo para o arquivo dentro da pasta 'dados'
        caminho_arquivo = os.path.join(pasta_dados, f'pessoasDrift{i}.csv')

        # Salvar os dados rotulados em um arquivo CSV
        np.savetxt(caminho_arquivo, labeled_data, delimiter=',', fmt='%s', header="Dados,Label", comments='')




#def aplicar_ruido_demonstracao():
    # Parâmetros
    #initial_values = [42, 42, 42, 43, 43, 43, 43, 44, 44, 44, 44, 45, 45 ,45 , 45]  # Valores iniciais de teste
    #drift(initial_values)
    #bias(initial_values)
    #freezing(initial_values)
    #loss_accuracy(initial_values)
    #noise(initial_values)


# Função para aplicar drift em pontos esporádicos
def drift(initial_values, indices_anomalos):
    noise_stddev = 2  # Desvio padrão do ruído
    results = initial_values.copy()

    # Aplicar drift apenas nos índices escolhidos
    for i in indices_anomalos:
        noise = np.random.normal(0, noise_stddev)  # Gerar ruído
        y = results[i] + i * noise
        results[i] = y # Aplicar o drift nos pontos aleatórios
    return results


def bias(initial_values, indices_anomalos):
    intensidade = 2
    results = initial_values.copy()

    for i in indices_anomalos:
        results[i] = results[i] + intensidade # Aplicar a fórmula

    return results


def freezing(initial_values, indices_anomalos):
    for i in range(len(initial_values) // 2, len(initial_values)):
        initial_values[i] = initial_values[0]  # Aplicar a fórmula

    return initial_values


def loss_accuracy(initial_values, indices_anomalos):
    intensity = 0.5

    for i in indices_anomalos:
        random_operator = '+' if random.random() < 0.5 else '_'

        if random_operator == '+':
            initial_values[i] = initial_values[i] + intensity
        else:
            initial_values[i]  = initial_values[i] - intensity

    return initial_values


def noise(initial_values, indices_anomalos):
    noise_stddev = 7

    for i in indices_anomalos:
        initial_values[i] = initial_values[i] + random.normalvariate(0, noise_stddev)

    return initial_values



# Chamada da função para gerar os dados
generate_sensor_data(num_sensors=10)
#aplicar_ruido_demonstracao()

