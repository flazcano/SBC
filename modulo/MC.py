'''
Created on 29/10/2011

@author: Fernando

Modulo de Configuracion (MC)
'''

# importaciones
from modulo import MIS, MII, ME, MIW, MA
from Logger import handler
from sys import exit

# definiciones

# clases

# funciones
def valida():
    handler.log.info('iniciando validacion de modulos')
    
    try:
        # validando MIS
        handler.log.debug('validando integridad de MIS')
        MIS.valida()
        
        # validando MII
        handler.log.debug('validando integridad de MII')
        MII.valida()
        
        # validando ME
        handler.log.debug('validando integridad de ME')
        ME.valida()
        
        # validando MIW
        handler.log.debug('validando integridad de MIW')
        MIW.valida()
        
        # validando MA
        handler.log.debug('validando integridad de MA')
        MA.valida()
    
        handler.log.info('validacion de los modulos finalizada')
    except Exception as message:
        handler.log.error('la validacion finalizo con problemas: %s', message)
        exit(1)

# main
if __name__ == '__main__':
    miValidacion = valida()