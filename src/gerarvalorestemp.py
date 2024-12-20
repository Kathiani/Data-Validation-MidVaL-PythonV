
import numpy as np
import os
import matplotlib.pyplot as plt


# Função para gerar dados de temperatura considerando as horas especificadas
def generate_temperature_data(pasta_dadoscorretos, num_dias=1):
    # Temperaturas para os horários específicos - Previsão para Dia 19/11 São Paulo - SP
    times_of_day = [
        (0, 22),  # 00:00h - 22°C
        (6, 18),  # 06:00h - 18°C
        (12, 30),  # 12:00h - 30°C
        (18, 24)  # 18:00h - 24°C
    ]

    # Gerar dados para cada dia
    for dia in range(1, num_dias + 1):
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
        nomesensor = f"temperatura_dia{dia}"

        # Caminho completo para salvar os dados
        caminho_arquivo = os.path.join(pasta_dadoscorretos, f'{nomesensor}.csv')

        # Salvar os dados de temperatura para o dia
        np.savetxt(caminho_arquivo, daily_data, delimiter=',', fmt='%.1f', header="Temperatura", comments='')

def plot_temperature_data(caminho_arquivo):
    # Carregar os dados do CSV
    dados = np.loadtxt(caminho_arquivo, delimiter=',', skiprows=1)  # Ignorar o header

    # Criar o gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(dados, label="Temperatura", color='tab:blue')

    # Adicionar título e rótulos
    plt.title("Variação da Temperatura ao Longo do Dia", fontsize=14)
    plt.xlabel("Tempo (segundos)", fontsize=12)
    plt.ylabel("Temperatura (°C)", fontsize=12)

    # Mostrar a legenda
    plt.legend()

    # Exibir o gráfico
    plt.grid(True)
    plt.show()


# Exemplo de uso da função
generate_temperature_data('/home/kathiani/midval/dados/')
plot_temperature_data('/home/kathiani/midval/dados/temperatura_dia1.csv')


