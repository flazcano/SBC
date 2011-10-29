#!/usr/bin/env python

'''
Created on 23/10/2011

@author: Fernando

Sistema Balanceador de Carga
'''

import sys
from threading import Thread;
from Logger import handler;
import ME
import MIS

class ThreadxME(Thread):
        def __init__(self):
            Thread.__init__(self)

        def run(self):
            ME.run()

class ThreadxMIS(Thread):
        def __init__(self):
            Thread.__init__(self)

        def run(self):
            MIS.run()

if __name__ == '__main__':
    handler.log.info('iniciando SBC')
    
    try:
        tME = ThreadxME()
        tME.start()
    except Exception, (message):
        handler.log.error('ha ocurrido un error en el modulo')
        handler.log.exception(message)
        sys.exit(1);
    
    try:
        tMIS = ThreadxMIS()
        tMIS.start()
    except Exception, (message):
        handler.log.error('ha ocurrido un error en el modulo')
        handler.log.exception(message)
        sys.exit(1);
    
    
    