# coding=utf-8

import codecs
import nltk
from ..stembr.stembr import stem
import string
from .sentenca import Sentenca
from .palavra import Palavra
import math
import re
import networkx as nx
import itertools
import random
import numpy as np
from scipy import spatial

# ---------------- leitura das stopwords -------------------
stopwords = ['a', 'à', 'agora', 'ainda', 'alguém', 'algum', 'alguma', 'algumas', 'alguns', 'ampla', 'amplas', 'amplo', 'amplos', 'ante', 'antes', 'ao', 'aos', 'após', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aquilo', 'as', 'até', 'através', 'cada', 'coisa', 'coisas', 'com', 'como', 'contra', 'contudo', 'da', 'daquele', 'daqueles', 'das', 'de', 'dela', 'delas', 'dele', 'deles', 'depois', 'dessa', 'dessas', 'desse', 'desses', 'desta', 'destas', 'deste', 'deste', 'destes', 'deve', 'devem', 'devendo', 'dever', 'deverá', 'deverão', 'deveria', 'deveriam', 'devia', 'deviam', 'disse', 'disso', 'disto', 'dito', 'diz', 'dizem', 'do', 'dos', 'e', 'é', 'ela', 'elas', 'ele', 'eles', 'em', 'enquanto', 'entre', 'era', 'essa', 'essas', 'esse', 'esses', 'esta', 'está', 'estamos', 'estão', 'estas', 'estava', 'estavam', 'estávamos', 'este', 'estes', 'estou', 'eu', 'fazendo', 'fazer', 'feita', 'feitas', 'feito', 'feitos', 'foi', 'for', 'foram', 'fosse', 'fossem', 'grande', 'grandes', 'há', 'isso', 'isto', 'já', 'lá', 'la', 'lhe', 'lhes', 'lo', 'mas', 'me', 'mesma', 'mesmas', 'mesmo', 'mesmos', 'meu', 'meus', 'minha', 'minhas', 'muita', 'muitas', 'muito', 'muitos', 'na', 'não', 'nas', 'nem', 'nenhum', 'nessa', 'nessas', 'nesta', 'nestas', 'ninguém', 'no', 'nos', 'nós', 'nossa', 'nossas', 'nosso', 'nossos', 'num', 'numa', 'nunca', 'o', 'os', 'ou', 'outra', 'outras', 'outro', 'outros', 'para', 'pela', 'pelas', 'pelo', 'pelos', 'pequena', 'pequenas', 'pequeno', 'pequenos', 'per', 'perante', 'pode', 'pôde', 'podendo', 'poder', 'poderia', 'poderiam', 'podia', 'podiam', 'pois', 'por', 'porém', 'porque', 'posso', 'pouca', 'poucas', 'pouco', 'poucos', 'primeiro', 'primeiros', 'própria', 'próprias', 'próprio', 'próprios', 'quais', 'qual', 'quando', 'quanto', 'quantos', 'que', 'quem', 'são', 'se', 'seja', 'sejam', 'sem', 'sempre', 'sendo', 'será', 'serão', 'seu', 'seus', 'si', 'sido', 'só', 'sob', 'sobre', 'sua', 'suas', 'talvez', 'também', 'tampouco', 'te', 'tem', 'tendo', 'tenha', 'ter', 'teu', 'teus', 'ti', 'tido', 'tinha', 'tinham', 'toda', 'todas', 'todavia', 'todo', 'todos', 'tu', 'tua', 'tuas', 'tudo', 'última', 'últimas', 'último', 'últimos', 'um', 'uma', 'umas', 'uns', 'vendo', 'ver', 'vez', 'vindo', 'vir', 'vos', 'vós']
#stopwords = list(filter(lambda x: x != '', [linha.rstrip('\n\r') for linha in codecs.open('./stopwords.txt', 'r')]))


# ---------------- variáveis auxiliares --------------------
sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
translator = str.maketrans('', '', string.punctuation)

# ---------------- fatores da análise sintática ------------
fatorSubstantivoProprio = 1.1

# ---------------- dados -----------------------------------
palavrasUnicas = list()
textoTratado = list()


# ---------------- separação das sentenças -----------------
def criaGrafo(paragrafos):
    grafo = nx.Graph()
    contSentenca = 0
    totalParagrafos = len(paragrafos)
    if totalParagrafos != 0:
        fatorParagrafo = 1 / totalParagrafos
    else:
        fatorParagrafo = 1

    for contParagrafo, paragrafo in enumerate(paragrafos):
        frasesComStopwords = sent_tokenizer.tokenize(paragrafo)
        totalFrases = len(frasesComStopwords)
        if totalFrases != 0:
            fatorPosicao = 1 / totalFrases
        else:
            fatorPosicao = 1

        for frase in frasesComStopwords:
            sentenca = Sentenca()
            sentenca.ordem = contSentenca
            sentenca.original = frase

            sentenca.fatorMultiplicativo(1 + fatorParagrafo)
            sentenca.fatorMultiplicativo(1 + fatorPosicao)
            fatorPosicao /= 2

            contSentenca += 1

            palavras = list(
                filter(lambda x: x.lower() not in stopwords, re.sub(r'\d+', '', frase.translate(translator)).split()))

            trataPalavras(sentenca, palavras)
            grafo.add_node(sentenca)
        fatorParagrafo /= 2
    return grafo


# ---------------- tratamento das palavras -----------------
def trataPalavras(sentenca, palavras):
    stems = list(map(lambda x: stem(x), palavras))
    textoTratado.append(stems)
    contMaiusculas = 0

    for pal, stm in zip(palavras, stems):
        existe = list(filter(lambda x: x.stem == stm, palavrasUnicas))
        if existe == []:
            termo = Palavra(pal, stm)
            termo.frequencia = 1
            palavrasUnicas.append(termo)
            sentenca.addPalavra(termo)
        else:
            existe[0].frequencia += 1
            sentenca.addPalavra(existe[0])

        if pal[0].isupper():
            contMaiusculas += 1

    sentenca.fatorMultiplicativo(math.pow(fatorSubstantivoProprio, contMaiusculas))


# ---------------- similaridade entre sentenças ------------
def similaridade(sent1, sent2):
    comuns = 0
    for palavra1 in sent1.palavras:
        for palavra2 in sent2.palavras:
            if palavra1.stem == palavra2.stem:
                comuns += 1
    if (len(sent1.palavras) > 1) and (len(sent2.palavras) > 1) and (comuns != 0):
        return comuns / (math.log10(len(sent1.palavras)) + math.log10(len(sent2.palavras)))
    return 0


# ---------------- cria arestas do grafo -------------------
def criaArestas(grafo):
    for a, b in itertools.combinations(grafo.nodes(), 2):
        peso = similaridade(a, b)
        if peso != 0:
            grafo.add_edge(a, b, weight=peso)


# ---------------- textrank --------------------------------
def textrank(grafo):
    d = 0.85
    dif = 0

    sentenca = random.choice(grafo.nodes())
    while dif > 0.01:
        recomeca = random.random()
        if recomeca <= 0.15:
            sentenca = random.choice(grafo.nodes())

        soma = 0
        vizinhos = grafo.neighbors(sentenca)
        for vizinho in vizinhos:
            soma2 = 0
            vizinhosDoVizinho = grafo.neighbors(vizinho)

            for vizinhoDoVizinho in vizinhosDoVizinho:
                soma2 += grafo.edge[vizinhoDoVizinho][vizinho]['weight']
            if soma2 == 0:
                soma2 = 1
            soma += (grafo.edge[sentenca][vizinho]['weight'] / soma2) * vizinho.nota
        resultado = (1 - d) + d * soma
        dif = sentenca.nota - resultado
        sentenca.nota = resultado

    for sent in grafo.nodes():
        sent.aplicaFator()



# ---------------- faz sumário -----------------------------
def sumarizar(texto):
    paragrafos = list(filter(lambda x: x != '', [linha.rstrip('\r\n') for linha in re.split(r'\r\n', texto)]))
    grafo = criaGrafo(paragrafos)
    criaArestas(grafo)
    textrank(grafo)
    ordenadas = sorted(grafo.nodes(), key=lambda x: x.nota, reverse=True)
    selecionadas = sorted(ordenadas[:4], key=lambda x: x.ordem)
    resultado = ' '.join(list(map(lambda x: x.original, selecionadas)))
    grafo.clear()
    palavrasUnicas.clear()
    return resultado
