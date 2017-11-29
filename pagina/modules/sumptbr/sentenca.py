class Sentenca:
    original = ''
    processada = ''
    fator = 1
    nota = 1
    ordem = 0
    palavras = list()

    def __init__(self):
        self.palavras = []

    def fatorMultiplicativo(self, fator):
        self.fator = self.fator * fator

    def addPalavra(self, palavra):
        self.palavras.append(palavra)

    def aplicaFator(self):
        self.nota *= self.fator

    def __repr__(self):
        return 'Frase: ' + self.original
        #return 'ord ' + str(self.ordem) + ' - fator ' + str(self.fator)