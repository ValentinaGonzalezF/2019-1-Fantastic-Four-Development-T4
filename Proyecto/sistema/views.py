from django.shortcuts import render, redirect, reverse
from django.utils.crypto import random
from django.contrib.auth.decorators import login_required

from .models import Instancia, Evaluador, Evaluacion, Rubrica, Grupo, EvaluacionRubrica, Evalua, InstanciaGrupo, \
    Presentacion
from .forms import EvaluadorForm, EvaluacionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Contraseña
abc = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
def nueva_pass():
    #Genera pass aleatoria
	p = ""
	for _ in range(16):
		p += abc[random.randint(0, len(abc)-1)]
	return p


#   LOGIN
def login_validate(request):
    #Si se ha ingresado mediante login
    if request.method == "POST":
        #Verifica si el correo y la contraseña ingresada es valida
        mail=request.POST['correo']
        passw=request.POST['password']
        user = authenticate(username= mail, password=passw)
        #
        if (user) is not None:
            login(request, user)
            eval = Evaluador.objects.get(correo=mail)
            #Creo variables de sessiones para tener informacionn de la persona
            #que entro por login
            request.session['correo'] = mail
            request.session['es_admin'] = eval.es_admin
            request.session['nombre']=eval.nombre
            return redirect(reverse("sistema:index_landing_admin"))
        else:
            user_exist = User.objects.filter(username=mail).count() > 0
            if user_exist:
                mensaje = "La contraseña ingresada no es válida"
            else:
                mensaje = "El correo ingresado no existe"
            context = {
                'error': mensaje
            }
            return render(request, 'sistema/login.html', context)
    return redirect(reverse("sistema:index_login"))

def log_out(request):
    #Setea las variables de session para reconocer el usuario en None
    logout(request)
    request.session['correo'] = None
    request.session['es_admin'] = None
    request.session['nombre'] = None
    return redirect(reverse("sistema:index_login"))

#   INDICES
@login_required
def index_landing_admin(request):
    #Si es admin, muestra el landing page de admin
    if request.session.get('es_admin'):
        return render(request, 'sistema/landing.html')
    else:
        #Obtiene evaluador a traves de variables de session correo
        eval = Evaluador.objects.get(correo=request.session.get('correo'))
        #Saca todas las evaluaciones que le corresponden al evaluador
        evaluas = eval.evalua_set.all()
        Evaluaciones = []
        for evalua in evaluas:
            Evaluaciones.append(evalua.evaluacion)
        # Luego ordeno las evaluaciones por la fecha de inicio
        evaluaciones_order = sorted(Evaluaciones, key=lambda x: x.fecha_inicio,reverse=True)
        context = {
            'lista_rubricas': Rubrica.objects.all(),
            'lista_evaluaciones': evaluaciones_order[:10],
            'lista_cursos': Instancia.objects.all()
        }
        return render(request, 'sistema/landingevaluador.html', context)

def index_login(request):
    #Dirige al login
    return render(request,'sistema/login.html')

@login_required
def index_cursos(request):
    #Muestra todos los cursos
    context = {
        'lista_cursos': Instancia.objects.all()
    }
    return render(request, 'sistema/admin/pag_cursos.html', context)

# error = True  fechas incorrectas (ver Evaluacion.validar_fechas)
@login_required
def index_evaluaciones(request, error = False):
    #Si es admin
    if request.session.get('es_admin'):
        #Muestra todas las evaluaciones
        context = {
            'lista_rubricas': Rubrica.objects.all(),
            'lista_evaluaciones': Evaluacion.objects.all(),
            'lista_cursos': Instancia.objects.all()
        }
    else:
        #Rescata las evaluaciones asociadas al evaluador
        eval=Evaluador.objects.get(correo=request.session.get('correo'))
        evaluas=eval.evalua_set.all()
        Evaluaciones=[]
        for evalua in evaluas:
            Evaluaciones.append(evalua.evaluacion)

        context = {
            'lista_rubricas': Rubrica.objects.all(),
            'lista_evaluaciones': Evaluaciones,
            'lista_cursos': Instancia.objects.all()
        }

    if error:
        context['mensaje'] = "Las fechas ingresadas son incorrectas"
    return render(request, 'sistema/admin/pag_evaluaciones.html', context)

