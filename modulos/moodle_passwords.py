# Librerías para generación de contraseñas aleatorias
import secrets
import string

# Librería para encriptar contraseñas
from passlib.hash import md5_crypt


# Creación de clase especializada únicamente para el manejo de contraseñas
class Passwords:

    # Declaramos el constructor inicial de la clase
    def __init__(self):
        pass

    # Declaramos método para generación de contraseñas
    def gen_password(self, tam=20):

        try:
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(tam))

            return password
        except:
            print('Error en generación de contraseña')

    # Declaramos método para encriptación de contraseñas
    def encrypt_password(self, passw):
        password = md5_crypt.encrypt(passw)

        # print(password)
        if md5_crypt.verify(passw, password):
            return password
        else:
            self.encrypt_password(passw)
