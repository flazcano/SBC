'''
Created on 29/10/2011

@author: Fernando

Modulo de Alertas (MA)
'''

# importaciones
from smtplib import SMTP
from Logger import handler
from email import Utils
from email.mime.multipart import MIMEMultipart #@UnresolvedImport
from email.mime.text import MIMEText #@UnresolvedImport
try: import xmpp #@UnresolvedImport
except: handler.log.critical('no se encuentra python-xmpp necesario para correr el modulo MII'); exit(1)

# definiciones
SMTPHOST = "smtp.gmail.com"
SMTPPORT = 587
SMTPUSER = "fernandojavierlazcano@gmail.com"
SMTPPASS = "nirvana1234"
SMTPDEBUGLEVEL = 1
XMPPCLIENT = "gmail.com"
XMPPHOST = "talk.google.com"
XMPPRESOURCE = "SBC"
XMPPPORT = 5223
XMPPUSER = 'fernandojavierlazcano@gmail.com'
XMPPPASS = 'nirvana1234'

# clases

# funciones
def EnviaCorreo(TOADDRESS):
    handler.log.error('enviando alerta por correo a ' + TOADDRESS)
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
        msg['Subject'] = "Alerta SBC"
        
        # Create the body of the message (a plain-text and an HTML version).
        text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
        html = """\
        <html>
          <head></head>
          <body>
            <p>Hi!<br>
               How are you?<br>
               Here is the <a href="http://www.python.org">link</a> you wanted.
            </p>
          </body>
        </html>
        """
        
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

def EnviaJabber(TOJID):
    handler.log.error('enviando alerta por Jabber a ' + TOJID)
    try:
        txt = "Hola"
        jid  = xmpp.protocol.JID(XMPPUSER)
        jabber = xmpp.Client(jid.getDomain(), debug=[])
        connection = jabber.connect(('talk.google.com',5222))
        if not connection:
            raise IOError('no se pudo conectar a ' + XMPPCLIENT)
        jabber.auth(jid.getNode(), XMPPPASS, XMPPRESOURCE)
        if not jabber.auth:
            raise IOError('no se pudo autentificar con ' + XMPPCLIENT)
        jabber.sendInitPresence(requestRoster=1)
        jabber.send(xmpp.Message(TOJID ,txt))
    except Exception as message:
        handler.log.error('error al enviar alerta por Jabber')
        handler.log.exception(message) 

def EnviaSMS(TONUMBER):
    pass
    
def Valida():
    pass

def run():
    handler.log.info('iniciando modulo')

# main