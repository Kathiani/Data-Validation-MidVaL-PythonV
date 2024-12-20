import pandas as pd
import matplotlib.pyplot as plt

#file_path = '/home/kathiani/midval/dados/temperatura/incorretos/L1/Bias-temperatura1.csv'


def plotardados_e_erros():

    # Substitua pelo caminho correto do seu arquivo CSV
    file_path = '/home/kathiani/midval/dados/temperatura-sazonais/incorretos/L2/LossAccuracy-temperatura1.csv'

    # Carregar o CSV e garantir nomes de colunas limpos
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()  # Remove espaços extras nos nomes das colunas

    # Filtrar os 20 primeiros pontos
    data_firstpoints = data.head(5000)

    # Obter índices e valores dos 20 primeiros
    x = data_firstpoints.index
    y = data_firstpoints['Dados']

    # Identificar os pontos com Label "incorreto" nos 20 primeiros
    incorrect_points = data_firstpoints[data_firstpoints['Label'].str.strip() == 'incorreto']

    # Plotar a curva dos 200 primeiros
    plt.figure(figsize=(15, 6), facecolor='gray')  # Garante fundo branco
    plt.plot(x, y, label='Dados Corretos', color='blue', marker='o', linestyle='-', alpha=0.7)

    # Adicionar os valores dos dados em cada ponto
    for i in range(len(data_firstpoints)):
        plt.text(x[i], y.iloc[i], str(y.iloc[i]), fontsize=10, ha='center', va='bottom')

    # Destacar os pontos "incorretos" entre os 20 primeiros
    plt.scatter(incorrect_points.index, incorrect_points['Dados'], color='red', label='Dado com Erro Aplicado', zorder=5)

    # Configurar o gráfico
    #plt.title('Curva dos 20 Primeiros Dados com Destaque e Valores')
    plt.xlabel('50 Leituras com Erros Injetados')
    plt.ylabel('Valor do Dado')
    plt.legend()
    plt.grid(True)

    # Salvar o gráfico em um arquivo
    output_path = '/home/kathiani/midval/dados/plots/LossAccuracy-temperatura1.png'
    plt.savefig(output_path, bbox_inches='tight', dpi=300)  # Aumenta a resolução

    # Exibir o gráfico
    plt.show()



plotardados_e_erros()
