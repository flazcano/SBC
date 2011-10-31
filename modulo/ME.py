"""
Created on 23/10/2011

@author: Fernando

Modulo de Escucha y Obtencion para AOC (ME)
"""

import select
import socket

from sys import exit, stdin
from threading import Thread
from time import sleep

from Logger import handler
from modulo import MIS

class Servidor():
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 12345
        self.timeout = None
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        try:
            # instanciando el socket
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
            self.server.settimeout(self.timeout)
        except socket.error, (message):
            if self.server:
                self.server.close()
            handler.log.critical('no se puede abrir el socket: %s', message)
            exit(1)

    def run(self):
        self.open_socket()
        input = [self.server,stdin]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])
            
            for server in inputready:

                if server == self.server:
                    # manejando el socket del servidor
                    cliente = Cliente(self.server.accept());
                    cliente.start();
                    # creando un hilo
                    self.threads.append(cliente);

                # elif server == sys.stdin:
                    # manejando la entrada estandar del servidor
                    # junk = sys.stdin.readline();

        # cerrando los hilos
        if self.server:
            self.server.close()
        for c in self.threads:
            c.join()

class Cliente(Thread):
    def __init__(self,(client,address)):
        Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024

    def run(self):
        try:
            handler.log.info('conectado desde ' + self.address[0] + ':' + str(self.address[1]));
            running = 1
            while running:
                data = self.client.recv(self.size)
                if data:
                    # confirmando la data recibida
                    handler.log.debug('cliente ' + self.address[0] + ':' + str(self.address[1]) + ' envia: ' + data)
                    # si se recibe 'HELLO', se agrega el HOST a las Servidores a Balancear
                    if data == 'HELLO':
                        handler.log.info('agregando nuevo cliente a balancear: ' + self.address[0])
                         
                else:
                    handler.log.info('desconectado desde ' + self.address[0] + ':' + str(self.address[1]))
                    self.client.close()
                    # cerrando el hilo
                    running = 0
        except socket.error, (message):
            handler.log.debug('error de conexion de ' + self.address[0] + ':' + str(self.address[1]) + ': %s', message)
        finally:
            if self.client:
                self.client.close()

class ThreadxLAV(Thread):
        def __init__(self, host, puerto):
            Thread.__init__(self)
            self.host = host
            self.puerto = puerto

        def run(self):
            try:
                cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                cliente.connect((self.host, self.puerto))
                cliente.send(':)')
                LAVcliente = cliente.recv(1024)
                handler.log.debug('obtenido LAV desde ' + self.host + ':' + str(self.puerto) + ': ' + LAVcliente)
                # guardando la informacion del servidor a traves del MIS
                
                
            except Exception, (message):
                handler.log.error('no se pudo establecer la conexion con ' + self.host + ':' + str(self.puerto) + ': %s', message)
                # marcando al servidor con problemas
                
                exit(1)
                   
def consultaEstadoServidores():
    try:
        handler.log.info('consultando estado de servidores a balancear')
        
        # se revisa los servidores para obtener la carga de cada uno de ellos
        servidores = MIS.consulta_servidores()
        for servidor in servidores:
            host = servidor[0]
            puerto = servidor[1]
        
            ThreadxLAV(host, puerto).start()
            sleep(1)       
        
    except Exception, (message):
        handler.log.debug('error al consultar estado del servidor')
        handler.log.exception(message)

def run():
    handler.log.info('iniciando modulo ME')
    myservidor = Servidor()
    myservidor.run()
    