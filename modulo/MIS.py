"""
Created on 23/10/2011

@author: Fernando

Modulo de Integracion para SQLite3 (MIS)
"""

import sqlite3

from sys import exit

from Logger import handler

db="sbc.db"
        
class crea():
    def esquema(self):
        try:
            handler.log.debug('creando esquema en ' + db)
            connection_crear=sqlite3.connect(db, isolation_level=None)
            cursor_crear=connection_crear.cursor()
            cursor_crear.execute('CREATE TABLE configuraciones (Id INTEGER PRIMARY KEY, Date TEXT, Entry TEXT);')
            cursor_crear.close();
        except Exception, (message):
            handler.log.error('no se puede crear esquema de ' + db)
            handler.log.exception(message)
            exit(1)
        finally:
            if cursor_crear:
                cursor_crear.close()

def consulta_servidores():
    try:
        handler.log.debug('consultando listado de servidores en ' + db)
        #connection_consultar_estado=sqlite3.connect(db, isolation_level=None)
        #cursor_consultar_estado=connection_consultar_estado.cursor()
        #resultado = cursor_consultar_estado.execute('SELECT nombre, ip FROM servidores;')
        #cursor_consultar_estado.close();
        resultado = [('localhost', 54321), ('127.0.0.1', 54321)]
        return resultado
    except Exception, (message):
        handler.log.error('no se puede obtener listado de servidores de ' + db)
        handler.log.exception(message)
        exit(1)
    #finally:
    #    if cursor_consultar_estado:
    #        cursor_consultar_estado.close()

def run():
    handler.log.info('iniciando modulo MIS')
    
    # se conecta a SQLite3
    try:
        connection=sqlite3.connect(db, isolation_level=None)
        cursor=connection.cursor()
        cont = cursor.execute("pragma table_info(configuraciones);").fetchall()
        if not cont:
            crea.esquema()
        else:
            handler.log.debug('la estructura de la db ' + db + ' parece estar correcta')
    except Exception, (message):
        handler.log.error('no se puede acceder a ' + db)
        handler.log.exception(message)
        exit(0)
    finally:
        if cursor:
            cursor.close()