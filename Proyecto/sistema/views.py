from django.shortcuts import render, redirect, reverse
import re

from .models import Instancia, Evaluador, Evaluacion, Rubrica
from .forms import EvaluadorForm

# expresion regular para verificar email
#email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

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

# error = 1     email repetido
# error = 2     email incorrecto
def index_evaluadores(request, error = 0, nombre = None):
    if error == 1:
        mensaje = "El correo ya se encuentra registrado"
    elif error == 2:
        mensaje = "El correo ingresado no es válido"
    context = {
            'lista_evaluadores': Evaluador.objects.filter(id__gt=2)
    }
    if error:
        context['mensaje'] = mensaje
        context['nombre'] = nombre
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
    if request.method != "POST":
        return redirect(reverse('sistema:index_evaluadores'))
    form = EvaluadorForm(request.POST)
    if form.is_valid():
        # No hay evaluador con el mismo correo
        if Evaluador.objects.filter(correo__iexact=correo).count() == 0:
            ev = Evaluador.objects.create(nombre = form.cleaned_data['nombre'],
                                          correo = form.cleaned_data['correo'],
                                          password = "1111", es_admin = False)
            ev.save()
            # enviar correo
            return redirect(reverse('sistema:index_evaluadores'))
        return index_evaluadores(request, error = 1, nombre = request.POST['nombre'])
    return index_evaluadores(request, error = 2, nombre = request.POST['nombre'])

def modificar_evaluador(request):
    if request.method != "POST":
        return redirect(reverse('sistema:index_evaluadores'))
    form = EvaluadorForm(request.POST)
    if form.is_valid():
        for ev in Evaluador.objects.filter(correo__iexact=form.cleaned_data['correo']):
            # Otro evaluador ya tiene el correo
            if ev.id != request.POST['id']:
                return index_evaluadores(request, error = 1)
        ev = Evaluador.objects.get(pk=request.POST['id'])
        ev.nombre = form.cleaned_data['nombre']
        ev.correo = form.cleaned_data['correo']
        ev.save()
        return redirect(reverse('sistema:index_evaluadores'))
    return index_evaluadores(request, error = 2)

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
