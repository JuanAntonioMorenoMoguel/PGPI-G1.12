from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext as _

from .models import Curso

# admin.site.unregister(User)

# class CustomUserAdmin(admin.ModelAdmin):
#     verbose_name = _('Mi Usuario')  # Nombre singular
#     verbose_name_plural = _('Mis Usuarios')  # Nombre plural

# admin.site.register(User, CustomUserAdmin)
# Desregistrar el modelo Group predeterminado
# admin.site.unregister(Group)

# # Personalizar el modelo Group directamente
# Group._meta.verbose_name = _("Curso")
# Group._meta.verbose_name_plural = _("Cursos")

# # Registrar el modelo Group con una clase personalizada
# @admin.register(Group)
# class CustomGroupAdmin(admin.ModelAdmin):
#     # Opcionalmente personaliza las vistas del admin
#     list_display = ['name']

# Desregistrar el modelo Grupos
admin.site.unregister(Group)

# Registrar el modelo Curso con el Admin personalizado
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    fields = ('nombre', 'especialidad', 'modalidad', 'fecha_inicio', 'fecha_finalizacion', 'precio')
    list_display = ('nombre', 'especialidad', 'modalidad', 'precio')