#!/usr/bin/env python

'''
Created on 23/10/2011

@author: Fernando

Sistema Balanceador de Carga
'''

# importaciones
from sys import exit, argv
from threading import Thread;
from modulo import MC, MIS, MII, ME
from Logger import handler;
try: from argparse import ArgumentParser #@UnresolvedImport
except: handler.log.critical('no se encuentra python::argparse necesario para correr el SBC'); exit(1)

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

class ThreadxMII(Thread):
        def __init__(self):
            Thread.__init__(self)
        def run(self):
            MII.run()

class ThreadxObtieneEstadoServidoresActivos(Thread):
        def __init__(self):
            Thread.__init__(self)
        def run(self):
            ME.ObtieneEstadoServidoresActivos()

class ThreadxObtieneEstadoServidoresInactivos(Thread):
        def __init__(self):
            Thread.__init__(self)
        def run(self):
            ME.ObtieneEstadoServidoresInactivos()
            
# funciones
def Valida():
    pass

# main
if __name__ == '__main__':
    handler.log.info('iniciando el sistema SBC')
    
    # comprobando los argumentos pasados desde la linea de comando
    if argv[1:]:
        parser = ArgumentParser(description='Sistema Balanceador de Carga')
        parser.add_argument('-c', '--createdb', action='store_true', help='crea el esquema de la base de datos del SBC', type=MIS.CreaEsquema())
        args = parser.parse_args()
        
    # ejecutando la funcion de validacion de modulos desde MC 
    try: MC.Valida()
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
    try: tMII = ThreadxMII().start()
    except Exception as message:
        handler.log.error('ha ocurrido un error al cargar el modulo MII')
        handler.log.exception(message)
        exit(1);
            
    # ejecutando el modulo ME como hilo
    try: tME = ThreadxME().start()
    except Exception as message:
        handler.log.error('ha ocurrido un error al cargar el modulo ME')
        handler.log.exception(message)
        exit(1);
        
    handler.log.info('el sistema se ha iniciado correctamente')
 
    # ejecutando el proceso de obtencion de estado de los servidores activos como hilo
    try: tObtieneEstadoServidoresActivos = ThreadxObtieneEstadoServidoresActivos().start()
    except Exception as message:
        handler.log.error('ha ocurrido un error al obtener el estado de los servidores activos')
        handler.log.exception(message)
        exit(1);
        
    # ejecutando el proceso de obtencion de estado de los servidores inactivos como hilo
    try: tObtieneEstadoServidoresInactivos = ThreadxObtieneEstadoServidoresInactivos().start()
    except Exception as message:
        handler.log.error('ha ocurrido un error al obtener el estado de los servidores inactivos')
        handler.log.exception(message)
        exit(1);
    