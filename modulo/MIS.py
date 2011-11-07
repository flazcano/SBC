"""
Created on 23/10/2011

@author: Fernando

Modulo de Integracion para SQLite3 (MIS)
"""

# importaciones
import sqlite3
from exceptions import Exception
from time import time
from sys import exit
from os import path
from Logger import handler

# definiciones
SBCDB = "sbc.db"
SBCDUMP = "sbc.sql"

conexion=sqlite3.connect(SBCDB, isolation_level=None)

# clases

# funciones
def CreaEsquema():
    try:
        handler.log.info('creando esquema en ' + SBCDB)
        fileSBCDUMP = open(SBCDUMP)
        ESQUEMA = fileSBCDUMP.read()
        conexion=sqlite3.connect(SBCDB, isolation_level=None)
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

        
def ConsultaListaServidores():
    try:
        handler.log.debug('consultando listado de servidores')
        conexion=sqlite3.connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        servidores = cursor.execute('SELECT fqdn, puerto FROM servidor WHERE activo = "TRUE";')
        return servidores
    except Exception as message:
        handler.log.error('no se puede obtener listado de servidores activos: %s', message)
        exit(1)

def ConsultaTotalServidores():
    try:
        handler.log.debug('consultando total de servidores activos')
        conexion=sqlite3.connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        total = cursor.execute('SELECT count(id) FROM servidor WHERE activo = "TRUE";')
        return total
    except Exception as message:
        handler.log.error('no se puede obtener total de servidores activos: %s', message)
        exit(1)

def AgregaServidor(fqdn, puerto):
    try:
        handler.log.debug('agregando servidor: ' + fqdn + ':' + str(puerto))
        conexion=sqlite3.connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        PUERTO = cursor.execute('SELECT puerto FROM servidor WHERE fqdn = ?;', ([fqdn])).fetchall()
        modificado = time()
        # si el servidor ya existe en la base de datos
        if PUERTO:
            # pero tiene distinto puerto al registrado
            if puerto is not str(PUERTO[0][0]):
                handler.log.debug('actualizando puerto de servidor existente, de ' + str(PUERTO[0][0])+ ' a ' + puerto)
                cursor.execute('UPDATE servidor SET puerto = ? WHERE fqdn = ?;', (puerto, fqdn))
                cursor.execute('UPDATE servidor SET modificado = ? WHERE fqdn = ?;', (modificado, fqdn))
        # si el servidor no existe
        else:
            handler.log.debug('agregando servidor nuevo: ' + fqdn + ':' + puerto)
            cursor.execute('INSERT INTO servidor (fqdn, puerto, activo, modificado) VALUES (?, ?, ?, ?);', (fqdn, puerto, 'TRUE', modificado))
    except Exception as message:
        handler.log.error('no se puede agregar servidor: %s', message)
        handler.log.exception(message)
        exit(1)

def AgregaLAV(fqdn, LAV):
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
        
        handler.log.debug('agregando LAV de ' + fqdn)
        conexion=sqlite3.connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        ID = cursor.execute('SELECT id FROM servidor WHERE fqdn = ?;', ([fqdn])).fetchall()
        servidorid = ID[0][0]
        cursor.execute('INSERT INTO cargas (servidorid, time_unix, cpu_total, cpu_cores, mem_total, mem_used, mem_free, mem_percent, io_read_count, io_write_count, io_read_bytes, io_write_bytes, io_read_time, io_write_time, net_bytes_sent, net_bytes_recv, net_packets_sent, net_packets_recv, hdd_device, hdd_total, hdd_used, hdd_free, hdd_percent) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', 
                        (servidorid, time_unix, cpu_total, cpu_cores, mem_total, mem_used, mem_free, mem_percent, io_read_count, io_write_count, io_read_bytes, io_write_bytes, io_read_time, io_write_time, net_bytes_sent, net_bytes_recv, net_packets_sent, net_packets_recv, hdd_device, hdd_total, hdd_used, hdd_free, hdd_percent))
    except Exception as message:
        handler.log.error('no se puede agregar LAV de cliente: %s', message)
        handler.log.exception(message)

def Valida():
    try:
        # comprobando que la db existe
        if not path.exists(SBCDB):
            raise ValueError("no existe la BD en " + path.abspath(SBCDB))
        
        # se conecta a la db
        conexion=sqlite3.connect(SBCDB, isolation_level=None)
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
        
    except Exception as message:
        handler.log.error('ha ocurrido un problema al validar la integridad del modulo: %s', message)
        handler.log.exception(message)
        exit(1)

def run():
    handler.log.info('iniciando modulo')

# main
if __name__ == '__main__':
    Valida()
