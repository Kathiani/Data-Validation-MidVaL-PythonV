
from src.Correlacao import startrankeamento
from src.IsolationForest import startisolationforest, salvar_infos_em_arquivo
from src.MediaMovel import startmediamovel
import time
import os

from src.SvmOneClass import startsvm

if __name__ == "__main__":
    startrankeamento()   #correlação
    startisolationforest()   #isolationforest
    startsvm()





