# Sistema de Certificación de Documentos de la Universidad de Los Andes (CERTIULA)

CERTIULA es un sistema para certificar documentos a los estudiantes egresados de la Universidad de Los Andes, basada en el uso de la tecnologia blockchain para la certificación digital. Fue construido en Django con base de datos PostgreSQL y para la ceritificacion digitial en blockchain se usa la API CertsGen que se encarga de garantizar la generación y registro de los certificados digitales en la red blockchain.

# Instrucciones de Instalación

## Entorno de Instalación

### Pre-requisitos

1. Realizar la instación de la API CertsGen siguiendo las instrucciones que allí se muestran.
```bash
	https://github.com/LizanLycan/CertsGen
```

2. Asegúrese de tener instalado Python v3.8 para evitar conflicto entre versiones.

3. Tener instalado PostgreSQL

### Instalación

1. Clonar el repositorio.
```bash
	$ git clone https://github.com/m-mendez96/certiula.git
```

2. Crear la base de datos en su maquina local.

3. Configurar los parametros del la base de datos creada en el archivo settings.py del proyecto.

4. Crear el entorno local.
```bash
	$ python3 -m venv enviroment
```

5. Activar el entorno creado.
```bash
	$ source enviroment/bin/activate
```

6. Una vez el entorno este activado, puede proceder a instalar las dependencias en el entorno.
```bash
	$ pip install requeriments.txt
```

7. Crear las migraciones.
```bash
	$ python manage.py makemigrations
```

8. Migrar los modelos.
```bash
	$ python manage.py migrate
```

9. Crear el usuario de acceso de administrador.
```bash
	$ python manage.py createsuperuser
```

10. Correr el proyecto.
```bash
	$ python manage.py runserver 127.0.0.1:8000
```
