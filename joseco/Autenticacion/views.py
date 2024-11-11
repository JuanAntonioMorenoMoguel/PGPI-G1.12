from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomLoginForm, CustomRegisterForm, EditarPerfilForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def registro(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()

            # Autenticar y loguear al usuario automáticamente
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registro exitoso e inicio de sesión automático.')
                return redirect('index')  # Redirige a la página principal u otra vista
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CustomRegisterForm()

    return render(request, 'registro.html', {'form': form})


def inicio_sesion(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('index')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CustomLoginForm()

    return render(request, 'inicio_sesion.html', {'form': form})

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado correctamente!')
            return redirect('index')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = EditarPerfilForm(instance=request.user)

    return render(request, 'editar_perfil.html', {'form': form})