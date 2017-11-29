from django.conf.urls import url

from . import views

app_name = 'tcc'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^teoria/$', views.teoria, name='teoria'),
    url(r'^proposta/$', views.proposta, name='proposta'),
    url(r'^algoritmo/$', views.algoritmo, name='algoritmo'),
    url(r'^teste/$', views.teste, name='teste'),
    url(r'^avalie/$', views.avalie, name='avalie'),
    url(r'^obrigada/$', views.obrigada, name='obrigada'),
    url(r'^(?P<question_id>[0-9]+)/voteTeste/$', views.voteTeste, name='voteTeste'),
    url(r'^(?P<question_id>[0-9]+)/voteAvalie/$', views.voteAvalie, name='voteAvalie'),
]