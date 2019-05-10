from django.shortcuts import render, redirect, reverse

from .models import Instancia, Evaluador, Evaluacion, Rubrica, Grupo, EvaluacionRubrica, Evalua, InstanciaGrupo
from .forms import EvaluadorForm, EvaluacionForm

#   INDICES
def index_landing(request):
    return render(request,'sistema/landing.html')

def index_login(request):
    return render(request,'sistema/login.html')


def index_cursos(request):
    context = {
        'lista_cursos': Instancia.objects.all()
    }
    return render(request, 'sistema/admin/pag_cursos.html', context)

# error = True  fechas incorrectas (ver Evaluacion.validar_fechas)
def index_evaluaciones(request, error = False):
    context = {
        'lista_rubricas': Rubrica.objects.all(),
        'lista_evaluaciones': Evaluacion.objects.all(),
        'lista_cursos': Instancia.objects.all()
    }
    if error:
        context['mensaje'] = "Las fechas ingresadas son incorrectas"
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
        #Filtra los valores mayores a gt
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
	#grupos del curso de la evaluacion
    ev = Evaluacion.objects.get(pk=eval_id)
    grupos = InstanciaGrupo.objects.filter(instancia=ev.instancia)
    #a=[]
    #for g in range(len(grupos)):
        #a[i]=Alumno.objects.filter(grupo_id=i.g)
    context = {
		'evaluacion': ev,
        'lista_grupos': grupos
    }
    return render(request, 'sistema/evaluacion/gruposevaluacion.html',context)


def evaluacion_grupo(request, eval_id=0,grupo_id=0):
    #evalu = Evaluacion.objects.get(id=eval_id)
    # diferencia=eva.fecha_fin-eva.fecha_inicio
    #Si esta en curso la evaluación
    #context = {
     #   'evaluacion': evalu
    #}
    if True:#if diferencia<0:
        return render(request,'sistema/evaluacion/evaluacionadmin.html')#,context)
    #Si ya termino
    return render(request, 'sistema/evaluacion/posteval.html')#,context)

def postevaluacion(request, eval_id=0):
    return render(request, 'sistema/evaluacion/posteval.html')


#   RUBRICA

# Ver rubrica
def rubrica(request, rubrica_id):
    context = {
        'rubrica': Rubrica.objects.get(pk=rubrica_id)
    }
    return render(request, 'sistema/rubricas/rubrica.html', context)

# Editar rubrica
def rubrica_editar(request, rubrica_id):
    context = {
        'rubrica': Rubrica.objects.get(pk=rubrica_id)
    }
    return render(request, 'sistema/rubricas/rubrica_admin.html', context)


#   GESTIONAR EVALUADOR
def agregar_evaluador(request):
    # Si se carga la pagina normalmente
    if request.method != "POST":
        return redirect(reverse('sistema:index_evaluadores'))
    # Validar el formato del correo
    form = EvaluadorForm(request.POST)
    if form.is_valid():
        # Si no hay evaluador con el mismo correo
        if Evaluador.objects.filter(correo__iexact=form.cleaned_data['correo']).count() == 0:
            # password y es_admin reciben valores por defecto
            ev = Evaluador.objects.create(nombre = form.cleaned_data['nombre'],
                                          correo = form.cleaned_data['correo'],
                                          password = "1111", es_admin = False)
            ev.save()


            # TODO: enviar correo
            
            
            return redirect(reverse('sistema:index_evaluadores'))
        return index_evaluadores(request, error = 1, nombre = request.POST['nombre'])
    return index_evaluadores(request, error = 2, nombre = request.POST['nombre'])

def modificar_evaluador(request):
    # Si se carga la pagina normalmente
    if request.method != "POST":
        return redirect(reverse('sistema:index_evaluadores'))
    # Validar el formato del correo
    form = EvaluadorForm(request.POST)
    if form.is_valid():
        # Si otro evaluador ya tiene el correo
        if Evaluador.objects.exclude(pk=request.POST['id']).filter(correo__iexact=form.cleaned_data['correo']).count() > 0:
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
    # Si se carga la pagina normalmente
    if request.method != "POST":
        return redirect(reverse('sistema:index_evaluaciones'))
    form = EvaluacionForm(request.POST)
    # Validar el formato de las fechas
    if form.is_valid():
        # Tiempo recibe valor por defecto
        ev = Evaluacion.objects.create(instancia=Instancia.objects.get(pk=request.POST['curso']),
									   nombre=request.POST['nombre'],
                                       fecha_inicio=form.cleaned_data['inicio'],
                                       fecha_fin=form.cleaned_data['fin'],
                                       tiempo_min=form.cleaned_data['minimo'],
                                       tiempo_max=form.cleaned_data['maximo'])
        # Si las fechas estan correctas
        if ev.validar_fechas():
            ev.save()
            # Crear relacion entre rubrica y evaluacion
            EvaluacionRubrica.objects.create(evaluacion=ev,
                                             rubrica=Rubrica.objects.get(pk=request.POST['rubrica'])).save()
            # Admin como evaluador por defecto (Cambiar a usuario que realiza la accion?)
            Evalua.objects.create(evaluacion=ev, evaluador=Evaluador.objects.get(pk=2)).save()
            return redirect("sistema:evaluacion", ev.id)
    return index_evaluaciones(request, error = True)
    

def modificar_evaluacion(request):
    return #redirect("sistema:evaluacion", ev.id)
    
def eliminar_evaluacion(request):
    id = int(request.POST['id'])
    Evaluacion.objects.get(pk=id).delete()
    return redirect(reverse("sistema:index_evaluaciones"))


#   GESTIONAR RUBRICA

def agregar_rubrica(request):
    # Crea objeto
    r = Rubrica.objects.create(nombre = request.POST['nombre'], archivo = "")
    # Crea archivo
    d = r.crear()
    r.save()
    # Asocia objeto a archivo
    r.archivo = d
    r.save()
    return redirect("sistema:rubrica_editar", r.id)

def modificar_rubrica(request, rubrica_id):
    i = 0 # Cuenta columnas
    while "celda:0,{}".format(i) in request.POST:
        cols = i
        i+=1
    i = 0 # Cuenta filas
    while "celda:{},0".format(i) in request.POST:
        fils = i
        i+=1
    cols += 1
    fils += 1
    # Crea tabla de rubrica
    tabla = [[request.POST['celda:{},{}'.format(i,j)] for j in range(cols)] for i in range(fils)]
    r = Rubrica.objects.get(pk=rubrica_id)
    r.modificar(tabla) # Guarda la tabla
    r.nombre = request.POST['nombre']
    r.save()
    return redirect("sistema:rubrica", rubrica_id)
    
def eliminar_rubrica(request):
    r = Rubrica.objects.get(pk=request.POST['id'])
    r.borrar() # Elimina archivo
    r.delete() # Elimina objeto
    return redirect(reverse("sistema:index_rubricas"))
