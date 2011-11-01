'''
Created on 29/10/2011

@author: Fernando

Modulo de Escucha para Agente de Obtencion de Cargas (AOCME)
'''

# importaciones
import select, socket
from sys import exit, stdin
from threading import Thread
from Logger import handler
from modulo.AOCMR import LAV

# definiciones

# clases
class Servidor():
    def __init__(self, HOST, PORT):
        self.host = HOST
        self.port = PORT
        self.timeout = None
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        try:
            # instanciando el socket
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            self.server.settimeout(self.timeout)
        except socket.error as message:
            if self.server:
                self.server.close()
            handler.log.critical('no se puede abrir el socket: %s', message)
            exit(1)

    def run(self):
        self.open_socket()
        input = [self.server,stdin]
        running = 1
        while running:
            inputready, outputready, exceptready = select.select(input,[],[])
            for server in inputready:
                if server == self.server:
                    # manejando el socket del servidor
                    cliente = Cliente(self.server.accept());
                    cliente.start();
                    # creando un hilo
                    self.threads.append(cliente);

        # cerrando los hilos
        if self.server:
            self.server.close()
        for c in self.threads:
            c.join()

class Cliente(Thread):
    def __init__(self, cliente):
        Thread.__init__(self)
        client, address = cliente
        self.client = client
        self.address = address
        self.size = 1024

    def run(self):
        try:
            handler.log.debug('conectado desde ' + self.address[0] + ':' + str(self.address[1]));
            running = 1
            while running:
                data = self.client.recv(self.size)
                if data:
                    # enviando carga
                    self.client.send(str.encode(LAV()))
                self.client.close()    
                break
            handler.log.debug('desconectado desde ' + self.address[0] + ':' + str(self.address[1]))                    
        except socket.error as message:
            handler.log.debug('error de conexion de ' + self.address[0] + ':' + str(self.address[1]) + ': %s', message)
        finally:
            if self.client:
                self.client.close()

# funciones
def run(HOST, PORT):
    handler.log.info('iniciando el modulo')
    myservidor = Servidor(HOST, PORT)
    myservidor.run()
    
# main