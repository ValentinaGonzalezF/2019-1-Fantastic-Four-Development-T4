from django import forms

class EvaluadorForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    correo = forms.EmailField(max_length=90)

class EvaluacionForm(forms.Form):
    inicio = forms.DateField()
    fin = forms.DateField()
    maximo= forms.TimeField()
    minimo = forms.TimeField()
