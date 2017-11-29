from .modules.sumptbr.sumptbr import sumarizar
from .modules.sumy_textrank import sumarizar as sumyTR
from .modules.sumy_lsa import sumarizar as sumyLSA

def sumarios(texto):
    meu = sumarizar(texto)
    sumytr = sumyTR(texto)
    sumylsa = sumyLSA(texto)

    resultados = {'10' : meu, '11' : sumytr, '12' : sumylsa}
    return resultados
