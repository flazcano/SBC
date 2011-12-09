'''
Created on 29/10/2011

@author: Fernando

Modulo de Interfaz Web (MIW)
'''

# importaciones
from os import popen
from Logger import handler


# definiciones
DJANGOAPP          = None
DJANGOBINDADDRESSS = None
DJANGOPORT         = None

# clases

# funciones
def LevantaDjango():
    try:
        handler.log.info('sincronizando esquema para django')
        #run('python ../MIW/manage.py syncdb')
    
        handler.log.info('iniciando servidor django para aplicacion %s', DJANGOAPP)
        popen("cd .. && sh MIW.sh " + DJANGOBINDADDRESSS + " " + str(DJANGOPORT))
    except Exception as message:
        handler.log.error('no se pudo levantar el servidor: %s', message)

def Valida():
    pass

def run():
    handler.log.info('iniciando modulo')
    LevantaDjango()

def setDJANGOAPP(VALUE):
    global DJANGOAPP; DJANGOAPP = VALUE
    handler.log.debug('DJANGOAPP: ' + DJANGOAPP)

def setDJANGOBINDADDRESSS(VALUE):
    global DJANGOBINDADDRESSS; DJANGOBINDADDRESSS = VALUE
    handler.log.debug('DJANGOBINDADDRESSS: ' + DJANGOBINDADDRESSS)

def setDJANGOPORT(VALUE):
    global DJANGOPORT; DJANGOPORT = VALUE
    handler.log.debug('DJANGOPORT: ' + str(DJANGOPORT))

# main
if __name__ == '__main__':
    run()