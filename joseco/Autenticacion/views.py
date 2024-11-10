from django.shortcuts import render, redirect
from .forms import CustomRegisterForm
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
