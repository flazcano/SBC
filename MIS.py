#!/usr/bin/env python

"""
Created on 23/10/2011

@author: Fernando

Modulo de Integracion de SQLite3 para SBC
"""

import sys
from Logger import handler
import sqlite3

db="sbc.db"

def run():
    handler.log.info('iniciando modulo MIS')
    
    # se conecta a SQLite3
    try:
        connection=sqlite3.connect(db, isolation_level=None)
        cursor=connection.cursor()
        cont = cursor.execute("pragma table_info(configuraciones);").fetchall()
        if not cont:
            crear_esquema()
            
    except Exception, (message):
        handler.log.error('no se puede acceder a ' + db)
        handler.log.exception(message)
        sys.exit(0)
        
    if cursor:
        cursor.close()
        
def crear_esquema():
    try:
        handler.log.debug('creando esquema en ' + db)
        connection_crear=sqlite3.connect(db, isolation_level=None)
        cursor_crear=connection_crear.cursor()
        cursor_crear.execute('CREATE TABLE configuraciones (Id INTEGER PRIMARY KEY, Date TEXT, Entry TEXT);')
        cursor_crear.close();
    except Exception, (message):
        handler.log.error('no se puede crear esquema de ' + db)
        handler.log.exception(message)
        sys.exit(1)
    if cursor_crear:
        cursor_crear.close()
        
def consultar_servidores():
    try:
        handler.log.debug('consultando listado de servidores en ' + db)
        connection_consultar_estado=sqlite3.connect(db, isolation_level=None)
        cursor_consultar_estado=connection_consultar_estado.cursor()
        resultado = cursor_consultar_estado.execute('SELECT nombre, ip FROM servidores;')
        cursor_consultar_estado.close();
        return resultado        
    except Exception, (message):
        handler.log.error('no se puede obtener listado de servidores de ' + db)
        handler.log.exception(message)
        sys.exit(1)
    if cursor_consultar_estado:
        cursor_consultar_estado.close()
        