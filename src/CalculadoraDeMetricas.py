
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score
import pandas as pd
import os
import csv


def computa_Fmeasure(caminho_nome_arquivo, pasta_resumo, grupo_execucao, n_sensores, tempo_processamento):

    df = pd.read_csv(caminho_nome_arquivo)

    #df['Label_Cod'] = df['Label'].map({'correto': 1, 'incorreto': 0})
    #df['Predicao_Cod'] = df['Predição'].map({'P-correto': 1, 'P-incorreto': 0})

    #precision = precision_score(df['Label_Cod'], df['Predicao_Cod'])
    #recall = recall_score(df['Label_Cod'], df['Predicao_Cod'])
    #f_measure = f1_score(df['Label_Cod'], df['Predicao_Cod'])

    df['Label_Cod'] = df['Label'].map({'correto': 0, 'incorreto':1})
    df['Predicao_Cod'] = df['Predição'].map({'P-correto': 0, 'P-incorreto':1})

    # Calcular a matriz de confusão
    cm = confusion_matrix(df['Label_Cod'], df['Predicao_Cod'])

    vp = len(df[(df['Label_Cod'] == 1) & (df['Predicao_Cod'] == 1)])  # Verdadeiros Positivos
    vn = len(df[(df['Label_Cod'] == 0) & (df['Predicao_Cod'] == 0)])  # Verdadeiros Negativos
    fp = len(df[(df['Label_Cod'] == 0) & (df['Predicao_Cod'] == 1)])  # Falsos Positivos
    fn = len(df[(df['Label_Cod'] == 1) & (df['Predicao_Cod'] == 0)])  # Falsos Negativos

    # Cálculo manual das métricas
    precision = vp / (vp + fp) if (vp + fp) != 0 else 0
    recall = vp / (vp + fn) if (vp + fn) != 0 else 0
    f1_measure = (2 * precision * recall) / (precision + recall) if (precision + recall) != 0 else 0



    accuracy = accuracy_score(df['Label_Cod'], df['Predicao_Cod'])

    # Definir o nome do arquivo
    arquivo_resultados = f'{pasta_resumo}/Metricas-Por-Sensor/{grupo_execucao}_{n_sensores}.txt'
    os.makedirs(os.path.dirname(arquivo_resultados), exist_ok=True)

    # Abrir o arquivo no modo de escrita
    with open(arquivo_resultados, 'w') as f:
        # Escrever os resultados de forma formatada
        f.write(f"Número do Sensor: {n_sensores}\n")
        f.write(f"Resultados da Execução: {grupo_execucao}\n")
        f.write("=" * 50 + "\n")
        f.write("Matriz de Confusão:\n")
        f.write(f"{cm}\n\n")  # Exibindo a matriz de confusão

        f.write(f"Verdadeiros Positivos (VP): {vp}\n")
        f.write(f"Verdadeiros Negativos (VN): {vn}\n")
        f.write(f"Falsos Positivos (FP): {fp}\n")
        f.write(f"Falsos Negativos (FN): {fn}\n\n")

        f.write(f"Precision: {precision:.4f}\n")
        f.write(f"Recall: {recall:.4f}\n")
        f.write(f"F1-Score: {f1_measure:.4f}\n")
        f.write(f"Acurácia: {accuracy:.4f}\n")

        # Separador final
        f.write("=" * 50 + "\n")


        with open(f"{pasta_resumo}/F1-Measure-{grupo_execucao}-.csv", mode='a', newline='') as file:
            writer = csv.writer(file)

            # Escrevendo o cabeçalho se for o primeiro registro no arquivo
            if file.tell() == 0:
               writer.writerow(["Sensor", "Grupo de Execução", "Precision", "Recall", "F1-Measure", "Accuracy", "Tempo Processa Sensor"])

            writer.writerow([n_sensores, grupo_execucao, precision, recall, f1_measure, accuracy, tempo_processamento])


def computa_media_geral_metricas(pasta_resultados, pasta_resumo):

    medias_resultados = []
    caminho_resumo = f'{pasta_resumo}/Media-Geral/Media_Geral_Metricas.csv'
    os.makedirs(os.path.dirname(caminho_resumo), exist_ok=True)

    # Escrever o cabeçalho no arquivo de resumos
    with open(caminho_resumo, mode='w', newline='') as file:  # Use 'w' para sobrescrever
        writer = csv.writer(file)
        writer.writerow(["Arquivo", "Média F1-Measure", "Média Accuracy", "Média Tempo Processamento"])

    # Loop por cada arquivo na pasta
    for arquivo in os.listdir(pasta_resumo):
        if arquivo.endswith('.csv') and "Media-metricas" not in arquivo:  # Evita processar o próprio arquivo de resumo
            caminho_arquivo = os.path.join(pasta_resumo, arquivo)

            # Ler o arquivo CSV em um DataFrame
            df = pd.read_csv(caminho_arquivo)

            # Calcular as métricas
            media_f_measure = df['F1-Measure'].mean()
            media_accuracy = df['Accuracy'].mean()
            media_tempo_processamento = df['Tempo Processa Sensor'].mean()

            # Adicionar os resultados no arquivo de resumo
            with open(caminho_resumo, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([arquivo, media_f_measure, media_accuracy, media_tempo_processamento])










def computa_media_Fmeasure(pasta_resumo, grupo_execucao, nsensor):
    df = pd.read_csv(pasta_resumo)

    # Calcular médias
    media_f_measure = df['F1-Measure'].mean()
    media_t_processamento = df['Tempo Processamento Dado'].mean()
    media_accuracy = df['Accuracy'].mean()
    print("Media accuracy")


    with open(f"{pasta_resumo}/F1-Measure-{grupo_execucao}-.csv", mode='a', newline='') as file:
        writer = csv.writer(file)

        # Escrevendo o cabeçalho se for o primeiro registro no arquivo
        if file.tell() == 0:
            writer.writerow(["Sensor", "Grupo de Execução", "F1-Measure", "Accuracy", "Tempo Processamento"])

        writer.writerow([nsensor, grupo_execucao, media_f_measure, media_accuracy, media_t_processamento])

