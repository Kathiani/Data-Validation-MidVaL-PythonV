
from sklearn.metrics import precision_score, recall_score, f1_score
import pandas as pd


def startmetricas(caminho_arquivo, tecnica):

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
    #comparemetricas(caminho_arquivo, tecnica)

def comparemetricas(caminho_arquivo, tecnica):

    # Ler o CSV usando pandas
    df = pd.read_csv(caminho_arquivo)

    # Calcular a média da coluna 'F-Measure'
    media_f_measure = df['F-Measure'].mean()

    # Exibir o resultado
    print(f"Média do F-Measure de {tecnica}: {media_f_measure}")



