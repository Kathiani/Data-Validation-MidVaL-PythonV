
from sklearn.metrics import precision_score, recall_score, f1_score
import pandas as pd
import os
import csv


def computa_Fmeasure(caminho_nome_arquivo, pasta_resumo, grupo_execucao, q_sensores, tempo_processamento):

    df = pd.read_csv(caminho_nome_arquivo)

    df['Label_Cod'] = df['Label'].map({'correto': 1, 'incorreto': 0})
    df['Predicao_Cod'] = df['Predição'].map({'P-correto': 1, 'P-incorreto': 0})

    # Calcular métricas
    precision = precision_score(df['Label_Cod'], df['Predicao_Cod'])
    recall = recall_score(df['Label_Cod'], df['Predicao_Cod'])
    f_measure = f1_score(df['Label_Cod'], df['Predicao_Cod'])

    with open(f"{pasta_resumo}/F1-Measure-{grupo_execucao}-.csv", mode='a', newline='') as file:
        writer = csv.writer(file)

        # Escrevendo o cabeçalho se for o primeiro registro no arquivo
        if file.tell() == 0:
            writer.writerow(["Sensor", "Grupo de Execução", "Precision", "Recall", "F1-Measure", "Tempo Processa Sensor"])

        writer.writerow([q_sensores, grupo_execucao, precision, recall, f_measure, tempo_processamento])


def computa_media_geral_metricas(pasta_resultados, pasta_resumo):

    medias_resultados = []

    # Loop por cada arquivo na pasta
    for arquivo in os.listdir(pasta_resumo):
        if arquivo.endswith('.csv'):  # Apenas processa arquivos CSV
            caminho_arquivo = os.path.join(pasta_resumo, arquivo)

            # Ler o arquivo CSV em um DataFrame
            df = pd.read_csv(caminho_arquivo)

            # Calcular a média da coluna 'F1-Measure' e 'Tempo Processamento'
            media_f_measure = df['F1-Measure'].mean()
            media_tempo_processamento = df['Tempo Processa Sensor'].mean()

            # Armazenar as médias com o nome do arquivo
            medias_resultados.append((arquivo, media_f_measure, media_tempo_processamento))

    # Calcular a média geral de F1-Measure e Tempo Processamento de todos os arquivos
    media_geral_f_measure = sum(media_f for _, media_f, _ in medias_resultados) / len(medias_resultados)
    media_geral_tempo_processamento = sum(media_t for _, _, media_t in medias_resultados) / len(medias_resultados)

    # Caminho para o arquivo de resumo
    caminho_resumo = f'{pasta_resumo}/Media_Geral_Metricas.csv'
    os.makedirs(os.path.dirname(caminho_resumo), exist_ok=True)

    # Escrever as médias no arquivo de resumos
    with open(caminho_resumo, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Escrever o cabeçalho
        writer.writerow(["Arquivo", "Média F1-Measure", "Média Tempo Processamento"])

        # Adicionar as médias de cada arquivo
        for arquivo, media_f, media_t in medias_resultados:
            writer.writerow([arquivo, media_f, media_t])

















def computa_media_Fmeasure(pasta_resumo, grupo_execucao, nsensor):
    df = pd.read_csv(pasta_resumo)

    # Calcular a média da coluna 'F-Measure'
    media_f_measure = df['F1-Measure'].mean()
    media_t_processamento = df['Tempo Processamento Dado'].mean()


    with open(f"{pasta_resumo}/F1-Measure-{grupo_execucao}-.csv", mode='a', newline='') as file:
        writer = csv.writer(file)

        # Escrevendo o cabeçalho se for o primeiro registro no arquivo
        if file.tell() == 0:
            writer.writerow(["Sensor", "Grupo de Execução", "F1-Measure", "Tempo Processamento"])

        writer.writerow([nsensor, grupo_execucao, media_f_measure, media_t_processamento])




