# Web Service para automatización de registro de usuarios Moodle

Este REST API Service está destinado a la automatización del registro de usuarios para 
la plataforma de moodle. Fue desarrollado en el framework Flask que está escrito en Python 
y se encuentra diseñado con la posibilidad de ser desplegado en Azure para conexión con una
base de datos MySQL y el servidor SMTP escogido para el desarrollo fue SendGrid.

Para realizar el despliegue en entorno local para desarrollo seguir los siguientes pasos:

* Clonar el repositorio desde GitHub directamente desde el IDE a usar (Se recomienda 
  PyCharm) o clonarlo en un directorio y acceder al contenido del proyecto desde el IDE a 
  escoger. Advertencia: Se recomienda que todo proceso local para la manipulación del 
  proyecto sea por medio de la rama/branch **develop**.
  
* Mediante la terminal interna del IDE realizar la configuración del intérprete Python en
versión 3.8 o posterior, se recomienda hacer por medio de Anaconda para tener gestión 
  directa de entornos virtuales. 
  
* Realizar la configuración de un entorno virtual para la gestión de recursos directa del 
proyecto (Nota: Al usar Anaconda, esta configuración es más sencilla). Si no se usa 
  Anaconda, usar Virtualenv. Para configuración manual de Anaconda o Virtualenv al usar un
  IDE distinto a PyCharm, revisar la documentación correspondiente de dichos recursos.
  
* Instalar los recursos del proyecto, para ello se requiere usar el comando: 
`pip install -r requirements.txt`.
  
* De ser necesario, cambiar los datos de acceso y llaves API para MySQL y SendGrid, ello 
se puede realizar modificando los archivos: **database.yaml** y **apikey.yaml**.
  
* Posterior a ello ya se puede realizar la ejecución del proyecto para temas de desarrollo,
pruebas y calidad.
  

Para realizar el despliegue continuo en Azure seguir los siguientes pasos:

* Previo al despliegue revisar y modificar los archivosarchivos: **database.yaml** y **apikey.yaml**.
Estos contienen la información de acceso a la base de datos MySQL y a SendGrid. La edición
  es requerida debido a que el repositorio cuenta con los datos del entorno local y de
  pruebas del SMTP.

* Crear y/o asignar grupo de recursos para el despliegue del App service.

* Crear el servicio de aplicativo web, destinandolo para el despliegue de un recurso 
en Python 3.8 o superior.
  
* Seleccionar GitHub para la gestíon de despliegue continuo. Nota: Para entorno en la 
nube para pruebas porfavor seleccionar la rama develop, para producción seleccionar la
  master.
  
* Seguir las indicaciones del portal Azure para configuración de recursos y despliegue.


Nota: Para pruebas de POST request, tanto en Azure como en entorno local, utilizar Postman.