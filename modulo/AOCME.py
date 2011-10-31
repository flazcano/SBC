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
    def __init__(self, host, puerto):
        self.host = host
        self.port = puerto
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
            handler.log.critical('no se puede abrir el socket: %s', message)
            if self.server:
                self.server.close()
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
            handler.log.debug('SBC conectado desde ' + self.address[0] + ':' + str(self.address[1]));
            running = 1
            while running:
                data = self.client.recv(self.size)
                if data:
                    # enviando carga
                    miLAV = LAV()
                    handler.log.debug('enviando LAV:' + miLAV)
                    self.client.send(miLAV)
                self.client.close()    
                break
            handler.log.debug('SBC desconectado desde ' + self.address[0] + ':' + str(self.address[1]))
        except socket.error, (message):
            handler.log.debug('error de conexion de ' + self.address[0] + ':' + str(self.address[1]) + ': %s', message)
        finally:
            if self.client:
                self.client.close()

def run(host, puerto):
    handler.log.info('iniciando modulo AOCME')
    myservidor = Servidor(host, puerto)
    myservidor.run()