from django.db import models
from django.db import models
from django.utils import timezone

import os

# Create your models here.
from django.utils.datetime_safe import datetime


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
    seccion=models.IntegerField()

    def __str__(self):
        return " ".join([self.curso.nombre, self.semestre, str(self.ano), "Sección", str(self.seccion)])

class InstanciaGrupo(models.Model):
    instancia = models.ForeignKey(Instancia, on_delete=models.CASCADE)#sin on delete tira error
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)#sin on delete tira error

    def __str__(self):
        return str(self.instancia) +" "+ str(self.grupo)

class Evaluacion(models.Model):
    instancia = models.ForeignKey(Instancia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, default="Evaluacion")
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    tiempo=models.TimeField(default='00:00:00')
    tiempo_min=models.TimeField(default='00:00:00')
    tiempo_max=models.TimeField(default='00:00:00')

    def __str__(self):
        return str(self.fecha_inicio)

    # True si fecha_inicio es posterio a fecha actual (al agregar)
    # y fecha_fin es posterior a fecha_inicio
    def validar_fechas(self, agregar=False):
        if agregar and not (self.fecha_inicio >= timezone.now().date()):
            return False
        return self.fecha_inicio <= self.fecha_fin

    # True si fecha actual esta entre fecha_inicio y fecha_fin
    def abierta(self):
        return self.fecha_inicio <= timezone.now().date() <= self.fecha_fin

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
    t = None # tabla donde se guarda la info de archivo

    def __str__(self):
        return self.nombre

    # Crea el archivo y devuelve su ruta
    def crear(self):
        fn = "rubricas/rubrica_{}.csv".format(self.id)
        f = open(fn, "w")
        f.writelines(["$0.0\n","Aspecto1$Descripcion1\n"])
        f.close()
        return fn

    # Carga y devuelve los datos de la rubrica
    def tabla(self):
        if self.t == None:
            f = open(str(self.archivo), "r")
            self.t = [line.rstrip('\n').split('$') for line in f]
            f.close()
        return self.t

    # Devuelvelos niveles de cumplimiento
    def niveles(self):
        if self.t == None:
            self.tabla()
        return self.t[0][1:]

    # Devuelve los aspectos a evaluar
    def aspectos(self):
        if self.t == None:
            self.tabla()
        return [self.t[i][0] for i in range(1, len(self.t))]

    # Borra el archivo asociado
    def borrar(self):
        os.remove(str(self.archivo))

    # Modifica el archivo de acuerdo a la tabla entregada
    def modificar(self, tabla):
        tabla = self.reordenar(tabla)
        f = open(str(self.archivo), "w")
        for linea in tabla:
            f.write("$".join(linea) + "\n")
        self.t = None

    # Reordena las celdas en puntaje de menor a mayor
    def reordenar(self, tabla):
        nt = [[tabla[i].pop(0)] for i in range(len(tabla))]
        while len(tabla[0]) > 0:
            i = tabla[0].index(min(tabla[0]))
            for j in range(len(tabla)):
                nt[j].append(tabla[j].pop(i))
        return nt

    # True si el puntaje maximo es 6.0
    def validar(self):
        t = self.tabla()
        pmax = float(t[0][-1])
        return int(10 * pmax * (len(t) - 1)) == 60

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

