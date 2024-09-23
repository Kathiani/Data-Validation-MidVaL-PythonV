
import pandas as pd
from sklearn.svm import OneClassSVM
import time
from src.CalculadoraDeMetricas import startmetricas
from src.CalculadoraDeMetricas import comparemetricas


def salvar_infos_em_arquivo(sensor_data, data, svm_preds, caminho_arquivo):

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


def startsvms(n_sensores, nomesensor, tecnica):

    for i in range(1, n_sensores + 1):

        start_time = time.time()

        sensor_name = f'dados/{nomesensor}{i}.csv'

        # Carregar dados do arquivo CSV
        sensor_data = pd.read_csv(sensor_name)

        # Supondo que a coluna de interesse seja a primeira coluna
        data = sensor_data.iloc[:, 0].values
        #print(sensor_data)

        # Reshape dos dados para ajuste do modelo
        data = data.reshape(-1, 1)

        # Ajustar o modelo One-Class svm
        svm = OneClassSVM(gamma=0.1, nu=0.1)
        svm.fit(data)

        # Fazer previsões
        svm_preds = svm.predict(data)


        end_time = time.time()
        execution_time = end_time - start_time

        nomearquivo = f'ResultadosSVM-{nomesensor}{i}.csv'
        caminho_arquivo = f'resultados/{tecnica}/{nomearquivo}'


        salvar_infos_em_arquivo(sensor_data, data, svm_preds, caminho_arquivo)
        startmetricas(caminho_arquivo, tecnica)

    comparemetricas(caminho_arquivo, tecnica)


