# banking-system-emulator

Simulador de productos bancarios con base de datos simulada con archivos .csv

## Requerimientos

* python: flask, wtforms, pandas, numpy, flask_login, werkzeug, flask_script, flask_bootstrap, flask_wtf
* node.js: npm, electron

## Arquitectura

La aplicación esta constituida por 2 técnologías principales: Electron y Flask. Con Flask, librería de python para el desarrollo de servidores web, se desarrolla el backend el cual es el responsable de administrar las vistas que el usuario ve y ejecuta acciones en la base de datos simulada. Para iniciar el servidor se debe ejecutar en CLI (en la raiz del repositorio) el comando `python manage.py runserver` el cual inicia el servidor local. Se accede con el # ip asignado a través del navegador y con eso ingresa al sistema. Se le va a solicitar que inicie sesión con el usuario *admin* y la contraseña *1234*.

## Ejecutable

Con Electron podemos utilizar estas técnologías web para transformar nuestro servidor local en un ejecutable, aprovechando de las excelentes interfaces de usuario que nos provee HTML, CSS y JS. Para iniciar la aplicación en modo de desarrollo, se debe ejecutar en CLI el comando `npm start` el cual iniciará la aplicación de escritorio. Nota: el servidor de Flask debe haberse iniciado previamente.
