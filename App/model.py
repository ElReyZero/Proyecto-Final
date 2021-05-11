import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.DataStructures import edge as ed
from DISClib.Algorithms.Graphs import bfs
from DISClib.ADT import stack
assert config
from math import radians, cos, sin, asin, sqrt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
import datetime
from JARClib import maxMinDict
from DISClib.DataStructures import adjlist as alt

def newAnalyzer():
    analyzer = {
                'companies': None,
                'taxis': None,
                'dates': None,
                'communityAreas': None, 
                'paths': None
                    }

    analyzer['companies'] = m.newMap(numelements=150,
                                     maptype='PROBING',
                                     comparefunction=compareCompanies)
    
    analyzer['dates'] = om.newMap(omaptype="RBT", comparefunction=compareDates)

    analyzer['communityAreas'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=10000,
                                              comparefunction=compareCAs)
    return analyzer

def getDateTimeTaxiTrip(taxitrip):
    tripstartdate = taxitrip['trip_start_timestamp']
    taxitripdatetime = datetime.datetime.strptime(tripstartdate, '%Y-%m-%dT%H:%M:%S.%f')
    return taxitripdatetime.date(), taxitripdatetime.time()

def newCompany(trip):
    company = {"name": "", "taxis":None, "trips":1}
    company["name"] = trip["company"]
    company["taxis"] = lt.newList("ARRAY_LIST", compareTaxiIdsInt)
    lt.addLast(company["taxis"], trip["taxi_id"])
    return company

def addCompany(analyzer, trip):
    companies = analyzer["companies"]
    companyName = trip["company"]
    existComp = m.get(companies, companyName)
    if existComp is None:
        company = newCompany(trip)
        m.put(companies, companyName, company)
    else:
        entry = m.get(companies, companyName)
        taxiId = trip["taxi_id"]
        info = entry["value"]
        info["trips"] += 1
        taxilst = info["taxis"]
        if lt.isPresent(taxilst, taxiId) == 0:
            lt.addLast(taxilst, taxiId)

def updateDates(map, trip):
    mapa = map["dates"]
    tripdate = trip['trip_start_timestamp']
    taxitripdatetime = datetime.datetime.strptime(tripdate, '%Y-%m-%dT%H:%M:%S.%f')
    entry = om.get(mapa, taxitripdatetime.date())
    if entry is None:
        datentry = newDataEntry(trip)
        om.put(mapa, taxitripdatetime.date(), datentry)
    else:
        datentry = me.getValue(entry)
        updateEntry(trip, datentry)
    return mapa

def newDataEntry(trip):
    entry = {'taxis': None}
    entry['taxis'] = m.newMap(numelements=1000, maptype="PROBING", comparefunction=compareTaxiIdsDict)
    taxidata = lt.newList("ARRAY_LIST")
    if trip["trip_miles"] == "":
        lt.addLast(taxidata, 0)
    else:
        lt.addLast(taxidata, float(trip["trip_miles"]))
    if trip["trip_total"] == "":
        lt.addLast(taxidata, 0)
    else:
        lt.addLast(taxidata, float(trip["trip_total"]))
    lt.addLast(taxidata, 1)
    m.put(entry['taxis'], trip["taxi_id"], taxidata)
    return entry

def updateEntry(trip, datentry):
    taxis = datentry["taxis"]
    existtaxi = m.get(taxis, trip["taxi_id"])
    if existtaxi is None:
        taxidata = lt.newList("ARRAY_LIST")
        if trip["trip_miles"] == "":
            lt.addLast(taxidata, 0)
        else:
            lt.addLast(taxidata, float(trip["trip_miles"]))
        if trip["trip_total"] == "":
            lt.addLast(taxidata, 0)
        else:
            lt.addLast(taxidata, float(trip["trip_total"]))
        lt.addLast(taxidata, 1)
        m.put(taxis, trip["taxi_id"], taxidata)
    else:
        entry = existtaxi["value"]
        if trip["trip_miles"] != "":
            entry["elements"][0] += float(trip["trip_miles"])
        if trip["trip_total"] != "":
            entry["elements"][1] += float(trip["trip_total"])
        entry["elements"][2] += 1
    return datentry

