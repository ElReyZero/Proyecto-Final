import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from time import process_time
assert config
from DISClib.DataStructures import listiterator as it
from DISClib.ADT.graph import gr

initialStation = None
recursionLimit = 20000

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información")
    print("3- Información sobre compañías y taxis / top de compañías con más servicios y taxis")
    print("4- Top de taxis con más puntos en ciertas fechas")
    print("5- Horario entre community areas")
    print("0- Salir")
    print("*******************************************")

def printPoints():
    print("*******************************************")
    print("1- Top de taxis con más puntos para una fecha determinada")
    print("2- Top de taxis con más puntos para un rango de fechas")
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
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
        sys.setrecursionlimit(recursionLimit)
    elif int(inputs[0]) == 3:
        top = int(input("Ingrese la cantidad de compañías mostradas en el top: "))
        cantTax = controller.cantTaxis(cont)
        cantComp = controller.cantComp(cont)
        topTaxi, topServices = controller.topCompTaxi(cont, top)
        print("Cantidad total de taxis reportados: {0}".format(cantTax))
        print("Cantidad total de compañías con un taxi inscrito: {0}".format(cantComp))
        print("\nEl top {0} de compañías con más taxis es: ".format(top))
        iterador1 = it.newIterator(topTaxi)
        num = 1
        while it.hasNext(iterador1):
            taxi = it.next(iterador1)
            print("{0}. {1} con {2} taxis.".format(num, list(taxi.keys())[0], list(taxi.values())[0]))
            num += 1
        print("\nEl top {0} de compañías con más servicios es: ".format(top))
        iterador2 = it.newIterator(topServices)
        num = 1
        while it.hasNext(iterador2):
            service = it.next(iterador2)
            print("{0}. {1} con {2} servicios.".format(num, list(service.keys())[0], list(service.values())[0]))
            num += 1
    elif int(inputs[0]) == 4:
        printPoints()
        dec = input('Seleccione una opción para continuar\n>')
        if dec == "1":
            fecha = input("Entre la fecha a buscar (Formato: YYYY-MM-DD): ")
            top = int(input("Ingrese la cantidad de taxis mostrados en el top: "))
            print("\nBuscando taxis dentro de la fecha {0}".format(fecha))
            res = controller.topPuntosTaxiSingle(cont, fecha, top)
            if res is not None:
                iterador1 = it.newIterator(res)
                num = 1
                while it.hasNext(iterador1):
                    taxi = it.next(iterador1)
                    print("{0}. Taxi ID: {1}\nCantidad de puntos: {2}\n".format(num, list(taxi.keys())[0], list(taxi.values())[0]))
                    num += 1
            else:
                print("La fecha ingresada no existe.")
        elif dec == "2":
            fechaIni = input("Entre la fecha inicial a buscar (Formato: YYYY-MM-DD): ")
            fechaFin = input("Entre la fecha final a buscar (Formato: YYYY-MM-DD): ")
            top = int(input("Ingrese la cantidad de taxis mostrados en el top: "))
            print("\nBuscando taxis dentro de la fechas {0} y {1}".format(fechaIni, fechaFin))
            res = controller.topPuntosTaxiMultiple(cont, fechaIni, fechaFin, top)
            if res is not None:
                iterador1 = it.newIterator(res)
                num = 1
                while it.hasNext(iterador1):
                    taxi = it.next(iterador1)
                    print("{0}. Taxi ID: {1}\nCantidad de puntos: {2}\n".format(num, list(taxi.keys())[0], list(taxi.values())[0]))
                    num += 1
            else:
                print("Alguna de las fechas no existen.")

    elif int(inputs[0]) == 5:
        CAOrigen = int(input("Ingrese la 'Community Area' de origen: "))
        CADest = int(input("Ingrese la 'Community Area' de destino: "))
        horaIni = input("Entre la hora inicial a buscar (Formato: HH:MM): ")
        horaFin = input("Entre la hora final a buscar (Formato: HH:MM): ")
        path, tiempo = controller.findShortestCAs(cont, CAOrigen, CADest, horaIni, horaFin)
        if path is not None:
            print("\nLa ruta encontrada es la siguiente: ")
            iterador = it.newIterator(path)
            while it.hasNext(iterador):
                element = it.next(iterador)
                vertA = element["vertexA"]
                print("'Community Area': ID {0}".format(vertA))
                if it.hasNext(iterador) is False:
                    print("'Community Area': ID {0}".format(element["vertexB"]))
            print("El tiempo estimado en viaje es de: {0} segundos o {1} minutos.".format(round(tiempo), round(tiempo/60)))
        elif path is None:
            print("No se encontró camino entre las 'Community Areas' en el horario introducido.")
        else:
            print("Alguna de las 'Community Areas' introducidas no existe.")
            
    else:
        sys.exit(0)
sys.exit(0)