# error = 1     email repetido
# error = 2     email incorrecto
@login_required
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

@login_required
def index_rubricas(request):
    #Entrega todas las rubricas
    context = {
        'lista_rubricas': Rubrica.objects.all()
    }
    return render(request, 'sistema/admin/pag_rubricas.html', context)


#   EVALUACION
@login_required
def evaluacion(request, eval_id):
    #Evaluacion
    ev = Evaluacion.objects.get(pk=eval_id)
    #Evaluadores que no son admin
    evaluadores = Evaluador.objects.filter(es_admin=0)
    # Evaluadores que son admin
    evaluadores_admin = Evaluador.objects.filter(es_admin=1)
    id_eval_admin=[]
    for eval in evaluadores_admin:
        id_eval_admin.append(eval.id)
    # Evaluadores de la evaluacion que no son admin
    evaluadores_eval = ev.evalua_set.all().exclude(evaluador_id__in=id_eval_admin)
    for eval in evaluadores_eval:
        id_eval_admin.append(eval.evaluador_id)
    #Evaluadores que se pueden agregar
    evaluadores_para_agregar=evaluadores.exclude(id__in=id_eval_admin)

    # grupos del curso de la evaluacion
    grupos = InstanciaGrupo.objects.filter(instancia=ev.instancia)
    context = {
		'evaluacion': ev,
        'lista_grupos': grupos,
        'lista_evaluadores':  evaluadores_para_agregar,
        'lista_evalua':evaluadores_eval
    }

    return render(request, 'sistema/evaluacion/gruposevaluacion.html',context)

@login_required
def evaluacion_grupo(request,eval_id=0,grupo_id=0,rubrica_id=0):
    #Entrega evaluacion grupo y rubrica que estan relacionadas
    ev = Evaluacion.objects.get(pk=eval_id)
    gr = Grupo.objects.get(pk=grupo_id)
    rub = Rubrica.objects.get(pk=rubrica_id)
    context = {
        'evaluacion': ev,
        'grupo' : gr,
        'rubrica':rub,
        'puntajes': rub.niveles
    }
    #Si esta en curso la evaluación
    if ev.abierta():
        #Si es admin
        if request.session.get('es_admin'):
            return render(request,'sistema/evaluacion/evaluacionadmin.html',context)
        else:
            return render(request, 'sistema/evaluacion/evaluacion.html', context)
    #Si ya termino
    return render(request, 'sistema/evaluacion/posteval.html',context)

@login_required
def postevaluacion(request, eval_id=0,grupo_id=0,rubrica_id=0):
    if request.method == "POST":
        #Rescata evaluacion, grupo, rubrica, puntajes y puntajes base de la evaluacion
        ev = Evaluacion.objects.get(pk=eval_id)
        gr = Grupo.objects.get(pk=grupo_id)
        rub = Rubrica.objects.get(pk=rubrica_id)
        puntaje=request.POST['lista-puntajes'].split(',')
        puntaje_base=(request.POST['lista-pj-base'])
        # Crear evaluacion de grupo si aun no esta en el sistema
        pre = Presentacion.objects.filter(evaluacion=ev,
                                          grupo=gr,evaluador=request.session.get('nombre')).exists()
        # Si no existe la presentacion se crea
        if not (pre):
            if(request.session.get('es_admin')):
                #Saca los presentadores que fueron agregados
                presentadores = (request.POST['presentadores_grupo']).split(',')
                pre = Presentacion.objects.create(evaluacion=ev,
                                              grupo=gr,
                                              puntajes=puntaje,
                                              evaluador=request.session.get('nombre'),
                                              presentador=presentadores)
            else:
                #Crea nueva presentacion en donde se registra el puntaje
                pre = Presentacion.objects.create(evaluacion=ev,
                                                  grupo=gr,
                                                  puntajes=puntaje,
                                                  evaluador=request.session.get('nombre'))
            pre.save()
        #Se modifica
        else:
            #Obtiene presentacion que corresponde
             pre=Presentacion.objects.get(evaluacion=ev,
                                          grupo=gr,evaluador=request.session.get('nombre'))
             #Modifica puntajes
             pre.puntajes = puntaje
             if (request.session.get('es_admin')):
                 #Si es admin modifica los presentadores del grupo
                 presentadores=(request.POST['presentadores_grupo']).split(',')
                 pre.presentador=presentadores
             pre.save()
        context = {
            'evaluacion': ev,
            'grupo' : gr,
            'rubrica': rub,
            'puntajes':puntaje,
            'puntaje_base':puntaje_base
        }
        if request.session.get('es_admin'):
            return render(request, 'sistema/evaluacion/postevaladmin.html', context)
        else:
            return render(request, 'sistema/evaluacion/posteval.html', context)


