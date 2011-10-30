'''
Created on 29/10/2011

@author: Fernando

Modulo de Escucha para Agente de Obtencion de Cargas (AOCME)
'''

import select
import socket

from sys import exit, stdin
from threading import Thread

from Logger import handler
from AOCMR import LAV

class Servidor():
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 54321
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
                    # enviando carga
                    self.client.send(LAV())
                self.client.close()    
                break
            handler.log.info('desconectado desde ' + self.address[0] + ':' + str(self.address[1]))                    
        except socket.error, (message):
            handler.log.debug('error de conexion de ' + self.address[0] + ':' + str(self.address[1]) + ': %s', message)
        finally:
            if self.client:
                self.client.close()

def run():
    handler.log.info('iniciando modulo AOCME')
    myservidor = Servidor()
    myservidor.run()