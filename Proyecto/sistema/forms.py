from django import forms

class EvaluadorForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    correo = forms.EmailField(max_length=90)