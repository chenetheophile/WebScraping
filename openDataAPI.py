# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 18:21:07 2022

@author: chene
"""
import requests,json,time
import pandas as pd

APIKey="bad227eccf537ed5af09f2939567a801707d42faafb94228f31ac684"


champList=['annee','parc_hydraulique_mw','region','parc_solaire_mw','parc_thermique_fossile_mw','parc_eolien_mw','parc_nucleaire_mw','parc_bioenergies_mw']

urlbase="https://opendata.reseaux-energies.fr/api/v2/catalog/datasets/parc-region-annuel-production-filiere/records?apikey="+APIKey+"&where=annee>=2014&select="

for i in range(len(champList)):
    urlbase+=champList[i]
    if i!=len(champList)-1:
        urlbase+=','
ListRequete=[]
url=urlbase
offset=0
data=json.loads(requests.get(url).text)['records']
while len(data)!=0:
    offset+=20
    for record in data:
        ListRequete.append(record['record']['fields'])
    url=urlbase+"&rows=20&offset="+str(offset)
    data=json.loads(requests.get(url).text)['records']
    time.sleep(1)

df=pd.DataFrame(ListRequete)

print(df.head(10))
print(df.info())

df.to_csv('./Csv/ProductionEergieAPI.csv',sep=";")







