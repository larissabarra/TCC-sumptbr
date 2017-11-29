from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question, Vote
from .functions import sumarios

import uuid


class IndexView(generic.ListView):
    template_name = 'pagina/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

def teoria(request):
    if 'usuario' not in request.session:
        request.session['usuario'] = str(uuid.uuid4())
    return render(request, 'pagina/teoria.html')

def obrigada(request):
    return render(request, 'pagina/obrigada.html')

def proposta(request):
    if 'usuario' not in request.session:
        request.session['usuario'] = str(uuid.uuid4())
    return render(request, 'pagina/proposta.html')

def algoritmo(request):
    if 'usuario' not in request.session:
        request.session['usuario'] = str(uuid.uuid4())
    return render(request, 'pagina/algoritmo.html')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'pagina/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'pagina/results.html'


def teste(request):
    if 'usuario' not in request.session:
        request.session['usuario'] = str(uuid.uuid4())

    questao = Question.objects.get(pk=4)
    if request.POST.get('texto') and request.POST.get('genero'):
        genero = request.POST.get('genero')
        qual = ''
        if genero == '15':
            qual = request.POST.get('outro-genero')
            if qual == '':
                return render(request, 'pagina/teste.html', {
                    'questao': questao,
                    'error_message': "Opa! Faltou preencher tudo!",
                })
        choice = Choice.objects.get(pk=genero)
        voto = Vote(choice_id=choice, user=request.session['usuario'], vote_text=qual)
        voto.save()

        texto = request.POST.get('texto')
        resultados = sumarios(texto)
        return render(request, 'pagina/results.html', {
            'resultados': resultados,
            'questao': questao
        })
    else:
        return render(request, 'pagina/teste.html', {
            'questao': questao,
            'error_message': "Opa! Faltou preencher tudo!",
        })

def avalie(request):

    if 'usuario' not in request.session:
        request.session['usuario'] = str(uuid.uuid4())

    artigo = Question.objects.get(pk=1)
    noticia = Question.objects.get(pk=2)
    outro = Question.objects.get(pk=3)
    return render(request, 'pagina/avalie.html', {
        'artigo': artigo,
        'noticia': noticia,
        'outro': outro
    })

def voteTeste(request, question_id):
    questao = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = questao.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'pagina/results.html', {
            'questao': questao,
            'error_message': "Opa! Faltou selecionar um resumo!",
        })
    else:
        choice = Choice.objects.get(pk=selected_choice.id)
        voto = Vote(choice_id=choice, user=request.session['usuario'], vote_text=request.POST.get('comentario'))
        voto.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('tcc:obrigada'))

def voteAvalie(request, question_id):
    questao = get_object_or_404(Question, pk=question_id)
    try:
        comentario = ''
        if question_id == '1':
            choice = Choice.objects.get(pk=request.POST.get('artigo'))
            comentario = request.POST.get('comentario-artigo')
        elif question_id == '2':
            choice = Choice.objects.get(pk=request.POST.get('noticia'))
            comentario = request.POST.get('comentario-noticia')
        elif question_id == '3':
            comentario = request.POST.get('comentario-outro')
            choice = Choice.objects.get(pk=request.POST.get('outro'))
        else:
            choice = questao.choice_set.get(pk=request.POST['erro'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        '''key = 'error_message' + question_id
        return render(request, 'pagina/avalie.html', {
            'questao': questao,
            key: "Opa! Faltou selecionar um resumo!",
        })'''
        return HttpResponseRedirect(reverse('tcc:avalie'))
    else:
        voto = Vote(choice_id=choice, user=request.session['usuario'], vote_text=comentario)
        voto.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('tcc:obrigada'))