"""iteracion1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

app_name = 'sistema'

urlpatterns = [
    path('cursos/', views.index_cursos, name = 'index_cursos'),
    path('evaluaciones/', views.index_evaluaciones, name = 'index_evaluaciones'),
    path('evaluadores/', views.index_evaluadores, name = 'index_evaluadores'),
    path('rubricas/', views.index_rubricas, name = 'index_rubricas'),
    path('evaluaciones/<int:eval_id>/', views.evaluacion, name = 'evaluacion'),
    path('rubricas/<int:rubrica_id>/', views.rubrica, name = 'rubrica'),
    path('rubricas/<int:rubrica_id>/editar', views.rubrica_editar, name = 'rubrica_editar'),

    path('evaluadores/agregar/', views.agregar_evaluador, name = 'evaluador_agr'),
    path('evaluadores/modificar/', views.modificar_evaluador, name = 'evaluador_mod'),
    path('evaluadores/eliminar/', views.eliminar_evaluador, name = 'evaluador_eli'),

    path('rubricas/agregar/', views.agregar_rubrica, name = 'rubrica_agr'),
    path('rubricas/modificar/', views.modificar_rubrica, name = 'rubrica_mod'),
    path('rubricas/eliminar/', views.eliminar_rubrica, name = 'rubrica_eli'),
]
