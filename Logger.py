#!/usr/bin/env python

'''
Created on 23/10/2011

@author: Fernando

Sub Modulo de gestion de Logs
'''

import logging

class handler(logging.getLoggerClass()):
    log = logging.getLogger("Logger")
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s [%(module)-3s] %(levelname)-8s - %(message)s")
    # Alternative formatting available on python 3.2+:
    # formatter = logging.Formatter(
    #     "{asctime} {threadName:>11} {levelname} {message}", style='{')

    # Log to file
    filehandler = logging.FileHandler("sbc.log")
    filehandler.setLevel(logging.DEBUG)
    filehandler.setFormatter(formatter)
    log.addHandler(filehandler)

    # Log to stdout too
    streamhandler = logging.StreamHandler()
    streamhandler.setLevel(logging.DEBUG)
    streamhandler.setFormatter(formatter)
    log.addHandler(streamhandler)