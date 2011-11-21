"""
Created on 23/10/2011

@author: Fernando

Modulo de Integracion para SQLite3 (MIS)
"""

# importaciones
from sqlite3 import connect  #@UnusedImport
from exceptions import Exception
from time import time
from os import path
from Logger import handler
from sys import exit

# definiciones
SBCDB = "sbc.db"
SBCDUMP = "sbc.sql"
NUMEROINTENTOS = 3
# conexion = connect(SBCDB, isolation_level=None)

# clases

# funciones
def CreaEsquema():
    try:
        handler.log.info('creando esquema en ' + SBCDB)
        fileSBCDUMP = open(SBCDUMP)
        ESQUEMA = fileSBCDUMP.read()
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        for sql in ESQUEMA.split(";"):
            cursor.execute(sql)
        handler.log.info('esquema creado correctamente')
        exit(0)
    except Exception as message:
        handler.log.error('no se puede crear esquema de ' + SBCDB + ': %s', message)
        exit(1)
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

        
def ConsultaServidoresActivos():
    try:
        handler.log.debug('consultando servidores activos')
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        servidores = cursor.execute('SELECT fqdn, puerto FROM servidor WHERE activo = "TRUE";')
        return servidores
    except Exception as message:
        handler.log.error('no se puede obtener servidores activos: %s', message)
        exit(1)

def ConsultaServidoresInactivos():
    try:
        handler.log.debug('consultando servidores inactivos')
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        servidores = cursor.execute('SELECT fqdn, puerto FROM servidor WHERE activo = "FALSE";')
        return servidores
    except Exception as message:
        handler.log.error('no se puede obtener servidores inactivos: %s', message)
        exit(1)

def ConsultaTotalServidoresActivos():
    try:
        handler.log.debug('consultando total de servidores activos')
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        total = cursor.execute('SELECT count(id) FROM servidor WHERE activo = "TRUE";')
        return total
    except Exception as message:
        handler.log.error('no se puede obtener total de servidores activos: %s', message)
        exit(1)

def ConsultaTotalServidoresInactivos():
    try:
        handler.log.debug('consultando total de servidores inactivos')
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        total = cursor.execute('SELECT count(id) FROM servidor WHERE activo = "FALSE";')
        return total
    except Exception as message:
        handler.log.error('no se puede obtener total de servidores inactivos: %s', message)
        exit(1)

def AgregaServidor(FQDN, PUERTO):
    try:
        handler.log.debug('agregando servidor: ' + FQDN + ':' + str(PUERTO))
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        PUERTO = cursor.execute('SELECT puerto FROM servidor WHERE fqdn = ?;', ([FQDN])).fetchall()
        MODIFICADO = time()
        # si el servidor ya existe en la base de datos
        if PUERTO:
            # pero tiene distinto puerto al registrado
            if PUERTO is not str(PUERTO[0][0]):
                handler.log.debug('actualizando puerto de servidor existente, de ' + str(PUERTO[0][0]) + ' a ' + PUERTO)
                cursor.execute('UPDATE servidor SET puerto = ? WHERE fqdn = ?;', (PUERTO, FQDN))
                cursor.execute('UPDATE servidor SET modificado = ? WHERE fqdn = ?;', (MODIFICADO, FQDN))
            cursor.execute('UPDATE servidor SET activo = ? WHERE fqdn = ?;', ('TRUE', FQDN))
        # si el servidor no existe
        else:
            handler.log.debug('agregando servidor nuevo: ' + FQDN + ':' + PUERTO)
            cursor.execute('INSERT INTO servidor (fqdn, puerto, activo, modificado) VALUES (?, ?, ?, ?);', (FQDN, PUERTO, 'TRUE', MODIFICADO))
    except Exception as message:
        handler.log.error('no se puede agregar servidor: %s', message)
        handler.log.exception(message)
        exit(1)

def ServidorVuelveActivo(FQDN, PUERTO):
    try:
        handler.log.debug('servidor vuelve a actividad: ' + FQDN + ':' + str(PUERTO))
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        cursor.execute('UPDATE servidor SET activo = ? WHERE fqdn = ?;', ('TRUE', FQDN))
    except Exception as message:
        handler.log.error('no se puede agregar servidor: %s', message)
        handler.log.exception(message)
        exit(1)


