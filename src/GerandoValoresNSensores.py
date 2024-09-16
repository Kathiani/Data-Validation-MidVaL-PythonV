import numpy as np
import os

def generate_sensor_data(num_sensors):
    # Configurações para os dados
    #np.random.seed(100)

    for i in range(1, num_sensors + 1):
        # Simular dados normais com variação dependente do sensor
        normal_temperatures = np.random.normal(loc=300, scale=0.5, size=100)  # Dados normais

        # Arredondar os valores normais para inteiros
        normal_temperatures = np.round(normal_temperatures).astype(int)

        # Adicionar valores anômalos
        anomalous_temperatures = np.array([50, 55, 6, 200, 500, 3])  # Valores anômalos

        # Combinar os dados
        combined_temperatures = np.concatenate((normal_temperatures, anomalous_temperatures))

        # Embaralhar a ordem dos dados
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

        pasta_dados = 'dados'
        if not os.path.exists(pasta_dados):
            os.makedirs(pasta_dados)

        # Caminho completo para o arquivo dentro da pasta 'dados'
        caminho_arquivo = os.path.join(pasta_dados, f'carros{i}.csv')

        # Salvar os dados rotulados em um arquivo CSV
        np.savetxt(caminho_arquivo, labeled_data, delimiter=',', fmt='%s', header="Dados,Label", comments='')

# Chamada da função para gerar os dados
#generate_sensor_data(num_sensors=100)
