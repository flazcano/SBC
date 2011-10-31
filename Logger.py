'''
Created on 23/10/2011

@author: Fernando

Sub-Modulo de Gestion de Logs
'''

import logging

from sys import exit

logFile = 'sbc.log'

class handler(logging.getLoggerClass()):
    try:
        log = logging.getLogger("SBC")
        log.setLevel(logging.DEBUG)

        # Formato en python 2.4+:
        formatter = logging.Formatter(
            "%(asctime)s [%(module)-5s] %(levelname)-6s - %(message)s")
        # Formato en python 3.2+:
        # formatter = logging.Formatter(
        #     "{asctime} {threadName:>11} {levelname} {message}", style='{')
    
        # Log a archivo
        filehandler = logging.FileHandler(logFile)
        filehandler.setLevel(logging.DEBUG)
        filehandler.setFormatter(formatter)
        log.addHandler(filehandler)
    
        # Log a stdout
        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(logging.DEBUG)
        streamhandler.setFormatter(formatter)
        log.addHandler(streamhandler)
    except IOError, (message):
        print 'no se puede escribir en ' + logFile
        print message
        exit(1)
    except Exception, (message):
        print 'error al instanciar el log del SBC'
        print message
        exit(1)