
import pandas as pd
import time, os
from sklearn.ensemble import IsolationForest
from src.CalculadoraDeMetricas import computa_Fmeasure
from sklearn.metrics import f1_score


def salvar_predicoes_avaliacoes(sensor_data, forecasts, caminho_arquivo):

    # Avaliando verdadeiros positivos
    labels = sensor_data.iloc[:, 1].values
    comparacao = []


    for true, pred in zip(labels, forecasts): #Ponto de vista de detecção de erros
        if true == 'correto' and pred == -1:
            comparacao.append('FN')
        elif true == 'incorreto' and pred == 1:
            comparacao.append('FP')
        elif true == 'correto' and pred == 1:
            comparacao.append('VN')
        elif true == 'incorreto' and pred == -1:
            comparacao.append('VP')
        else:
            comparacao.append('Análise incorreta!')



    # Criar DataFrame para salvar os valores e previsões
    df = pd.DataFrame({
        'Dado': sensor_data.iloc[:, 0].values,
        'Label': sensor_data.iloc[:, 1].values,
        'Predição': [f'P-correto' if pred == 1 else f'P-incorreto' for pred in forecasts],
        'Avaliação': comparacao
    })

    df.to_csv(caminho_arquivo, index=False)



def startisolationforest(n_sensores, tecnica, pasta_incorretos, pasta_resultados, pasta_resumo, tipo_sensor):


    tipo_erro = ['LossAccuracy', 'Noise', 'Bias', 'Freezing']
    #tipo_erro = ['Noise', 'Bias']
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
                    'max_features': 1,
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


                salvar_predicoes_avaliacoes(sensor_data, iso_preds, caminho_nome_arquivo)  # Computa e armazena predições para as leituras do sensor atual
                #computa_Fmeasure(caminho_nome_arquivo, pasta_resumo, grupo_execucao, i, tempoprocessamento_atual)                                  # Comp
                computa_Fmeasure(caminho_nome_arquivo, pasta_resumo, grupo_execucao, i, tempoprocessamento_atual)


def startisolationforest2(n_sensores, tecnica, pasta_incorretos, pasta_resultados, pasta_resumo, tipo_sensor):
# Configuração de parâmetros para teste

    tipo_erro = ['LossAccuracy', 'Noise', 'Bias', 'Freezing']
    #tipo_erro = ['Noise', 'Bias']
    lotes = ['L1', 'L2']

    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_samples': ['auto', 0.8],
        'contamination': [0.1, 0.2],
        'max_features': [1, 0.5],
        'random_state': [42]
    }

    # Função para gerar combinações de parâmetros
    from itertools import product
    param_combinations = list(product(
        param_grid['n_estimators'],
        param_grid['max_samples'],
        param_grid['contamination'],
        param_grid['max_features'],
        param_grid['random_state']
    ))
    # Loop pelos lotes e tipos de erro
    for nlote in lotes:
        for n in tipo_erro:
            grupo_execucao = f'{tecnica}-{n}-{nlote}'
            caminho_resultados = f'{pasta_resultados}/{tecnica}/{n}/{nlote}/'
            os.makedirs(os.path.dirname(caminho_resultados), exist_ok=True)

            for i in range(1, n_sensores + 1):
                sensor_name = f'{pasta_incorretos}/{nlote}/{n}-{tipo_sensor}{i}.csv'
                sensor_data = pd.read_csv(sensor_name)

                # Supondo que a coluna de interesse seja a primeira coluna
                data = sensor_data.iloc[:, 0].values
                data = data.reshape(-1, 1)

                for params in param_combinations:
                    # Desempacotar os parâmetros
                    n_estimators, max_samples, contamination, max_features, random_state = params

                    # Criar o modelo com os parâmetros atuais
                    iso_forest = IsolationForest(
                        n_estimators=n_estimators,
                        max_samples=max_samples,
                        contamination=contamination,
                        max_features=max_features,
                        random_state=random_state
                    )

                    start_time = time.time()
                    iso_forest.fit(data)
                    iso_preds = iso_forest.predict(data)  # -1: Anomaly, 1: Normal
                    end_time = time.time()
                    tempoprocessamento_atual = end_time - start_time

                    # Calcular o F1-Score
                    true_labels = sensor_data['label'].values  # Supondo uma coluna de rótulos
                    iso_preds_binary = [1 if p == -1 else 0 for p in iso_preds]  # Convertendo para binário
                    f1 = f1_score(true_labels, iso_preds_binary)

                    # Caminho para salvar resultados
                    param_str = f"ne{n_estimators}_ms{max_samples}_ct{contamination}_mf{max_features}"
                    caminho_nome_arquivo = f'{caminho_resultados}/{grupo_execucao}-{tipo_sensor}-{i}-{param_str}.csv'

                    # Salvar predições e avaliações
                    salvar_predicoes_avaliacoes(sensor_data, iso_preds, caminho_nome_arquivo)
                    computa_Fmeasure(caminho_nome_arquivo, pasta_resumo, grupo_execucao, i, tempoprocessamento_atual)

                    # Salvar F1-Score
                    with open(f"{caminho_resultados}/f1_scores.csv", 'a') as f:
                        f.write(f"{grupo_execucao},{tipo_sensor},{i},{param_str},{f1:.4f},{tempoprocessamento_atual:.4f}\n")


