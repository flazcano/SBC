'''
Created on 29/10/2011

@author: Fernando

Modulo de Alertas (MA)
'''

# importaciones
import warnings
try: from smtplib import SMTP
except: print 'no se encuentra python-smtplib necesario para correr el modulo MA'; exit(1)
try: from email import Utils; from email.mime.multipart import MIMEMultipart; from email.mime.text import MIMEText #@UnresolvedImport
except: print 'no se encuentra python-email necesario para correr el modulo MA'; exit(1)
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=DeprecationWarning)
    try: import xmpp #@UnresolvedImport
    except: print 'no se encuentra python-xmpp necesario para correr el modulo MA'; exit(1)
from Logger import handler

# definiciones
XMPPDEBUG      = 0
SMTPHOST       = None
SMTPPORT       = None
SMTPUSER       = None
SMTPPASS       = None
SMTPDEBUGLEVEL = None
XMPPCLIENT     = None
XMPPHOST       = None
XMPPRESOURCE   = None
XMPPPORT       = None
XMPPUSER       = None
XMPPPASS       = None

# clases

# funciones
def EnviaCorreo(TOADDRESS, HOST, TIPO):
    handler.log.info('enviando alerta por correo a ' + TOADDRESS)
    try:
        mailServer = SMTP(SMTPHOST, SMTPPORT)
        mailServer.set_debuglevel(SMTPDEBUGLEVEL)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(SMTPUSER, SMTPPASS)
    
        # creo el mensaje
        msg = MIMEMultipart('alternative')
        msg['From'] = SMTPUSER
        msg['To'] = TOADDRESS
        msg['Date'] = Utils.formatdate(localtime = 1)
        msg['Message-ID'] = Utils.make_msgid()
        msg['Subject'] = "Alerta SBC - " + HOST
        if TIPO == 0:
            
            # Create the body of the message (a plain-text and an HTML version).
            text = "Estimado " + TOADDRESS + "!\n\n el servidor " + HOST + " ha vuelto a estar en linea"
            html = """\
            <html>
              <head></head>
              <body>
                <p>Estimado usuario!<br><br>
                   el servidor ha vuelto a estar en linea
                </p>
              </body>
            </html>
            """
        elif TIPO == 1:
            # Create the body of the message (a plain-text and an HTML version).
            text = "Estimado " + TOADDRESS + "!\n\n el servidor " + HOST + " esta fuera de linea"
            html = """\
            <html>
              <head></head>
              <body>
                <p>Estimado usuario!<br><br>
                   el servidor esta fuera de linea
                </p>
              </body>
            </html>
            """
        else:
            handler.log.info('el tipo ' + TIPO + ' no es un valor valido')
        
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)
        
        # envio del mensaje
        mailServer.sendmail(msg['From'], [msg['To']], msg.as_string())
        mailServer.quit()
    except Exception as message:
        handler.log.error('error al enviar alerta por correo')
        handler.log.exception(message)
    finally:
        mailServer.close()

def EnviaJabber(TOJID, HOST, TIPO):
    handler.log.info('enviando alerta por Jabber a ' + TOJID)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            jid  = xmpp.protocol.JID(TOJID)
            jabber = xmpp.Client(XMPPCLIENT, debug=XMPPDEBUG)
            handler.log.debug('domain: ' + jid.getDomain())
            connection = jabber.connect((XMPPHOST, XMPPPORT))
            if not connection:
                raise IOError('no se pudo conectar a ' + XMPPCLIENT)
            jabber.auth(XMPPUSER, XMPPPASS, XMPPRESOURCE)
            if not jabber.auth:
                raise IOError('no se pudo autentificar con ' + XMPPCLIENT)
            jabber.sendInitPresence(requestRoster=1)
            if int(TIPO) == 0:
                MSG = xmpp.Message(TOJID, 'El Servidor ' + HOST + ' se encuentra en linea')
                MSG.setAttr('type', 'chat')
                jabber.send(MSG)
            elif int(TIPO) == 1:
                MSG = xmpp.Message(TOJID, 'El Servidor ' + HOST + ' se encuentra fuera de linea')
                MSG.setAttr('type', 'chat')
                jabber.send(MSG)
            else:
                handler.log.error('el tipo ' + TIPO + ' no es un valor valido')
    except Exception as message:
        handler.log.error('error al enviar alerta por Jabber')
        handler.log.exception(message)

def EnviaSMS(TONUMBER, HOST, TIPO):
    pass
    
def Valida():
    pass

def run():
    handler.log.info('iniciando modulo')

def setSMTPHOST(VALUE):
    global SMTPHOST; SMTPHOST = VALUE
    handler.log.debug('SMTPHOST: ' + SMTPHOST)

def setSMTPPORT(VALUE):
    global SMTPPORT; SMTPPORT = VALUE
    handler.log.debug('SMTPPORT: ' + str(SMTPPORT))

def setSMTPUSER(VALUE):
    global SMTPUSER; SMTPUSER = VALUE
    handler.log.debug('SMTPUSER: ' + SMTPUSER)

def setSMTPPASS(VALUE):
    global SMTPPASS; SMTPPASS = VALUE
    handler.log.debug('SMTPPASS: [OMITIDO]')

def setSMTPDEBUGLEVEL(VALUE):
    global SMTPDEBUGLEVEL; SMTPDEBUGLEVEL = VALUE
    handler.log.debug('SMTPDEBUGLEVEL: ' + str(SMTPDEBUGLEVEL))

def setXMPPCLIENT(VALUE):
    global XMPPCLIENT; XMPPCLIENT = VALUE
    handler.log.debug('XMPPCLIENT: ' + XMPPCLIENT)

def setXMPPHOST(VALUE):
    global XMPPHOST; XMPPHOST = VALUE
    handler.log.debug('XMPPHOST: ' + XMPPHOST)

def setXMPPRESOURCE(VALUE):
    global XMPPRESOURCE; XMPPRESOURCE = VALUE
    handler.log.debug('XMPPRESOURCE: ' + XMPPRESOURCE)

def setXMPPPORT(VALUE):
    global XMPPPORT; XMPPPORT = VALUE
    handler.log.debug('XMPPPORT: ' + str(XMPPPORT))

def setXMPPUSER(VALUE):
    global XMPPUSER; XMPPUSER = VALUE
    handler.log.debug('XMPPUSER: ' + XMPPUSER)

def setXMPPPASS(VALUE):
    global XMPPPASS; XMPPPASS = VALUE
    handler.log.debug('XMPPPASS: [OMITIDO]')

# main