# Librerías para configuración de servidor SMTP con SendGrid
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Librería para manipular archivos .YAML
import yaml


# Creación de clase especializada únicamente para el envío de mensajes
class SMTP:

    # Declaramos el constructor inicial de la clase, definiendo variables requeridas por SendGrid
    def __init__(self):
        self.SENDER_MAIL = 'ricardoq@tics-sas.com'

        api = yaml.load(open('../apikey.yaml'), Loader=yaml.FullLoader)
        os.environ['SENDGRID_API_KEY'] = api['SENDGRID_API_KEY']

    # Construimos nuestro método requerido con el objeto necesario para realizar el envío del mensaje
    def enviar_notificacion(self, nombre, apellido, correo, usuario, password):
        message = Mail(
            from_email=self.SENDER_MAIL,
            to_emails=correo,
            subject='Notificación de usuario creado en plataforma Moodle',
            plain_text_content='Mensaje de prueba. '
                               '(' + nombre + ', ' + apellido + ', ' + usuario + ', ' + password + ').'
        )

        # Capturamos el proceso de envío del mensaje con una exepción para evitar inconvenientes de uso
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            # print(response.status_code)
            # print(response.body)
            # print(response.headers)
        except Exception as e:
            print(e.args)
