from scipy.stats import shapiro
from scipy import stats
from scipy.stats import mannwhitneyu
import os
import pandas as pd

def teste_shapiro():
    # Diretório onde os arquivos CSV estão localizados
    diretorio_csv = '/home/kathiani/PycharmProjects/Algoritmos-Validacao/src/resultados/resumo'

    # Diretório onde o arquivo de resultados será salvo
    diretorio_resultado = '/home/kathiani/PycharmProjects/Algoritmos-Validacao/src/resultados/resumo'

    # Caminho completo para o arquivo onde os resultados serão salvos
    arquivo_resultado = os.path.join(diretorio_resultado, 'Resultados-shapiro-tempo-processamento.csv')

    if not os.path.exists(diretorio_resultado):
        os.makedirs(diretorio_resultado)

    # Abre o arquivo de resultados em modo de escrita
    with open(arquivo_resultado, 'w') as f:
        f.write("Arquivo, Resultado Shapiro-Wilk, p-valor\n")

        # Itera sobre todos os arquivos no diretório de arquivos CSV
        for arquivo in os.listdir(diretorio_csv):
            if arquivo.endswith('.csv'):
                # Lê o arquivo CSV com tratamento de erro
                caminho_arquivo = os.path.join(diretorio_csv, arquivo)
                try:
                    df = pd.read_csv(caminho_arquivo)

                    # Verifica se a coluna 'F1-Measure' está presente
                    if 'Tempo Processamento' in df.columns:
                        # Realiza o teste de Shapiro-Wilk
                        estatistica, p_valor = shapiro(df['Tempo Processamento'])

                        # Define o nível de significância (ex: 0.05)
                        alpha = 0.05
                        resultado = "Distribuição Normal" if p_valor > alpha else "Distribuição  Não Normal"

                        # Escreve o resultado no arquivo
                        f.write(f"{arquivo}, {resultado}, {p_valor:.15f}\n")
                    else:
                        # Coluna 'F1-Measure' ausente
                        f.write(f"{arquivo}, Coluna 'F1-Measure' ausente, N/A\n")

                except Exception as e:
                    # Registra qualquer erro ao ler o CSV ou ao realizar o teste
                    f.write(f"{arquivo}, Erro ao processar o arquivo: {e}, N/A\n")


def testTStudent(): #se os dados servem como distribuição normal

    # Especifique o caminho do arquivo para cada grupo
    arquivo_grupo1 = '/home/kathiani/PycharmProjects/Algoritmos-Validacao/src/resultados/resumo/F1-Measure-svm-Freezing-L1-.csv'
    arquivo_grupo2 = '/home/kathiani/PycharmProjects/Algoritmos-Validacao/src/resultados/resumo/F1-Measure-diversidade-Freezing-L1-.csv'
    # Especifique o caminho do arquivo de saída para gravar os resultados

    pasta_saida = '/home/kathiani/PycharmProjects/Algoritmos-Validacao/src/resultados/resumo/'
    arquivo_saida = os.path.join(pasta_saida, 'Resultados_T_Student.csv')

    with open(arquivo_saida, 'a') as f:
        f.write("Arquivo Grupo 1, Arquivo Grupo 2, Resultado, p-valor\n")

        try:
            # Lê os dados dos dois arquivos
            df_grupo1 = pd.read_csv(arquivo_grupo1)
            df_grupo2 = pd.read_csv(arquivo_grupo2)

            # Verifica se a coluna 'F1-Measure' está presente em ambos os arquivos
            if 'F1-Measure' in df_grupo1.columns and 'F1-Measure' in df_grupo2.columns:
                # Seleciona a coluna 'F1-Measure' para cada grupo
                grupo1 = df_grupo1['F1-Measure']
                grupo2 = df_grupo2['F1-Measure']


                if len(grupo1) > 1 and len(grupo2) > 1:
                    estatistica, p_valor = stats.ttest_ind(grupo1, grupo2)

                    # Define o nível de significância (ex: 0.05)
                    alpha = 0.05
                    resultado = "Distribuições Diferentes" if p_valor < alpha else "Distribuições Iguais"

                    # Escreve o resultado no arquivo
                    f.write(f"{arquivo_grupo1}, {arquivo_grupo2}, {resultado}, {p_valor}\n")
                else:
                    # Grupos insuficientes
                    f.write(f"{arquivo_grupo1}, {arquivo_grupo2}, Grupos insuficientes para o teste, N/A\n")

            else:
                # Coluna 'F1-Measure' ausente em um dos arquivos
                if 'F1-Measure' not in df_grupo1.columns:
                    f.write(f"{arquivo_grupo1}, Coluna 'F1-Measure' ausente, N/A\n")
                if 'F1-Measure' not in df_grupo2.columns:
                    f.write(f"{arquivo_grupo2}, Coluna 'F1-Measure' ausente, N/A\n")

        except Exception as e:
            # Registra qualquer erro ao ler os arquivos ou ao realizar o teste
            f.write(f"Erro ao processar os arquivos {arquivo_grupo1} e {arquivo_grupo2}: {e}\n")



