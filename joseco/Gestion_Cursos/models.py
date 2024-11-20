from django.db import models
from django.conf import settings
from Administrador.models import Curso


class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)  # Por si se permite añadir varias veces
    fecha_agregado = models.DateTimeField(auto_now_add=True)
