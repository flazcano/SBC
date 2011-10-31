#!/usr/bin/env python

'''
Created on 29/10/2011

@author: Fernando

Agente de Obtencion de Cargas
'''

import Config

from threading import Thread

from Logger import handler
from modulo import AOCME

configFile = 'aoc.conf'

class ThreadxAOCME(Thread):
        def __init__(self):
            Thread.__init__(self)

        def run(self):
            AOCME.run(puerto)

if __name__ == '__main__':
    handler.log.info('iniciando el Agente de Obtencion de Cargas')
    
    # cargando configuraciones del agente
    try:
        cfg = Config.load(configFile)
        puerto = cfg["puerto"]
    except KeyError, (message):
        handler.log.error('no se ha podido encontrar una variable de confifguracion necesaria')
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
    
    # ejecutando el modulo como hilo
    try: tAOCME = ThreadxAOCME().start(puerto)
    except Exception, (message):
        handler.log.error('ha ocurrido un error en el modulo')
        handler.log.exception(message)
        exit(1);
    else: handler.log.info('el Agente de Obtencion de Cargas se ha iniciado correctamente')