#   RUBRICA

# Ver rubrica
@login_required
def rubrica(request, rubrica_id):
    #Rescata rubrica que tiene id=rubrica_id
    context = {
        'rubrica': Rubrica.objects.get(pk=rubrica_id)
    }
    return render(request, 'sistema/rubricas/rubrica.html', context)

# Editar rubrica
@login_required
def rubrica_editar(request, rubrica_id):
    if not request.session['es_admin']:
        return redirect("sistema:rubrica", rubrica_id = rubrica_id)
    rub = Rubrica.objects.get(pk=rubrica_id)
    # Obtengo evaluaciones que usan esta rubrica
    evaluaciones_con_rubrica = rub.evaluacionrubrica_set.all()
    evaluaciones=[]
    for eval in evaluaciones_con_rubrica:
        evaluaciones.append(eval.evaluacion)

    puede_editar = True

    for evaluacion in evaluaciones:
        numero_notas_puestas_de_evaluacion=Presentacion.objects.filter(evaluacion=evaluacion).count()
        if(numero_notas_puestas_de_evaluacion>0):
            puede_editar=False
            break

    if(puede_editar):
        context = {
        'rubrica': Rubrica.objects.get(pk=rubrica_id)
        }
        return render(request, 'sistema/rubricas/rubrica_admin.html', context)
    else:
        return redirect("sistema:rubrica", rubrica_id=rubrica_id)



#   GESTIONAR EVALUADOR
@login_required
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
            contraseña= nueva_pass()
            ev = Evaluador.objects.create(nombre = form.cleaned_data['nombre'],
                                          correo = form.cleaned_data['correo'],
                                          password = contraseña, es_admin = False)
            ev.save()
            #Crea usuario con su contraseña para poder entrar al login
            user = User.objects.create_user(form.cleaned_data['correo'], form.cleaned_data['correo'], contraseña)
            user.save()
            user.email_user("Creacion de usuario",
                            "Bienvenido al sistema de evaluacion de presentaciones. Tu usuario es "+ user.username+
                            " y tu contraseña es " +contraseña)
            return redirect(reverse('sistema:index_evaluadores'))
        return index_evaluadores(request, error = 1, nombre = request.POST['nombre'])
    return index_evaluadores(request, error = 2, nombre = request.POST['nombre'])

@login_required
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
        #Modifica usuario del login
        user = User.objects.get(username=ev.correo)
        user.username=form.cleaned_data['correo']
        user.save()
        ev.nombre = form.cleaned_data['nombre']
        ev.correo = form.cleaned_data['correo']
        ev.save()
        return redirect(reverse('sistema:index_evaluadores'))
    return index_evaluadores(request, error = 2)

@login_required
def eliminar_evaluador(request):
    id = int(request.POST['id'])
    Eval= Evaluador.objects.get(pk=id)
    #Elimina cuenta de evaluador del sistema del login
    User.objects.get(username=Eval.correo).delete()
    Eval.delete()
    return redirect(reverse("sistema:index_evaluadores"))


