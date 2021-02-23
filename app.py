"""
REST Web Service para automatización de registro de usuarios - MOODLE
Este es el recurso principal para la creación del servicio web consumible.
Dentro de este recurso se ejecutarán las acciones principales acorde a los
requerimientos instaurados para el funcionamiento y objetivo de este proyecto.
=================================================================================


TICS SAS 2021
"""


# Las Librerías a importar por defecto para la creación del abb web a usar
from flask import (
    Flask,    # importación de Flask para el diseño general del aplicativo
    request   # importación de request para la manipulación de web requests del servidor
)

# Librerías adicionales para adaptar el app web a un RESTfull Web Service
from flask_mysqldb import MySQL
from flask_restful import (
    Api,       # importación de Api para estructurar un API REST
    Resource   # flask_restful para definir el API
)

# Librerías diseñadas para mos módulos SMTP y SQL REGISTER para el Web Service
import moodle_smtp
import moodle_passwords

# Librería para manipular archivos .YAML
import yaml


# Definición de App web y RESTFull Web Service API a través de la App Web
app = Flask(__name__)
api = Api(app)

# Configuración de la base de datos, Flask requiere hacerlo en el mismo archivo principal de la aplicación
try:
    db = yaml.load(
        open('database.yaml'),  # Leemos el archivo .YAML con datos de conexión a MySQL
        Loader=yaml.FullLoader
    )

    app.config['MYSQL_HOST'] = db['mysql_host']          # Definimos el nombre del host servidor MySQL
    app.config['MYSQL_USER'] = db['mysql_user']          # Indicamos el nombre de usuario de la base de datos
    app.config['MYSQL_PASSWORD'] = db['mysql_password']  # Especificamos la contraseña del usuario asignado
    app.config['MYSQL_DB'] = db['mysql_db']              # Denotamos en nombre de la base de datos a usar del servidor

    # Creamos el objeto MySQL referenciando a la APP Flask para de esta forma inicializar la conexión
    mysql = MySQL(app)

except:
    print(
        'Error de configuración de base de datos. Revise el archivo .YAML del proyecto o verifique los datos de'
        'conexión de la base de datos'
    )
    raise


# Definimos el método de registro en MySQL de la información procesada
def moodle_mysql(nombre, apellido, correo, usuario, password):
    """
    Este módulo es el encargado de procesar los datos para enviarlos a la base de datos MySQL configurada
    para el proyecto.

    Posteriór a la declaración y asignación del objeto MySQL y la extracción de datos de la lista JSON obtenida
    en el web request, definimos ciertos parametros para de esta forma hacer el query requerido y registrar la
    información en la base de datos. Este método fue definido para que el envío de datos sea sencillo, solo se
    requiere pasar las variables a registrar en la base de  datos, todos extraidos.

    :param nombre: Nombre del usuario, extraido de la lista JSON obtenida en el web request.
    :param apellido: Apellido del usuario, extraido de la lista JSON obtenida en el web request.
    :param correo: Correo electrónico, extraido de la lista JSON obtenida en el web request.
    :param usuario: Usuario personalizado, extraido de la lista JSON obtenida en el web request.
    :param password: Contraseña de acceso, extraida de la lista JSON obtenida en el web request.
    :return: Esta función no retorna valores específicos.
    """

    try:

        # Creamos el objeto REG para de esta forma manipular la base de datos
        reg = mysql.connection.cursor()
        reg.execute(
            # Creamos el query para insertar los datos en la base de datos MySQL
            "INSERT INTO test (nombre, apellido, correo, usuario, password) VALUES(%s, %s, %s, %s, %s)",
            (nombre, apellido, correo, usuario, password)
        )
        mysql.connection.commit()
    except:
        print('Error de registro en base de datos.')
        raise


