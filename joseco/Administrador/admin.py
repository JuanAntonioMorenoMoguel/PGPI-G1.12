from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext as _

from .models import Curso, Horario


# Desregistrar el modelo Grupos
admin.site.unregister(Group)

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especialidad', 'modalidad', 'fecha_inicio', 'fecha_finalizacion', 'precio', 'vacantes')
    # search_fields = ('nombre', 'especialidad')
    # list_filter = ('especialidad', 'modalidad', 'fecha_inicio', 'fecha_finalizacion')


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('curso', 'dia', 'hora_inicio', 'hora_fin', 'horas_totales')
    # list_filter = ('curso', 'dia')
    # search_fields = ('curso__nombre', 'dia')

    def horas_totales(self, obj):
        return obj.horas_totales()
    horas_totales.short_description = 'Horas Totales'
