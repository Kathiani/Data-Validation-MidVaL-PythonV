import os
import numpy as np
import matplotlib.pyplot as plt
from PIL.ImageCms import isIntentSupported
from scipy.interpolate import interp1d
import random

def generate_sensor_data(num_sensors):
    # Configurações para os L1-10pt
    #np.random.seed(100)

    for i in range(1, num_sensors + 1):
        # Simular L1-10pt normais com variação dependente do sensor
        normal_temperatures = np.random.normal(loc=300, scale=0.5, size=100)  # Dados normais

        # Arredondar os valores normais para inteiros
        normal_temperatures = np.round(normal_temperatures).astype(int)

        # Adicionar valores anômalos
        anomalous_temperatures = np.array([50, 55, 6, 200, 500, 3])  # Valores anômalos

        # Combinar os L1-10pt
        combined_temperatures = np.concatenate((normal_temperatures, anomalous_temperatures))

        # Embaralhar a ordem dos L1-10pt
        shuffled_indices = np.random.permutation(len(combined_temperatures))
        shuffled_temperatures = combined_temperatures[shuffled_indices]

        # Criar rótulos iniciais como 'correto'
        labels = ['correto'] * len(shuffled_temperatures)

        # Encontrar índices dos valores anômalos
        anomalous_indices = np.isin(shuffled_temperatures, anomalous_temperatures)

        # Atualizar rótulos para valores anômalos
        labels = np.where(anomalous_indices, 'incorreto', 'correto')

        # Combinar temperaturas e rótulos
        labeled_data = np.column_stack((shuffled_temperatures, labels))

        pasta_dados = 'L1-10pt'
        if not os.path.exists(pasta_dados):
            os.makedirs(pasta_dados)

        # Caminho completo para o arquivo dentro da pasta 'L1-10pt'
        caminho_arquivo = os.path.join(pasta_dados, f'pessoas{i}.csv')

        # Salvar os L1-10pt rotulados em um arquivo CSV
        np.savetxt(caminho_arquivo, labeled_data, delimiter=',', fmt='%s', header="Dados,Label", comments='')



def aplicar_ruido_demonstracao():
    # Parâmetros
    initial_values = [42, 42, 42, 43, 43, 43, 43, 44, 44, 44, 44, 45, 45 ,45 , 45]  # Valores iniciais de teste
    drift(initial_values)
    #bias(initial_values)
    #freezing(initial_values)
    #loss_accuracy(initial_values)
    #noise(initial_values)


def drift(initial_values): #-> Drift Linear
    noise_stddev = 2  # Desvio padrão do ruído
    results = []
    for i, initial_value in enumerate(initial_values):
        x = i  # Índice
        noise = np.random.normal(0, noise_stddev)  # Gerar ruído
        y = initial_value + i * noise  # Aplicar a fórmula
        results.append(y)

    # Suavizando os L1-10pt
    x_values = np.arange(len(initial_values))  # Índices: 0, 1, 2, ..., 9
    x_new = np.linspace(0, len(initial_values) - 1, 300)  # Novos índices para interpolação

    # Interpolação
    interp_initial = interp1d(x_values, initial_values, kind='cubic')
    interp_results = interp1d(x_values, results, kind='cubic')

    # Gerando os valores suavizados
    smooth_initial = interp_initial(x_new)
    smooth_results = interp_results(x_new)

    # Visualização
    plt.plot(x_new, smooth_initial, label='Valores Iniciais Suavizados', color='blue')
    plt.plot(x_new, smooth_results, label='Valores com Drift Suavizados', color='orange')
    plt.title('Comparação de Valores Iniciais e Valores com Drift e (Suavizados)')
    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.legend()
    plt.grid()
    plt.show()



