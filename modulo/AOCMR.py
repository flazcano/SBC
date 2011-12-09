'''
Created on 29/10/2011

@author: Fernando

Modulo de Monitorizacion de Recursos para Agente de Obtencion de Cargas (AOCMR)
'''
# importaciones
from sys import exit
from time import sleep, time
from Logger import handler
try: import psutil #@UnresolvedImport
except: handler.log.critical('no se encuentra python-psutil necesario para correr el modulo AOCMR'); exit(1)

# definiciones
AOCMRSLEEPTIME = None
CPU            = None
MEM            = None
IO             = None
NET            = None
HDD            = None
HORA           = None

# clases

# funciones
def getCPU(): # devuelve el valor del % CPU utilizado, mas un arreglo de % utilizacion por CPU
    try:
        miCPU = str(psutil.cpu_percent(interval=1, percpu=False)) + ',' + str(psutil.cpu_percent(interval=1, percpu=True)).replace(" ", "").replace("[", "").replace("]", "")
        return miCPU
    except:
        return ''

def getMEM(): # devuelve un arreglo con la memoria fisica total, la memoria fisica utilizada, la memoria fisica disponible y el % de utilizacion
    try:
        getMEM = psutil.phymem_usage()
        miMEM = str(getMEM[0]) + ',' + str(getMEM[1]) + ',' + str(getMEM[2]) + ',' + str(getMEM[3])
        return miMEM
    except:
        return ''

def getIO(): # devuelve un arreglo con un contador de lecturas IO, un contador de escrituras IO, el total de bits escritos, el total bis leidos, el tiempo de lectura y el tiempo de escritura
    try:
        getIO = psutil.disk_io_counters()
        miIO = str(getIO[0]) + ',' + str(getIO[1]) + ',' + str(getIO[2]) + ',' + str(getIO[3]) + ',' + str(getIO[4]) + ',' + str(getIO[5])
        return miIO
    except:
        return ''

def getNET(): # devuelve un arreglo con la cantidad de bits enviados, la cantidad de bits recibidos, la cantidad de paquetes enviados y la cantidad de paquetes recibidos por las interfaces de red
    try:
        getNET = psutil.network_io_counters(pernic=False)
        miNET = str(getNET[0]) + ',' + str(getNET[1]) + ',' + str(getNET[2]) + ',' + str(getNET[3])
        return miNET
    except:
        return ''

def getHDD(): # devuelve un arreglo de Devices, el cual contiene un arreglo con el device, el espacio total, el espacio utilizado, el espacio disponible y el % de espacio utilizado
    try:
        getDEV = psutil.disk_partitions()
        miHDD = ''
        for dev in range(0, len(getDEV)):
            getHDD = psutil.disk_usage(getDEV[dev][1])
            miHDD = miHDD + getDEV[dev][0] + ',' + str(getHDD[0]) + ',' + str(getHDD[1]) + ',' + str(getHDD[2]) + ',' + str(getHDD[3]) 
            if (dev + 1) < len(getDEV):
                miHDD = miHDD + '-'
        return miHDD
    except:
        return ''

def getCarga():
    miLAV = str(HORA) + ' '  + str(CPU) + ' ' + str(MEM) + ' ' + str(IO) + ' ' + str(NET) + ' ' + str(HDD)
    return miLAV

def ObtieneCarga():
    obtieneLAV = 1
    while obtieneLAV:
        try:
            handler.log.debug('obteniendo CPU')
            global CPU; CPU = str(getCPU())
            sleep(float(AOCMRSLEEPTIME))
            
            handler.log.debug('obteniendo MEM')
            global MEM; MEM = str(getMEM())
            sleep(float(AOCMRSLEEPTIME))
            
            handler.log.debug('obteniendo IO')
            global IO; IO = str(getIO())
            sleep(float(AOCMRSLEEPTIME))
            
            handler.log.debug('obteniendo NET')
            global NET; NET = str(getNET())
            sleep(float(AOCMRSLEEPTIME))
            
            handler.log.debug('obteniendo HDD')
            global HDD; HDD = str(getHDD())
            
            global HORA; HORA = time()
            
            handler.log.debug('carga obtenida correctamente')
            #handler.log.debug('LAV: %s', getCarga())
        except Exception as message:
            handler.log.error('error al obtener carga: %s', message)
            handler.log.exception(message)
        finally:
            sleep(float(AOCMRSLEEPTIME))

def run():
    handler.log.info('iniciando el modulo')
    
    try:
        global CPU; CPU = getCPU()
        global MEM; MEM = str(getMEM())
        global IO ; IO  = str(getIO())
        global NET; NET = str(getNET()) 
        global HDD; HDD = str(getHDD())
        
        global HORA; HORA = time()
    except Exception as message:
        handler.log.error('error al obtener carga: %s', message)
        exit(1)

def setAOCMRSLEEPTIME(VALUE):
    global AOCMRSLEEPTIME; AOCMRSLEEPTIME = VALUE
    handler.log.debug('AOCMRSLEEPTIME : ' + str(AOCMRSLEEPTIME))
    
# main
if __name__ == '__main__':
    getCarga()