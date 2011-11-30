'''
Created on 29/10/2011

@author: Fernando

Modulo de Interfaz Web (MIW)
'''

# importaciones
from os import popen
from Logger import handler


# definiciones
DJANGOAPP="Web"
DJANGOADDRESSS="0.0.0.0"
DJANGOPORT=8080

# clases

# funciones
def LevantaDjango():
    try:
        handler.log.info('sincronizando esquema para django')
        #run('python ../MIW/manage.py syncdb')
    
        handler.log.info('iniciando servidor django para aplicacion %s', DJANGOAPP)
        popen("cd .. && sh MIW.sh " + DJANGOADDRESSS + " " + str(DJANGOPORT))
    except Exception as message:
        handler.log.error('no se pudo levantar el servidor: %s', message)

def Valida():
    pass

def run():
    handler.log.info('iniciando modulo')
    LevantaDjango()

# main
if __name__ == '__main__':
    run()