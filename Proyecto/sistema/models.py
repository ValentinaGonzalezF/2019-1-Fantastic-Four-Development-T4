from django.db import models
from django.db import models
from django.utils import timezone

# Create your models here.
class Grupo(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=90)
    rut = models.CharField(max_length=10)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class HistorialGrupos(models.Model):
    alumno= models.ForeignKey(Alumno,on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo,on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return self.grupo + ", " + self.fecha

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre + " " + self.codigo

class Instancia(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    ano=models.IntegerField()
    semestre= models.CharField(max_length=100)
    #No se si tomar la seccion como numero o string
    seccion=models.IntegerField()

    def __str__(self):
        return self.curso +" "+ self.ano +" "+ self.semestre +" "+ self.seccion

class InstanciaGrupo(models.Model):
    instancia = models.ForeignKey(Instancia, on_delete=models.CASCADE)#sin on delete tira error
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)#sin on delete tira error

    def __str__(self):
        return self.instancia +" "+ self.grupo

class Evaluacion(models.Model):
    instancia = models.ForeignKey(Instancia, on_delete=models.CASCADE)
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    tiempo=models.TimeField()

    def __str__(self):
        return self.fecha_inicio

class Evaluador(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=90)
    password=models.CharField(max_length=100)
    es_admin=models.BooleanField()

    def __str__(self):
        return self.nombre

class Rubrica(models.Model):
    nombre=models.CharField(max_length=100)
    archivo=models.FileField(upload_to=None, max_length=100)

    def __str__(self):
        return self.nombre

class EvaluacionRubrica(models.Model):
    evaluacion = models.ForeignKey(Evaluacion,on_delete=models.CASCADE)
    rubrica = models.ForeignKey(Rubrica,on_delete=models.CASCADE)

class Presentacion(models.Model):
    presentador=models.CharField(max_length=100)
    evaluador=models.CharField(max_length=100)
    puntajes=models.CharField(max_length=100)
    evaluacion = models.ForeignKey(Evaluacion,on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo,on_delete=models.CASCADE)

class Evalua(models.Model):
    evaluacion = models.ForeignKey(Evaluacion,on_delete=models.CASCADE)
    evaluador = models.ForeignKey(Evaluador,on_delete=models.SET_DEFAULT, default=1)
    puso_nota=models.BooleanField(default=False)