def AgregaLAV(FQDN, LAV):
    try:
        miLAV = LAV.split(" "); handler.log.debug('LAV: ' + LAV)
        
        # obtiene HORA
        HORA = None; HORA = str(miLAV[0]); handler.log.debug('HORA: ' + HORA)
        time_unix = HORA
        
        # obtiene CPU
        CPU = None; CPU = str(miLAV[1]); handler.log.debug('CPU: ' + CPU)
        cpu_total = None
        cpu_cores = None
        
        # obtiene MEM
        MEM = None; MEM = str(miLAV[2]); handler.log.debug('MEM: ' + MEM)
        mem_total = None
        mem_used = None
        mem_free = None
        mem_percent = None
        
        # obtiene IO
        IO = None; IO = str(miLAV[3]); handler.log.debug('IO: ' + IO)
        io_read_count = None
        io_write_count = None
        io_read_bytes = None
        io_write_bytes = None
        io_read_time = None
        io_write_time = None
        
        # obtiene NET
        NET = None; NET = str(miLAV[4]); handler.log.debug('NET: ' + NET)
        net_bytes_sent = None
        net_bytes_recv = None
        net_packets_sent = None
        net_packets_recv = None
        
        # obtiene HDD
        HDD = None; HDD = str(miLAV[5]); handler.log.debug('HDD: ' + HDD)
        hdd_device = None
        hdd_total = None
        hdd_used = None
        hdd_free = None
        hdd_percent = None
        
        handler.log.debug('agregando LAV de ' + FQDN)
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        ID = cursor.execute('SELECT id FROM servidor WHERE fqdn = ?;', ([FQDN])).fetchall()
        servidorid = ID[0][0]
        cursor.execute('INSERT INTO cargas (servidorid, time_unix, cpu_total, cpu_cores, mem_total, mem_used, mem_free, mem_percent, io_read_count, io_write_count, io_read_bytes, io_write_bytes, io_read_time, io_write_time, net_bytes_sent, net_bytes_recv, net_packets_sent, net_packets_recv, hdd_device, hdd_total, hdd_used, hdd_free, hdd_percent) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', 
                        (servidorid, time_unix, cpu_total, cpu_cores, mem_total, mem_used, mem_free, mem_percent, io_read_count, io_write_count, io_read_bytes, io_write_bytes, io_read_time, io_write_time, net_bytes_sent, net_bytes_recv, net_packets_sent, net_packets_recv, hdd_device, hdd_total, hdd_used, hdd_free, hdd_percent))
    except Exception as message:
        handler.log.error('no se puede agregar LAV de cliente: %s', message)
        handler.log.exception(message)

def ServidorConProblemas(FQDN, PUERTO):
    try:
        handler.log.debug('servidor con problemas: ' + FQDN + ':' + str(PUERTO))
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        INTENTO = cursor.execute('SELECT intento FROM servidor WHERE fqdn = ?;', ([FQDN])).fetchall()
        MODIFICADO = time()
        if INTENTO:
            # si se ha intentado menos de NUMEROINTENTOS veces consultar el servidor
            if INTENTO < NUMEROINTENTOS:
                handler.log.debug('actualizando intentos con problemas de servidor a ' + (INTENTO + 1))
                cursor.execute('UPDATE servidor SET intento = ? WHERE fqdn = ?;', ((INTENTO + 1), FQDN))
                cursor.execute('UPDATE servidor SET modificado = ? WHERE fqdn = ?;', (MODIFICADO, FQDN))
            # si se ha intentado menos de NUMEROINTENTOS veces consultar el servidor
            else:
                handler.log.debug('actualizando a inactivo estado de servidor')
                cursor.execute('UPDATE servidor SET activo = ? WHERE fqdn = ?;', ('FALSE', FQDN))
                cursor.execute('UPDATE servidor SET modificado = ? WHERE fqdn = ?;', (MODIFICADO, FQDN))
    except Exception as message:
        handler.log.error('no se puede modificar estado de servidor: %s', message)
        handler.log.exception(message)
        exit(1)


def Valida():
    try:
        # comprobando que la db existe
        if not path.exists(SBCDB):
            raise ValueError("no existe la BD en " + path.abspath(SBCDB))
        
        # se conecta a la db
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        
        # comprobando tabla configuracion
        tabla = 'configuracion'
        cont = cursor.execute('pragma table_info(configuracion);').fetchall()
        if cont: handler.log.debug('la tabla %s parece bien', tabla)
        else:
            raise ValueError, "no existe la tabla " + tabla
        
        # comprobando tabla servidor
        tabla = 'servidor'
        cont = cursor.execute('pragma table_info(servidor);').fetchall()
        if cont: handler.log.debug('la tabla %s parece bien', tabla)
        else:
            raise ValueError("no existe la tabla " + tabla)
            
        # comprobando tabla cargas
        tabla = 'cargas'
        cont = cursor.execute('pragma table_info(cargas);').fetchall()
        if cont: handler.log.debug('la tabla %s parece bien', tabla)
        else:
            raise ValueError("no existe la tabla " + tabla)
        
        # comprobando tabla operador
        tabla = 'operador'
        cont = cursor.execute('pragma table_info(operador);').fetchall()
        if cont: handler.log.debug('la tabla %s parece bien', tabla)
        else:
            raise ValueError("no existe la tabla " + tabla)
        
        # comprobando tabla alerta
        tabla = 'alerta'
        cont = cursor.execute('pragma table_info(alerta);').fetchall()
        if cont: handler.log.debug('la tabla %s parece bien', tabla)
        else:
            raise ValueError("no existe la tabla " + tabla)
        
    except Exception as message:
        handler.log.error('ha ocurrido un problema al validar la integridad del modulo: %s', message)
        handler.log.exception(message)
        exit(1)

def run():
    handler.log.info('iniciando modulo')

# main
if __name__ == '__main__':
    Valida()
