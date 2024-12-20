from io import StringIO
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score


def computa_Metricas(caminho_nome_arquivo, pasta_resumo, grupo_execucao, q_sensores, tempo_processamento):
    # Carregar o arquivo CSV
    try:
        df = pd.read_csv((caminho_nome_arquivo))
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        exit()

    #sensor_data = pd.read_csv(caminho_nome_arquivo)
    # Verificar se as colunas esperadas existem
    required_columns = ['Label', 'Predição']
    if not all(col in df.columns for col in required_columns):
        print(f"Erro: O arquivo CSV deve conter as colunas {required_columns}")
        exit()

    # Verificar e tratar valores nulos
    if df[required_columns].isnull().any().any():
        print("Aviso: Valores nulos encontrados. Eles serão removidos.")
        df.dropna(subset=required_columns, inplace=True)

    # Mapeamento para transformar 'correto/incorreto' em valores binários
   # df['Label_Cod'] = df['Label'].map({'correto': 1, 'incorreto': 0})
   # df['Predicao_Cod'] = df['Predição'].map({'P-correto': 1, 'P-incorreto': 0})

    # Calcular VP, VN, FP e FN
   # vp = len(df[(df['Label_Cod'] == 0) & (df['Predicao_Cod'] == 0)])  # Verdadeiros Positivos
    #vn = len(df[(df['Label_Cod'] == 1) & (df['Predicao_Cod'] == 1)])  # Verdadeiros Negativos
   # fp = len(df[(df['Label_Cod'] == 1) & (df['Predicao_Cod'] == 0)])  # Falsos Positivos
    #fn = len(df[(df['Label_Cod'] == 0) & (df['Predicao_Cod'] == 1)])  # Falsos Negativos

    df['Label_Cod'] = df['Label'].map({'correto': 0, 'incorreto': 1})
    df['Predicao_Cod'] = df['Predição'].map({'P-correto': 0, 'P-incorreto': 1})

    # Calcular VP, VN, FP e FN
    vp = len(df[(df['Label_Cod'] == 1) & (df['Predicao_Cod'] == 1)])  # Verdadeiros Positivos
    vn = len(df[(df['Label_Cod'] == 0) & (df['Predicao_Cod'] == 0)])  # Verdadeiros Negativos
    fp = len(df[(df['Label_Cod'] == 0) & (df['Predicao_Cod'] == 1)])  # Falsos Positivos
    fn = len(df[(df['Label_Cod'] == 1) & (df['Predicao_Cod'] == 0)])  # Falsos Negativos

    # Calcular métricas usando sklearn
    precision = precision_score(df['Label_Cod'], df['Predicao_Cod'])
    recall = recall_score(df['Label_Cod'], df['Predicao_Cod'])
    f_measure = f1_score(df['Label_Cod'], df['Predicao_Cod'])

    # Calcular métricas
    # precision = precision_score(df['Label_Cod'], df['Predicao_Cod'])
    # recall = recall_score(df['Label_Cod'], df['Predicao_Cod'])
    # f_measure = f1_score(df['Label_Cod'], df['Predicao_Cod'])
    # accuracy = accuracy_score(df['Label_Cod'], df['Predicao_Cod'])

    # Cálculo manual das métricas
    precision2 = vp / (vp + fp) if (vp + fp) != 0 else 0
    recall2 = vp / (vp + fn) if (vp + fn) != 0 else 0
    f1_measure2 = (2 * precision2 * recall2) / (precision2 + recall2) if (precision2 + recall2) != 0 else 0

    # Exibir resultados
    print(f'f*****************Grupo execução***/{grupo_execucao}')
    print(f"VP (Verdadeiros Positivos): {vp}")
    print(f"VN (Verdadeiros Negativos): {vn}")
    print(f"FP (Falsos Positivos): {fp}")
    print(f"FN (Falsos Negativos): {fn}")
    print(f"Precisão: {precision:.2f}")
    print(f"Revocação: {recall:.2f}")
    print(f"F1-Score: {f_measure:.2f}")
    print(f"\nPrecisão2: {precision2:.2f}")
    print(f"Revocação2: {recall2:.2f}")
    print(f"F1-Score2: {f1_measure2:.2f}")


