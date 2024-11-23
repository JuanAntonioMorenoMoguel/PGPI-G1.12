from django import forms
from .models import Curso, Horario
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['curso', 'dia', 'hora_inicio', 'hora_fin']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'placeholder': '00:00', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'placeholder': '00:00', 'class': 'form-control'}),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_superuser', 'is_active', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Usar email como username
        if commit:
            user.save()
        return user
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe un usuario con este correo electrónico.")
        return email


class CustomUserChangeForm(UserChangeForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_superuser', 'is_active', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])  # Cifra la contraseña antes de guardar
        if commit:
            user.save()
        return user


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'especialidad', 'modalidad', 'fecha_inicio', 'fecha_finalizacion', 'precio', 'vacantes']
        widgets = {
            'fecha_inicio': forms.DateInput(
                attrs={
                    'type': 'date',  # Esto genera un selector de fecha compatible con navegadores modernos
                    'class': 'form-control',
                }
            ),
            'fecha_finalizacion': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.Select(attrs={'class': 'form-control'}),
            'modalidad': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'vacantes': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_finalizacion = cleaned_data.get('fecha_finalizacion')

        if fecha_inicio and fecha_finalizacion and fecha_inicio > fecha_finalizacion:
            raise forms.ValidationError("La fecha de inicio no puede ser posterior a la fecha de finalización.")
        return cleaned_data