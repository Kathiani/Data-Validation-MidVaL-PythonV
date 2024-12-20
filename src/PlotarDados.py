import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#file_path = '/home/kathiani/midval/dados/temperatura/incorretos/L1/Bias-temperatura1.csv'


def plotardados_e_erros():

    # Substitua pelo caminho correto do seu arquivo CSV
    file_path = '/home/kathiani/midval/dados/temperatura-sazonais/incorretos/L1/Bias-temperatura1.csv'

    # Carregar o CSV e garantir nomes de colunas limpos
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()  # Remove espaços extras nos nomes das colunas

    # Filtrar os 20 primeiros pontos
    data_firstpoints = data.head(8000)

    # Obter índices e valores dos 20 primeiros
    x = data_firstpoints.index
    y = data_firstpoints['Dados']

    # Identificar os pontos com Label "incorreto" nos 20 primeiros
    incorrect_points = data_firstpoints[data_firstpoints['Label'].str.strip() == 'incorreto']

    # Plotar a curva dos 200 primeiros
    plt.figure(figsize=(20, 10), facecolor='gray')  # Garante fundo branco
    plt.plot(x, y, label='Dados Corretos', color='blue', marker='o', linestyle='-', alpha=0.6)

    # Adicionar os valores dos dados em cada ponto
    for i in range(len(data_firstpoints)):
        plt.text(x[i], y.iloc[i], str(y.iloc[i]), fontsize=10, ha='center', va='bottom')

    # Destacar os pontos "incorretos" entre os 20 primeiros
    plt.scatter(incorrect_points.index, incorrect_points['Dados'], color='purple', label='Dado com Erro Aplicado', zorder=5)

    # Configurar o gráfico
    #plt.title('Curva dos 20 Primeiros Dados com Destaque e Valores')
    plt.xlabel('60 Leituras - Sensor Temperatura')
    plt.ylabel('Valor do Dado')
    plt.legend()
    plt.grid(True)

    # Salvar o gráfico em um arquivo
    #output_path = '/home/kathiani/midval/dados/plots/exemplo-Bias-corrigidos.png'
    #plt.savefig(output_path, bbox_inches='tight', dpi=300)  # Aumenta a resolução

    # Exibir o gráfico
    plt.show()

def plotar_erros_comparados(caminho_corretos, caminho_incorretos):

        # Ler dados corretos
        dados_corretos = pd.read_csv(caminho_corretos)
        dados_corretos.columns = dados_corretos.columns.str.strip()

        # Ler dados incorretos
        dados_incorretos = pd.read_csv(caminho_incorretos)
        dados_incorretos.columns = dados_incorretos.columns.str.strip()

        # Garantir que os dois têm o mesmo índice para comparação
        if len(dados_corretos) != len(dados_incorretos):
            print("Os arquivos possuem tamanhos diferentes!")
            return

        # Filtrar para as 60 primeiras leituras
        dados_corretos = dados_corretos.head(20)
        dados_incorretos = dados_incorretos.head(20)

        # Comparar e identificar diferenças
        comparacao = pd.DataFrame({
            "Valor Correto": dados_corretos['Dados'],
            "Valor Errôneo": dados_incorretos['Dados']
        })
        comparacao['Desvio'] = comparacao['Valor Errôneo'] - comparacao['Valor Correto']

        # Exibir os primeiros 10 registros para validação
        print(comparacao.head(10))

        # Criar gráfico
        plt.figure(figsize=(15, 10))

        # Plotar valores corretos e errôneos com pontos
        plt.plot(comparacao.index, comparacao['Valor Correto'], label='Sequência Normal', color='green', alpha=0.8)
        plt.plot(comparacao.index, comparacao['Valor Errôneo'], label='Sequência com Erros', color='red', alpha=0.8)

        # Adicionar linhas conectando os valores corretos e errôneos
        for i in comparacao.index:
            plt.plot(
                [i, i],
                [comparacao['Valor Correto'][i], comparacao['Valor Errôneo'][i]],
                color='blue', linestyle='--', alpha=0.5
            )

        # Adicionar valores como texto no gráfico
        for i in comparacao.index:
            plt.text(i, comparacao['Valor Correto'][i], f"{comparacao['Valor Correto'][i]:.2f}",
                    color='green', fontsize=8, ha='center', va='bottom')
            plt.text(i, comparacao['Valor Errôneo'][i], f"{comparacao['Valor Errôneo'][i]:.2f}",
                     color='red', fontsize=8, ha='center', va='top')

        # Configurações do gráfico
        plt.xlabel('Índice')
        plt.ylabel('Valor')
        plt.title('Comparação entre Valores Corretos e Errôneos (60 Leituras)')
        plt.legend()
        plt.grid(True)

        # Salvar gráfico
        output_path = '/home/kathiani/midval/dados/plots/temperatura-Bias.png'
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.show()



# Chamar a função
def comparar_sequencias_plotar_erros():
    caminho_corretos = '/home/kathiani/midval/dados/temperatura/corretos/L2/temperatura1.csv'
    caminho_incorretos = '/home/kathiani/midval/dados/temperatura/incorretos/L2/Drift-temperatura1.csv'
    plotar_erros_comparados(caminho_corretos, caminho_incorretos)


