import django_filters
from django_filters import DateFilter, CharFilter
from django import forms
from Administrador.models import Curso

class CursoFilter(django_filters.FilterSet):
    nombre = CharFilter(
        field_name='nombre',
        lookup_expr='icontains',
        label='Nombre del Curso',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar curso...'})
    )
    especialidad = django_filters.ChoiceFilter(
        field_name='especialidad',
        choices=Curso.EspecialidadChoices.choices,
        label='Especialidad'
    )
    modalidad = django_filters.ChoiceFilter(
        field_name='modalidad',
        choices=Curso.ModalidadChoices.choices,
        label='Modalidad'
    )
    fecha_inicio = DateFilter(
        field_name='fecha_inicio',
        lookup_expr='gte',
        label='Fecha de Inicio (Desde)',
        widget=forms.DateInput(attrs={'placeholder': 'dd/mm/YYYY', 'type': 'date'})
    )
    fecha_finalizacion = DateFilter(
        field_name='fecha_finalizacion',
        lookup_expr='lte',
        label='Fecha de Fin (Hasta)',
        widget=forms.DateInput(attrs={'placeholder': 'dd/mm/YYYY', 'type': 'date'})
    )

    class Meta:
        model = Curso
        fields = ['nombre', 'especialidad', 'modalidad', 'fecha_inicio', 'fecha_finalizacion']
