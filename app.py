"""
REST Web Service para automatización de registro de usuarios - MOODLE

Este es el recurso principal para la creación del servicio web consumible.

TICS SAS 2021
"""

# Las Librerías a importar por defecto para la creación del abb web a usar
from flask import (
    Flask,    # importación de Flask para el diseño general del aplicativo
    request  # importación de request para la manipulación de web requests del servidor
)

# Librerías adicionales para adaptar el app web a un RESTfull Web Service
from flask_mysqldb import MySQL
from flask_restful import (
    Api,       # importación de Api para estructurar un API REST
    Resource   # flask_restful para definir el API
)

# Librerías diseñadas para mos módulos SMTP y SQL REGISTER para el Web Service
from modulos import (
    moodle_smtp,           # Módulo para envío de  notificaciones por SMTP
    moodle_passwords       # Módulo para el manejo de contraseñas para el registro en MySQL
)

# Librería para manipular archivos .YAML
import yaml


# Definición de App web y RESTFull Web Service API a través de la App Web, además de configurar la DB
app = Flask(__name__)
api = Api(app)

db = yaml.load(open('database.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)


# Definimos el método principal donde se realizará el proceso  de registro datos y envío de mensajes
def procesar_datos(data_json):
    smtp = moodle_smtp.SMTP()
    pasw = moodle_passwords.Passwords()

    for index in range(len(data_json)):

        # Extracción de los datos del JSON obtenido
        nombre = data_json[index]['Datos']['Nombre']
        apellido = data_json[index]['Datos']['Apellido']
        correo = data_json[index]['Datos']['Correo']
        usuario = data_json[index]['Datos']['Usuario']

        # Generación y encriptación de contraeña para el usuario
        password = pasw.gen_password()
        pass_enc = pasw.encrypt_password(password)

        # Registro de datos en base de datos MySQL
        try:
            reg = mysql.connection.cursor()
            reg.execute(
                "INSERT INTO test (nombre, apellido, correo, usuario, password) VALUES(%s, %s, %s, %s, %s)",
                (nombre, apellido, correo, usuario, pass_enc)
            )
            mysql.connection.commit()
        except:
            print('Error de registro en base de datos.')

        # Envío de datos de registro de usuario a los correos electrónicos de los usuarios registrados
        smtp.enviar_notificacion(nombre, apellido, correo, usuario, password)

        print('datos:', nombre, apellido, correo, usuario, password)


# Creamos nuestra clase principal que llevará a cabo el proceso GET y POST de nuestro Web Service
class MoodleRequestParser(Resource):

    # Definimos nuestro método GET (el cual no tendrá uso en este proyecto)
    @staticmethod
    def get():
        return {
            'Estado': 'Por favor realice el envío de información para el registro de usuarios en la plataforma.'
        }

    # Definimos nuestro método POST que se usará para recibir la información de registro de datos de usuarios Moodle.
    @staticmethod
    def post():

        # Validamos la obtención de información en el request recibido
        if request.get_json():

            # Capturamos la información JSON y la capturamos en una lista
            datos = request.get_json()

            # Visualizamos en consola los datos (En desarrollo y QA)
            print(type(datos))

            # Procesamos los datos recibidos
            procesar_datos(datos)

            return {
                'Estado': str(len(datos)) + ' usuarios creados exitosamente.'
            }
        else:
            return {
                'Estado': 'Error. Verifique la información o sintaxis de la solicitud realizada.'
            }


# Registramos la clase desarrollada a la ruta raiz de acceso web para ser consultada inmediatamente
api.add_resource(MoodleRequestParser, '/')

# Configuramos la ejecución del recurso web
if __name__ == '__main__':
    app.run(debug=True)
