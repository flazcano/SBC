#!/usr/bin/env python

'''
Created on 23/10/2011

@author: Fernando

Sistema Balanceador de Carga
'''

# importaciones
import argparse
from sys import exit, argv
from threading import Thread;
from modulo import MC, MIS, ME
from Logger import handler;

# definiciones

# clases
def usage():
    pass

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

class ThreadxObtieneEstadoServidores(Thread):
        def __init__(self):
            Thread.__init__(self)

        def run(self):
            ME.ObtieneEstadoServidores()

# funciones
def valida():
    pass

# main
if __name__ == '__main__':
    handler.log.info('iniciando el sistema SBC')
    
    # comprobando los argumentos pasados desde la linea de comando
    if argv[1:]:
        parser = argparse.ArgumentParser(description='Sistema Balanceador de Carga')
        parser.add_argument('-c', '--createdb', action='store_true', help='crea el esquema de la base de datos del SBC', type=MIS.creaEsquema())
        args = parser.parse_args()
        
    # ejecutando la funcion de validacion de modulos desde MC 
    try: MC.valida()
    except Exception as message:
        handler.log.error('ha ocurrido un error al validar los modulos del sistema: %s', message)
        exit(1)
    
    # ejecutando el modulo MIS como hilo
    try: tMIS = ThreadxMIS().start()
    except Exception as message:
        handler.log.error('ha ocurrido un error al cargar el modulo MIS')
        handler.log.exception(message)
        exit(1);
    
    # ejecutando el modulo ME como hilo
    try: tME = ThreadxME().start()
    except Exception as message:
        handler.log.error('ha ocurrido un error al cargar el modulo ME')
        handler.log.exception(message)
        exit(1);
        
    handler.log.info('el sistema se ha iniciado correctamente')
 
    # ejecutando el proceso de Obtencion de Estado de los Servidores como hilo
    try: tObtieneEstadoServidores = ThreadxObtieneEstadoServidores().start()
    except Exception as message:
        handler.log.error('ha ocurrido un error al obtener el estadode los servidores')
        handler.log.exception(message)
        exit(1);
