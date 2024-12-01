import os
import numpy as np
import random


def gerar_dados_aleatoriamente(num_sensors, indices_erroneos, pasta_dadoscorretos, pasta_dadosincorretos):
    for i in range(1, num_sensors + 1):
        normal_data = np.random.normal(loc=42, scale=0.5, size = 8640)  # Dados normais, 8640
        normal_data = np.round(normal_data).astype(int)
        nomesensor = "temperatura" + str(i)


        # Caminho completo para salvar os dados normais
        caminho_arquivo = os.path.join(pasta_dadoscorretos, f'{nomesensor}.csv')

        # Salvar os L1-10pt rotulados em um arquivo CSV
        np.savetxt(caminho_arquivo, normal_data, delimiter=',', fmt='%s', header="Dados", comments='')


        # Selecionar num_pontos_drift índices aleatórios da sequência para aplicar drift
        indices_anomalos = random.sample(range(len(normal_data)), indices_erroneos)
        meio = len(normal_data) // 2
        indices_freezing = random.sample(range(meio, len(normal_data)), len(normal_data) - meio)


        # Aplicar drift nos dados e salvar dados incorretos
        drift(normal_data, indices_anomalos, nomesensor, pasta_dadosincorretos)
        bias(normal_data, indices_anomalos, nomesensor, pasta_dadosincorretos)
        freezing(normal_data, indices_freezing, nomesensor, pasta_dadosincorretos)
        loss_accuracy(normal_data, indices_anomalos, nomesensor, pasta_dadosincorretos)
        noise(normal_data, indices_anomalos, nomesensor, pasta_dadosincorretos)

def gerar_dados_secionados(num_sensores, indices_erroneos, pasta_dadoscorretos, pasta_dadosincorretos):
# Temperaturas para os horários específicos - Previsão para Dia 19/11 São Paulo - SP
    times_of_day = [
        (0, 22),  # 00:00h - 22°C
        (6, 18),  # 06:00h - 18°C
        (12, 30),  # 12:00h - 30°C
        (18, 24)  # 18:00h - 24°C
    ]

    # Gerar dados para cada dia
    for j in range(1, num_sensores + 1):
        daily_data = []

        # Gerar leituras a cada 10 segundos durante o dia inteiro (24 horas)
        for i in range(len(times_of_day) - 1):
            start_time, start_temp = times_of_day[i]
            end_time, end_temp = times_of_day[i + 1]

            # Número de pontos de dados entre os horários (cada 10 segundos)
            time_steps = (end_time - start_time) * 3600 // 10  # convertendo para segundos, dividindo por 10 segundos
            times = np.linspace(start_time * 3600, end_time * 3600, time_steps)  # convertendo para segundos
            temps = np.linspace(start_temp, end_temp, time_steps)  # Temperatura linear entre os dois pontos

            # Adicionando os dados ao dia
            daily_data.extend(temps)


        # Para o intervalo entre 18:00h e 00:00h
        start_time, start_temp = times_of_day[-1]  # 18:00h, 24°C
        end_time, end_temp = (24, 22)  # 00:00h, 22°C
        time_steps = (end_time - start_time) * 3600 // 10
        times = np.linspace(start_time * 3600, end_time * 3600, time_steps)
        temps = np.linspace(start_temp, end_temp, time_steps)
        daily_data.extend(temps)


        # Salvar os dados para o dia
        nomesensor = f"temperatura{j}"

        # Caminho completo para salvar os dados
        caminho_arquivo = os.path.join(pasta_dadoscorretos, f'{nomesensor}.csv')

        # Salvar os dados de temperatura para o dia
        np.savetxt(caminho_arquivo, daily_data, delimiter=',', fmt='%f', header="Dados", comments='')

        # Selecionar num_pontos_drift índices aleatórios da sequência para aplicar drift
        indices_anomalos = random.sample(range(len(daily_data)), indices_erroneos)
        meio = len(daily_data) // 2
        indices_freezing = random.sample(range(meio, len(daily_data)), len(daily_data) - meio)

        # Aplicar drift nos L1-10pt normais
        drift(daily_data, indices_anomalos, nomesensor, pasta_dadosincorretos)
        bias(daily_data, indices_anomalos, nomesensor, pasta_dadosincorretos)
        freezing(daily_data, indices_freezing, nomesensor, pasta_dadosincorretos)
        loss_accuracy(daily_data, indices_anomalos, nomesensor, pasta_dadosincorretos)
        noise(daily_data, indices_anomalos, nomesensor, pasta_dadosincorretos)


