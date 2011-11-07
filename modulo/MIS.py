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

conexion=sqlite3.connect(SBCDB, isolation_level=None)

# clases

# funciones
def CreaEsquema():
    try:
        handler.log.info('creando esquema en ' + SBCDB)
        cursor=conexion.cursor()
        cursor.execute('CREATE TABLE configuracion (id INTEGER NOT NULL PRIMARY KEY, clave TEXT UNIQUE NOT NULL, valor TEXT NOT NULL, modificado TEXT NOT NULL, defvalor TEXT, prevalor TEXT);')
        cursor.execute('CREATE TABLE servidor (id INTEGER NOT NULL PRIMARY KEY, fqdn TEXT UNIQUE NOT NULL, puerto INTEGER NOT NULL, activo BOOLEAN DEFAULT TRUE, visto TEXT, modificado TEXT);')
        cursor.execute('CREATE TABLE cargas (id INTEGER NOT NULL PRIMARY KEY, servidorid CONSTRAINT fk_id_srv REFERENCES servidores(id) ON DELETE CASCADE, modificado TEXT);')
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

def AgregaServidor(HOST, PORT):
    try:
        handler.log.debug('agregando servidor: ' + HOST + ':' + str(PORT))
        conexion=sqlite3.connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        PUERTO = cursor.execute('SELECT puerto FROM servidor WHERE fqdn = ?;', ([HOST])).fetchall()
        # si el servidor ya existe en la base dedatos
        if PUERTO:
            # pero tiene distinto puerto al registrado
            if PORT is not str(PUERTO[0][0]):
                handler.log.debug('actualizando puerto de servidor existente, de ' + str(PUERTO[0][0])+ ' a ' + PORT)
                cursor.execute('UPDATE servidor SET puerto = ? WHERE fqdn = ?;', (PORT, HOST))
                HORA = time()
                cursor.execute('UPDATE servidor SET modificado = ? WHERE fqdn = ?;', (HORA, HOST))
        # si el servidor no existe
        else:
            handler.log.debug('agregando servidor nuevo: ' + HOST + ':' + PORT)
            cursor.execute('INSERT INTO servidor (fqdn, puerto, activo) VALUES (?, ?, ?);', (HOST, PORT, 'TRUE'))
    except Exception as message:
        handler.log.error('no se puede agregar servidor: %s', message)
        handler.log.exception(message)
        exit(1)

def AgregaLAV(HOST, LAV):
    try:
        
        miLAV = LAV.split(" "); handler.log.debug('LAV: ' + LAV)
        
        # obtiene HORA
        HORA = None; HORA = str(miLAV[0]); handler.log.debug('HORA: ' + HORA)
        
        # obtiene CPU
        CPU = None; CPU = str(miLAV[1]); handler.log.debug('CPU: ' + CPU)
        
        # obtiene MEM
        MEM = None; MEM = str(miLAV[2]); handler.log.debug('MEM: ' + MEM)
        
        # obtiene IO
        IO = None; IO = str(miLAV[3]); handler.log.debug('IO: ' + IO)
        
        # obtiene NET
        NET = None; NET = str(miLAV[4]); handler.log.debug('NET: ' + NET)
        
        # obtiene HDD
        HDD = None; HDD = str(miLAV[5]); handler.log.debug('HDD: ' + HDD)
        
        pass
        
        handler.log.debug('agregando LAV de cliente')
        conexion=sqlite3.connect(SBCDB, isolation_level=None)
        cursor=conexion.cursor()
        SERVERID = cursor.execute('SELECT id FROM servidor WHERE fqdn = ?;', ([HOST])).fetchall()
        cursor.execute('INSERT INTO cargas (serverid, hora, cpu, mem) VALUES (?);', (SERVERID))
    except Exception as message:
        handler.log.error('no se puede agregar LAV de cliente: %s', message)
        handler.log.exception(message)

def Valida():
    try:
        # comprobando que la db existe
        fileDB = open(SBCDB,"r")
        handler.log.debug('la base de datos existe, en: ' + path.abspath(SBCDB))
        fileDB.close()
        
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
        exit(1)

def run():
    handler.log.info('iniciando modulo')

# main
if __name__ == '__main__':
    SBCDB = "../sbc.db"
    Valida()
