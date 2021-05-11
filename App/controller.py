import config as cf
from App import model
import csv
import os
import datetime

def init():
    analyzer = model.newAnalyzer()
    return analyzer

def loadTrips(analyzer):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(analyzer, filename)
    return analyzer

def loadFile(analyzer, tripfile):
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addCompany(analyzer, trip)
        model.updateDates(analyzer, trip)
        model.addTrip(analyzer, trip)
    return analyzer

def cantTaxis(analyzer):
    return model.cantTaxis(analyzer)

def cantComp(analyzer):
    return model.cantCompany(analyzer)

def topCompTaxi(analyzer, top):
    return model.topCompTaxi(analyzer, top)

def topPuntosTaxiSingle(analyzer, date, top):
    fecha = datetime.datetime.strptime(date, '%Y-%m-%d')
    return model.topPuntosTaxiSingle(analyzer, fecha.date(), top)

def topPuntosTaxiMultiple(analyzer, dateIni, dateFin, top):
    fechaIni = datetime.datetime.strptime(dateIni, '%Y-%m-%d')
    fechaFin = datetime.datetime.strptime(dateFin, '%Y-%m-%d')
    return model.topPuntosTaxiMultiple(analyzer, fechaIni.date(), fechaFin.date(), top)

def findShortestCAs(analyzer, initCA, destCA, horaIni, horaFin):
    horaI = datetime.datetime.strptime(horaIni, "%H:%M")
    horaF = datetime.datetime.strptime(horaFin, "%H:%M")
    return model.findShortestCAs(analyzer, initCA, destCA, horaI.time(), horaF.time())
