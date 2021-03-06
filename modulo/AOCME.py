'''
Created on 29/10/2011

@author: Fernando

Modulo de Escucha para Agente de Obtencion de Cargas (AOCME)
'''

# importaciones
from sys import exit, stdin
from time import sleep
import socket
from select import select
from threading import Thread
from Logger import handler
from modulo.AOCMR import getCarga

# definiciones
AOCMESLEEPTIME = None
SBCTIMEOUT     = None

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
            handler.log.debug('abriendo el socket de comunicacion')
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
        running = 1
        handler.log.debug('socket de comunicacion abierto, esperando clientes')
        while running:
            inputready  = select([self.server, stdin], [], [])
            outputready = select([self.server, stdin], [], []) #@UnusedVariable
            exceptready = select([self.server, stdin], [], []) #@UnusedVariable
            for server in inputready:
                # manejando el socket del servidor
                cliente = Cliente(self.server.accept());
                cliente.start();
                # creando un hilo
                self.threads.append(cliente);

        # cerrando los hilos
        if self.server:
            handler.log.debug('cerrando servidor')
            self.server.close()
        for c in self.threads:
            handler.log.debug('cerrando hilo')
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
                DATA = self.client.recv(self.size).decode()
                if DATA:
                    if 'HELLO' in DATA:
                        handler.log.debug('SBC ' + self.address[0] + ':' + str(self.address[1]) + ' envia peticion de carga')
                        
                        # enviando carga
                        LAV = getCarga()
                        handler.log.debug('enviando: ' + LAV)
                        self.client.send(str.encode(LAV))
                    else:
                        handler.log.debug('se descarta el mensaje, SBC ' + self.address[0] + ':' + str(self.address[1]) + ' envia: ' + DATA)
                    
                self.client.close()    
                break
            handler.log.debug('desconectado desde ' + self.address[0] + ':' + str(self.address[1]))                    
        except socket.error as message:
            handler.log.debug('error de conexion de ' + self.address[0] + ':' + str(self.address[1]) + ': %s', message)
        finally:
            if self.client:
                self.client.close()

# funciones
def AgenteVivo(SBCHOST, SBCPORT, PORT):
    sinConexion = 1
    while sinConexion:
        try:
            MSG = 'HELLO ' + str(PORT)
            handler.log.debug('enviando keep alive a SBC: ' + MSG)
            sbccon = socket.socket()
            sbccon.settimeout(SBCTIMEOUT)
            sbccon.connect((SBCHOST, SBCPORT))
            sbccon.send(str.encode(MSG))
            handler.log.debug('keep alive enviado correctamente')
            sinConexion = 0
        except Exception as message:
            handler.log.error('no se pudo conectar al SBC: %s', message)
            sleep(float(AOCMESLEEPTIME))
        finally:
            if sbccon:
                handler.log.debug('cerrando conexion con SBC')
                sbccon.close()

def run(HOST, PORT):
    handler.log.info('iniciando el modulo')
    handler.log.debug('creando servidor')
    myservidor = Servidor(HOST, PORT)
    handler.log.info('corriendo servidor')
    myservidor.run()
    
def setAOCMESLEEPTIME(VALUE):
    global AOCMESLEEPTIME; AOCMESLEEPTIME = VALUE
    handler.log.debug('AOCMESLEEPTIME : ' + str(AOCMESLEEPTIME))

def setSBCTIMEOUT(VALUE):
    global SBCTIMEOUT; SBCTIMEOUT = VALUE
    handler.log.debug('SBCTIMEOUT     : ' + str(SBCTIMEOUT))

# main