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
SBCDB = "MIW/sbc.db"
SBCDUMP = "sbc.sql"
NUMEROINTENTOS = 3
TABLA_CONFIGURACION = "Web_configuracion"
TABLA_SERVIDOR = "Web_servidor"
TABLA_CARGAS = "Web_cargas"
TABLA_OPERADOR = "Web_operador"
TABLA_ALERTA = "Web_alerta"

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
        servidores = cursor.execute('SELECT fqdn, puerto FROM ' + TABLA_SERVIDOR + ' WHERE activo = "TRUE";')
        return servidores
    except Exception as message:
        handler.log.error('no se puede obtener servidores activos: %s', message)
        exit(1)

def ConsultaServidoresInactivos():
    try:
        handler.log.debug('consultando servidores inactivos')
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        servidores = cursor.execute('SELECT fqdn, puerto FROM ' + TABLA_SERVIDOR + ' WHERE activo = "FALSE";')
        return servidores
    except Exception as message:
        handler.log.error('no se puede obtener servidores inactivos: %s', message)
        exit(1)

def ConsultaTotalServidoresActivos():
    try:
        handler.log.debug('consultando total de servidores activos')
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        total = cursor.execute('SELECT count(id) FROM ' + TABLA_SERVIDOR + ' WHERE activo = "TRUE";')
        return total
    except Exception as message:
        handler.log.error('no se puede obtener total de servidores activos: %s', message)
        exit(1)

def ConsultaTotalServidoresInactivos():
    try:
        handler.log.debug('consultando total de servidores inactivos')
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        total = cursor.execute('SELECT count(id) FROM ' + TABLA_SERVIDOR + ' WHERE activo = "FALSE";')
        return total
    except Exception as message:
        handler.log.error('no se puede obtener total de servidores inactivos: %s', message)
        exit(1)

def AgregaServidor(FQDN, PUERTO):
    try:
        handler.log.debug('agregando servidor: ' + FQDN + ':' + str(PUERTO))
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        PUERTODB = cursor.execute('SELECT puerto FROM ' + TABLA_SERVIDOR + ' WHERE fqdn = ?;', ([FQDN])).fetchall()
        MODIFICADO = time()
        # si el servidor ya existe en la base de datos
        if PUERTODB:
            # pero tiene distinto puerto al registrado
            if PUERTO is not str(PUERTODB[0][0]):
                handler.log.debug('actualizando puerto de servidor existente, de ' + str(PUERTODB[0][0]) + ' a ' + PUERTO)
                cursor.execute('UPDATE ' + TABLA_SERVIDOR + ' SET puerto = ? WHERE fqdn = ?;', (PUERTO, FQDN))
                cursor.execute('UPDATE ' + TABLA_SERVIDOR + ' SET modificado = ? WHERE fqdn = ?;', (MODIFICADO, FQDN))
            cursor.execute('UPDATE ' + TABLA_SERVIDOR + ' SET activo = ? WHERE fqdn = ?;', ('TRUE', FQDN))
            cursor.execute('UPDATE ' + TABLA_SERVIDOR + ' SET intento = ? WHERE fqdn = ?;', (0, FQDN))
        # si el servidor no existe
        else:
            handler.log.debug('agregando servidor nuevo: ' + FQDN + ':' + str(PUERTO))
            cursor.execute('INSERT INTO ' + TABLA_SERVIDOR + ' (fqdn, puerto, activo, modificado, intento) VALUES (?, ?, ?, ?, ?);', (FQDN, PUERTO, 'TRUE', MODIFICADO, 0))
    except Exception as message:
        handler.log.error('no se puede agregar servidor: %s', message)
        handler.log.exception(message)
        exit(1)

def ServidorVuelveActivo(FQDN, PUERTO):
    try:
        handler.log.debug('servidor vuelve a actividad: ' + FQDN + ':' + str(PUERTO))
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        cursor.execute('UPDATE ' + TABLA_SERVIDOR + ' SET activo = ? WHERE fqdn = ?;', ('TRUE', FQDN))
        cursor.execute('UPDATE ' + TABLA_SERVIDOR + ' SET intento = ? WHERE fqdn = ?;', (0, FQDN))
    except Exception as message:
        handler.log.error('no se puede agregar servidor: %s', message)
        handler.log.exception(message)
        exit(1)


