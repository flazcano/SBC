'''
Created on 31/10/2011

@author: Fernando
'''
# importaciones
import exceptions

# definiciones

# clases
class Error(exceptions.Exception):
    def __init__(self):
        return
        
    def __str__(self):
        pass

# funciones
def main():
    raise Error

# main    
if __name__=="__main__":
    try:
        main()
    except Exception, e:
        raise e