def addTrip(analyzer, trip):
    origin = trip['pickup_community_area']
    destination = trip['dropoff_community_area']
    if origin == "":
        origin = "-1"
    else:
       origin = round(float(origin))
    if destination == "":
        destination = "-1"
    else:
        destination = round(float(destination))
    if trip['trip_seconds'] == "":
        duration = 0
    else:
        duration = float(trip['trip_seconds'])
    horaIni = trip["trip_start_timestamp"]
    horaFin = trip["trip_end_timestamp"]
    if horaIni == "" or horaFin == "":
        pass
    else:
        timeSt = datetime.datetime.strptime(horaIni, '%Y-%m-%dT%H:%M:%S.%f')
        timeEnd = datetime.datetime.strptime(horaFin, '%Y-%m-%dT%H:%M:%S.%f')
        vertOrigen = str(origin)+" - "+str(timeSt.time())
        vertDestino = str(destination)+" - "+str(timeEnd.time())
        addCA(analyzer, vertOrigen)
        addCA(analyzer, vertDestino)
        addConnection(analyzer, vertOrigen, vertDestino, duration)
        return analyzer

def addCA(analyzer, CAid):
    if not gr.containsVertex(analyzer["communityAreas"], CAid):
            gr.insertVertex(analyzer["communityAreas"], CAid)
    return analyzer

def addConnection(analyzer, origin, destination, duration):
    edge = gr.getEdge(analyzer["communityAreas"], origin, destination)
    if edge is None:
        splitOrig = origin.split(" - ")
        splitDest = destination.split(" - ")
        if splitOrig[0] != splitDest[0]:
            gr.addEdge(analyzer["communityAreas"], origin, destination, duration)
        else:
            pass
    else:
        ed.updateAverageWeight(edge, duration) 
    return analyzer    

# ==============================
# Funciones de consulta
# ==============================
def cantTaxis(analyzer):
    companies = m.keySet(analyzer["companies"])
    iterador = it.newIterator(companies)
    cantTax = 0
    while it.hasNext(iterador):
        company = it.next(iterador)
        data = m.get(analyzer["companies"], company)
        cantTax += lt.size(data["value"]["taxis"])
    return cantTax

def cantCompany(analyzer):
    companies = m.keySet(analyzer["companies"])
    num = lt.size(companies)
    return num

def topCompTaxi(analyzer, top):
    companies = m.keySet(analyzer["companies"])
    iterador = it.newIterator(companies)
    dicc1 = {}
    dicc2 = {}
    topTaxis = lt.newList("ARRAY_LIST")
    topServices = lt.newList("ARRAY_LIST")
    num = 1
    while it.hasNext(iterador):
        company = it.next(iterador)
        data = m.get(analyzer["companies"], company)
        cantTax = lt.size(data["value"]["taxis"])
        dicc1[company] = cantTax
        dicc2[company] = data["value"]["trips"]

    while num <= top:
        resultado1 = maxMinDict.maxDicc(dicc1)
        resultado2 = maxMinDict.maxDicc(dicc2)
        inp1 = {resultado1: dicc1[resultado1]}
        inp2 = {resultado2: dicc2[resultado1]}
        lt.addLast(topTaxis, inp1)
        lt.addLast(topServices, inp2)
        dicc1.pop(resultado1)
        dicc2.pop(resultado2)
        num +=1
    return topTaxis, topServices

def topPuntosTaxiSingle(analyzer, fecha, top):
    dateanalyzed = om.get(analyzer['dates'], fecha)
    if dateanalyzed["key"] is not None:
        entry = dateanalyzed["value"]["taxis"]
        llaves = m.keySet(entry)
        iterador = it.newIterator(llaves)
        dicc = {}
        num = 1
        topTaxis = lt.newList("ARRAY_LIST")

        while it.hasNext(iterador):
            taxi = it.next(iterador)
            valor = m.get(entry, taxi)
            data = valor["value"]
            if data["elements"][1] == 0:
                puntos = 0
            else:
                puntos = (data["elements"][0]/data["elements"][1])*data["elements"][2]
            dicc[taxi] = puntos
        
        while num <= top:
            resultado = maxMinDict.maxDicc(dicc)
            inp = {resultado: dicc[resultado]}
            lt.addLast(topTaxis, inp)
            dicc.pop(resultado)
            num += 1
        return topTaxis
    else:
        return None
        