# Definimos el método principal donde se realizará el proceso  de registro datos y envío de mensajes
def procesar_datos(data_json):
    """
    Este módulo es el principal actor del web service, dentro de este se realizará la extracción de los datos
    en la lista JSON obtenida y se invocarán los metodos requeridos para la inyección de datos en MySQL y la
    notificación de credenciales para los usuarios de la plataforma Moodle.

    El módulo se encarga de obtener la lista de datos JSON y procesarla por cada registro en ella, segmentando y
    separando los datos en NOMBRE, APELLIDO, CORREO, USUARIO y generando la CONTRASEÑA por medio de los módulos
    importados y diseñados para dicha tarea. Además de ello se usa otro método adicional para el registro de datos en
    la base de datos MySQL y un módulo adicional que es usado para notificar dichos datos de acceso vía SMTP.

    :param data_json: Es la lista con los datos de usuarios a registrar, procesada del JSON obtenido en el request.
    :return: Esta función no retorna valores específicos.
    """

    try:

        # Inicializamos un objeto de la clase SMTP importado para la conexión con el servidor SMTP
        smtp = moodle_smtp.SMTP()

        # Iniciamos un objeto de la clase Passwords importado para la manipulación de contraseñas para Moodle
        pasw = moodle_passwords.Passwords()

        # Recorremos la lista referenciada en el método dependiendo del tamaño de esta para extraer los datos
        for index in range(len(data_json)):

            # Extracción de los datos de la lista, gracias al JSON obtenido
            nombre = data_json[index]['Datos']['Nombre']
            apellido = data_json[index]['Datos']['Apellido']
            correo = data_json[index]['Datos']['Correo']
            usuario = data_json[index]['Datos']['Usuario']

            # Generación y encriptación de contraeña para el usuario
            password = pasw.gen_password()
            pass_enc = pasw.encrypt_password(password)

            # Registro de datos en base de datos MySQL
            moodle_mysql(nombre, apellido, correo, usuario, pass_enc)

            # Envío de datos de registro de usuario a los correos electrónicos de los usuarios registrados
            smtp.enviar_notificacion(nombre, apellido, correo, usuario, password)

            print('datos:', nombre, apellido, correo, usuario, password)

    except:
        print('Error en la extracción de datos recibidos')
        raise


# Creamos nuestra clase principal que llevará a cabo el proceso GET y POST de nuestro Web Service
class MoodleRequestParser(Resource):
    """
    Clase MoodleRequestParser.

    Esta es la clase principal del aplicativo Flask, es la que se configura en la ruta de dominio para recibir
    las peticiones y de eta forma manipular los GET y POST entrantes. Esta clace viene sobrecargada para funcionar
    como RESTful Web Service y siempre procesar los datos entrates de peticiones en tiempo real.
    """

    # Definimos nuestro método GET (el cual no tendrá uso en este proyecto)
    @staticmethod
    def get():
        """
        Función GET del Web Service.

        Este método es para manejar los GET request entrantes a al aplicación. Debido a que la función principal de
        este aplicativo es recibir POST requests para el registro de información en base de datos y envío de correos,
        el método GET no está definido de forma especifica. De igual forma se deja estructurado y preparado por si
        se requiere mas adelante darle relevancia a este tipo de requests.

        :return: Respuesta String del aplicativo al servidor de request para realizar la petición POST.
        """

        return {
            'Estado': 'Por favor realice el envío de información para el registro de usuarios en la plataforma.'
        }

    # Definimos nuestro método POST que se usará para recibir la información de registro de datos de usuarios Moodle.
    @staticmethod
    def post():
        """
        Función POST del Web Service.

        Este método es el que se encargará de las peticiones POST entrantes a la aplicación. Este método recibirá
        el JSON de datos para el registro de usuarios en la base de datos MySQL.

        Dentro del método se procesará la información del JSON para almacenarla en una lista y de esta forma empezar
        a procesarla por medio del método procesar_datos y realizar las funciones fundamentales del Web Service.

        :return: Respuesta String del aplicativo al servidor para notificar el estado final de la petición enviada.
        """

        # Validamos la obtención de información en el request recibido
        if request.get_json():

            try:
                # Capturamos la información JSON y la capturamos en una lista
                datos = request.get_json()

                # Visualizamos en consola los datos (En desarrollo y QA)
                print(type(datos))

                # Procesamos los datos recibidos
                procesar_datos(datos)

                return {
                    'Estado': str(len(datos)) + ' usuarios creados exitosamente.'
                }
            except:
                return {
                    'Estado': 'Se ha presentado un error inesperado.'
                }
        else:

            return {
                'Estado': 'Error. Verifique la información o sintaxis de la información '
                          'dentro de la solicitud enviada.'
            }


# Registramos la clase desarrollada a la ruta raiz de acceso web para ser consultada inmediatamente
api.add_resource(MoodleRequestParser, '/')

# Configuramos la ejecución del recurso web
if __name__ == '__main__':
    app.run(debug=True)
