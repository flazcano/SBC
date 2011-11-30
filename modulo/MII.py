'''
Created on 29/10/2011

@author: Fernando

Modulo de Integracion para IPTables (MII)
'''

# importaciones
from Logger import handler
from sys import exit
from time import sleep
try: import iptc #@UnresolvedImport
except: handler.log.critical('no se encuentra python-iptc necesario para correr el modulo MII'); exit(1)
from modulo import MIS

# definiciones
IFACE = "eth0"
CHAINNAME = "PREROUTING"
TARGETNAME = "REDIRECT"
IPINICIAL = "192.168.0.2"
PUERTODEFECTO = 80             # puerto a redireccionar
PROTOCOLODEFECTO = "tcp"
ORIGENDEFECTO = "0.0.0.0/0.0.0.0"
SLEEPREGLAMEJORSERVIDOR = 30

# clases

# funciones
def CreaRegla(IPORIGEN, IPDESTINO, PROTO, PUERTODESTINO):
    handler.log.info('creando regla: ' + IPORIGEN + ':' + str(PUERTODESTINO) + ' -> ' + IPDESTINO + ':' + str(PUERTODESTINO) + ' ' + PROTO)
    try:
        # se crea la regla
        rule = iptc.Rule()
        # IP de origen de la peticion
        rule.src = IPORIGEN
        # IP hacia donde se envia la peticion, un servidor balanceado
        rule.dst = IPDESTINO
        # PROTOCOLO de transmicion, suele ser TCP
        rule.protocol = PROTO
        # INTERFAS FISICA DE RED que realiza el enrutamiento
        rule.in_interface = IFACE
        
        # regla
        match = iptc.Match(rule, PROTO)
        # PUERTO hacia donde va la peticion
        match.dport = str(PUERTODESTINO)
        rule.add_match(match)
        
        # objetivo de la regla, DNAT o NAT Dinamico
        target = iptc.Target(rule, TARGETNAME)
        rule.target = target
        
        # cadena a utilizar, siempre se utiliza PRERUTEO para el DNAT
        chain = iptc.Chain(iptc.TABLE_NAT, CHAINNAME)
        target.reset()
        # IP y PUERTO a donde redirigir la peticion
        target.to_ports = str(PUERTODESTINO)
        rule.target = target
        chain.insert_rule(rule)
        handler.log.info('regla aplicada correctamente')
    except Exception as message:
            handler.log.error('no se pudo crear la regla')
            handler.log.exception(message)


def EliminaRegla(IPORIGEN, IPDESTINO, PROTO, PUERTODESTINO):
    handler.log.info('eliminando regla: ' + IPORIGEN + ':' + str(PUERTODESTINO) + ' -> ' + IPDESTINO + ':' + str(PUERTODESTINO) + ' ' + PROTO)
    try:
        # se crea la regla
        rule = iptc.Rule()
        # IP de origen de la peticion
        rule.src = IPORIGEN
        # IP hacia donde se envia la peticion, un servidor balanceado
        rule.dst = IPDESTINO
        # INTERFAS FISICA DE RED que realiza el enrutamiento
        rule.protocol = PROTO
        # INTERFAS FISICA DE RED que realiza el enrutamiento
        rule.in_interface = IFACE
        
        # regla
        match = iptc.Match(rule, PROTO)
        # PUERTO hacia donde va la peticion
        match.dport = str(PUERTODESTINO)
        rule.add_match(match)
        
        # objetivo de la regla, DNAT o NAT Dinamico
        target = iptc.Target(rule, TARGETNAME)
        rule.target = target
        
        # cadena a utilizar, siempre se utiliza PRERUTEO para el DNAT
        chain = iptc.Chain(iptc.TABLE_NAT, CHAINNAME)
        target.reset()
        # IP y PUERTO a donde redirigir la peticion
        target.to_ports = str(PUERTODESTINO)
        rule.target = target
        chain.delete_rule(rule)
        handler.log.info('regla eliminada correctamente')
    except Exception as message:
            handler.log.error('no se pudo eliminar la regla')
            handler.log.exception(message)
    
def MuestraReglas():
    handler.log.info('mostrando reglas: %s', CHAINNAME)
    try:
        chain = iptc.Chain(iptc.TABLE_NAT, CHAINNAME)
        for r in chain.rules:
            #print r.src, "->", r.dst, "L4:", r.protocol,
            for m in r.matches:
                #print "match:", m.name,
                #print "target:", r.target.name
                handler.log.debug(r.src + ' -> ' + r.dst + ' L4: ' + r.protocol + ' match: ' + m.name + ' target: ' + r.target.name)
    except Exception as message:
            handler.log.error('error al obtener las reglas')
            handler.log.exception(message)

def LimpiaReglas():
    handler.log.info('limpiando reglas: %s', CHAINNAME)
    try:
        chain = iptc.Chain(iptc.TABLE_NAT, CHAINNAME)
        chain.flush()
        handler.log.info('las reglas fueron limpiadas')
    except Exception as message:
            handler.log.error('error al limpiar las reglas')
            handler.log.exception(message)  

def ReglaInicial():
    handler.log.info('aplicando regla por defecto')
    CreaRegla(ORIGENDEFECTO, IPINICIAL, PROTOCOLODEFECTO, PUERTODEFECTO)

def ReglasEspeciales():
    pass

def ModificaReglas():
    obtieneMejorServidor = 1
    while obtieneMejorServidor:
        try:
            handler.log.info('obteniendo mejor servidor para reglas de IPTABLES')
            DESTINO = MIS.ConsultaMejorServidor()
            LimpiaReglas()
            if DESTINO:
                handler.log.info('modificando reglas de IPTABLES con mejor servidor %s', DESTINO)
                CreaRegla(ORIGENDEFECTO, DESTINO, PROTOCOLODEFECTO, PUERTODEFECTO)
            else:
                handler.log.info('modificando reglas de IPTABLES con servidor por defecto')
                ReglaInicial()
            handler.log.info('aplicando reglas especiales en IPTABLES')
            #ReglasEspeciales()
        except Exception as message:
            handler.log.error('error al aplicar la reglas en IPTABLES')
            handler.log.exception(message)
        finally:
            #MuestraReglas()
            sleep(SLEEPREGLAMEJORSERVIDOR)

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
    
# main
if __name__ == '__main__':
    run()
    