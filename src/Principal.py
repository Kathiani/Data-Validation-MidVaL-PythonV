
from src.Correlacao import startrankeamento
from src.MediaMovel import startmediamovel
from src.IsolationForestSequencia import startisolationforest, startisolationforest
import os
from src.SvmOneClassSequencia import startsvms

if __name__ == "__main__":

    nsensores = 1
    nomesensor = 'carros'

    #startisolationforest(nsensores, nomesensor, 'Isolation')   #isolationforest
    startsvms(nsensores, nomesensor, 'SVM')




