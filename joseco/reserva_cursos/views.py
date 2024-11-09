from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def reserva_cursos(request):
    return render(request, 'index.html', {'welcome_text': 'Bienvenido a JOSECO!'})