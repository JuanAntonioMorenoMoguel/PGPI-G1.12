# Generated by Django 4.2.16 on 2024-12-03 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Administrador', '0007_alter_curso_imagen'),
        ('Gestion_Cursos', '0005_alter_recibo_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarritoNoAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('fecha_agregado', models.DateTimeField(auto_now_add=True)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Administrador.curso')),
            ],
        ),
    ]
