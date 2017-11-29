class Palavra:
    original = list()
    stem = ''
    frequencia = 0
    relacionadas = list()

    def __init__(self, original, stem):
        self.original = []
        self.original.append(original)
        self.stem = stem
        self.relacionadas = []

    def addRelacionada(self, relacionada):
        self.relacionadas.append(relacionada)

    def __repr__(self):
        return 'Stem: ' + self.stem + ' - freq: ' + str(self.frequencia) + '\n'