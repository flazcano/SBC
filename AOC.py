#!/usr/bin/env python

'''
Created on 29/10/2011

@author: Fernando

Agente de Obtencion de Cargas
'''

# importaciones
from Config import Load
from threading import Thread
from Logger import setLOGFILE, setLOGLEVEL
from modulo import AOCMR, AOCME

# definiciones
CONFIGFILE = 'aoc.conf'
AOCHOST    = None
AOCPORT    = None
SBCHOST    = None
SBCPORT    = None

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
def setAOCHOST(VALUE):
    global AOCHOST; AOCHOST = VALUE
    handler.log.debug('AOCHOST        : ' + AOCHOST)

def setAOCPORT(VALUE):
    global AOCPORT; AOCPORT = VALUE
    handler.log.debug('AOCPORT        : ' + str(AOCPORT))
    
def setSBCHOST(VALUE):
    global SBCHOST; SBCHOST = VALUE
    handler.log.debug('SBCHOST        : ' + SBCHOST)
    
def setSBCPORT(VALUE):
    global SBCPORT; SBCPORT = VALUE
    handler.log.debug('SBCPORT        : ' + str(SBCPORT))
        
# cargando configuraciones del agente
try:
    cfg = Load(CONFIGFILE)
    LOGFILE = cfg["LOGFILE"]; setLOGFILE(LOGFILE)
    LOGLEVEL = cfg["LOGLEVEL"]; setLOGLEVEL(LOGLEVEL)
    from Logger import handler
    handler.log.info('cargando configuraciones')
    AOCHOST = cfg["AOCHOST"]; setAOCHOST(AOCHOST)
    AOCPORT = int(cfg["AOCPORT"]); setAOCPORT(AOCPORT)
    SBCHOST = cfg["SBCHOST"]; setSBCHOST(SBCHOST)
    SBCPORT = int(cfg["SBCPORT"]); setSBCPORT(SBCPORT)
    AOCMESLEEPTIME = cfg["AOCMESLEEPTIME"]; AOCME.setAOCMESLEEPTIME(AOCMESLEEPTIME)
    SBCTIMEOUT = int(cfg["SBCTIMEOUT"]); AOCME.setSBCTIMEOUT(SBCTIMEOUT)
    AOCMRSLEEPTIME = cfg["AOCMRSLEEPTIME"]; AOCMR.setAOCMRSLEEPTIME(AOCMRSLEEPTIME)
except KeyError as message:
    handler.log.critical('no se ha podido encontrar una variable de configuracion necesaria: %s', message)
    handler.log.exception(message)
    exit(1);
except Exception as message:
    handler.log.error('ha ocurrido un error al cargar el archivo de configuracion: ' + CONFIGFILE)
    handler.log.exception(message)
    exit(1);
else: handler.log.info('configuraciones cargadas correctamente')

# main
if __name__ == '__main__':
    handler.log.info('iniciando el agente')
    
    try: AOCMR.run()
    except Exception as message:
        handler.log.error('ha ocurrido un error al cargar el modulo AOCMR')
        handler.log.exception(message)
        exit(1);

    # ejecutando el modulo AOCME como hilo
    try: tAOCME = ThreadxAOCME(AOCHOST, AOCPORT).start()
    except Exception as message:
        handler.log.error('ha ocurrido un error al cargar el modulo AOCME')
        handler.log.exception(message)
        exit(1);
    
    handler.log.info('el agente se ha iniciado correctamente')
    
    # enviando keep alive a SBC
    try: tAgenteVivo = ThreadxAgenteVivo(SBCHOST, SBCPORT, AOCPORT).start()
    except Exception as message:
        handler.log.error('ha ocurrido un error al enviar signo de vida a SBC')
        handler.log.exception(message)
        exit(1);

    try:
        AOCMR.ObtieneCarga()
    except Exception as message:
        handler.log.error('ha ocurrido un error al obtener la carga del sistema')
        handler.log.exception(message)
        exit(1);
        