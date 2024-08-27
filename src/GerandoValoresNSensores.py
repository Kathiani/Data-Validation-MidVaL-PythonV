import numpy as np

def generate_sensor_data(num_sensors=10):
    # Configurações para os dados
    np.random.seed(42)

    for i in range(1, num_sensors + 1):
        # Definir a escala de variação com base no número do sensor
        scale_variation = i * 0.1  # Aumenta a escala em 0.1 a cada sensor

        # Simular dados normais de temperatura com variação dependente do sensor
        normal_temperatures = np.random.normal(loc=42, scale=0.5, size=100)  # Dados normais

        # Arredondar os valores normais para inteiros
        normal_temperatures = np.round(normal_temperatures).astype(int)

        # Adicionar valores anômalos
        anomalous_temperatures = np.array([50, 55, 6, 65, 52, 3, ])  # Valores anômalos

        # Combinar os dados
        combined_temperatures = np.concatenate((normal_temperatures, anomalous_temperatures))

        # Embaralhar a ordem dos dados
        shuffled_indices = np.random.permutation(len(combined_temperatures))
        shuffled_temperatures = combined_temperatures[shuffled_indices]

        # Salvar os dados em um arquivo com formato de inteiros
        filename = f'sensor_data{i}.csv'
        np.savetxt(filename, shuffled_temperatures, delimiter=',', fmt='%f')

if __name__ == "__main__":
    generate_sensor_data()
