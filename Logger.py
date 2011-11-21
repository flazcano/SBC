'''
Created on 23/10/2011

@author: Fernando

Sub-Modulo de Gestion de Logs
'''

# importaciones
from logging import getLogger, getLoggerClass, FileHandler, Formatter, StreamHandler
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL, FATAL #@UnusedImport
from sys import exit

# definiciones
logFile = 'sbc.log'

# clases
class handler(getLoggerClass()):
    try:
        log = getLogger("SBC")
        log.setLevel(DEBUG)

        # Formato en python 2.4+:
        formatter = Formatter(
            "%(asctime)s [%(module)-3s] %(levelname)-8s - %(message)s")
        # Formato en python 3.2+:
        # formatter = logging.Formatter(
        #     "{asctime} {threadName:>11} {levelname} {message}", style='{')
    
        # Log a archivo
        filehandler = FileHandler(logFile)
        filehandler.setLevel(DEBUG)
        filehandler.setFormatter(formatter)
        log.addHandler(filehandler)
    
        # Log a stdout
        streamhandler = StreamHandler()
        streamhandler.setLevel(DEBUG)
        streamhandler.setFormatter(formatter)
        log.addHandler(streamhandler)
    except IOError as message:
        print('no se puede escribir en ' + logFile)
        print(message)
        exit(1)
    except Exception as message:
        print('error al instanciar el log del SBC')
        print (message)
        exit(1)

# funciones

# main