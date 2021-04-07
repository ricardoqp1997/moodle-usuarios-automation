"""
Módulo para gestión de contraseñas de Moodle.

En este módulo se implementan los métodos de generación y encriptación de
contraseñas para el registro de los usuarios en la base de datos MySQL, con el
objetivo de poder realizar el ingreso a la plataforma Moodle.
=================================================================================


TICS SAS 2021
"""


# Librerías para generación de contraseñas aleatorias
import secrets
import string

# Librería para encriptar contraseñas
import bcrypt


# Creación de clase especializada únicamente para el manejo de contraseñas
class Passwords:
    """
    Se declara la clase Passwords para acceder a las funciones de creación y encriptación de contraseñas en
    el archivo principal app.py
    """

    # Declaramos el constructor inicial de la clase
    def __init__(self):
        """
        Constructor inicial de la clase Password. Se deja especificado por si mas adelante se requiere hacer
        declaraciones iniciales de los objetos de esta clase.
        """
        pass

    # Declaramos método para generación de contraseñas
    def gen_password(self, tam=20):
        """
        Método para generación de contraseñas.

        Dentro de este método se utiliza manipulación de strings y caracteres para la generación automatica y
        aleatoria de contraseñas por medio de las librerías STRING y SECRETS. Dichas librerías poseen las
        clases y objetos requeridos para hacer el proceso de creación de contraseñas mas impecable y sencillo ya
        que están diseñados para ello. Solo se requiere un parámetro dentro del método, el cual por defecto viene
        predefinido, solo se requeriría su modificacion respecto a los intereses u objetivos de uso para la
        creación de contraseñas.

        :param tam: Valor por defecto 20. Este parametro contiene el numero de caracteres requeridos en la contraseña.
        :return: Se retorna el String que contiene la contraseña generada aleatoriamente.
        """

        try:
            # Se genera un objeto que contenga las propiedades de la contraseña a generar
            alphabet = string.ascii_letters + string.digits

            # Se almacena la contraseña generada en el rango TAM especificado (por defecto 20)
            password = ''.join(secrets.choice(alphabet) for i in range(tam))

            return password
        except:
            print('Error en generación de contraseña')
            raise

    # Declaramos método para encriptación de contraseñas
    def encrypt_password(self, passw):
        """
        Método para encripcatión de contraseñas.

        Este método obtiene una contraseña y la encripta bajo el protocolo MD5 para de esta forma ser almacenada
        dentro de la base de datos. El procedimiento de encriptación es realizado por medio del objeto MD5_CRYPT
        proveniente de la librería PASSLIB.HASH y con ello se garantiza el encriptado de la contraseña
        introducida como parámetro dentro de la función, con ello se garantiza la entrada y salida exitosa de
        este proceso sin inconvenientes y solo con un parámetro.

        :param passw: Contraseña indicada por medio del llamado de la función para ser encripdata dentro del método.
        :return: Se retorna la contraseña entriptada y lista para ser almacenada en la base de datos MySQL.
        """

        try:

            # Verificamos que la contraseña generada sea str
            print(f'Contraseña type: {type(passw)}')

            # Generamos nuestra salt con el prefijo mas compatible: $2a$ y el número de rondas: 10 y encriptamos
            salt = bcrypt.gensalt(prefix=b'2a', rounds=10)
            hashed = bcrypt.hashpw(bytes(passw, 'utf-8'), salt)

            # Cambiamos el prefijo compatible $2a$ por el requerido: $2y$ para máxima compatibilidad con PHP
            password = str.replace(hashed.decode('utf-8'), '$2a$', '$2y$')

            print(f'HASH: {hashed} | Type: {type(hashed)}')
            print(f'PASS: {password} | Type: {type(password)}')

            # Verificamos el resultado exitoso de la encriptación, de ser negativo reenviamos el parámetro al método
            if bcrypt.checkpw(bytes(passw, 'utf-8'), hashed):

                return password
            else:
                self.encrypt_password(passw)

        except Exception as e:
            print(f'Error procesando la contraseña [{e}]')
            raise