def criarrotulos(data, indices_anomalos, nomesensor, nometecnica, pasta_dadosincorretos):
    # Criar rótulos iniciais como 'correto'
    labels = ['correto'] * len(data)  # Para o tamanho correto
    for idx in indices_anomalos:
        labels[idx] = 'incorreto'  # Atualiza para 'incorreto' onde for anômalo

    # Combinar temperaturas e rótulos
    labeled_data = np.column_stack((data, labels))

    # Caminho completo para o arquivo
    caminho_arquivo = os.path.join(pasta_dadosincorretos, f'{nometecnica}-{nomesensor}.csv')

     # Salvar os L1-10pt rotulados em um arquivo CSV
    np.savetxt(caminho_arquivo, labeled_data, delimiter=',', fmt='%s', header="Dados,Label", comments='')


# Função para aplicar drift em pontos esporádicos
def drift(initial_values, indices_anomalos, nomesensor, pasta_dadosincorretos):
    indices_anomalos.sort()
    incremento_drift = 2
    vini_drift = 1

    # Aplicar drift linear nos índices anômalos
    for i, idx in enumerate(indices_anomalos):
        initial_values[idx] =  initial_values[idx] + vini_drift
        vini_drift = vini_drift + incremento_drift

    criarrotulos(initial_values, indices_anomalos, nomesensor, 'Drift', pasta_dadosincorretos)


def bias(initial_values, indices_anomalos, nomesensor, pasta_dadosincorretos):
    intensidade = 10
    results = initial_values.copy()

    for i in indices_anomalos:
        results[i] = results[i] + intensidade  # Aplicar a fórmula

    criarrotulos(results, indices_anomalos, nomesensor, 'Bias', pasta_dadosincorretos)


def freezing(initial_values, indices_anomalos, nomesensor, pasta_dadosincorretos):
    meio = len(initial_values) // 2
    for i in range(meio, len(initial_values)):
        initial_values[i] = initial_values[meio]

    criarrotulos(initial_values, indices_anomalos, nomesensor, 'Freezing', pasta_dadosincorretos)


def loss_accuracy(initial_values, indices_anomalos, nomesensor, pasta_dadosincorretos):
    intensity = 0.5

    for i in indices_anomalos:
        random_operator = '+' if random.random() < 0.5 else '_'

        if random_operator == '+':
            initial_values[i] = float(initial_values[i] + intensity)
        else:
            initial_values[i]  = float(initial_values[i] - intensity)

    criarrotulos(initial_values, indices_anomalos, nomesensor, 'LossAccuracy', pasta_dadosincorretos)


def noise(initial_values, indices_anomalos, nomesensor, pasta_dadosincorretos):
    noise_stddev = 10

    for i in indices_anomalos:
        initial_values[i] = initial_values[i] + random.normalvariate(0, noise_stddev)

    criarrotulos(initial_values, indices_anomalos, nomesensor, 'Noise', pasta_dadosincorretos)



def gerar_dados():
# 864 10% dos dados incorretos   L1 - 100 sensores
# 1728  20% dos dados incorretos   L2 - 100 sensores
# Configurar a quantidade de indices, os lotes e os tipos de sequências {sazonais e não-sazonais}

    num_sensors = 3
    indices_erroneos = 1728

    pasta_dadoscorretos = '/home/kathiani/midval/dados/temperatura-corrigidos/corretos/L2'
    pasta_dadosincorretos = '/home/kathiani/midval/dados/temperatura-corrigidos/incorretos/L2'

    if not os.path.exists(pasta_dadoscorretos):
        os.makedirs(pasta_dadoscorretos)

    if not os.path.exists(pasta_dadosincorretos):
        os.makedirs(pasta_dadosincorretos)

    #gerar_dados_secionados(num_sensors, indices_erroneos, pasta_dadoscorretos, pasta_dadosincorretos)
    gerar_dados_aleatoriamente(num_sensors, indices_erroneos, pasta_dadoscorretos, pasta_dadosincorretos)


gerar_dados()



