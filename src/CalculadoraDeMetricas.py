
from sklearn.metrics import precision_score, recall_score, f1_score
import pandas as pd
import os
import csv


def computa_metricas(caminho_nome_arquivo):

    df = pd.read_csv(caminho_nome_arquivo)

    df['Label_Cod'] = df['Label'].map({'correto': 1, 'incorreto': 0})
    df['Predicao_Cod'] = df['Predição'].map({'P-correto': 1, 'P-incorreto': 0})

    # Calcular métricas
    precision = precision_score(df['Label_Cod'], df['Predicao_Cod'])
    recall = recall_score(df['Label_Cod'], df['Predicao_Cod'])
    f_measure = f1_score(df['Label_Cod'], df['Predicao_Cod'])

    # Adicionar as métricas como novas colunas ao DataFrame
    df['Precisao'] = precision
    df['Recall'] = recall
    df['F-Measure'] = f_measure

    # Salvar o dataFrame atualizado no mesmo arquivo do sensor
    df.to_csv(caminho_nome_arquivo, index=False)

def computa_media_metricas(caminho_arquivo, grupo_execucao, tempo_processamento_total, sensor):

    df = pd.read_csv(caminho_arquivo)

    # Calcular a média da coluna 'F-Measure'
    media_f_measure = df['F-Measure'].mean()

    os.makedirs(os.path.dirname('resultados/resumo/'), exist_ok=True)

    with open(f"{'resultados/resumo/'}F1-Measure-{grupo_execucao}-.csv", mode='a', newline='') as file:
        writer = csv.writer(file)

        # Escrevendo o cabeçalho se for o primeiro registro no arquivo
        if file.tell() == 0:
            writer.writerow(["Sensor","Grupo de Execução", "F1-Measure", "Tempo Processamento"])


        writer.writerow([sensor, grupo_execucao, media_f_measure, tempo_processamento_total])





