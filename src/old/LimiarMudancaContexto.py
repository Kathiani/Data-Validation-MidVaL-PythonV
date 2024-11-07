import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Função para carregar os L1-10pt do sensor
def load_sensor_data(filename):
    return pd.read_csv(filename, header=None).values.flatten()


# Função para identificar mudanças abruptas
def identify_abrupt_changes(data, threshold):
    # Calcula a diferença entre os valores consecutivos
    derivative = np.diff(data)

    # Identifica onde a diferença excede o limiar
    abrupt_changes_indices = np.where(np.abs(derivative) > threshold)[0] + 1  # Ajusta o índice

    return abrupt_changes_indices


# Função para verificar se os próximos 5 valores são próximos ao pico de mudança
def verify_values_near_peak(data, abrupt_changes_indices, num_near=5, tolerance=5):
    results = []

    for idx in abrupt_changes_indices:
        if idx + num_near < len(data):  # Verifica se há espaço suficiente para os próximos 5 valores
            peak_value = data[idx]
            next_values = data[idx + 1:idx + 1 + num_near]

            # Verifica se todos os próximos 5 valores estão dentro da tolerância do pico
            if np.all(np.abs(next_values - peak_value) <= tolerance):
                results.append((idx, peak_value, next_values))

    return results


if __name__ == "__main__":
    # Carregar os L1-10pt do sensor
    data = load_sensor_data('../../dados/L1-10pt/sets/sensor_data2.csv')

    # Definir o limiar para mudanças abruptas
    threshold = 5  # Ajuste conforme necessário

    # Identificar mudanças abruptas
    abrupt_changes_indices = identify_abrupt_changes(data, threshold)

    # Verificar se os próximos 5 valores são próximos ao pico de mudança
    results = verify_values_near_peak(data, abrupt_changes_indices, num_near=5, tolerance=1)

    # Plotar a série temporal e as mudanças abruptas
    plt.figure(figsize=(12, 6))
    plt.plot(data, label='Série Temporal', color='blue', marker='o')

    # Marcar mudanças abruptas com um ponto vermelho
    plt.scatter(abrupt_changes_indices, data[abrupt_changes_indices], color='red', label='Mudanças Abruptas', zorder=5)

    # Marcar picos de mudança e próximos valores
    for idx, peak_value, next_values in results:
        plt.scatter([idx], [peak_value], color='purple', label='Pico de Mudança', zorder=10)
        #plt.scatter(range(idx + 1, idx + 1 + len(next_values)), next_values, color='orange', label='Próximos Valores')

    plt.title('Detecção de Mudanças Abruptas e Verificação de Valores Próximos')
    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.legend()
    plt.show()

    # Mostrar resultados
    for idx, peak_value, next_values in results:
        print(f"Pico de mudança no índice {idx} com valor {peak_value}")
        print(f"Próximos 5 valores: {next_values}")
