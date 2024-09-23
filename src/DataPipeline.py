from src.ValidadorPorIsolationForest import startisolationforest
from src.ValidadorPorSvmOneClass import startsvms
from src.ValidadorPorCorrelacao import startcalculocorrelacao

if __name__ == "__main__":

    nsensores = 10
    nomesensor = 'carros'

    startisolationforest(nsensores, nomesensor, 'isolation')   #isolationforest
    startsvms(nsensores, nomesensor, 'svm')
    startcalculocorrelacao(nsensores, nomesensor, 'diversidade')




