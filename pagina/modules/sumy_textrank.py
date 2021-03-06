#coding=utf-8
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "portuguese"
SENTENCES_COUNT = 4

#text = 'Desde sua popularização, a Web se consolidou como um enorme repositório de dados, abrigando conteúdo, científico ou não, das mais diversas áreas. Olhando apenas para o nicho científico, Björk, Roos e Lauri (2008) estimaram que 1,35 milhão de artigos foram publicados no ano de 2006, e a quantidade de publicações nas áreas de ciência e tecnologia cresce, em média, 2,5% ao ano (National Science Board, 2010). Devido a essa grande quantidade de informações disponíveis, encontrar a informação desejada deixou de ser uma tarefa simples (CARBONELL; GOLDSTEIN, 1998). Neste contexto, nasceu a área da Recuperação de Informação (Information Retrieval, IR), que lida com armazenamento, organização, representação e acesso à informação, com o objetivo principal de responder a consultas do usuário com conteúdo relevante (BAEZA-YATES;RIBEIRO-NETO et al., 1999). Porém, mesmo com os avanços da IR, ainda é preciso filtrar os muitos resultados retornados quando se tenta encontrar algum conteúdo, e um importante auxílio ao acesso desse conteúdo desejado é a sumarização (MIRANDA-JIMÉNEZ; GELBUKH; SIDOROV, 2013). Sumarização automática é uma área do Processamento de Linguagem Natural (Natural Language Processing, NLP) dedicada ao estudo de técnicas para construir sumários de um documento ou conjunto de documentos automaticamente (LIDDY, 2001). Estes documentos podem conter dados em diversos formatos (texto, som, imagem, vídeo, etc). Os sumários ajudam a selecionar a informação desejada porque proveem o acesso rápido e acurado aos trechos mais relevantes de um documento (SQUIRE, 2016; LUHN, 1958). Por exemplo, numa filmagem feita por uma câmera de segurança de uma loja durante a noite, provavelmente a maior parte do vídeo mostrará apenas os produtos, embora o que interessa é qualquer movimento. Um algoritmo de sumarização poderia selecionar apenas as partes interessantes do vídeo, sem a necessidade de alguém assisti-lo inteiro. Já no caso de textos, foco deste trabalho, um sumário contem os principais tópicos abordados.'


def sumarizar(texto):
    parser = PlaintextParser.from_string(texto, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizerTR = TextRankSummarizer(stemmer)
    summarizerTR.stop_words = get_stop_words(LANGUAGE)

    return ' '.join(str(x) for x in summarizerTR(parser.document, SENTENCES_COUNT))


'''
resultado para inglês:
com 4 frases:

Olhando apenas para o nicho científico, Björk, Roos e Lauri (2008) estimaram que 1,35 milhão de artigos foram publicados no ano de 2006, e a quantidade de publicações nas áreas de ciência e tecnologia cresce, em média, 2,5% ao ano (National Science Board, 2010).
Sumarização automática é uma área do Processamento de Linguagem Natural (Natural Language Processing, NLP) dedicada ao estudo de técnicas para construir sumários de um documento ou conjunto de documentos automaticamente (LIDDY, 2001).
Por exemplo, numa filmagem feita por uma câmera de segurança de uma loja durante a noite, provavelmente a maior parte do vídeo mostrará apenas os produtos, embora o que interessa é qualquer movimento.
Um algoritmo de sumarização poderia selecionar apenas as partes interessantes do vídeo, sem a necessidade de alguém assisti-lo inteiro.


com 2 frases:

Olhando apenas para o nicho científico, Björk, Roos e Lauri (2008) estimaram que 1,35 milhão de artigos foram publicados no ano de 2006, e a quantidade de publicações nas áreas de ciência e tecnologia cresce, em média, 2,5% ao ano (National Science Board, 2010).
Sumarização automática é uma área do Processamento de Linguagem Natural (Natural Language Processing, NLP) dedicada ao estudo de técnicas para construir sumários de um documento ou conjunto de documentos automaticamente (LIDDY, 2001).
'''

'''
resultado para ptbr:
com 4 frases:

Neste contexto, nasceu a área da Recuperação de Informação (Information Retrieval, IR), que lida com armazenamento, organização, representação e acesso à informação, com o objetivo principal de responder a consultas do usuário com conteúdo relevante (BAEZA-YATES;RIBEIRO-NETO et al., 1999).
Porém, mesmo com os avanços da IR, ainda é preciso filtrar os muitos resultados retornados quando se tenta encontrar algum conteúdo, e um importante auxílio ao acesso desse conteúdo desejado é a sumarização (MIRANDA-JIMÉNEZ; GELBUKH; SIDOROV, 2013).
Sumarização automática é uma área do Processamento de Linguagem Natural (Natural Language Processing, NLP) dedicada ao estudo de técnicas para construir sumários de um documento ou conjunto de documentos automaticamente (LIDDY, 2001).
Os sumários ajudam a selecionar a informação desejada porque proveem o acesso rápido e acurado aos trechos mais relevantes de um documento (SQUIRE, 2016; LUHN, 1958).


com 2 frases:

Neste contexto, nasceu a área da Recuperação de Informação (Information Retrieval, IR), que lida com armazenamento, organização, representação e acesso à informação, com o objetivo principal de responder a consultas do usuário com conteúdo relevante (BAEZA-YATES;RIBEIRO-NETO et al., 1999).
Os sumários ajudam a selecionar a informação desejada porque proveem o acesso rápido e acurado aos trechos mais relevantes de um documento (SQUIRE, 2016; LUHN, 1958).
'''