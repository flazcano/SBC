"""
Created on 23/10/2011

@author: Fernando

Modulo de Escucha y Obtencion para AOC (ME)
"""

# importaciones
from sys import exit, stdin
from time import sleep
import socket
from select import select
from threading import Thread
from Logger import handler
from modulo import MIS
from MA import EnviaCorreo, EnviaJabber

# definiciones
CLIENTTIMEOUT        = None
SLEEPSERVERACTIVOS   = None
SLEEPSERVERINACTIVOS = None
BINDADDRESS          = None
MEPORT               = None

# clases
class Servidor():
    def __init__(self):
        self.host = BINDADDRESS
        self.port = MEPORT
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
        while running:
            inputready  = select([self.server, stdin],[],[])
            outputready = select([self.server, stdin],[],[]) #@UnusedVariable
            exceptready = select([self.server, stdin],[],[]) #@UnusedVariable
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
            handler.log.debug('cliente conectado desde ' + self.address[0] + ':' + str(self.address[1]));
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
                EnviaJabber("flazcano@paperlessla.com", self.HOST, 1)
                EnviaCorreo("flazcano@paperlessla.com", self.HOST, 1)

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
                EnviaJabber("flazcano@paperlessla.com", self.HOST, 0)
                EnviaCorreo("flazcano@paperlessla.com", self.HOST, 0)
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
            for cantidad in total: pass                
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
            sleep(float(SLEEPSERVERACTIVOS))

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
            sleep(float(SLEEPSERVERINACTIVOS))
            
def Valida():
    pass
    
def run():
    handler.log.info('iniciando modulo')
    myservidor = Servidor()
    myservidor.run()
    
def setCLIENTTIMEOUT(VALUE):
    global CLIENTTIMEOUT; CLIENTTIMEOUT = VALUE
    handler.log.debug('CLIENTTIMEOUT: ' + str(CLIENTTIMEOUT))

def setSLEEPSERVERACTIVOS(VALUE):
    global SLEEPSERVERACTIVOS; SLEEPSERVERACTIVOS = VALUE
    handler.log.debug('SLEEPSERVERACTIVOS: ' + str(SLEEPSERVERACTIVOS))

def setSLEEPSERVERINACTIVOS(VALUE):
    global SLEEPSERVERINACTIVOS; SLEEPSERVERINACTIVOS = VALUE
    handler.log.debug('SLEEPSERVERINACTIVOS: ' + str(SLEEPSERVERINACTIVOS))

def setBINDADDRESS(VALUE):
    global BINDADDRESS; BINDADDRESS = VALUE
    handler.log.debug('BINDADDRESS: ' + BINDADDRESS)

def setMEPORT(VALUE):
    global MEPORT; MEPORT = VALUE
    handler.log.debug('MEPORT: ' + str(MEPORT))

# main
if __name__ == '__main__':
    run()