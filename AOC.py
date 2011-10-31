#!/usr/bin/env python

'''
Created on 29/10/2011

@author: Fernando

Agente de Obtencion de Cargas
'''

import Config, socket

from threading import Thread
from time import sleep

from Logger import handler
from modulo import AOCME

configFile = 'aoc.conf'
host = None
puerto = None
sbchost = None
sbcpuerto = None
sleeptime = 5

class ThreadxAOCME(Thread):
        def __init__(self):
            Thread.__init__(self)

        def run(self):
            AOCME.run(host, puerto)

if __name__ == '__main__':
    handler.log.info('iniciando el Agente de Obtencion de Cargas')
    
    # cargando configuraciones del agente
    try:
        cfg = Config.load(configFile)
        host = cfg["local_host"]
        puerto = int(cfg["local_puerto"])
        sbchost = cfg["sbc_host"]
        sbcpuerto = int(cfg["sbc_puerto"])
        
    except KeyError, (message):
        handler.log.error('no se ha podido encontrar la variable de configuracion necesaria: %s', message)
        exit(1);
    except IOError, (message):
        handler.log.error('ha ocurrido un error al cargar el archivo de configuracion: ' + configFile)
        handler.log.exception(message)
        exit(1);
    except Exception, (message):
        handler.log.error('ha ocurrido un error al cargar el archivo de configuracion: ' + configFile)
        handler.log.exception(message)
        exit(1);
    
    # ejecutando el modulo como hilo
    try: tAOCME = ThreadxAOCME().start()
    except Exception, (message):
        handler.log.error('ha ocurrido un error en el modulo')
        handler.log.exception(message)
        exit(1);
    else: handler.log.info('el Agente de Obtencion de Cargas se ha iniciado correctamente')
    
    # envia una notificacion al ME del SBC, para que este sepa que debe monitorizarme
    sinconexion = 1
    while sinconexion:
        try:
            sbcconexion = socket.socket()
            sbcconexion.connect((sbchost, sbcpuerto))
            sbcconexion.send('HELLO')  
        except Exception, (message):
            handler.log.error('no se ha podido conectar con SBC ' + sbchost + ':' + str(sbcpuerto) + ': %s', message)
            sleep(sleeptime)
        else:
            handler.log.info('conectado correctamente con SBC en: ' + sbchost + ':' + str(sbcpuerto))
            sinconexion = 0
        finally:
            if sbcconexion:
                sbcconexion.close()
    