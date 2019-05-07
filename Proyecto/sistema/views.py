from django.shortcuts import render, redirect, reverse
from .models import Instancia, Evaluador, Evaluacion, Rubrica
import re

# expresion regular para verificar email
email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

#   INDICES

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
        'lista_evaluadores': Evaluador.objects.filter(id__gt=2)
    }
    return render(request, 'sistema/admin/pag_evaluadores.html', context)

def index_rubricas(request):
    context = {
        'lista_rubricas': Rubrica.objects.all()
    }
    return render(request, 'sistema/admin/pag_rubricas.html', context)

#   EVALUACION

def evaluacion(request, eval_id):
    if True:
        return
    return

def postevaluacion(request, eval_id):
    return

#   RUBRICA

def rubrica(request, rubrica_id):
    return

def rubrica_editar(request, rubrica_id):
    return

#   GESTIONAR EVALUADOR

def agregar_evaluador(request):
    ev = Evaluador.objects.create(nombre = request.POST['nombre'],
                                  correo = request.POST['correo'],
                                  password = "1111", es_admin = False)
    ev.save()

    # enviar correo

    return redirect(reverse("sistema:index_evaluadores"))

def modificar_evaluador():
    return

def eliminar_evaluador(request):
    id = int(request.POST['id'])
    Evaluador.objects.get(pk=id).delete()
    return redirect(reverse("sistema:index_evaluadores"))

#   GESTIONAR EVALUACION

def agregar_evaluacion():
    return

def modificar_evaluacion():
    return
    
def eliminar_evaluacion():
    return

#   GESTIONAR RUBRICA

def agregar_rubrica():
    return

def modificar_rubrica():
    return
    
def eliminar_rubrica():
    return
