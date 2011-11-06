"""
Created on 23/10/2011

@author: Fernando

Modulo de Integracion para SQLite3 (MIS)
"""

# importaciones
import sqlite3
from exceptions import Exception
from sys import exit
from os import path
from Logger import handler

# definiciones
db = "sbc.db"

conexion=sqlite3.connect(db, isolation_level=None)

# clases

# funciones
def CreaEsquema():
    try:
        handler.log.info('creando esquema en ' + db)
        cursor=conexion.cursor()
        cursor.execute('CREATE TABLE configuraciones (id INTEGER NOT NULL PRIMARY KEY, clave TEXT UNIQUE NOT NULL, valor TEXT NOT NULL, modificado TEXT NOT NULL, defvalor TEXT, prevalor TEXT);')
        cursor.execute('CREATE TABLE servidores (id INTEGER NOT NULL PRIMARY KEY, fqdn TEXT UNIQUE NOT NULL, puerto INTEGER NOT NULL, activo BOOLEAN DEFAULT TRUE, visto TEXT, modificado TEXT);')
        cursor.execute('CREATE TABLE infoservidores (id INTEGER NOT NULL PRIMARY KEY, servidorid CONSTRAINT fk_id_srv REFERENCES servidores(id) ON DELETE CASCADE, modificado TEXT);')
        handler.log.info('esquema creado correctamente')
        exit(0)
    except Exception as message:
        handler.log.error('no se puede crear esquema de ' + db + ': %s', message)
        exit(1)
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

        
def ConsultaListaServidores():
    try:
        handler.log.debug('consultando listado de servidores')
        conexion=sqlite3.connect(db, isolation_level=None)
        cursor=conexion.cursor()
        servidores = cursor.execute('SELECT id, fqdn, puerto FROM servidores WHERE activo = "TRUE";')
        return servidores
    except Exception as message:
        handler.log.error('no se puede obtener listado de servidores activos: %s', message)
        exit(1)

def ConsultaTotalServidores():
    try:
        handler.log.debug('consultando total de servidores activos')
        conexion=sqlite3.connect(db, isolation_level=None)
        cursor=conexion.cursor()
        total = cursor.execute('SELECT count(id) FROM servidores WHERE activo = "TRUE";')
        return total
    except Exception as message:
        handler.log.error('no se puede obtener total de servidores activos: %s', message)
        exit(1)

def AgregaServidor(HOST, PORT):
    try:
        handler.log.debug('agregando servidor')
        conexion=sqlite3.connect(db, isolation_level=None)
        cursor=conexion.cursor()
        total = cursor.execute('SELECT count(id) FROM servidores WHERE fqdn = ?;', ([HOST])).fetchall()
        if total[0][0] > 0: 
            handler.log.debug('actualizando servidor existente')
            cursor.execute('UPDATE servidores SET puerto = ? WHERE fqdn = ?;', (PORT, HOST))
        else: 
            handler.log.debug('agregando servidor nuevo')
            cursor.execute('INSERT INTO servidores (fqdn, puerto, activo) VALUES (?, ?, ?);', (HOST, PORT, 'TRUE'))
    except Exception as message:
        handler.log.error('no se puede agregar servidor: %s', message)
        handler.log.exception(message)
        exit(1)

def Valida():
    # se conecta a SQLite3
    try:
        # comprobando que la db existe
        fileDB = open(db,"r")
        handler.log.debug('la base de datos existe, en: ' + path.abspath(db))
        fileDB.close()
        
        # se conecta a la db
        conexion=sqlite3.connect(db, isolation_level=None)
        cursor=conexion.cursor()
        
        # comprobando tabla configuraciones
        tabla = 'configuraciones'
        cont = cursor.execute('pragma table_info(configuraciones);').fetchall()
        if cont: handler.log.debug('la tabla %s parece bien', tabla)
        else:
            raise ValueError, "no existe la tabla " + tabla
        
        # comprobando tabla servidores
        tabla = 'servidores'
        cont = cursor.execute('pragma table_info(servidores);').fetchall()
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
    Valida()