#   GESTIONAR EVALUACION
@login_required
def agregar_evaluacion(request):
    # Si se carga la pagina normalmente
    if request.method != "POST":
        return redirect(reverse('sistema:index_evaluaciones'))
    form = EvaluacionForm(request.POST)
    # Validar el formato de las fechas
    if form.is_valid():
        ev = Evaluacion.objects.create(instancia=Instancia.objects.get(pk=request.POST['curso']),
									   nombre=request.POST['nombre'],
                                       fecha_inicio=form.cleaned_data['inicio'],
                                       fecha_fin=form.cleaned_data['fin'],
                                       tiempo_min=form.cleaned_data['minimo'],
                                       tiempo_max=form.cleaned_data['maximo'])
        # Si las fechas estan correctas
        if ev.validar_fechas(agregar=True):
            ev.save()
            # Crear relacion entre rubrica y evaluacion
            EvaluacionRubrica.objects.create(evaluacion=ev,
                                             rubrica=Rubrica.objects.get(pk=request.POST['rubrica'])).save()
            # Admin como evaluador por defecto (Cambiar a usuario que realiza la accion?)
            Evalua.objects.create(evaluacion=ev, evaluador=Evaluador.objects.get(pk=2)).save()
            return redirect("sistema:evaluacion", ev.id)
        else:
            ev.delete()
    return index_evaluaciones(request, error = True)

@login_required
def modificar_evaluacion(request):
    # Si se carga la pagina normalmente
    if request.method != "POST":
        return redirect(reverse('sistema:index_evaluaciones'))
    form = EvaluacionForm(request.POST)
    # Validar el formato de las fechas
    if form.is_valid():
        eval = Evaluacion.objects.get(pk=request.POST['id'])
        eval.nombre = request.POST['nombre']
        # No se cambia la fecha de inicio si ya esta abierta
        if not eval.abierta():
            eval.fecha_inicio = form.cleaned_data['inicio']
        eval.fecha_fin = form.cleaned_data['fin']
        eval.tiempo_min = form.cleaned_data['minimo']
        eval.tiempo_max = form.cleaned_data['maximo']
        eval.instancia = Instancia.objects.get(pk=request.POST['curso'])
        # Si las fechas estan correctas
        if eval.validar_fechas():
            eval.save()
            r = Rubrica.objects.get(pk=request.POST['rubrica'])
            # Crear relacion entre rubrica y evaluacion
            relacion = eval.evaluacionrubrica_set.all()[0]
            relacion.rubrica = r
            relacion.save()
            # Admin como evaluador por defecto (Cambiar a usuario que realiza la accion?)
            return redirect("sistema:evaluacion", eval.id)
    return index_evaluaciones(request, error=True)
    
@login_required
def eliminar_evaluacion(request):
    #Elimina evaluacion a traves de id del post
    id = int(request.POST['id'])
    Evaluacion.objects.get(pk=id).delete()
    return redirect(reverse("sistema:index_evaluaciones"))

@login_required
def evaluacion_agr_evaluador(request,eval_id=0):
    #Agrega evaluador a la evaluacion para que pueda poner nota
    ev=Evaluacion.objects.get(pk=eval_id)
    Evalua.objects.create(evaluacion=ev, evaluador=Evaluador.objects.get(pk=request.POST['evalu'])).save()
    return redirect('sistema:evaluacion',eval_id)

@login_required
def evaluacion_eliminar_evaluador(request,eval_id=0):
    #Elimina evaluador de la evaluacion
    #Busca evaluador
    id = (request.POST['id'])
    #Elimina evaluador
    Evalua.objects.get(evaluacion_id=eval_id,evaluador_id=id).delete()
    return redirect("sistema:evaluacion", eval_id)

#   GESTIONAR RUBRICA
@login_required
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

@login_required
def modificar_rubrica(request, rubrica_id):
    i = 0 # Cuenta columnas
    while "celda:0,{}".format(i) in request.POST:
        cols = i
        i+=1
    i = 0 # Cuentaaaaq filas
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
    
@login_required
def eliminar_rubrica(request):
    r = Rubrica.objects.get(pk=request.POST['id'])
    r.borrar() # Elimina archivo
    r.delete() # Elimina objeto
    return redirect(reverse("sistema:index_rubricas"))

# Redirect home
def home(request):
    return redirect(reverse("sistema:index_login"))
