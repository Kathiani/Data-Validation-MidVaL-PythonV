
from src.ValidadorPorIsolationForest import startisolationforest
from src.ValidadorPorIsolationForest import startisolationforest2
from src.ValidadorPorSvmOneClass import startsvms2
from src.ValidadorPorSvmOneClass import startsvms
from src.ValidadorPorCorrelacao import startcalculocorrelacaot
from src.CalculadoraDeMetricas import computa_media_geral_metricas
from src.CalculadoraDeMetricas import computa_Fmeasure
from src.CalculadoraDeMetricas import computa_media_Fmeasure
import os



if __name__ == "__main__":

    pasta_dadoscorretos = '/home/kathiani/midval/dados/temperatura/corretos'
    pasta_dadosincorretos = '/home/kathiani/midval/dados/temperatura/incorretos'
    pasta_resultados = '/home/kathiani/PycharmProjects/Algoritmos_Validacao_AjusteMatrizConfusao/src/resultados-ajustes'
    pasta_resumo = '/home/kathiani/PycharmProjects/Algoritmos_Validacao_AjusteMatrizConfusao/src/resultados-ajustes/resumo'
    if not os.path.exists(pasta_resultados):
        os.makedirs(pasta_resultados)

    if not os.path.exists(pasta_resumo):
        os.makedirs(pasta_resumo)

    tipo_sensor = 'temperatura'
    n_sensores = 30


    startisolationforest(n_sensores,'isolation', pasta_dadosincorretos, pasta_resultados, pasta_resumo, tipo_sensor) #fixos os números dos lotes
    startsvms(n_sensores,'svm', pasta_dadosincorretos, pasta_resultados, pasta_resumo, tipo_sensor)
    startcalculocorrelacaot(n_sensores, 'diversidade', pasta_dadoscorretos, pasta_dadosincorretos, pasta_resultados, pasta_resumo, tipo_sensor)
    computa_media_geral_metricas(pasta_resultados, pasta_resumo)






