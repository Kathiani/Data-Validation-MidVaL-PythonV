from numpy.ma.core import concatenate
from sklearn.metrics import precision_score, recall_score, f1_score
import pandas as pd
import os

def startmetricas(caminho_arquivo):

    df = pd.read_csv(caminho_arquivo)

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

    # Salvar o DataFrame atualizado no mesmo arquivo CSV
    df.to_csv(caminho_arquivo, index=False)



