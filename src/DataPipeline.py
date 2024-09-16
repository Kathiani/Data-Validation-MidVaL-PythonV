from src.ValidadorPorSvmOneClass import startsvms

if __name__ == "__main__":

    nsensores = 1
    nomesensor = 'carros'

    #startisolationforest(nsensores, nomesensor, 'isolation')   #isolationforest
    startsvms(nsensores, nomesensor, 'svm')




