from django.db import models
from django.forms import ValidationError
from datetime import date
from django import forms
from datetime import timedelta

# Create your models here.

class Curso(models.Model):
    # Campos del modelo
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



    # Validaciones personalizadas en el nivel del modelo
    def clean(self):
        super().clean()

        # Validar fecha de inicio
        if self.fecha_inicio and self.fecha_inicio < date.today():
            raise ValidationError({"fecha_inicio": "La fecha de inicio no puede ser anterior a hoy."})

        # Validar fecha de finalización
        if self.fecha_finalizacion and self.fecha_finalizacion < date.today() and self.fecha_finalizacion <= self.fecha_inicio:
            raise ValidationError({"fecha_finalizacion": "La fecha de finalización no puede ser anterior a hoy ni anterior o igual a la fecha de inicio."})

        # Validar relación entre fechas
        if self.fecha_inicio and self.fecha_finalizacion and self.fecha_finalizacion == self.fecha_inicio:
            raise ValidationError({"fecha_finalizacion": "La fecha de finalización igual a la fecha de inicio."})

    @property
    def horas_semanales(self):
        """Calcula automáticamente las horas semanales basándose en los horarios asignados."""
        total_horas = sum(horario.duracion_horas() for horario in self.horarios.all())
        return total_horas

    def duracion_meses(self):
        """Calcula la duración del curso en meses."""
        delta = self.fecha_finalizacion - self.fecha_inicio
        return max(delta.days // 30, 0)

    def calcular_precio_final(self):
        """Calcula el precio final con base en las condiciones."""
        if (
            self.duracion_meses() >= 1 and  # Duración mínima de 1 mes
            4 <= self.horas_semanales and self.precio / self.duracion_meses() >= 75  # Precio mínimo de 100€
        ):
            return self.precio
        
        return self.precio
            

    def __str__(self):
        return self.nombre

    class Meta:
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
    
    def duracion_horas(self):
        """Calcula la duración del horario en horas."""
        inicio = timedelta(hours=self.hora_inicio.hour, minutes=self.hora_inicio.minute)
        fin = timedelta(hours=self.hora_fin.hour, minutes=self.hora_fin.minute)
        duracion = fin - inicio
        return duracion.total_seconds() / 3600  # Convertir segundos a horas

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

