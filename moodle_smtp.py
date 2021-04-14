"""
Módulo para gestión de mensajería y del servidor SMTP (SendGrid).

En este módulo se implementan los métodos de configuración SMTP y de envío
de correos electrónicos por medio de SendGrid.
=================================================================================


TICS SAS 2021
"""


# Librerías para configuración de servidor SMTP con SendGrid
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Cc

# Librería para manipular archivos .YAML
import yaml


# Creación de clase especializada únicamente para el envío de mensajes
class SMTP:
    """
    Se declara la clase SMTP para de esta forma en app.py llamar las funciones internas de esta clase
    por medio de un objeto.

    Advertencia: Tener precaución con los datos de SendGrid, la llave API debe coincidir con el correo electrónico
    de envíos en la configuración del servicio en SendGrid y el correo electrónico debe estar verificado para
    evitar inconvenientes.
    """

    # Declaramos el constructor inicial de la clase, definiendo variables requeridas por SendGrid
    def __init__(self):
        """
        Constructor inicial de la clase SMTP. Dentro de el se hace la carga y configuración de los datos de SendGrid
        para la ejecución correcta del servidor SMTP. Recordemos que:

        1. Se debe configurar una cuenta verificada de SendGrid para el acceso al servidor SMTP.
        2. Se debe generar la llave API con todos los permisos requeridos para el funcionamiento con Python.
        3. El correo electrónico debe estar verificado y coincidir con la llave API para evitar inconvenientes.
        """

        self.api = None
        self.cc_email = 'oscar_esquivel@wvi.org'

        try:
            api = yaml.load(
                open('sendgrid_smtp.yaml'),  # Leemos el archivo .YAML con datos de conexión a MySQL
                Loader=yaml.FullLoader
            )

            try:
                # Asignación de variable de entorno para almacenamiento de la API
                os.environ['SENDGRID_API_KEY'] = api['SENDGRID_API_KEY']
            except:
                self.api = api['SENDGRID_API_KEY']
                print(
                    'Error en la configuración de variables de entorno. '
                    'Posiblemente ya se ha realizado anteriormente'
                )
                pass

            # Asignación del correo electrónico para el servidor SMTP de SendGrid
            self.SENDER_MAIL = api['EMAIL_SENDGRID']
        except:
            print(
                'Error configurando los parámetros de envío de correos. Verifique el archivo .YAML, '
                'los datos de configuración del servidor o su configuración general de SendGrid.'
            )
            raise

    # Construimos nuestro método requerido con el objeto necesario para realizar el envío del mensaje
    def enviar_notificacion(self, nombre, apellido, correo, usuario, password):
        """
        Método de envío de notificaciones.
        
        En este método se usan las funciones generales de la librería SendGrid para el envío y configuración de
        mensajes por medio de SMTP. Este método fue diseñado para que únciamente se pasen las variables que
        contendrán la información del usuario a notificar, el cuerpo del mensaje es fijo y predefinido para este
        procedimiento.

        La información referenciada en las variables de este método ya viene procesada desde la clase principal en
        app.py y únicamente acá el proceso se encarga de enviar el mensaje. Las variables del cuerpo del mensaje son
        las siguientes:

        :param nombre: Nombre del usuario.
        :param apellido: Apellido del usuario.
        :param correo: Correo electrónico.
        :param usuario: Usuario personalizado.
        :param password: Contraseña de acceso.
        :return: Esta función no retorna valores específicos.
        """

        # Generación del mensaje con todas las variables para la mnotificación de usuario creado
        message = Mail(
            from_email=self.SENDER_MAIL,
            to_emails=correo,
            subject='Notificación de usuario creado en plataforma Moodle',
            plain_text_content='Sr(a). ' + nombre + ' ' + apellido + '.\n '
                               
                               '\nSe han creado sus nuevas credenciales para el ingreso al portal Moodle '
                               'http://formacioneswv.worldvision.co/moodle/login/index.php\n'
                               'Sus credenciales de acceso serán:\n\n '
                               ''
                               '(' + nombre + ', ' + apellido + ', ' + usuario + ', ' + password + ').',

            html_content=f'<h4 style="text-align: center;"><strong>Apreciado (a) Estudiante</strong></h4>\n'
                         
                         f'<p>Sea usted bienvenido(a) a este su diplomado. Es para nosotros un placer y un honor '
                         f'ver cómo ha decidido escoger este diplomado para ampliar sus conocimientos en el trabajo '
                         f'comunitario y fortalecer su formación y perfeccionamiento profesional.</p>'
                         
                         f'<p>Estaremos vinculados en la aventura de formación de tres módulos, los cuales se irán '
                         f'desarrollando cien por ciento virtual con unas sesiones en vivo cada martes a las 6 pm '
                         f'hora Colombia.</p>'
                         
                         f'<p>El martes 13 de abril se habilitará la plataforma (no antes) de acuerdo con el horario '
                         f'para que inicie el desarrollo del primer módulo y luego los siguientes de acuerdo con las '
                         f'fechas establecidas.</p>'
                         
                         f'<p>A continuación, estamos adjuntando link de zoom para que el próximo martes 13 de abril a '
                         f'las 06:00 nos podamos conectar durante una hora para iniciar este increíble tiempo de '
                         f'formación.</p>'
                         
                         f'<a href="https://worldvision.zoom.us/j/91474125045">'
                         f'https://worldvision.zoom.us/j/91474125045</a>.\n'
                         
                         f'<p>Se ha creado un usuario nuevo a su nombre para su ingreso en el '
                         f'<a href="http://formacioneswv.worldvision.co/moodle/login/index.php">Portal de Moodle</a>. '
                         f'Las credenciales correspondientes para que pueda ingresar a la plataforma son las '
                         f'siguientes:</p>'
                         f'<ul>'
                         f'<li><strong>Usuario:</strong> {usuario}</li>'
                         f'<li><strong>Contraseña:</strong> {password}</li>'
                         f'</ul>'
                         f'<p>Para cualquier inconveniente o novedad relacioada con su ingreso al portal por favor '
                         f'contactese con el área de soporte del portal.</p>\n'
                         
                         f'<p>Bienvenidos y esperamos que disfrutes esta experiencia de vida.</p>'

        )

        try:
            # configuramos el envío de CC desde el correo.
            Cc(self.cc_email)
            message.add_cc(Cc(self.cc_email))
        except Exception as e:
            print(f'Error configurando el CC [{e}]')
            pass

        # Capturamos el proceso de envío del mensaje con una exepción para evitar inconvenientes de uso
        try:
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            except:
                sg = SendGridAPIClient(os.environ.get(self.api))
                pass

            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            print('======================================================')
        except Exception as e:
            print('Error en SendGrid/SMTP')
            print('======================================================')
            print(e.args)
            raise
