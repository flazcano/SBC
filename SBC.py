#!/usr/bin/env python

'''
Created on 23/10/2011

@author: Fernando

Sistema Balanceador de Carga
'''

# importaciones
from Config import Load
from sys import exit, argv
from threading import Thread;
from modulo import MC, MIS, MII, ME, MA, MIW
from Logger import setLOGFILE, setLOGLEVEL
try: from argparse import ArgumentParser #@UnresolvedImport
except: print 'no se encuentra python::argparse necesario para correr el SBC'; exit(1)

# definiciones
CONFIGFILE = 'sbc.conf'

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

class ThreadxModificaReglas(Thread):
        def __init__(self):
            Thread.__init__(self)
        def run(self):
            MII.ModificaReglas()
            
# funciones
def Valida():
    pass

# cargando configuraciones del sistema
try:
    cfg = Load(CONFIGFILE)
    LOGFILE = cfg["LOGFILE"]; setLOGFILE(LOGFILE)
    LOGLEVEL = cfg["LOGLEVEL"]; setLOGLEVEL(LOGLEVEL)
    from Logger import handler
    handler.log.info('cargando configuraciones desde ' + CONFIGFILE)
    SBCDB = cfg["SBCDB"]; MIS.setSBCDB(SBCDB)
    SBCDUMP = cfg["SBCDUMP"]; MIS.setSBCDUMP(SBCDUMP)
    INTENTOSSERVERDOWN = int(cfg["INTENTOSSERVERDOWN"]); MIS.setINTENTOSSERVERDOWN(INTENTOSSERVERDOWN)
    TABLA_CONFIGURACION = cfg["TABLA_CONFIGURACION"]; MIS.setTABLA_CONFIGURACION(TABLA_CONFIGURACION)
    TABLA_SERVIDOR = cfg["TABLA_SERVIDOR"]; MIS.setTABLA_SERVIDOR(TABLA_SERVIDOR)
    TABLA_CARGAS = cfg["TABLA_CARGAS"]; MIS.setTABLA_CARGAS(TABLA_CARGAS)
    TABLA_OPERADOR = cfg["TABLA_OPERADOR"]; MIS.setTABLA_OPERADOR(TABLA_OPERADOR)
    TABLA_ALERTA = cfg["TABLA_ALERTA"]; MIS.setTABLA_ALERTA(TABLA_ALERTA)
    IFACE = cfg["IFACE"]; MII.setIFACE(IFACE)
    IPSBC = cfg["IPSBC"]; MII.setIPSBC(IPSBC)
    PRECHAIN = cfg["PRECHAIN"]; MII.setPRECHAIN(PRECHAIN)
    POSTCHAIN = cfg["POSTCHAIN"]; MII.setPOSTCHAIN(POSTCHAIN)
    TABLENAME = cfg["TABLENAME"]; MII.setTABLENAME(TABLENAME)
    TARGETNAME = cfg["TARGETNAME"]; MII.setTARGETNAME(TARGETNAME)          
    IPINICIAL = cfg["IPINICIAL"]; MII.setIPINICIAL(IPINICIAL)   
    PUERTODEFECTO = int(cfg["PUERTODEFECTO"]); MII.setPUERTODEFECTO(PUERTODEFECTO)
    PROTOCOLODEFECTO = cfg["PROTOCOLODEFECTO"]; MII.setPROTOCOLODEFECTO(PROTOCOLODEFECTO)
    SLEEPREGLAMEJORSERVIDOR = int(cfg["SLEEPREGLAMEJORSERVIDOR"]); MII.setSLEEPREGLAMEJORSERVIDOR(SLEEPREGLAMEJORSERVIDOR)
    CLIENTTIMEOUT = int(cfg["CLIENTTIMEOUT"]); ME.setCLIENTTIMEOUT(CLIENTTIMEOUT)
    SLEEPSERVERACTIVOS = int(cfg["SLEEPSERVERACTIVOS"]); ME.setSLEEPSERVERACTIVOS
    SLEEPSERVERINACTIVOS = float(cfg["SLEEPSERVERINACTIVOS"]); ME.setSLEEPSERVERACTIVOS(SLEEPSERVERACTIVOS)
    BINDADDRESS = cfg["BINDADDRESS"]; ME.setBINDADDRESS(BINDADDRESS)
    MEPORT = int(cfg["MEPORT"]); ME.setMEPORT(MEPORT)
    SMTPHOST = cfg["SMTPHOST"]; MA.setSMTPHOST(SMTPHOST)
    SMTPPORT = int(cfg["SMTPPORT"]); MA.setSMTPPORT(SMTPPORT)
    SMTPUSER = cfg["SMTPUSER"]; MA.setSMTPUSER(SMTPUSER)
    SMTPPASS = cfg["SMTPPASS"]; MA.setSMTPPASS(SMTPPASS)
    SMTPDEBUGLEVEL = int(cfg["SMTPDEBUGLEVEL"]); MA.setSMTPDEBUGLEVEL(SMTPDEBUGLEVEL)
    XMPPCLIENT = cfg["XMPPCLIENT"]; MA.setXMPPCLIENT(XMPPCLIENT)
    XMPPHOST = cfg["XMPPHOST"]; MA.setXMPPHOST(XMPPHOST)
    XMPPRESOURCE = cfg["XMPPRESOURCE"]; MA.setXMPPRESOURCE(XMPPRESOURCE)
    XMPPPORT = int(cfg["XMPPPORT"]); MA.setXMPPPORT(XMPPPORT)
    XMPPUSER = cfg["XMPPUSER"]; MA.setXMPPUSER(XMPPUSER)
    XMPPPASS = cfg["XMPPPASS"]; MA.setXMPPPASS(XMPPPASS)
    DJANGOAPP = cfg["DJANGOAPP"]; MIW.setDJANGOAPP(DJANGOAPP)
    DJANGOBINDADDRESSS = cfg["DJANGOBINDADDRESSS"]; MIW.setDJANGOBINDADDRESSS(DJANGOBINDADDRESSS)
    DJANGOPORT = int(cfg["DJANGOPORT"]); MIW.setDJANGOPORT(DJANGOPORT)     
except KeyError as message:
    handler.log.critical('no se ha podido encontrar una variable de confifguracion necesaria: %s', message)
    handler.log.exception(message)
    exit(1);
except Exception as message:
    handler.log.error('ha ocurrido un error al cargar el archivo de configuracion: ' + CONFIGFILE)
    handler.log.exception(message)
    exit(1);
else: handler.log.info('configuraciones cargadas correctamente')

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

    # ejecutando el proceso de balance por reglas como hilo
    try: tModificaReglas = ThreadxModificaReglas().start()
    except Exception as message:
        handler.log.error('ha ocurrido un error al modificar las reglas de IPTABLES')
        handler.log.exception(message)
        exit(1);    