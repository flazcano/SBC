'''
Created on 29/10/2011

@author: Fernando

Modulo de Integracion para IPTables (MII)

es necesario tener cargados los modulos:

modprobe ip_conntrack
modprobe ip_conntrack_ftp
modprobe iptable_nat
'''

# importaciones
from sys import exit
from time import sleep
from commands import getoutput as execute
from Logger import handler
from modulo import MIS

# definiciones
IFACE                   = None
IPSBC                   = None
PRECHAIN                = None
POSTCHAIN               = None
TABLENAME               = None
TARGETNAME              = None
IPINICIAL               = None
PUERTODEFECTO           = None # puerto a redireccionar
PROTOCOLODEFECTO        = None
SLEEPREGLAMEJORSERVIDOR = None

# clases

# funciones
def CreaRegla(IPORIGEN, IPDESTINO, PROTO, PUERTODESTINO):
    handler.log.info('creando regla: ' + IPORIGEN + ':' + str(PUERTODESTINO) + ' -> ' + IPDESTINO + ':' + str(PUERTODESTINO) + ' ' + PROTO)
    try:
        EXEC='iptables -t ' + TABLENAME + ' -A ' + PRECHAIN + ' -p ' + PROTO + ' -s 0/0 -d ' + IPSBC + ' --dport ' + str(PUERTODESTINO) + ' -j DNAT --to ' + IPDESTINO + ':' + str(PUERTODESTINO)
        STATUS = execute(EXEC)
        handler.log.debug('ejecutado: %s STATUS %s', EXEC, STATUS)
        
        EXEC='iptables -t ' + TABLENAME + ' -A ' + POSTCHAIN + ' -o ' + IFACE + ' -d ' + IPDESTINO + ' -j SNAT --to-source ' + IPSBC
        STATUS = execute(EXEC)
        handler.log.debug('ejecutado: %s STATUS %s', EXEC, STATUS)
        
        handler.log.info('regla aplicada correctamente')
    except Exception as message:
            handler.log.error('no se pudo crear la regla')
            handler.log.exception(message)

def EliminaRegla(IPORIGEN, IPDESTINO, PROTO, PUERTODESTINO):
    handler.log.info('eliminando regla: ' + IPORIGEN + ':' + str(PUERTODESTINO) + ' -> ' + IPDESTINO + ':' + str(PUERTODESTINO) + ' ' + PROTO)
    try:
        EXEC='iptables -t ' + TABLENAME + ' -D ' + PRECHAIN + ' -p ' + PROTO + ' -s 0/0 -d ' + IPSBC + ' --dport ' + str(PUERTODESTINO) + ' -j DNAT --to ' + IPDESTINO + ':' + str(PUERTODESTINO)
        STATUS = execute(EXEC)
        handler.log.debug('ejecutado: %s STATUS %s', EXEC, STATUS)
        
        EXEC='iptables -t ' + TABLENAME + ' -D ' + POSTCHAIN + ' -o ' + IFACE + ' -d ' + IPDESTINO + ' -j SNAT --to-source ' + IPSBC
        STATUS = execute(EXEC)
        handler.log.debug('ejecutado: %s STATUS %s', EXEC, STATUS)
        handler.log.info('regla eliminada correctamente')
    except Exception as message:
            handler.log.error('no se pudo eliminar la regla')
            handler.log.exception(message)
    
def MuestraReglas():
    handler.log.info('mostrando reglas: %s', PRECHAIN)
    try:
        EXEC='iptables -t ' + TABLENAME + ' -nvL'
        STATUS = execute(EXEC)
        handler.log.debug('ejecutado: %s STATUS %s', EXEC, STATUS)
    except Exception as message:
            handler.log.error('error al obtener las reglas')
            handler.log.exception(message)

