from django.shortcuts import render, redirect
from .forms import CustomRegisterForm, CustomLoginForm
from django.contrib import messages

def registro(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu cuenta ha sido creada exitosamente.')
            return redirect('index')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CustomRegisterForm()

    return render(request, 'registro.html', {'form': form})

def inicio_sesion(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('index')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CustomLoginForm()

    return render(request, 'inicio_sesion.html', {'form': form})
