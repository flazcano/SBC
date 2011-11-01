#!/usr/bin/env python

'''
Created on 23/10/2011

@author: Fernando

Sistema Balanceador de Carga
'''

# importaciones
from time import sleep
from sys import exit
from threading import Thread;
from modulo import MC, MIS, ME
from Logger import handler;

# definiciones

# clases
class ThreadxMIS(Thread):
        def __init__(self):
            Thread.__init__(self)

        def run(self):
            MIS.run()

class ThreadxME(Thread):
        def __init__(self):
            Thread.__init__(self)

        def run(self):
            ME.run()

# funciones
def valida():
    pass

# main
if __name__ == '__main__':
    handler.log.info('iniciando el sistema SBC')
    
    try: MC.valida()
    except Exception as message:
        handler.log.error('ha ocurrido un error al validar los modulos del sistema: %s', message)
        exit(1)
    
    # ejecutando el modulo como hilo
    try: tMIS = ThreadxMIS().start()
    except Exception as message:
        handler.log.error('ha ocurrido un error al cargar el modulo')
        handler.log.exception(message)
        exit(1);
    
    # ejecutando el modulo como hilo
    try: tME = ThreadxME().start()
    except Exception as message:
        handler.log.error('ha ocurrido un error al cargar el modulo')
        handler.log.exception(message)
        exit(1);
        
    handler.log.info('el sistema se ha iniciado correctamente')
 
    obtenerestado = 1
    while obtenerestado:
        ME.obtieneEstadoServidores()
        sleep(20)
