
import pandas as pd
import os
from sklearn.svm import OneClassSVM
import time
from src.CalculadoraDeMetricas import computa_metricas
from src.CalculadoraDeMetricas import computa_media_metricas


def salvar_em_arquivo(sensor_data, data, svm_preds, caminho_arquivo):

    # Avaliando
    labels = sensor_data.iloc[:, 1].values
    comparacao = []

    for true, pred in zip(labels, svm_preds):
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
        'Predição': ['P-correto' if pred == 1 else 'P-incorreto' for pred in svm_preds],
        'Avaliação': comparacao
    })

    # Salvando o DataFrame como CSV
    df.to_csv(caminho_arquivo, index=False)
    #print(f"resultados salvos em {caminho_arquivo}")


def startsvms(n_sensores, tecnica):

    tiposensor = 'temperatura'
    tipo_erro = ['LossAccuracy', 'Drift', 'Noise', 'Bias', 'Freezing']
    lotes = ['L1', 'L2']

    for nlote in lotes:
        for n in tipo_erro:

            grupo_execucao = f'{tecnica}-{n}-{nlote}'
            caminho_arquivo = f'resultados/{tecnica}/{n}/{nlote}/{grupo_execucao}/'
            os.makedirs(os.path.dirname(caminho_arquivo),
                        exist_ok=True)  # Criar diretório para salvar numa primeira execução


            for i in range(1, n_sensores + 1):

                sensor_name = f'/home/kathiani/midval/dados/{tiposensor}/{nlote}/{n}-{tiposensor}{i}.csv'

                sensor_data = pd.read_csv(sensor_name)

                data = sensor_data.iloc[:, 0].values

                # Reshape dos L1-10pt para ajuste do modelo
                data = data.reshape(-1, 1)

                start_time = time.time()
                # Ajustar o modelo One-Class Svm
                svm = OneClassSVM(gamma=0.1, nu=0.1)
                svm.fit(data)

                # Fazer previsões
                svm_preds = svm.predict(data)

                end_time = time.time()
                tempoprocessamento_atual = end_time - start_time

                caminho_nome_arquivo = f'{caminho_arquivo}/{grupo_execucao}-{tiposensor}-{i}.csv'

                salvar_em_arquivo(sensor_data, data, svm_preds, caminho_nome_arquivo)
                computa_metricas(caminho_nome_arquivo)  # Computa e armazena F1-Score para o sensor atual
                computa_media_metricas(caminho_nome_arquivo, grupo_execucao, tempoprocessamento_atual, i)



