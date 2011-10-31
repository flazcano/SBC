#!/usr/bin/env python

'''
Created on 29/10/2011

@author: Fernando

Agente de Obtencion de Cargas
'''

# importaciones
import socket, Config
from time import sleep
from threading import Thread
from Logger import handler
from modulo import AOCMR, AOCME

# definiciones
configFile = 'aoc.conf'

# clases
class ThreadxAOCME(Thread):
        def __init__(self, HOST, PORT):
            Thread.__init__(self)
            self.HOST = HOST
            self.PORT = PORT

        def run(self):
            AOCME.run(self.HOST, self.PORT)

# funciones
HOST = None
PORT = None
SBCHOST = None
SBCPORT = None

# main
if __name__ == '__main__':
    handler.log.info('iniciando el agente')
    
    # cargando configuraciones del agente
    try:
        handler.log.info('cargando configuraciones')
        cfg = Config.load(configFile)
        LOG = cfg["LOG"]
        HOST = cfg["HOST"]
        PORT = int(cfg["PORT"])
        SBCHOST = cfg["SBCHOST"]
        SBCPORT = int(cfg["SBCPORT"])
        
    except KeyError, (message):
        handler.log.critical('no se ha podido encontrar una variable de confifguracion necesaria: %s', message)
        handler.log.exception(message)
        exit(1);
    except IOError, (message):
        handler.log.error('ha ocurrido un error al cargar el archivo de configuracion: ' + configFile)
        handler.log.exception(message)
        exit(1);
    except Exception, (message):
        handler.log.error('ha ocurrido un error al cargar el archivo de configuracion: ' + configFile)
        handler.log.exception(message)
        exit(1);
    else: handler.log.info('configuraciones cargadas correctamente')
    
    try: AOCMR.run()
    except Exception, (message):
        handler.log.error('ha ocurrido un error al cargar el modulo')
        handler.log.exception(message)
        exit(1);

    # ejecutando el modulo AOCME como hilo
    try: tAOCME = ThreadxAOCME(HOST, PORT).start()
    except Exception, (message):
        handler.log.error('ha ocurrido un error al cargar el modulo')
        handler.log.exception(message)
        exit(1);
    
    handler.log.info('el agente se ha iniciado correctamente')
    
    # enviando alive a SBC
    sinconexion = 1
    while sinconexion:
        try:
            handler.log.debug('enviando alive signal a SBC')
            sbccon = socket.socket()
            sbccon.connect((SBCHOST, SBCPORT))
            sbccon.send('HELLO')
        except Exception, (message):
            handler.log.error('no se pudo conectar al SBC: %s', message)
        else:
            handler.log.debug('alive signal enviado correctamente')
            sinconexion = 0
        finally:
            sleep(5)
    