# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 11:16:54 2022

@author: chene
"""
import json,unicodedata
import pandas as pd

df=pd.read_csv("../Csv/CsvFinal.csv",sep=";")
listAnnee=[]
listRegions=[]
for annee in df.Annee:
    if annee not in listAnnee:
        listAnnee.append(annee)
for region in df.Region:
    if region not in listRegions:
        listRegions.append(region)   
        
def searchForRegion(list,region):
    for i in range(len(list)):
        if("".join((c for c in unicodedata.normalize("NFD",  list[i]["properties"]["nom"]) if unicodedata.category(c) != "Mn"))==region):
           return i
with open("../old/regionsjson.txt",encoding="UTF-8") as json_file:
    data = json.load(json_file)
    
    for annee in listAnnee:
        for nomregion in listRegions:
            ligne=df[(df.Region==nomregion) & (df.Annee==annee)]
            indexregion=searchForRegion(data["features"],nomregion)
            data["features"][indexregion]["properties"]["nom"]= "".join((c for c in unicodedata.normalize("NFD",  data["features"][indexregion]["properties"]["nom"]) if unicodedata.category(c) != "Mn"))
            data["features"][indexregion]["properties"]["population"]=int(ligne["Population"].values[0])
            data["features"][indexregion]["properties"]["nucleaire"]=float(ligne["Parc nucléaire (MW)"].values[0])
            data["features"][indexregion]["properties"]["thermique"]=float(ligne["Parc thermique fossile (MW)"].values[0])
            data["features"][indexregion]["properties"]["hydrolique"]=float(ligne["Parc hydraulique (MW)"].values[0])
            data["features"][indexregion]["properties"]["eolien"]=float(ligne["Parc éolien (MW)"].values[0])
            data["features"][indexregion]["properties"]["solaire"]=float(ligne["Parc solaire (MW)"].values[0])
            data["features"][indexregion]["properties"]["bioenergie"]=float(ligne["Parc bioénergies (MW)"].values[0])
            data["features"][indexregion]["properties"]["essence"]=str(ligne["Essence"].values[0])
            data["features"][indexregion]["properties"]["hybride"]=str(ligne["Hybride"].values[0])
            data["features"][indexregion]["properties"]["diesel"]=str(ligne["diesel"].values[0])
            data["features"][indexregion]["properties"]["gpl"]=str(ligne["GPL"].values[0])
            data["features"][indexregion]["properties"]["electrique"]=str(ligne["electrique"].values[0])
            data["features"][indexregion]["properties"]["autre"]=str(ligne["autre"].values[0])
            data["features"][indexregion]["properties"]["moyenneRegion"]=str(ligne["MoyenneRegion"].values[0])
            
        with open("../Map/regionsjson"+str(annee)+".geojson","w")as file:
            json.dump(data,file)