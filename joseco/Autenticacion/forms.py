from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class CustomRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellidos')
    email = forms.EmailField(required=True, label='Correo Electrónico')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Asignar email como username
        if commit:
            user.save()
        return user


class CustomLoginForm(forms.Form):
    email = forms.EmailField(required=True, label='Correo Electrónico')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        user = User.objects.get(email=email)
        # Verificar si el correo está registrado
        if user.exists() == False:
            raise forms.ValidationError('Este correo electrónico no está registrado.')

        # Autenticar al usuario con username y password
        user = authenticate(email=user.email, password=password)
        if user is None:
            raise forms.ValidationError('La contraseña no es correcta.')

        # Si todo está bien, retorna los datos limpios
        return cleaned_data
    

class EditarPerfilForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellidos')
    email = forms.EmailField(required=True, label='Correo Electrónico')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email
