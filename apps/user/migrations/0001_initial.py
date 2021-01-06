# Generated by Django 2.2.6 on 2021-01-06 10:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('organizacion_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name': 'Organización',
                'verbose_name_plural': 'Organizaciones',
                'ordering': ('organizacion_id',),
            },
        ),
        migrations.CreateModel(
            name='UserExtension',
            fields=[
                ('identificacion', models.CharField(help_text='Venezolano (V-), Extranjero (E-), Pasaporte (P-)', max_length=10, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message='Introduzca una indentificación válida de acuerdo al formato que corresponda (V-, E-, P-).\n                Sólo se permite una letra seguida de un guion y los números con una longitud de maximo 8 carácteres.', regex='^[V|E|P]\\-[1-9][0-9]{6,9}$')])),
                ('fecha_nacimiento', models.DateField()),
                ('telefono', models.CharField(max_length=15)),
                ('direccion', models.CharField(max_length=150)),
                ('foto_perfil', models.ImageField(blank=True, default='profile/user.png', null=True, upload_to='profile/', verbose_name='Foto Perfil')),
                ('registro_blockchain', models.BooleanField(blank=True, default=False, null=True)),
                ('cuenta_blockchain', models.CharField(default=' ', max_length=64)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'ordering': ('usuario',),
            },
        ),
        migrations.CreateModel(
            name='FunctionalUnit',
            fields=[
                ('unidad_id', models.CharField(choices=[('UR', 'Unidad de Receptoria'), ('UA', 'Unidad de Archivo'), ('UP', 'Unidad de Procesamiento')], max_length=2, primary_key=True, serialize=False)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Unidad Funcional',
                'verbose_name_plural': 'Unidades Funcionales',
                'ordering': ('unidad_id',),
            },
        ),
        migrations.CreateModel(
            name='Authority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('AA', 'Autoridad de Acreditación'), ('AC', 'Autoridad de Certificación'), ('C', 'Certificador')], max_length=2)),
                ('organizacion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Organization')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.UserExtension')),
            ],
            options={
                'verbose_name': 'Autoridad',
                'verbose_name_plural': 'Autoridades',
                'ordering': ('tipo',),
            },
        ),
    ]
