#!/usr/bin/env python

'''
Created on 23/10/2011

@author: Fernando

Sistema Balanceador de Carga
'''

from sys import exit
from threading import Thread;
from time import sleep

from modulo import MIS, ME
from Logger import handler;

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

if __name__ == '__main__':
    handler.log.info('iniciando el Sistema Balanceador de Carga')
    
    # ejecutando el modulo como hilo
    try: tMIS = ThreadxMIS().start()
    except Exception, (message):
        handler.log.error('ha ocurrido un error en el modulo')
        handler.log.exception(message)
        exit(1);
    
    # ejecutando el modulo como hilo
    try: tME = ThreadxME().start()
    except Exception, (message):
        handler.log.error('ha ocurrido un error en el modulo')
        handler.log.exception(message)
        exit(1);
    
    while 1:
        ME.consultaEstadoServidores()
        sleep(15)
    