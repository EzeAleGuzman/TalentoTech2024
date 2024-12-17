
<p align="center">
  <img src="Logo.png" alt="Logo de TechStock" width="400">
</p>

<h1 style="text-align: center;">TechStock</h1>

TechStock es una aplicación de consola desarrollada como parte de un proyecto de curso, enfocada en gestionar el control de stock de productos tecnológicos y los estados de cuenta de clientes y proveedores. La aplicación maneja la lógica necesaria para realizar compras, ventas y actualizaciones de inventario de manera eficiente. A medida que continúa en desarrollo, se añaden nuevas funcionalidades para mejorar la experiencia de usuario y optimizar el flujo de trabajo en la gestión del inventario. Este proyecto refleja el aprendizaje práctico adquirido durante el curso.

## Comenzando 🚀

Este proyecto esta desarrollado en python 3.11.5 y requiere la instalación de las siguientes dependencias:

1. Descargar el repositorio

Primero, clona este repositorio en tu máquina local. Abre una terminal y ejecuta el siguiente comando:

```
git clone https://github.com/usuario/techstock.git

```
Cambia al directorio del proyecto:

```
cd techstock

```


2. Crear y activar un entorno virtual (venv)

    *Para asegurarse que las dependencias esten aisladas de las dependencias del sistema operativo, se recomienda crear un entorno virtual.
    ejecutar el siguiente comando ebnn tu consola de comandos*

```
python3.11 -m venv venv

```

Luego, activa el entorno virtual:

En Windows:

```
.\venv\Scripts\activate

```

En MacOS/Linux:

```
source venv/bin/activate
```

3. instalar las dependencias
    *Para instalar las dependencias, ejecuta el siguiente comando en la terminal*

```
pip install -r requirements.txt
```
4. Ejecutar el proyecto
    *Para ejecutar el proyecto, ejecuta el siguiente comando en la terminal*

```
python main.py
``` 
## Estructura del Proyecto 📁

La estructura del proyecto es organizada para facilitar la gestión de las dependencias y los módulos. Se utiliza una técnica para importar módulos desde directorios superiores, lo que permite que el código sea más flexible y fácil de mantener.

La estructura del proyecto es la siguiente:

my_project/ │ ├── main.py ├── utilitys/ │ └── utilitys.py └── bd/ └── bd.py



### Solución para las importaciones

En el archivo `main.py`, se utiliza el siguiente código para asegurarse de que los módulos ubicados en directorios superiores o hermanos sean accesibles:

```python
import sys
import os

# Añadir el directorio superior a sys.path para que las importaciones funcionen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))




