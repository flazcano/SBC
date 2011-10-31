"""
Created on 23/10/2011

@author: Fernando

Modulo de Escucha y Obtencion para AOC (ME)
"""

# importaciones
import select, socket, MIS
from sys import exit, stdin
from threading import Thread
from Logger import handler

# definiciones
CLIENTTIMEOUT = 5

# clases
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
            handler.log.debug('conectado desde ' + self.address[0] + ':' + str(self.address[1]));
            running = 1
            while running:
                data = self.client.recv(self.size)
                if data:
                    if data == 'HELLO':
                        handler.log.debug('cliente ' + self.address[0] + ':' + str(self.address[1]) + ' envia alive signal')
                        # se comunica con MIS para agregar cliente a servidores a balancear
                        MIS.agregaServidor(self.address[0], self.address[1])
                    else:
                        pass
                        #handler.log.debug('se descarta el mensaje, cliente ' + self.address[0] + ':' + str(self.address[1]) + ' envia: ' + data)
                else:
                    handler.log.debug('desconectado desde ' + self.address[0] + ':' + str(self.address[1]))
                    self.client.close()
                    # cerrando el hilo
                    running = 0
        except socket.error, (message):
            handler.log.debug('error de conexion de ' + self.address[0] + ':' + str(self.address[1]) + ': %s', message)
        finally:
            if self.client:
                self.client.close()

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
                clientcon.send(':)')
                LAV = clientcon.recv(1024)
                handler.log.debug('se obtuvo LAV desde ' + self.HOST + ':' +str(self.PORT) + ': ' + LAV)
                # se comunica con MIS para agregar LAV
            except Exception, (message):
                handler.log.error('no se pudo conectar al servidor ' + self.HOST + ':' + str(self.PORT) + ': %s', message)
                # se comunica con MIS para informar el problema
                
# funciones
def obtieneEstadoServidor(HOST, PORT):
    try:
        handler.log.debug('obteniendo estado de servidor ' + HOST + ':' + str(PORT))
        ThreadxLAV(HOST, PORT).start()
    except Exception, (message):
        handler.log.debug('error al consultar estado del servidor')
        handler.log.exception(message)

def obtieneEstadoServidores():
    try:
        handler.log.info('iniciando obtencion de estado de servidores activos')
        for total in MIS.consultaTotalServidores():
            pass
        handler.log.info('obtenidos %i servidores activos', total[0])
        for servidor in MIS.consultaListaServidores():
            obtieneEstadoServidor(servidor[0], servidor[1])
    except Exception, (message):
        handler.log.debug('error al obtener el estado de los servidores activos')
        handler.log.exception(message)
    finally:
        handler.log.info('obtencion de estado de servidores activos finalizada')

def valida():
    pass
    
def run():
    handler.log.info('iniciando modulo')
    myservidor = Servidor()
    myservidor.run()
    
# main    