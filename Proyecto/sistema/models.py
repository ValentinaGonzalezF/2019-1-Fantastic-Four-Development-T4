from django.db import models
from django.db import models
from django.utils import timezone

# Create your models here.
class Grupo(models.Model):
    nombre = models.CharField(max_length=100)

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=90)
    rut = models.CharField(max_length=10)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

class HistorialGrupos(models.Model):
    alumno= models.ForeignKey(Alumno,on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo,on_delete=models.CASCADE)
    fecha = models.DateField()

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20)

class Instancia(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    ano=models.IntegerField()
    semestre= models.CharField(max_length=100)
    #No se si tomar la seccion como numero o string
    seccion=models.IntegerField()

class InstanciaGrupo(models.Model):
    instancia = models.ForeignKey(Instancia)
    grupo = models.ForeignKey(Grupo)

class Evaluacion(models.Model):
    instancia = models.ForeignKey(Instancia, on_delete=models.CASCADE)
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    tiempo=models.TimeField()

class Evaluador(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=90)
    password=models.CharField(max_length=100)
    es_admin=models.BooleanField()

class Rubrica(models.Model):
    nombre=models.CharField(max_length=100)
    archivo=models.FileField(upload_to=None, max_length=100)

class EvaluacionRubrica(models.Model):
    evaluacion = models.ForeignKey(Evaluacion,on_delete=models.CASCADE)
    rubrica = models.ForeignKey(Rubrica,on_delete=models.CASCADE)

class Presentacion(models.Model):
    presentador=models.CharField(max_length=100)
    evaluador=models.CharField(max_length=100)
    puntales=models.CharField(max_length=100)
    evaluacion = models.ForeignKey(Evaluacion,on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo,on_delete=models.CASCADE)
    #archivo rubrica?

class Evalua(models.Model):
    evaluacion = models.ForeignKey(Evaluacion,on_delete=models.CASCADE)
    evaluador = models.ForeignKey(Evaluador,on_delete=models.CASCADE)
    #Hay un atributo que no entiendo en la foto
    #dice nom_er algo asi
    puso_nota=models.BooleanField()










