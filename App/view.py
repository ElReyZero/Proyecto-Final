import sys
from App import controller
from DISClib.ADT import stack
import timeit
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from time import process_time 

initialStation = None
recursionLimit = 20000

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información")
    print("3- Pendiente")
    print("4- Pendiente")
    print("5- Pendiente")
    print("0- Salir")
    print("*******************************************")

"""
Menú principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        t1_start = process_time()
        print("\nCargando información de accidentes ....")
        controller.loadTrips(cont)
        t1_stop = process_time()
        """
        print('Accidentes cargados: ' + str(controller.accidentsSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")"""
    elif int(inputs[0]) == 3:
        pass
    elif int(inputs[0]) == 4:
        pass
    elif int(inputs[0]) == 5:
        pass
    else:
        sys.exit(0)
sys.exit(0)
