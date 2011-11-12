'''
Created on 29/10/2011

@author: Fernando

Modulo de Integracion para IPTables (MII)
'''

# importaciones
from Logger import handler
try: import iptc #@UnresolvedImport
except: handler.log.critical('no se encuentra python-iptc necesario para correr el modulo MII'); exit(1)

# definiciones
IFACE = "eth0"
CHAINNAME = "INPUT"    # "PREROUTING"
TARGETNAME = "ACCEPT"  # "REDIRECT"

# clases

# funciones
def CreaRegla(IPORIGEN, IPDESTINO, PROTO, PUERTODESTINO):
    rule = iptc.Rule()
    #rule.org = IPORIGEN
    rule.dst = IPDESTINO
    rule.protocol = PROTO
    rule.in_interface = IFACE
    match = iptc.Match(rule, PROTO)
    match.dport = str(PUERTODESTINO)
    rule.add_match(match)
    target = iptc.Target(rule, TARGETNAME)
    rule.target = target
    chain = iptc.Chain(iptc.TABLE_NAT, CHAINNAME)
    target.reset()
    #target.to_ports = PUERTODESTINO
    rule.target = target
    
    chain.insert_rule(rule)
    chain.flush()

def EliminaRegla(IPORIGEN, IPDESTINO, PROTO, PUERTODESTINO):
    rule = iptc.Rule()
    # rule.org = IPORIGEN
    rule.dst = IPDESTINO
    rule.protocol = PROTO
    rule.in_interface = IFACE
    match = iptc.Match(rule, PROTO)
    match.dport = str(PUERTODESTINO)
    rule.add_match(match)
    target = iptc.Target(rule, TARGETNAME)
    rule.target = target
    chain = iptc.Chain(iptc.TABLE_NAT, CHAINNAME)
    
    chain.delete_rule(rule)
    chain.flush()
    # chain.delete()
    
def MuestraReglas():
    handler.log.info('mostrando reglas de IPTABLES: %s', CHAINNAME)
    chain = iptc.Chain(iptc.TABLE_NAT, CHAINNAME)
    for RULES in chain.rules:
        handler.log.debug(RULES.src, "-> %s L4: %s", RULES.dst, RULES.protocol)
        for MATCH in RULES.matches:
            handler.log.debug('MATCH: %s TARGET: %s', MATCH.name, RULES.target.name)

def Valida():
    try:
        handler.log.debug('creando CHAIN %s', CHAINNAME)
        chain = iptc.Chain(iptc.TABLE_NAT, CHAINNAME)
        iptc.TABLE_NAT.create_chain(chain)
    except IPTCError as message: #@UndefinedVariable
        handler.log.debug('borrando CHAIN %s, y creando nuevamente', CHAINNAME)
        chain = iptc.Chain(iptc.TABLE_NAT, CHAINNAME)
        chain.delete()
        iptc.TABLE_NAT.create_chain(chain)
    except Exception as message:
        handler.log.error('error al crear las reglas de IPTABLES')
        handler.log.exception(message)    
        exit(1)

def run():
    handler.log.info('iniciando modulo')
    handler.log.info('aplicando regla por defecto')
    MuestraReglas()
    CreaRegla("192.168.0.6", "192.168.0.2", "tcp", 9999)
    MuestraReglas()
    
# main
if __name__ == '__main__':
    run()
    