def bias(initial_values):
    intensidade = 2
    results = []
    for i, initial_value in enumerate(initial_values):
        y = initial_value + intensidade # Aplicar a fórmula
        results.append(y)

    # Suavizando os L1-10pt
    x_values = np.arange(len(initial_values))  # Índices: 0, 1, 2, ..., 9
    x_new = np.linspace(0, len(initial_values) - 1, 300)  # Novos índices para interpolação

    # Interpolação
    interp_initial = interp1d(x_values, initial_values, kind='cubic')
    interp_results = interp1d(x_values, results, kind='cubic')

    # Gerando os valores suavizados
    smooth_initial = interp_initial(x_new)
    smooth_results = interp_results(x_new)

    # Visualização
    plt.plot(x_new, smooth_initial, label='Valores Iniciais Suavizados', color='blue')
    plt.plot(x_new, smooth_results, label='Valores com Bias e Ruído Suavizados', color='orange')
    plt.title('Comparação de Valores Iniciais e Valores com Bias e Ruído (Suavizados)')
    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.legend()
    plt.grid()
    plt.show()


def freezing(initial_values):
   # Desvio padrão do ruído
    results = []
    for i, initial_value in enumerate(initial_values):
        y = initial_values[0]  # Aplicar a fórmula
        results.append(y)

    # Suavizando os L1-10pt
    x_values = np.arange(len(initial_values))  # Índices: 0, 1, 2, ..., 9
    x_new = np.linspace(0, len(initial_values) - 1, 300)  # Novos índices para interpolação

    # Interpolação
    interp_initial = interp1d(x_values, initial_values, kind='cubic')
    interp_results = interp1d(x_values, results, kind='cubic')

    # Gerando os valores suavizados
    smooth_initial = interp_initial(x_new)
    smooth_results = interp_results(x_new)

    # Visualização
    plt.plot(x_new, smooth_initial, label='Valores Iniciais Suavizados', color='blue')
    plt.plot(x_new, smooth_results, label='Valores com Freezing Suavizados', color='orange')
    plt.title('Comparação de Valores Iniciais e Valores com Freezing e (Suavizados)')
    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.legend()
    plt.grid()
    plt.show()

def loss_accuracy(initial_values):
   # Desvio padrão do ruído
    intensity = 0.5
    results = []

    for i, initial_value in enumerate(initial_values):
        random_operator = '+' if random.random() < 0.5 else '_'

        if random_operator == '+':
            y = initial_value + intensity
        else:
            y  = initial_value - intensity

        results.append(y)

    # Suavizando os L1-10pt
    x_values = np.arange(len(initial_values))  # Índices: 0, 1, 2, ..., 9
    x_new = np.linspace(0, len(initial_values) - 1, 300)  # Novos índices para interpolação

    # Interpolação
    interp_initial = interp1d(x_values, initial_values, kind='cubic')
    interp_results = interp1d(x_values, results, kind='cubic')

    # Gerando os valores suavizados
    smooth_initial = interp_initial(x_new)
    smooth_results = interp_results(x_new)

    # Visualização
    plt.plot(x_new, smooth_initial, label='Valores Iniciais Suavizados', color='blue')
    plt.plot(x_new, smooth_results, label='Valores com Loss Accuracy Suavizados', color='orange')
    plt.title('Comparação de Valores Iniciais e Valores com Loss Accuracy e (Suavizados)')
    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.legend()
    plt.grid()
    plt.show()


def noise(initial_values):

    results = []
    noise_stddev = 7
    for i, initial_value in enumerate(initial_values):
        y = initial_value + random.normalvariate(0, noise_stddev)
        results.append(y)

    # Suavizando os L1-10pt
    x_values = np.arange(len(initial_values))  # Índices: 0, 1, 2, ..., 9
    x_new = np.linspace(0, len(initial_values) - 1, 300)  # Novos índices para interpolação

    # Interpolação
    interp_initial = interp1d(x_values, initial_values, kind='cubic')
    interp_results = interp1d(x_values, results, kind='cubic')

    # Gerando os valores suavizados
    smooth_initial = interp_initial(x_new)
    smooth_results = interp_results(x_new)

    # Visualização
    plt.plot(x_new, smooth_initial, label='Valores Iniciais Suavizados', color='blue')
    plt.plot(x_new, smooth_results, label='Valores com Random Suavizados', color='orange')
    plt.title('Comparação de Valores Iniciais e Valores com Random e (Suavizados)')
    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.legend()
    plt.grid()
    plt.show()



# Chamada da função para gerar os L1-10pt
#generate_sensor_data(num_sensors=10)
aplicar_ruido_demonstracao()