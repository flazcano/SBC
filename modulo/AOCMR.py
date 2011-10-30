'''
Created on 29/10/2011

@author: Fernando

Modulo de Monitorizacion de Recursos para Agente de Obtencion de Cargas (AOCMR)
'''

import psutil

# devuelve el valor del % CPU utilizado, mas un arreglo de % utilizacion por CPU
def CPU():
    try:
        miCPU = '[' + '[' + str(psutil.cpu_percent(interval=1, percpu=False)) + ']' + ', ' + str(psutil.cpu_percent(interval=1, percpu=True)) + ']'
        return miCPU 
    except:
        return '[]'

# devuelve un arreglo con la memoria fisica total, la memoria fisica utilizada, la memoria fisica disponible y el % de utilizacion
def MEM():
    try:
        getMEM = psutil.phymem_usage()
        miMEM = '[' + str(getMEM[0]) + ', ' + str(getMEM[1]) + ', ' + str(getMEM[2]) + ', ' + str(getMEM[3]) + ']'
        return miMEM
    except:
        return '[]'

# devuelve un arreglo con un contador de lecturas IO, un contador de escrituras IO, el total de bits escritos, el total bis leidos, el tiempo de lectura y el tiempo de escritura
def IO():
    try:
        getIO = psutil.disk_io_counters()
        miIO = '[' + str(getIO[0]) + ', ' + str(getIO[1]) + ', ' + str(getIO[2]) + ', ' +str(getIO[3]) + ']'
        return miIO
    except:
        return '[]'

# devuelve un arreglo con la cantidad de bita enviados, la cantidad de bita recibidos, la cantidad de paquetes enviados y la cantidad de paquetes recibidos por las interfaces de red
def NET():
    try:
        getNET = psutil.network_io_counters(pernic=False)
        miNET = '[' + str(getNET[0]) + ', ' + str(getNET[1]) + ', ' + str(getNET[2]) + ', ' + str(getNET[3]) + ']'
        return miNET
    except:
        return '[]'


# devuelve un arreglo de Devices, el cual contiene un arreglo con el device, el espacio total, el espacio utilizado, el espacio disponible y el % de espacio utilizado
def HDD():
    try:
        getDEV = psutil.disk_partitions()
        miHDD = '['
        for dev in range(0, len(getDEV)):
            getHDD = psutil.disk_usage(getDEV[dev][1])
            miHDD = miHDD + '[' + getDEV[dev][0] + ', ' + str(getHDD[0]) + ', ' + str(getHDD[1]) + ', ' + str(getHDD[2]) + ', ' + str(getHDD[3]) + ']' 
            if dev < len(getDEV):
                miHDD = miHDD + ', '
        miHDD = miHDD + ']'
        return miHDD
    except:
        return '[]'

def LAV():
    return '[' + str(CPU()) + ', ' + str(MEM()) + ', ' + str(IO()) + ', ' + str(NET()) + ', ' + str(HDD()) + ']'