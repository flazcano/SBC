'''
Created on 29/10/2011

@author: Fernando

Modulo de Configuracion (MC)
'''

# importaciones
from sys import exit
from Config import Load
from Logger import handler, setLOGFILE, setLOGLEVEL
from modulo import MIS, MII, ME, MIW, MA

# definiciones

# clases

# funciones
def CargaParametros(ConfigFile):
    # cargando configuraciones del sistema
    try:
        handler.log.info('cargando configuraciones desde ' + ConfigFile)
        cfg = Load(ConfigFile)
        LOGFILE = cfg["LOGFILE"]; setLOGFILE(LOGFILE)
        LOGLEVEL = cfg["LOGLEVEL"]; setLOGLEVEL(LOGLEVEL)
    
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
        SLEEPSERVERACTIVOS = int(cfg["SLEEPSERVERACTIVOS"]); ME.setSLEEPSERVERACTIVOS(SLEEPSERVERACTIVOS)
        SLEEPSERVERINACTIVOS = int(cfg["SLEEPSERVERINACTIVOS"]); ME.setSLEEPSERVERINACTIVOS(SLEEPSERVERINACTIVOS)
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
        handler.log.error('ha ocurrido un error al cargar el archivo de configuracion: ' + ConfigFile)
        handler.log.exception(message)
        exit(1);
    else: handler.log.info('configuraciones cargadas correctamente')

def Valida():
    handler.log.info('iniciando validacion de modulos')
    
    try:
        # validando MIS
        handler.log.debug('validando integridad de MIS')
        MIS.Valida()
        
        # validando MII
        handler.log.debug('validando integridad de MII')
        MII.Valida()
        
        # validando ME
        handler.log.debug('validando integridad de ME')
        ME.Valida()
        
        # validando MIW
        handler.log.debug('validando integridad de MIW')
        MIW.Valida()
        
        # validando MA
        handler.log.debug('validando integridad de MA')
        MA.Valida()
    
        handler.log.info('validacion de los modulos finalizada')
    except Exception as message:
        handler.log.error('la validacion finalizo con problemas: %s', message)
        exit(1)

# main
if __name__ == '__main__':
    miValidacion = Valida()