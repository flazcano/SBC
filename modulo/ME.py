"""
Created on 23/10/2011

@author: Fernando

Modulo de Escucha y Obtencion para AOC (ME)
"""

# importaciones
import socket, select
from time import sleep
from sys import exit, stdin
from threading import Thread
from Logger import handler
from modulo import MIS

# definiciones
CLIENTTIMEOUT = 10
SLEEPTIME = 30
HOST = "0.0.0.0"
PORT = 12345

# clases
class Servidor():
    def __init__(self):
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
        input = [self.server,stdin] #@ReservedAssignment
        running = 1
        while running:
            inputready, outputready, exceptready = select.select(input,[],[]) #@UnusedVariable
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
        self.cliente = client
        self.address = address
        self.size = 1024

    def run(self):
        try:
            handler.log.debug('conectado desde ' + self.address[0] + ':' + str(self.address[1]));
            running = 1
            while running:
                DATA = self.cliente.recv(self.size).decode()
                if DATA:
                    if 'HELLO' in DATA:
                        handler.log.debug('cliente ' + self.address[0] + ':' + str(self.address[1]) + ' envia keep alive: ' + DATA)
                        AOCHOST = self.address[0]
                        AOCPORT = DATA.replace("HELLO ", "", 1)
                        
                        # se comunica con MIS para agregar cliente a servidores a balancear
                        MIS.AgregaServidor(AOCHOST, AOCPORT)
                    else:
                        handler.log.debug('se descarta el mensaje, cliente ' + self.address[0] + ':' + str(self.address[1]) + ' envia: ' + DATA)
                else:
                    handler.log.debug('desconectado desde ' + self.address[0] + ':' + str(self.address[1]))
                    self.cliente.close()
                    # cerrando el hilo
                    running = 0
        except socket.error as message:
            handler.log.debug('error de conexion de ' + self.address[0] + ':' + str(self.address[1]) + ': %s', message)
        finally:
            if self.cliente:
                self.cliente.close()

class ThreadxLAV(Thread):
        def __init__(self, HOST, PORT):
            Thread.__init__(self)
            self.HOST = HOST
            self.PORT = PORT

        def run(self):
            try:
                clientcon = socket.socket()
                clientcon.settimeout(CLIENTTIMEOUT)
                clientcon.connect((self.HOST, self.PORT))
                clientcon.send(str.encode('HELLO'))
                LAV = clientcon.recv(1024).decode()
                handler.log.debug('se obtuvo LAV desde ' + str(self.HOST) + ':' +str(self.PORT) + ': ' + LAV)
                # se comunica con MIS para agregar LAV
                MIS.AgregaLAV(self.HOST, LAV)
            except Exception as message:
                handler.log.error('no se pudo conectar al servidor ' + str(self.HOST) + ':' + str(self.PORT) + ': %s', message)
                # se comunica con MIS para informar el problema
                
# funciones
def ObtieneEstadoServidor(HOST, PORT):
    try:
        handler.log.debug('obteniendo estado de servidor ' + HOST + ':' + str(PORT))
        ThreadxLAV(HOST, PORT).start()
    except Exception as message:
        handler.log.debug('error al consultar estado del servidor')
        handler.log.exception(message)

def ObtieneEstadoServidores():
    obtieneEstado = 1
    while obtieneEstado:
        try:
            handler.log.info('iniciando obtencion de estado de servidores activos')
            total = MIS.ConsultaTotalServidores()
            for cantidad in total:
                pass
            handler.log.info('obtenidos %i servidores activos', cantidad[0])
            for AOC in MIS.ConsultaListaServidores():
                AOCHOST = AOC[0]
                AOCPORT = AOC[1]
                ObtieneEstadoServidor(AOCHOST, AOCPORT)
        except Exception as message:
            handler.log.error('error al obtener el estado de los servidores activos')
            handler.log.exception(message)
        finally:
            handler.log.info('obtencion de estado de servidores activos finalizada')
            sleep(SLEEPTIME)

def Valida():
    pass
    
def run():
    handler.log.info('iniciando modulo')
    myservidor = Servidor()
    myservidor.run()
    
# main
if __name__ == '__main__':
    run()