
import pandas as pd
import time, os
from sklearn.ensemble import IsolationForest
from src.CalculadoraDeMetricas import computa_Fmeasure, computa_media_Fmeasure


def salvar_predicoes_avaliacoes(sensor_data, forecasts, caminho_arquivo):

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
        'Dado': sensor_data.iloc[:, 0].values,
        'Label': sensor_data.iloc[:, 1].values,
        'Predição': ['P-correto' if pred == 1 else 'P-incorreto' for pred in forecasts],
        'Avaliação': comparacao
    })

    df.to_csv(caminho_arquivo, index=False)



def startisolationforest(n_sensores, tecnica, pasta_incorretos, pasta_resultados, pasta_resumo, tipo_sensor):


    tipo_erro = ['LossAccuracy', 'Drift', 'Noise', 'Bias', 'Freezing']
    lotes = ['L1', 'L2']


    for nlote in lotes:
        for n in tipo_erro:
            grupo_execucao = f'{tecnica}-{n}-{nlote}'
            caminho_resultados = f'{pasta_resultados}/{tecnica}/{n}/{nlote}/'
            os.makedirs(os.path.dirname(caminho_resultados),
                        exist_ok=True)  # Criar diretório para salvar numa primeira execuç

            for i in range(1, n_sensores + 1):
                sensor_name = f'{pasta_incorretos}/{nlote}/{n}-{tipo_sensor}{i}.csv'

                sensor_data = pd.read_csv(sensor_name)

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

                # Caminho para salvar os resultados-series normais do algoritmo para as leituras
                caminho_nome_arquivo = f'{caminho_resultados}/{grupo_execucao}-{tipo_sensor}-{i}.csv'

                salvar_predicoes_avaliacoes(sensor_data, iso_preds, caminho_nome_arquivo)
                salvar_predicoes_avaliacoes(sensor_data, iso_preds, caminho_nome_arquivo)  # Computa e armazena predições para as leituras do sensor atual
                computa_Fmeasure(caminho_nome_arquivo, pasta_resumo, grupo_execucao, i, tempoprocessamento_atual)                                  # Comp





