#!/usr/bin/env python

'''
Created on 29/10/2011

@author: Fernando

Agente de Obtencion de Cargas
'''

# importaciones
import Config
from threading import Thread
from Logger import handler
from modulo import AOCMR, AOCME

# definiciones
CONFIGFILE = 'aoc.conf'
HOST = None
PORT = None
SBCHOST = None
SBCPORT = None

# clases
class ThreadxAOCME(Thread):
        def __init__(self, HOST, PORT):
            Thread.__init__(self)
            self.HOST = HOST
            self.PORT = PORT

        def run(self):
            AOCME.run(self.HOST, self.PORT)

class ThreadxAgenteVivo(Thread):
        def __init__(self, SBCHOST, SBCPORT, PORT):
            Thread.__init__(self)
            self.SBCHOST = SBCHOST
            self.SBCPORT = SBCPORT
            self.PORT = PORT

        def run(self):
            AOCME.AgenteVivo(self.SBCHOST, self.SBCPORT, self.PORT)

# funciones

# main
if __name__ == '__main__':
    handler.log.info('iniciando el agente')
    
    # cargando configuraciones del agente
    try:
        handler.log.info('cargando configuraciones')
        cfg = Config.load(CONFIGFILE)
        LOG = cfg["LOG"]
        HOST = cfg["HOST"]
        PORT = int(cfg["PORT"])
        SBCHOST = cfg["SBCHOST"]
        SBCPORT = int(cfg["SBCPORT"])
        
    except KeyError as message:
        handler.log.critical('no se ha podido encontrar una variable de confifguracion necesaria: %s', message)
        handler.log.exception(message)
        exit(1);
    except Exception as message:
        handler.log.error('ha ocurrido un error al cargar el archivo de configuracion: ' + CONFIGFILE)
        handler.log.exception(message)
        exit(1);
    else: handler.log.info('configuraciones cargadas correctamente')
    
    try: AOCMR.run()
    except Exception as message:
        handler.log.error('ha ocurrido un error al cargar el modulo AOCMR')
        handler.log.exception(message)
        exit(1);

    # ejecutando el modulo AOCME como hilo
    try: tAOCME = ThreadxAOCME(HOST, PORT).start()
    except Exception as message:
        handler.log.error('ha ocurrido un error al cargar el modulo AOCME')
        handler.log.exception(message)
        exit(1);
    
    handler.log.info('el agente se ha iniciado correctamente')
    
    # enviando keep alive a SBC
    try: tAgenteVivo = ThreadxAgenteVivo(SBCHOST, SBCPORT, PORT).start()
    except Exception as message:
        handler.log.error('ha ocurrido un error al enviar signo de vida a SBC')
        handler.log.exception(message)
        exit(1);

    try:
        AOCMR.ObtieneLAV()
    except Exception as message:
        handler.log.error('ha ocurrido un error al obtener la carga del sistema')
        handler.log.exception(message)
        exit(1);
        
    