from django.db import models
from django.forms import ValidationError

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

    vacantes = models.PositiveIntegerField(default=0, verbose_name="Vacantes disponibles")


    def __str__(self):
        return self.nombre
    
    class Meta:
        # app_label = 'auth'  # Asignar la sección "Autenticación y autorización"
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

class DiaSemanaChoices(models.TextChoices):
    LUNES = 'Lunes'
    MARTES = 'Martes'
    MIERCOLES = 'Miércoles'
    JUEVES = 'Jueves'
    VIERNES = 'Viernes'
    SABADO = 'Sábado'
    DOMINGO = 'Domingo'

class Horario(models.Model):
    dia = models.CharField(
        max_length=10,
        choices=DiaSemanaChoices.choices
    )
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='horarios')

    def horas_totales(self):
        """Devuelve la cantidad de horas entre hora_inicio y hora_fin."""
        from datetime import datetime
        fmt = '%H:%M'
        inicio = datetime.strptime(self.hora_inicio.strftime(fmt), fmt)
        fin = datetime.strptime(self.hora_fin.strftime(fmt), fmt)
        return (fin - inicio).seconds / 3600  # Devuelve las horas

    def __str__(self):
        return self.horas_totales()

    def clean(self):
        """Valida que no haya solapamiento de horarios en el mismo día."""
        horarios_existentes = self.curso.horarios.filter(dia=self.dia).exclude(pk=self.pk)
        for horario in horarios_existentes:
            if (self.hora_inicio < horario.hora_fin and self.hora_fin > horario.hora_inicio):
                raise ValidationError(f"El horario del día {self.dia} se solapa con {horario}.")

    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        constraints = [
            models.UniqueConstraint(fields=['curso', 'dia', 'hora_inicio', 'hora_fin'], name='unique_horario')
        ]