def plotar_freezing():
    import pandas as pd
    import matplotlib.pyplot as plt

    # Caminho do arquivo CSV
    file_path = '/home/kathiani/midval/dados/temperatura-sazonais/corretos/L2/temperatura1.csv'

    # Carregar o CSV e garantir nomes de colunas limpos
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()  # Remove espaços extras nos nomes das colunas

    # Definir o intervalo para os dados do meio
    meio = len(data) // 2  # Meio do DataFrame
    tamanho_selecao = 300  # O tamanho da seção a ser plotada

    # Selecionar os dados do meio
    data_middle = data.iloc[meio - tamanho_selecao // 2: meio + tamanho_selecao // 2]

    # Obter índices e valores da seção do meio
    x = data_middle.index
    y = data_middle['Dados']

    # Identificar os pontos com Label "incorreto" nos dados do meio
   # incorrect_points = data_middle[data_middle['Label'].str.strip() == 'incorreto']

    # Plotar a curva dos dados do meio
    plt.figure(figsize=(20, 10), facecolor='gray')  # Garante fundo branco
    plt.plot(x, y, label='Dados Corretos', color='blue', marker='o', linestyle='-', alpha=0.6)

    # Adicionar os valores dos dados em cada ponto
    for i in range(len(data_middle)):
        plt.text(x[i], y.iloc[i], str(y.iloc[i]), fontsize=10, ha='center', va='bottom')

    # Destacar os pontos "incorretos" nos dados do meio
    #plt.scatter(incorrect_points.index, incorrect_points['Dados'], color='purple', label='Dado com Erro Aplicado',
              #  zorder=5)

    # Configurar o gráfico
    plt.xlabel('Leituras - Sensor Temperatura')
    plt.ylabel('Valor do Dado')
    plt.legend()
    plt.grid(True)

    # Salvar o gráfico em um arquivo
    #output_path = '/home/kathiani/midval/dados/plots/exemplo-Freezing.png'
    #plt.savefig(output_path, bbox_inches='tight', dpi=300)  # Aumenta a resolução

    # Exibir o gráfico
    plt.show()

def plotardeteccoes():
    import pandas as pd
    import matplotlib.pyplot as plt

    # Caminho do arquivo CSV
    caminho_entrada = '/home/kathiani/PycharmProjects/Algoritmos_Validacao_AjusteMatrizConfusao/src/resultados-ajustes/svm/Noise/L1/L1svm-Noise-L1-temperatura-13.csv'
    # Carregar o CSV e garantir nomes de colunas limpos
    data = pd.read_csv(caminho_entrada)
    data.columns = data.columns.str.strip()  # Remove espaços extras nos nomes das colunas

    # Filtrar os 50 primeiros pontos
    data_firstpoints = data.head(50)

    # Obter índices e valores dos 50 primeiros
    x = data_firstpoints.index
    y = data_firstpoints['Dado']

    # Identificar os pontos com Avaliação "VN" (Verdadeiros Negativos)
    vn_points = data_firstpoints[data_firstpoints['Avaliação'].str.strip() == 'VN']

    # Identificar os pontos com Avaliação "VP" (Verdadeiros Positivos)
    vp_points = data_firstpoints[data_firstpoints['Avaliação'].str.strip() == 'VP']

    # Identificar os pontos com Avaliação "VP" (Verdadeiros Positivos)
    #fp_points = data_firstpoints[data_firstpoints['Avaliação'].str.strip() == 'FP']

    fn_points = data_firstpoints[data_firstpoints['Avaliação'].str.strip() == 'FN']

    # Criar o gráfico
    plt.figure(figsize=(20, 10), facecolor='white')  # Fundo branco para o gráfico

    # Plotar a curva completa dos 50 primeiros
    plt.plot(x, y, label='Curva de Dados', color='black', marker='o', linestyle='-', alpha=0.6)

    # Destacar os pontos "Verdadeiros Negativos (VN)"
    plt.scatter(vn_points.index, vn_points['Dado'], color='blue', label='Verdadeiros Negativos (VN)', zorder=5)

    # Destacar os pontos "Verdadeiros Positivos (VP)"
    plt.scatter(vp_points.index, vp_points['Dado'], color='red', label='Verdadeiros Positivos (VP)', zorder=5)

    # Destacar os pontos "Verdadeiros Positivos (VP)"
    #plt.scatter(vp_points.index, fp_points['Dado'], color='green', label='Falso Positivos (FP)', zorder=5)

    # Destacar os pontos "Verdadeiros Positivos (VP)"
    #plt.scatter(vp_points.index, fn_points['Dado'], color='orange', label='Falso Negativo (FN)', zorder=5)

    # Adicionar os valores dos dados em cada ponto
    for i in range(len(data_firstpoints)):
        plt.text(x[i], y.iloc[i], str(y.iloc[i]), fontsize=10, ha='center', va='bottom')

    # Configurar o gráfico
    plt.title('Curva dos 50 Primeiros Dados com Destaque para VN e VP', fontsize=16)
    plt.xlabel('Índice dos Dados', fontsize=12)
    plt.ylabel('Valor do Dado', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True)

    # Salvar o gráfico como PNG
    plt.savefig('/home/kathiani/midval/dados/plots/deteccoes/svm-Noise-L1-temperatura-13.png', dpi=300)

    # Mostrar o gráfico
    plt.show()


#plotardados_e_erros()
#comparar_sequencias_plotar_erros()
#plotar_freezing()
plotardeteccoes()