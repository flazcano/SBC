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

# clases
class DBTableError(BaseException):
    def __init__(self, tabla):
        self.tabla = tabla
        return
        
    def __str__(self):
        return 'No existe la tabla ' + self.tabla

# funciones
def creaEsquema():
    try:
        handler.log.debug('creando esquema en ' + db)
        conexion=sqlite3.connect(db, isolation_level=None)
        cursor=conexion.cursor()
        cursor.execute('CREATE TABLE configuraciones (id INTEGER NOT NULL PRIMARY KEY, clave TEXT UNIQUE NOT NULL, valor TEXT NOT NULL, modificado TEXT NOT NULL, defvalor TEXT, prevalor TEXT);')
        cursor.execute('CREATE TABLE servidores (id INTEGER NOT NULL PRIMARY KEY, fqdn TEXT UNIQUE NOT NULL, puerto INTEGER NOT NULL, activo BOOLEAN DEFAULT TRUE, visto TEXT, modificado TEXT);')
        cursor.execute('CREATE TABLE infoservidores (id INTEGER NOT NULL PRIMARY KEY, servidorid CONSTRAINT fk_id_srv REFERENCES servidores(id) ON DELETE CASCADE, modificado TEXT);')
    except Exception, (message):
        handler.log.error('no se puede crear esquema de ' + db + ': %s', message)
        exit(1)
    finally:
        if cursor: cursor.close()

def consultaListaServidores():
    try:
        handler.log.debug('consultando listado de servidores en ' + db)
        conexion=sqlite3.connect(db, isolation_level=None)
        cursor=conexion.cursor()
        servidores = cursor.execute('SELECT id, fqdn, puerto FROM servidores WHERE activo = ?;', ('TRUE'))
        return servidores
    except Exception, (message):
        handler.log.error('no se puede obtener listado de servidores activos de ' + db + ': %s', message)
        exit(1)
    finally:
        if cursor: cursor.close()

def consultaTotalServidores():
    try:
        handler.log.debug('consultando total de servidores activos en ' + db)
        conexion=sqlite3.connect(db, isolation_level=None)
        cursor=conexion.cursor()
        total = cursor.execute('SELECT count(id) FROM servidores WHERE activo = ?;', ('TRUE'))
        return total
    except Exception, (message):
        handler.log.error('no se puede obtener total de servidores activos de ' + db + ': %s', message)
        exit(1)
    finally:
        if cursor: cursor.close()

def agregaServidor(HOST, PORT):
    try:
        handler.log.debug('agregando servidor en ' + db)
        conexion=sqlite3.connect(db, isolation_level=None)
        cursor=conexion.cursor()
        total = cursor.execute('SELECT count(id) FROM servidores WHERE fqdn = ?;', ([HOST])).fetchall()
        if total[0][0] > 0: 
            handler.log.debug('actualizando servidor')
            cursor.execute('UPDATE servidores SET puerto = ? WHERE fqdn = ?;', (PORT, HOST))
        else: 
            handler.log.debug('agregando servidor')
            cursor.execute('INSERT INTO servidores (fqdn, puerto, activo) VALUES (?, ?, ?);', (HOST, PORT, 'TRUE'))
    except Exception, (message):
        handler.log.error('no se puede agregar servidor en ' + db + ': %s', message)
        handler.log.exception(message)
        exit(1)
    finally:
        if cursor: cursor.close()

def valida():
    # se conecta a SQLite3
    try:
        # comprobando que la db existe
        fileDB = open(db,"r")
        handler.log.debug('existe la base de datos sqlite3 en: '  + path.abspath(fileDB))
    except Exception, (message):
        fileDB = open(db,"w")
        handler.log.debug('creada la base de datos sqlite3 en: '  + path.abspath(db))
    finally: 
        if fileDB: fileDB.close()
            
    try:
        # se conecta a la db
        conexion=sqlite3.connect(db, isolation_level=None)
        cursor=conexion.cursor()
        
        # comprobando tabla configuraciones
        tabla = 'configuraciones'
        cont = cursor.execute('pragma table_info(configuraciones);').fetchall()
        if cont: handler.log.debug('la tabla %s parece bien', tabla)
        else:
            creaEsquema()
            exit(1)
        
        # comprobando tabla servidores
        tabla = 'servidores'
        cont = cursor.execute('pragma table_info(servidores);').fetchall()
        if cont: handler.log.debug('la tabla %s parece bien', tabla)
        else:
            creaEsquema()
            exit(1)
            
    except Exception, (message):
        handler.log.error('ha ocurrido un problema al validar la integridad del modulo: %s', message)
        handler.log.exception(message)
        exit(1)
    finally:
        if cursor: cursor.close()

def run():
    handler.log.info('iniciando modulo')

# main
if __name__ == '__main__':
    #valida()
    agregaServidor('192.168.0.3', 54321)