def AgregaLAV(FQDN, LAV):
    try:
        miLAV = LAV.split(" "); 
        # handler.log.debug('LAV: ' + LAV)
        
        # obtiene HORA
        HORA = None; HORA = str(miLAV[0]); handler.log.debug('HORA: ' + HORA)
        time_unix = HORA
        
        # obtiene CPU
        CPU = None; CPU = str(miLAV[1]);
        handler.log.debug('CPU: ' + CPU)
        cpu_total = None; cpu_total = str(CPU).split(",", )[0]; handler.log.debug('cpu_total: ' + cpu_total)
        cpu_cores = None; cpu_cores = str(CPU).split(",", 1)[1]; handler.log.debug('cpu_cores: ' + cpu_cores)
        
        # obtiene MEM
        MEM = None; MEM = str(miLAV[2]); handler.log.debug('MEM: ' + MEM)
        mem_total = None; mem_total = str(MEM).split(",", )[0]; handler.log.debug('mem_total: ' + mem_total)
        mem_used = None; mem_used = str(MEM).split(",", )[1]; handler.log.debug('mem_used: ' + mem_used)
        mem_free = None; mem_free = str(MEM).split(",", )[2]; handler.log.debug('mem_free: ' + mem_free)
        mem_percent = None; mem_percent = str(MEM).split(",", )[3]; handler.log.debug('mem_percent: ' + mem_percent)
        
        # obtiene IO
        IO = None; IO = str(miLAV[3]); handler.log.debug('IO: ' + IO)
        io_read_count = None; io_read_count = str(IO).split(",", )[0]; handler.log.debug('io_read_count: ' + io_read_count)
        io_write_count = None; io_write_count = str(IO).split(",", )[1]; handler.log.debug('io_write_count: ' + io_write_count)
        io_read_bytes = None; io_read_bytes = str(IO).split(",", )[2]; handler.log.debug('io_read_bytes: ' + io_read_bytes)
        io_write_bytes = None; io_write_bytes = str(IO).split(",", )[3]; handler.log.debug('io_write_bytes: ' + io_write_bytes)
        io_read_time = None; io_read_time = str(IO).split(",", )[4]; handler.log.debug('io_read_time: ' + io_read_time)
        io_write_time = None; io_write_time = str(IO).split(",", )[5]; handler.log.debug('io_write_time: ' + io_write_time)
        
        # obtiene NET
        NET = None; NET = str(miLAV[4]); handler.log.debug('NET: ' + NET)
        net_bytes_sent = None; net_bytes_sent = str(NET).split(",", )[0]; handler.log.debug('net_bytes_sent: ' + net_bytes_sent)
        net_bytes_recv = None; net_bytes_recv = str(NET).split(",", )[1]; handler.log.debug('net_bytes_recv: ' + net_bytes_recv)
        net_packets_sent = None; net_packets_sent = str(NET).split(",", )[2]; handler.log.debug('net_packets_sent: ' + net_packets_sent)
        net_packets_recv = None; net_packets_recv = str(NET).split(",", )[3]; handler.log.debug('net_packets_recv: ' + net_packets_recv)
        
        # obtiene HDD
        HDD = None; HDD = str(miLAV[5]); handler.log.debug('HDD: ' + HDD)
        hdd_device = None; hdd_device = str(HDD).split(",", )[0]; handler.log.debug('hdd_device: ' + hdd_device)
        hdd_total = None; hdd_total = str(HDD).split(",", )[1]; handler.log.debug('hdd_total: ' + hdd_total)
        hdd_used = None; hdd_used = str(HDD).split(",", )[2]; handler.log.debug('hdd_used: ' + hdd_used)
        hdd_free = None; hdd_free = str(HDD).split(",", )[3]; handler.log.debug('hdd_free: ' + hdd_free)
        hdd_percent = None; hdd_percent = str(HDD).split(",", )[4]; handler.log.debug('hdd_percent: ' + hdd_percent)
        
        handler.log.debug('agregando LAV de ' + FQDN)
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        # actualiza intentos de chequeo a 0
        cursor.execute('UPDATE ' + TABLA_SERVIDOR + ' SET intento = ? WHERE fqdn = ?;', (0, FQDN))
        # obtiene identificador del host, para agregar carga
        ID = cursor.execute('SELECT id FROM ' + TABLA_SERVIDOR + ' WHERE fqdn = ?;', ([FQDN])).fetchall()
        servidorid_id = ID[0][0]
        # agrega carga a la DB
        cursor.execute('INSERT INTO ' + TABLA_CARGAS + ' (servidorid_id, time_unix, cpu_total, cpu_cores, mem_total, mem_used, mem_free, mem_percent, io_read_count, io_write_count, io_read_bytes, io_write_bytes, io_read_time, io_write_time, net_bytes_sent, net_bytes_recv, net_packets_sent, net_packets_recv, hdd_device, hdd_total, hdd_used, hdd_free, hdd_percent) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', 
                        (servidorid_id, time_unix, cpu_total, cpu_cores, mem_total, mem_used, mem_free, mem_percent, io_read_count, io_write_count, io_read_bytes, io_write_bytes, io_read_time, io_write_time, net_bytes_sent, net_bytes_recv, net_packets_sent, net_packets_recv, hdd_device, hdd_total, hdd_used, hdd_free, hdd_percent))
        handler.log.debug('LAV agregado correctamente para ' + FQDN)
    except Exception as message:
        handler.log.error('no se puede agregar LAV de cliente: %s', message)
        handler.log.exception(message)

