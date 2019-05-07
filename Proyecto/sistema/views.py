from django.shortcuts import render
from .models import Instancia, Evaluador, Evaluacion, Rubrica

def index_cursos(request):
    context = {
        'lista_cursos': Instancia.objects.all()
    }
    return render(request, 'sistema/admin/pag_cursos.html', context)

def index_evaluaciones(request):
    context = {
        'lista_evaluaciones': Evaluacion.objects.all()
    }
    return render(request, 'sistema/admin/pag_evaluaciones.html', context)

def index_evaluadores(request):
    context = {
        'lista_evaluadores': Evaluador.objects.all()
    }
    return render(request, 'sistema/admin/pag_evaluadores.html', context)

def index_rubricas(request):
    context = {
        'lista_rubricas': Rubrica.objects.all()
    }
    return render(request, 'sistema/admin/pag_rubricas.html', context)

def evaluacion(request, eval_id):
    if True:
        return
    return

def postevaluacion(request, eval_id):
    return

def rubrica(request, rubrica_id):
    return