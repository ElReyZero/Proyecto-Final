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

def newAnalyzer():
    analyzer = {
                'companies': None,
                'taxis': None,
                'dates': None,
                'comunityAreas': None
                    }

    analyzer['companies'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareCompanies)

    analyzer['taxis'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareTaxiIds)
    
    analyzer['dates'] = om.newMap(omaptype="RBT", comparefunction=compareDates)

    analyzer['communityAreas'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=10000,
                                              comparefunction=compareStations)
    return analyzer


def newCompany(trip):
    company = {"name": "", "taxis":None, "trips":1}
    company["name"] = trip["company"]
    company["taxis"] = lt.newList("ARRAY_LIST", compareTaxiIds)
    lt.addLast(company["taxis"], trip["taxi_id"])
    return company



def addCompany(analyzer, trip):
    companies = analyzer["companies"]
    companyName = trip["company"]
    existComp = m.contains(companies, companyName)
    if existComp is None:
        company = newCompany(trip)
        m.put(companies, companyName, company)
    else:
        entry = m.get(companies, companyName)
        taxiId = trip["taxi_id"]
        info = entry["value"]
        info["trips"] += 1
        taxilst = info["taxis"]
        if lt.isPresent(taxilst, taxiId) is False:
            lt.addLast(taxilst, taxiId)

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

def compareTaxiIds(id1, id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareCompanies(comp1, comp2):
    if (comp1 == comp2):
        return 0
    elif (comp1 > comp2):
        return 1
    else:
        return -1