def topPuntosTaxiMultiple(analyzer, dateIni, dateFin, top):
    dateanalyzed1 = om.get(analyzer['dates'], dateIni)
    dateanalyzed2 = om.get(analyzer['dates'], dateFin)
    if dateanalyzed1["key"] is not None and dateanalyzed2["key"]:
        valor = om.keys(analyzer["dates"], dateIni, dateFin)
        iterador = it.newIterator(valor)
        taxis = {}
        topRangoTaxis = lt.newList("ARRAY_LIST")
        num = 1
        while it.hasNext(iterador):
            fecha = it.next(iterador)
            lista = topPuntosTaxiSingle(analyzer, fecha, top)
            iterador2 = it.newIterator(lista)
            while it.hasNext(iterador2):
                taxi = it.next(iterador2)
                if str(taxi.keys()) in str(taxis.keys()):
                    taxis[str(taxi.keys())] += float(taxi.values())
                else:
                    taxis.update(taxi)
        while num <= top:
            resultado = maxMinDict.maxDicc(taxis)
            inp = {resultado: taxis[resultado]}
            lt.addLast(topRangoTaxis, inp)
            taxis.pop(resultado)
            num += 1
        return topRangoTaxis
    else:
        return None
        
def totalEdges(analyzer):
    return gr.numEdges(analyzer['communityAreas'])

def totalStations(analyzer):
    return gr.numVertices(analyzer['communityAreas'])

def minimumCostPaths(analyzer, initialStation):
    if gr.containsVertex(analyzer["communityAreas"], initialStation) == True:
        analyzer['paths'] = djk.Dijkstra(analyzer['communityAreas'], initialStation)
        return analyzer
    else:
        return "0"

def minimumCostPath(analyzer, destStation):
    path = djk.pathTo(analyzer['paths'], destStation)
    return path

def findShortestCAs(analyzer, initCA, destCA, hourStart, hourEnd):
    if hourStart.minute >= 0 and hourStart.minute <= 15:
        horaIni = hourStart.replace(minute=0, second=0, microsecond=0)
    elif hourStart.minute > 15 and hourStart.minute <= 30:
        horaIni = hourStart.replace(minute=15, second=0, microsecond=0)
    elif hourStart.minute > 30 and hourStart.minute <= 45:
        horaIni = hourStart.replace(minute=45, second=0, microsecond=0)
    elif hourStart.minute > 45 and hourStart.minute <= 59:
        horaIni = hourStart.replace(minute=0, second=0, microsecond=0)    
        if hourStart.hour == 23:
            hora = 0
        else:
            hora = hourStart.hour + 1
        horaIni = hourStart.replace(hour=hora, minute=0, second=0, microsecond=0)

    if hourEnd.minute >= 0 and hourEnd.minute <= 15:
        horaFin = hourEnd.replace(minute=0, second=0, microsecond=0)
    elif hourEnd.minute > 15 and hourEnd.minute <= 30:
        horaFin = hourEnd.replace(minute=15, second=0, microsecond=0)
    elif hourEnd.minute > 30 and hourEnd.minute <= 45:
        horaFin = hourEnd.replace(minute=45, second=0, microsecond=0)
    elif hourEnd.minute > 45 and hourEnd.minute <= 59:
        horaFin = hourEnd.replace(minute=0, second=0, microsecond=0)    
        if hourEnd.hour == 23:
            hora = 0
        else:
            hora = hourEnd.hour + 1
        horaFin = hourEnd.replace(hour=hora, minute=0, second=0, microsecond=0)
    
    vertIni = str(initCA)+ " - " + str(horaIni)
    vertDest = str(destCA) + " - " + str(horaFin)
    if gr.containsVertex(analyzer["communityAreas"], vertIni) == True and gr.containsVertex(analyzer["communityAreas"], vertDest) == True:
        minimumCostPaths(analyzer, vertIni)
        path = minimumCostPath(analyzer, vertDest)
        if path is not None:
            tiempo = 0
            iterador2 = it.newIterator(path)
            while it.hasNext(iterador2):
                camino = it.next(iterador2)
                tiempo += camino["weight"]
            return path, tiempo
        else:
            return None, None
    else:
        return False, False
        
             
# ==============================
# Funciones de Comparación
# ==============================

def compareDates(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareTaxiIdsInt(id1, id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareTaxiIdsDict(id1, id2):
    tax = id2['key']
    if (id1 == tax):
        return 0
    elif id1 > tax:
        return 1
    else:
        return -1

def compareCompanies(comp1, comp2):
    est = comp2['key']
    if (comp1 == est):
        return 0
    elif (comp1 > est):
        return 1
    else:
        return -1

def compareCAs(id1, id2):
    id1 = id1
    CA2 = id2['key']
    
    if (id1 == CA2):
        return 0
    elif id1 > CA2:
        return 1
    else:
        return -1

def compareint(int1, int2):
    if (int1 == int2):
        return 0
    else:
        pass