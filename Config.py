'''
Created on 30/10/2011

@author: Fernando

Sub-Modulo de Gestion de Archivos de Configuracion
'''

# importaciones
import re

# definiciones

# clases

# funciones
def load(filename): # carga un archivo de configuracion
    try: configfile = open(filename, "r")
    except Exception, e: raise e
    try: configtext = configfile.read()
    except Exception, e: raise e
    
    # Compile a pattern that matches our key-value line structure
    pattern = re.compile("\\n([\w_]+)[\t ]*([\w: \\\/~.-]+)")
    
    # Find all matches to this pattern in the text of the config file
    tuples = re.findall(pattern, configtext)
    
    # Create a new dictionary and fill it: for every tuple (key, value) in
    # the 'tuples' list, set ret[key] to value 
    configuraciones = dict()
    for x in tuples:
        configuraciones[x[0]] = x[1]
    
    # Return the fully-loaded dictionary object
    return configuraciones

# main