def ServidorConProblemas(FQDN, PUERTO):
    try:
        handler.log.debug('servidor con problemas: ' + FQDN + ':' + str(PUERTO))
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        INTENTO = cursor.execute('SELECT intento FROM ' + TABLA_SERVIDOR + ' WHERE fqdn = ?;', ([FQDN])).fetchall()
        MODIFICADO = time()
        if INTENTO:
            # si se ha intentado menos de NUMEROINTENTOS veces consultar el servidor
            if INTENTO < NUMEROINTENTOS:
                handler.log.debug('actualizando intentos con problemas de servidor a ' + (INTENTO + 1))
                cursor.execute('UPDATE ' + TABLA_SERVIDOR + ' SET intento = ? WHERE fqdn = ?;', ((INTENTO + 1), FQDN))
                cursor.execute('UPDATE ' + TABLA_SERVIDOR + ' SET modificado = ? WHERE fqdn = ?;', (MODIFICADO, FQDN))
            # si se ha intentado menos de NUMEROINTENTOS veces consultar el servidor
            else:
                handler.log.debug('actualizando a inactivo estado de servidor')
                cursor.execute('UPDATE ' + TABLA_SERVIDOR + ' SET activo = ? WHERE fqdn = ?;', ('FALSE', FQDN))
                cursor.execute('UPDATE ' + TABLA_SERVIDOR + ' SET modificado = ? WHERE fqdn = ?;', (MODIFICADO, FQDN))
    except Exception as message:
        handler.log.error('no se puede modificar estado de servidor: %s', message)
        handler.log.exception(message)
        exit(1)

def ConsultaMejorServidor():
    try:
        handler.log.debug('consultando por mejor servidores')
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        # se obtiene el mejor servidor del momento en base a las cargas entregadas
        mejorservidor = cursor.execute('SELECT fqdn FROM (SELECT fqdn, min(cpu) AS cpu FROM (SELECT servidor.id, servidor.fqdn, sum(carga.cpu_total)/count(carga.id) AS cpu FROM ' + TABLA_SERVIDOR + ' AS servidor, ' + TABLA_CARGAS + ' AS carga WHERE servidor.id = carga.servidorid_id AND servidor.intento <= 1 AND servidor.activo = "TRUE" GROUP BY servidor.id));').fetchall()
        handler.log.debug('mejor servidor: %s', mejorservidor[0][0])
    except Exception as message:
        handler.log.error('no se puede obtener mejor servidor: %s', message)
        handler.log.exception(message)
        exit(1)
    finally:
        return mejorservidor[0][0]

def Valida():
    try:
        # comprobando que la db existe
        if not path.exists(SBCDB):
            raise ValueError("no existe la BD en " + path.abspath(SBCDB))
        
        # se conecta a la db
        conexion = connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        
        # comprobando tabla configuracion
        for TABLA in (TABLA_CONFIGURACION, TABLA_SERVIDOR, TABLA_CARGAS, TABLA_OPERADOR, TABLA_ALERTA):
            cont = cursor.execute('pragma table_info(' + TABLA + ');').fetchall()
            if cont: handler.log.debug('la tabla %s parece estar bien', TABLA)
            else:
                raise ValueError, "no existe la tabla " + TABLA      
    except Exception as message:
        handler.log.error('ha ocurrido un problema al validar la integridad del modulo: %s', message)
        handler.log.exception(message)
        exit(1)

def run():
    handler.log.info('iniciando modulo')

# main
if __name__ == '__main__':
    Valida()
