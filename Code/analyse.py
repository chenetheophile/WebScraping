# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 11:16:37 2022

@author: chene
"""

import pandas as pd
import matplotlib.pyplot as plt
df= pd.read_csv("../Csv/donneeSansBiais.csv", sep=";") #copie pour éviter de charger le programme a chaque fois

#tri par année :
df.sort_values(["Annee"], axis=0,ascending=[True], inplace=True)
df= df.reset_index(drop=True)
print(df)

Regions=df['Region']
Annee=df['Annee']
ListeRegions=[]
list_date = [] 
for element in Annee:
    if element not in list_date:
        list_date.append(element)
for region in Regions:
    if region not in ListeRegions:
        ListeRegions.append(region)
for region in ListeRegions:
    dfregion = df[(df.Region == region)]
    list_elec_region= dfregion["electrique"].to_list()
    plt.plot(list_date,list_elec_region,label=region)
    plt.rc('legend', fontsize= 6)
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.xlabel('Année')
    plt.ylabel('nombre de véhicules éléctriques vendus')
    plt.title('Evolution de la vente de véhicules électriques en France')
plt.show()


for region in ListeRegions:
    dfregion = df[(df.Region == region)]
    list_elec_region= dfregion["electrique_pop"].to_list()
    plt.plot(list_date,list_elec_region,label=region)
    plt.rc('legend', fontsize= 6)
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.xlabel('Année')
    plt.ylabel('% de population ayant réalisé un achat de voiture électrique')
    plt.title('Evolution de la vente de véhicules électriques en France')
plt.show()


for region in ListeRegions:
    dataFrame_region = df[(df.Region == region)]
    list_aqi_region= dataFrame_region["MoyenneRegion"].to_list()
    plt.plot(list_date,list_aqi_region,label=region)
    plt.rc('legend', fontsize= 6)
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.xlabel('Année')
    plt.ylabel("Indice de la qualité de l'air AQI")
    plt.title("Evolution de la qualité de l'air en France métropolitaine")
plt.show()

for region in ListeRegions:
    dfregion = df[(df.Region == region)]
    list_elec_region= dfregion["electrique_pop"].to_list()
    list_elec_echelle=[]
    for element in list_elec_region:
        misaechelle = element *1000
        list_elec_echelle.append(misaechelle)
    plt.plot(list_date,list_elec_echelle,label='Vente vehicules éléctriques')
    list_aqi_region= dfregion["MoyenneRegion"].to_list()
    plt.plot(list_date,list_aqi_region,label='Indice AQI')
    plt.rc('legend', fontsize= 6)
    plt.legend()
    plt.xlabel('Année')
    plt.ylabel("Indice de la qualité de l'air AQI" + "\n" + "Pourcentage *1000 de la population achetant un véhicule électrique")
    plt.title("Région" + " " + region )
    plt.show()
    

for region in ListeRegions:
    df_idf = df[(df.Region == region)]
    list_annee = df_idf["Annee"]
    list_list_idf = [df_idf[i].to_list() for i in df_idf.columns[6:11]]
    list_c = ["red", "blue","green", "orange", "purple","black"]
    list_moy = (df_idf["MoyenneRegion"].to_list())
    list_moy = [i*100 for i in list_moy]
    for i in range(5):
        plt.plot(list_annee, list_list_idf[i], color = list_c[i], label = df_idf.columns[i+6])
    plt.plot(list_annee, list_moy, color = "red", linestyle = "-." , label = "pollution")
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.xlabel('Année')
    plt.ylabel('Energie produite en MW ')
    plt.title("Evolution de l'AQI selon les énergies produites en" + " " + region)
    plt.show()
    
Regions=df['Region']
Annee=df['Annee']
ListeRegions=[]
list_date = [] 
for element in Annee:
    if element not in list_date:
        list_date.append(element)
for region in Regions:
    if region not in ListeRegions:
        ListeRegions.append(region)
for region in ListeRegions:
    dfregion = df[(df.Region == region)]
    list_elec_region= dfregion["Parc solaire (MW)"].to_list()
    plt.plot(list_date,list_elec_region,label=region)
    plt.rc('legend', fontsize= 6)
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.xlabel('Année')
    plt.ylabel('Energie produite en MW')
    plt.title("Evolution de la production d'energie solaire en France")
plt.show()