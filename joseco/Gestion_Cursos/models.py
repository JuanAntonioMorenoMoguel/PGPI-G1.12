from django.db import models
from django.conf import settings
from Administrador.models import Curso
from django.utils.timezone import now
from django.contrib.auth.models import User


class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)  # Por si se permite añadir varias veces
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    

class Recibo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='recibos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recibos')
    fecha_pago = models.DateTimeField()
    importe = models.DecimalField(max_digits=8, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)

    