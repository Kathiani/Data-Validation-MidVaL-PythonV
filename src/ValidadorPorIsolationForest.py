
import pandas as pd
import time, os
from sklearn.ensemble import IsolationForest
from src.CalculadoraDeMetricas import computa_metricas
from src.CalculadoraDeMetricas import computa_media_metricas


def salvar_em_arquivo(sensor_data, data, forecasts, caminho_arquivo):

    # Avaliando verdadeiros positivos
    labels = sensor_data.iloc[:, 1].values
    comparacao = []

    for true, pred in zip(labels, forecasts):
        if true == 'correto' and pred == 1:
            comparacao.append('VP')
        elif true == 'incorreto' and pred == 1:
            comparacao.append('FN')
        elif true == 'correto' and pred == -1:
            comparacao.append('FP')
        elif true == 'incorreto' and pred == -1:
            comparacao.append('VN')
        else:
            comparacao.append('Análise incorreta!')


    # Criar DataFrame para salvar os valores e previsões
    df = pd.DataFrame({
        'Dado': data.flatten(),
        'Label': sensor_data.iloc[:, 1].values,
        'Predição': ['P-correto' if pred == 1 else 'P-incorreto' for pred in forecasts],
        'Avaliação': comparacao
    })

    df.to_csv(caminho_arquivo, index=False)



def startisolationforest(n_sensores, tecnica):

    tiposensor = 'temperatura'
    tipo_erro = ['LossAccuracy', 'Drift', 'Noise', 'Bias', 'Freezing']
    lote = 'L1'


    for n in tipo_erro:
        grupo_execucao = f'{tecnica}-{n}-{lote}'

        caminho_arquivo = f'resultados/{tecnica}/{n}/{grupo_execucao}'
        os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)  # Criar diretório para salvar numa primeira execução

        for i in range(1, n_sensores + 1):
            sensor_name = f'{n}-{tiposensor}{i}'
            sensor_open = f'/home/kathiani/midval/dados/{tiposensor}/{lote}/{sensor_name}.csv' #Os arquivos foram salvos seguindo essa ordem

            sensor_data = pd.read_csv(sensor_open)

            # Supondo que a coluna de interesse seja a primeira coluna
            data = sensor_data.iloc[:, 0].values

            # Reshape dos L1-10pt para ajuste do modelo
            data = data.reshape(-1, 1)

            start_time = time.time()

            # Definir os parâmetros para o modelo Isolation Forest
            params = {
                'n_estimators': 100,
                'max_samples': 'auto',
                'contamination': 0.1,
                'max_features': 1.0,
                'random_state': 42
            }

            # Ajustar o modelo
            iso_forest = IsolationForest(**params)
            iso_forest.fit(data)
            iso_preds = iso_forest.predict(data)


            end_time = time.time()
            tempoprocessamento_atual = end_time - start_time


            caminho_nome_arquivo = f'resultados/{tecnica}/{n}/{grupo_execucao}-{tiposensor}-{i}.csv'

            salvar_em_arquivo(sensor_data, data, iso_preds, caminho_nome_arquivo)
            computa_metricas(caminho_nome_arquivo)  # Computa e armazena F1-Score para o sensor atual
            computa_media_metricas(caminho_nome_arquivo, grupo_execucao, tempoprocessamento_atual, i)





