"""
Created on 23/10/2011

@author: Fernando

Modulo de Escucha y Obtencion para AOC (ME)
"""

# importaciones
import socket
from select import select
from time import sleep
from sys import exit, stdin
from threading import Thread
from Logger import handler
from modulo import MIS

# definiciones
CLIENTTIMEOUT = 10
SLEEPSERVIDORESACTIVOS = 40
SLEEPSERVIDORESINACTIVOS = 25
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
        input = [self.server, stdin] #@ReservedAssignment
        running = 1
        while running:
            inputready, outputready, exceptready = select(input,[],[]) #@UnusedVariable
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

class ThreadxCarga(Thread):
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
                MIS.ServidorConProblemas(self.HOST, self.PORT)

class ThreadxConexion(Thread):
        def __init__(self, HOST, PORT):
            Thread.__init__(self)
            self.HOST = HOST
            self.PORT = PORT

        def run(self):
            try:
                clientcon = socket.socket()
                clientcon.settimeout(CLIENTTIMEOUT)
                clientcon.connect((self.HOST, self.PORT))
                handler.log.debug('se pudo volver a conectar al servidor ' + str(self.HOST) + ':' +str(self.PORT))
                # se comunica con MIS para agregar LAV
                MIS.ServidorVuelveActivo(self.HOST, self.PORT)
            except Exception as message:
                handler.log.error('no se pudo conectar al servidor ' + str(self.HOST) + ':' + str(self.PORT) + ': %s', message)
                                
# funciones
def ObtieneCargaServidor(HOST, PORT):
    try:
        handler.log.debug('obteniendo carga de servidor ' + HOST + ':' + str(PORT))
        ThreadxCarga(HOST, PORT).start()
    except Exception as message:
        handler.log.debug('error al consultar carga del servidor')
        handler.log.exception(message)

def ObtieneConexionServidorInactivo(HOST, PORT):
    try:
        handler.log.debug('obteniendo conexion con servidor ' + HOST + ':' + str(PORT))
        ThreadxConexion(HOST, PORT).start()
    except Exception as message:
        handler.log.debug('error al consultar conexion del servidor')
        handler.log.exception(message)
        
def ObtieneEstadoServidoresActivos():
    obtieneEstado = 1
    while obtieneEstado:
        try:
            handler.log.info('iniciando obtencion de estado de servidores activos')
            total = MIS.ConsultaTotalServidoresActivos()
            for cantidad in total:
                pass
            handler.log.info('obtenidos %i servidores activos', cantidad[0])
            for AOC in MIS.ConsultaServidoresActivos():
                AOCHOST = AOC[0]
                AOCPORT = AOC[1]
                ObtieneCargaServidor(AOCHOST, AOCPORT)
        except Exception as message:
            handler.log.error('error al obtener el estado de los servidores activos')
            handler.log.exception(message)
        finally:
            handler.log.info('obtencion de estado de servidores activos finalizada')
            sleep(SLEEPSERVIDORESACTIVOS)

def ObtieneEstadoServidoresInactivos():
    obtieneEstado = 1
    while obtieneEstado:
        try:
            handler.log.info('iniciando obtencion de estado de servidores inactivos')
            total = MIS.ConsultaTotalServidoresInactivos()
            for cantidad in total:
                pass
            handler.log.info('obtenidos %i servidores inactivos', cantidad[0])
            for AOC in MIS.ConsultaServidoresInactivos():
                AOCHOST = AOC[0]
                AOCPORT = AOC[1]
                ObtieneConexionServidorInactivo(AOCHOST, AOCPORT)
        except Exception as message:
            handler.log.error('error al obtener el estado de los servidores inactivos')
            handler.log.exception(message)
        finally:
            handler.log.info('obtencion de estado de servidores inactivos finalizada')
            sleep(SLEEPSERVIDORESINACTIVOS)
            
def Valida():
    pass
    
def run():
    handler.log.info('iniciando modulo')
    myservidor = Servidor()
    myservidor.run()
    
# main
if __name__ == '__main__':
    run()