
import pandas as pd
import os
from sklearn.svm import OneClassSVM
import time
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score, make_scorer
from sklearn.model_selection import GridSearchCV

from src.CalculadoraDeMetricas import computa_Fmeasure, computa_media_Fmeasure


def salvar_predicoes_avaliacoes(sensor_data, svm_preds, caminho_arquivo):

    # Avaliando
    labels = sensor_data.iloc[:, 1].values
    comparacao = []

    for true, pred in zip(labels, svm_preds):  # Ponto de vista de detecção de erros
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
        'Predição': ['P-correto' if pred == 1 else 'P-incorreto' for pred in svm_preds],
        'Avaliação': comparacao
    })

    # Salvando o DataFrame como CSV
    df.to_csv(caminho_arquivo, index=False)
    #print(f"resultados-series normais salvos em {caminho_arquivo}")


def startsvms(n_sensores, tecnica,  pasta_dadosincorretos, pasta_resultados, pasta_resumo, tipo_sensor):

    tiposensor = 'temperatura'
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
                sensor_name = f'{pasta_dadosincorretos}/{nlote}/{n}-{tipo_sensor}{i}.csv'

                sensor_data = pd.read_csv(sensor_name)

                data = sensor_data.iloc[:, 0].values

                # Reshape dos L1-10pt para ajuste do modelo
                data = data.reshape(-1, 1)

                start_time = time.time()
                # Ajustar o modelo One-Class Svm


                svm = OneClassSVM(gamma=0.1, nu=0.1)
                svm.fit(data)
                svm_preds = svm.predict(data)


                end_time = time.time()
                tempoprocessamento_atual = end_time - start_time

                caminho_nome_arquivo = f'{caminho_resultados}/{nlote}{grupo_execucao}-{tiposensor}-{i}.csv'

                salvar_predicoes_avaliacoes(sensor_data, svm_preds, caminho_nome_arquivo)  # Computa e armazena predições para as leituras do sensor atual
                computa_Fmeasure(caminho_nome_arquivo, pasta_resumo, grupo_execucao, i, tempoprocessamento_atual)  # Comp






def ajustar_svm_com_grid_search(data, labels):
    # Parâmetros do Grid Search
    param_grid = {
        'gamma': [0.01, 0.1, 0.5, 1],
        'nu': [0.1, 0.2, 0.3, 0.5]
    }

    # Definir o modelo base
    base_model = OneClassSVM()

    # Scorer baseado no F1-Score
    def custom_f1(y_true, y_pred):
        y_true_binary = [1 if y == 'incorreto' else -1 for y in y_true]
        return f1_score(y_true_binary, y_pred, pos_label=-1)

    scorer = make_scorer(custom_f1)

    # Configurar Grid Search
    grid_search = GridSearchCV(
        estimator=base_model,
        param_grid=param_grid,
        scoring=scorer,
        cv=3,
        verbose=1
    )

    # Ajustar o modelo com o Grid Search
    grid_search.fit(data, labels)

    # Retornar o melhor modelo
    return grid_search.best_estimator_, grid_search.best_params_


def startsvms2(n_sensores, tecnica, pasta_dadosincorretos, pasta_resultados, pasta_resumo, tipo_sensor):
    tiposensor = 'temperatura'
    tipo_erro = ['LossAccuracy', 'Noise', 'Bias', 'Freezing']
    lotes = ['L1', 'L2']

    for nlote in lotes:
        for n in tipo_erro:
            grupo_execucao = f'{tecnica}-{n}-{nlote}'
            caminho_resultados = f'{pasta_resultados}/{tecnica}/{n}/{nlote}/'
            os.makedirs(os.path.dirname(caminho_resultados), exist_ok=True)

            for i in range(1, n_sensores + 1):
                sensor_name = f'{pasta_dadosincorretos}/{nlote}/{n}-{tipo_sensor}{i}.csv'

                sensor_data = pd.read_csv(sensor_name)
                data = sensor_data.iloc[:, 0].values.reshape(-1, 1)
                labels = sensor_data.iloc[:, 1].values

                # Grid Search para encontrar os melhores parâmetros
                start_time = time.time()
                best_svm, best_params = ajustar_svm_com_grid_search(data, labels)
                print(f"Melhores parâmetros para o sensor {i}: {best_params}")

                # Fazer previsões usando o melhor modelo encontrado
                svm_preds = best_svm.predict(data)
                end_time = time.time()
                tempoprocessamento_atual = end_time - start_time

                caminho_nome_arquivo = f'{caminho_resultados}/{nlote}{grupo_execucao}-{tiposensor}-{i}.csv'
                salvar_predicoes_avaliacoes(sensor_data, svm_preds, caminho_nome_arquivo)

                # Calcular métricas e salvar
                computa_Fmeasure(caminho_nome_arquivo, pasta_resumo, grupo_execucao, i, tempoprocessamento_atual)