def testMannWhitney():

    # Especifique o caminho do arquivo para cada grupo
    arquivo_grupo1 = '/home/kathiani/PycharmProjects/Algoritmos-Validacao/src/resultados/resumo/F1-Measure-isolation-Noise-L2-.csv'
    arquivo_grupo2 = '/home/kathiani/PycharmProjects/Algoritmos-Validacao/src/resultados/resumo/F1-Measure-svm-Noise-L2-.csv'
    # Especifique o caminho do arquivo de saída para gravar os resultados

    pasta_saida = '/home/kathiani/PycharmProjects/Algoritmos-Validacao/src/resultados/resumo/'
    arquivo_saida = os.path.join(pasta_saida, 'Resultados_mann_whitney.csv')


    with open(arquivo_saida, 'a') as f:
        f.write("Arquivo Grupo 1, Arquivo Grupo 2, Resultado, p-valor\n")

        try:
            # Lê os dados dos dois arquivos
            df_grupo1 = pd.read_csv(arquivo_grupo1)
            df_grupo2 = pd.read_csv(arquivo_grupo2)

            # Verifica se a coluna 'F1-Measure' está presente em ambos os arquivos
            if 'F1-Measure' in df_grupo1.columns and 'F1-Measure' in df_grupo2.columns:
                # Seleciona a coluna 'F1-Measure' para cada grupo
                grupo1 = df_grupo1['F1-Measure']
                grupo2 = df_grupo2['F1-Measure']

                # Verifica se ambos os grupos têm dados suficientes para o teste
                if len(grupo1) > 1 and len(grupo2) > 1:
                    # Realiza o teste de Mann-Whitney
                    estatistica, p_valor = mannwhitneyu(grupo1, grupo2)

                    # Define o nível de significância (ex: 0.05)
                    alpha = 0.05
                    resultado = "Distribuições Diferentes" if p_valor < alpha else "Distribuições Iguais"

                    # Escreve o resultado no arquivo
                    f.write(f"{arquivo_grupo1}, {arquivo_grupo2}, {resultado}, {p_valor:.15f}\n")
                else:
                    # Grupos insuficientes
                    f.write(f"{arquivo_grupo1}, {arquivo_grupo2}, Grupos insuficientes para o teste, N/A\n")

            else:
                # Coluna 'F1-Measure' ausente em um dos arquivos
                if 'F1-Measure' not in df_grupo1.columns:
                    f.write(f"{arquivo_grupo1}, Coluna 'F1-Measure' ausente, N/A\n")
                if 'F1-Measure' not in df_grupo2.columns:
                    f.write(f"{arquivo_grupo2}, Coluna 'F1-Measure' ausente, N/A\n")

        except Exception as e:
            # Registra qualquer erro ao ler os arquivos ou ao realizar o teste
            f.write(f"Erro ao processar os arquivos {arquivo_grupo1} e {arquivo_grupo2}: {e}\n")


teste_shapiro()
#testTStudent()
#testMannWhitney()
