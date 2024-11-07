import os
import numpy as np
import random

#Gerando dados L1 e L2 com erros em 10pt, 20pt dos dados de 8.640 leituras por dia (1 leitura a cada 10 segundos)
#864 10% dos dados incorretos   L1 - 100 sensores
#1728  20% dos dados incorretos   L2 - 100 sensores


def generate_sensor_data():
    # Configurações para os lotes
    num_sensors = 100
    indices_erroneos = 1728

    for i in range(1, num_sensors + 1):
        normal_temperatures = np.random.normal(loc=42, scale=0.5, size = 8640)  # Dados normais
        normal_temperatures = np.round(normal_temperatures).astype(int)  # Arredondar

        # Selecionar num_pontos_drift índices aleatórios da sequência para aplicar drift
        indices_anomalos = random.sample(range(len(normal_temperatures)), indices_erroneos)
        meio = len(normal_temperatures) // 2
        indices_freezing = random.sample(range(meio, len(normal_temperatures)), len(normal_temperatures) - meio)

        nomesensor = "temperatura" + str(i)
        # Aplicar drift nos L1-10pt normais
        drift(normal_temperatures, indices_anomalos, nomesensor)
        bias(normal_temperatures, indices_anomalos, nomesensor)
        freezing(normal_temperatures, indices_freezing, nomesensor)
        loss_accuracy(normal_temperatures, indices_anomalos, nomesensor)
        noise(normal_temperatures, indices_anomalos, nomesensor)


def criarrotulos(data, indices_anomalos, nomesensor, nometecnica):
    # Criar rótulos iniciais como 'correto'
    labels = ['correto'] * len(data)  # Para o tamanho correto
    for idx in indices_anomalos:
        labels[idx] = 'incorreto'  # Atualiza para 'incorreto' onde for anômalo

    # Combinar temperaturas e rótulos
    labeled_data = np.column_stack((data, labels))

    pasta_dados = '/home/kathiani/midval/dados/temperatura/L2'
    if not os.path.exists(pasta_dados):
         os.makedirs(pasta_dados)

    # Caminho completo para o arquivo dentro da pasta 'L1-10pt'
    caminho_arquivo = os.path.join(pasta_dados, f'{nometecnica}-{nomesensor}.csv')

     # Salvar os L1-10pt rotulados em um arquivo CSV
    np.savetxt(caminho_arquivo, labeled_data, delimiter=',', fmt='%s', header="Dados,Label", comments='')


# Função para aplicar drift em pontos esporádicos
def drift(initial_values, indices_anomalos, nomesensor):
    noise_stddev = 10  # Desvio padrão do ruído
    results = initial_values.copy()

    # Aplicar drift apenas nos índices escolhidos
    for i in indices_anomalos:
        noise = np.random.normal(0, noise_stddev)  # Gerar ruído
        y = results[i] + i * noise
        results[i] = y # Aplicar o drift nos pontos aleatórios

    criarrotulos(results, indices_anomalos, nomesensor, 'Drift')


def bias(initial_values, indices_anomalos, nomesensor):
    intensidade = 10
    results = initial_values.copy()

    for i in indices_anomalos:
        results[i] = results[i] + intensidade # Aplicar a fórmula

    criarrotulos(results, indices_anomalos, nomesensor, 'Bias')


def freezing(initial_values, indices_anomalos, nomesensor):
    meio = len(initial_values) // 2
    for i in range(meio, len(initial_values)):
        initial_values[i] = initial_values[meio]

    criarrotulos(initial_values, indices_anomalos, nomesensor, 'Freezing')


def loss_accuracy(initial_values, indices_anomalos, nomesensor):
    intensity = 0.5

    for i in indices_anomalos:
        random_operator = '+' if random.random() < 0.5 else '_'

        if random_operator == '+':
            initial_values[i] = initial_values[i] + intensity
        else:
            initial_values[i]  = initial_values[i] - intensity

    criarrotulos(initial_values, indices_anomalos, nomesensor, 'LossAccuracy')


def noise(initial_values, indices_anomalos, nomesensor):
    noise_stddev = 10

    for i in indices_anomalos:
        initial_values[i] = initial_values[i] + random.normalvariate(0, noise_stddev)

    criarrotulos(initial_values, indices_anomalos, nomesensor, 'Noise')



#Gerar dados e aplicar ruído
generate_sensor_data()


