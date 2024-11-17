from django.db import models

# Create your models here.

class Curso(models.Model):
    # Campo Nombre
    nombre = models.CharField(max_length=200)

    # Enumerado para Especialidad
    class EspecialidadChoices(models.TextChoices):
        JUSTICIA = 'Justicia'
        SANIDAD = 'Sanidad'
        EDUCACION = 'Educación'
        SEGURIDAD = 'Fuerzas y cuerpos de seguridad'
        ADMIN_GENERAL = 'Administración General'
        TECNICAS = 'Técnicas y Especialidad'
        SERV_SOCIALES = 'Servicios Sociales'
        CULTURALES = 'Culturales'
        CORREOS = 'Correos'
        ECONOMIA = 'Economía y Estadística'

    especialidad = models.CharField(
        max_length=50,
        choices=EspecialidadChoices.choices,
    )

    # Enumerado para Modalidad
    class ModalidadChoices(models.TextChoices):
        HIBRIDO = 'Híbrido'
        ONLINE = 'On-Line'
        PRESENCIAL = 'Presencial'

    modalidad = models.CharField(
        max_length=20,
        choices=ModalidadChoices.choices,
    )

    # Fechas
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()

    # Precio
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre
    
    class Meta:
        app_label = 'auth'  # Asignar la sección "Autenticación y autorización"
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