def LimpiaReglas():
    handler.log.info('limpiando reglas: %s', PRECHAIN)
    try:
        EXEC='iptables -t ' + TABLENAME + ' -F '
        STATUS = execute(EXEC)
        handler.log.debug('ejecutado: %s STATUS %s', EXEC, STATUS)
        
        
        EXEC='iptables -t ' + TABLENAME + ' -F ' + PRECHAIN
        STATUS = execute(EXEC)
        handler.log.debug('ejecutado: %s STATUS %s', EXEC, STATUS)
        
        EXEC='iptables -t ' + TABLENAME + ' -F ' + POSTCHAIN
        STATUS = execute(EXEC)
        handler.log.debug('ejecutado: %s STATUS %s', EXEC, STATUS)
        
        handler.log.info('las reglas fueron limpiadas')
    except Exception as message:
            handler.log.error('error al limpiar las reglas')
            handler.log.exception(message)  

def ReglaInicial():
    handler.log.info('aplicando regla por defecto')
    CreaRegla(IPSBC, IPINICIAL, PROTOCOLODEFECTO, PUERTODEFECTO)

def ReglasEspeciales():
    handler.log.info('aplicando reglas especiales')

def ModificaReglas():
    obtieneMejorServidor = 1
    while obtieneMejorServidor:
        try:
            ReglasEspeciales()
            handler.log.info('obteniendo mejor servidor para reglas de IPTABLES')
            DESTINO = MIS.ConsultaMejorServidor()
            handler.log.debug('mejor servidor: ' + str(DESTINO))
            LimpiaReglas()
            if str(DESTINO) == 'None':
                handler.log.info('modificando reglas de IPTABLES con servidor por defecto')
                ReglaInicial()
            else:
                handler.log.info('modificando reglas de IPTABLES con mejor servidor %s', DESTINO)
                CreaRegla(IPSBC, DESTINO, PROTOCOLODEFECTO, PUERTODEFECTO)
            handler.log.info('aplicando reglas especiales en IPTABLES')
            #ReglasEspeciales()
        except Exception as message:
            handler.log.error('error al aplicar la reglas en IPTABLES')
            handler.log.exception(message)
        finally:
            #MuestraReglas()
            sleep(float(SLEEPREGLAMEJORSERVIDOR))

def Valida():
    try:
        LimpiaReglas()
        ReglaInicial()
    except Exception as message:
        handler.log.error('error al validar IPTABLES')
        handler.log.exception(message)
        exit(1)

def run():
    handler.log.info('iniciando modulo')

def setIFACE(VALUE):
    global IFACE; IFACE = VALUE
    handler.log.debug('IFACE: ' + IFACE)

def setIPSBC(VALUE):
    global IPSBC; IPSBC = VALUE
    handler.log.debug('IPSBC: ' + IPSBC)

def setPRECHAIN(VALUE):
    global PRECHAIN; PRECHAIN = VALUE
    handler.log.debug('PRECHAIN: ' + PRECHAIN)

def setPOSTCHAIN(VALUE):
    global POSTCHAIN; POSTCHAIN = VALUE
    handler.log.debug('POSTCHAIN: ' + POSTCHAIN)

def setTABLENAME(VALUE):
    global TABLENAME; TABLENAME = VALUE
    handler.log.debug('TABLENAME: ' + TABLENAME)

def setTARGETNAME(VALUE):
    global TARGETNAME; TARGETNAME = VALUE
    handler.log.debug('TARGETNAME: ' + TARGETNAME)

def setIPINICIAL(VALUE):
    global IPINICIAL; IPINICIAL = VALUE
    handler.log.debug('IPINICIAL: ' + IPINICIAL)

def setPUERTODEFECTO(VALUE):
    global PUERTODEFECTO; PUERTODEFECTO = VALUE
    handler.log.debug('PUERTODEFECTO: ' + str(PUERTODEFECTO))

def setPROTOCOLODEFECTO(VALUE):
    global PROTOCOLODEFECTO; PROTOCOLODEFECTO = VALUE
    handler.log.debug('PROTOCOLODEFECTO: ' + PROTOCOLODEFECTO)

def setSLEEPREGLAMEJORSERVIDOR(VALUE):
    global SLEEPREGLAMEJORSERVIDOR; SLEEPREGLAMEJORSERVIDOR = VALUE
    handler.log.debug('SLEEPREGLAMEJORSERVIDOR: ' + str(SLEEPREGLAMEJORSERVIDOR))

# main
if __name__ == '__main__':
    run()
    