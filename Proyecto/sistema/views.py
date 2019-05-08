from django.shortcuts import render, redirect, reverse

from .models import Instancia, Evaluador, Evaluacion, Rubrica
from .forms import EvaluadorForm


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
        #id 1 es evaluadores eliminados
        #id 2 es el admin
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
    context = {
        'rubrica': Rubrica.objects.get(pk=rubrica_id)
    }
    return render(request, 'sistema/rubricas/rubrica.html', context)

def rubrica_editar(request, rubrica_id):
    context = {
        'rubrica': Rubrica.objects.get(pk=rubrica_id)
    }
    return render(request, 'sistema/rubricas/rubrica_admin.html', context)


#   GESTIONAR EVALUADOR

def agregar_evaluador(request):
    if request.method != "POST":
        return redirect(reverse('sistema:index_evaluadores'))
    form = EvaluadorForm(request.POST)
    if form.is_valid():
        # No hay evaluador con el mismo correo
        if Evaluador.objects.filter(correo__iexact=form.cleaned_data['correo']).count() == 0:
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
        if Evaluador.objects.exclude(pk=request.POST['id']).filter(correo__iexact=form.cleaned_data['correo']).count() > 0:
            # Otro evaluador ya tiene el correo
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

def agregar_evaluacion(request):
    return
    
def eliminar_evaluacion():
    return


#   GESTIONAR RUBRICA

def agregar_rubrica(request):
    r = Rubrica.objects.create(nombre = request.POST['nombre'], archivo = "")
    d = r.crear()
    r.save()
    r.archivo = d
    r.save()
    return redirect("sistema:rubrica_editar", r.id)

def modificar_rubrica(request, rubrica_id):
    i = 0
    while "celda:0,{}".format(i) in request.POST:
        cols = i
        i+=1
    i = 0
    while "celda:{},0".format(i) in request.POST:
        fils = i
        i+=1
    cols += 1
    fils += 1
    tabla = [[request.POST['celda:{},{}'.format(i,j)] for j in range(cols)] for i in range(fils)]
    r = Rubrica.objects.get(pk=rubrica_id)
    r.modificar(tabla)
    r.nombre = request.POST['nombre']
    r.save()
    return redirect("sistema:rubrica", rubrica_id)
    
def eliminar_rubrica(request):
    r = Rubrica.objects.get(pk=request.POST['id'])
    r.borrar()
    r.delete()
    return redirect(reverse("sistema:index_rubricas"))
