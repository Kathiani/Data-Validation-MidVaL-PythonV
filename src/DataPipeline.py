from src.ValidadorPorIsolationForest import startisolationforest
from src.ValidadorPorSvmOneClass import startsvms
from src.ValidadorPorCorrelacao import startcalculocorrelacao


if __name__ == "__main__":


    n_sensores = 4

    startisolationforest(n_sensores,'isolation') #fixos os números dos lotes
    startsvms(n_sensores,'svm')
    startcalculocorrelacao(n_sensores, 'diversidade')






