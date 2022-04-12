# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 21:45:08 2022

@author: chene
"""

"""

Partie Scraping

"""
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import pandas as pd


def CalculMoyenne(list):
    sum=0
    for element in list:
        if type(element)==type(""):
            sum+=int(element)
        else:
            sum+=element
    return sum/len(list)

VilleList=[]
AnneeList=[]
MoyenneList=[]
RegionList=[]
nomRegion=["Ile-de-France","Centre-Val de Loire","Bourgogne-Franche-Comte","Normandie","Hauts-de-France","Grand Est",
                "Pays de la Loire","Bretagne","Nouvelle-Aquitaine","Occitanie","Auvergne-Rhone-Alpes","Provence-Alpes-Cote d'Azur","Corse"]
site=["https://aqicn.org/map/france/en/","https://e.infogram.com/d106e364-d435-4e45-8a64-e059d8f4d5e8?parent_url=https%3A%2F%2Fwww.automobile-propre.com%2Fdossiers%2Fchiffres-vente-immatriculations-france%2F&src=embed#async_embed"]
driver = webdriver.Firefox()
ImmatriculationsElectrique={}
Pollutiondelair={}
for url in site:
    driver.get(url)
    time.sleep(2)
    if url is site[0]:
        villeAScrap=["Paris","Saint-Denis a1","Tours Joue les Tours","Orleans St Jean de Braye","Dijon","Besancon","Havre parc de brotonne","Rouen","Lille fives","Amiens",
          "Reims Jean d'Aulan","Mulhouse sud","Nantes","Angers","Rennes","Brest Jean","Talence","Poitier","Toulouse","Montpellier","Lyon Centre",
          "Saint-etienne sud","Marseille rabatau","Nice","Bastia montesoro"]
        for nom in villeAScrap:
            time1=time.perf_counter()
            recherche=driver.find_element(By.ID,"full-page-search-input")
            time.sleep(2)
            recherche.send_keys(nom)
            time.sleep(3)
            recherche.location_once_scrolled_into_view
            time.sleep(3)
            driver.find_element(By.ID,"searchResults").find_element(By.TAG_NAME,"a").click()
            time.sleep(2)
            driver.find_element(By.ID,"h1header3").location_once_scrolled_into_view
            time.sleep(2)
            donneeshistorique=driver.find_element(By.CLASS_NAME,"historical-yearly-data")
            time.sleep(2)
            Annee=donneeshistorique.find_elements(By.CLASS_NAME,"year-divider")
            marqueurAnnee=[]
            time.sleep(2)
            ligneTab=donneeshistorique.find_elements(By.TAG_NAME,"tr")
            time.sleep(2)
            for element in Annee:
                marqueurAnnee.append(element.text)
            time.sleep(1)
            anneeDic={}
            diction={}
            for i in range(len(ligneTab)-1,-1,-1):  
                    if ligneTab[i].get_attribute("class")=="year-divider":
                        diction[ligneTab[i].text]=(anneeDic)
                        Pollutiondelair[nom.split(" ")[0]]=diction
                        anneeDic={}
                    else:
                        mois=[]
                        carre=ligneTab[i].find_elements(By.CLASS_NAME,"squares")
                        time.sleep(1)
                        for element in carre:
                            text=element.find_elements(By.TAG_NAME,"text")
                            for balise in text:
                                if balise.text!="-" and balise.text!="-":
                                    mois.append(balise.text)
                        labelmois=ligneTab[i].find_element(By.TAG_NAME,"td").text
                        if labelmois!="-" and labelmois!="" :
                            anneeDic[labelmois]=mois
            temps=(time.perf_counter()-time1)
            print("nombre de seconde pour "+nom+":"+str(temps))
            
        iter=0
        for ville in Pollutiondelair:
            for anneeVille in Pollutiondelair[ville]:
                SommeMoyenne=0
                for mois in Pollutiondelair[ville][anneeVille]:
                    if len(Pollutiondelair[ville][anneeVille][mois])!=0:
                        SommeMoyenne+=CalculMoyenne(Pollutiondelair[ville][anneeVille][mois])
                if len(Pollutiondelair[ville][anneeVille])!=0:
                    MoyenneList.append(SommeMoyenne/len(Pollutiondelair[ville][anneeVille]))
                AnneeList.append(anneeVille)
                VilleList.append(ville)
                RegionList.append(nomRegion[iter])
            if ville in ["Saint-Denis","Orleans","Besancon","Rouen","Amiens","Mulhouse","Angers","Brest","Poitier","Montpellier","Saint-etienne","Nice"]:
                iter+=1
        df=pd.DataFrame({"Annee":AnneeList,"Region":RegionList,"Ville":VilleList,"Moyenne Annuel":MoyenneList}).to_csv("../Csv/QualiteAir.csv",sep=";")

"""

Partie Merge Données

"""
import pandas as pd
dfProduction=pd.read_csv("../Csv/parc-region-annuel-production-filiere.csv",sep=";")
dfProduction=dfProduction.drop(["Code INSEE région","Géo-shape région","Géo-point région"],axis=1)
dfProduction=dfProduction.fillna(0)

dfImmatriculations=pd.read_csv("../Csv/ImmatriculationsTypeEnergieRegion.csv",sep=";")


dfPopulation=pd.read_csv("../Csv/region_habitant.csv",sep=";")

Population=[]

dfQualite=pd.read_csv("../Csv/QualiteAir.csv",sep=";")

nomRegion=["Ile-de-France","Centre-Val de Loire","Bourgogne-Franche-Comte","Normandie","Hauts-de-France","Grand Est",
                "Pays de la Loire","Bretagne","Nouvelle-Aquitaine","Occitanie","Auvergne-Rhone-Alpes","Provence-Alpes-Cote d'Azur","Corse"]
moyenneRegion=[]
Region=[]
listAnnee=[]
for region in nomRegion:
    tabAnnee=[]
    for annee in dfQualite.loc[lambda ligne:ligne["Region"]==region]["Annee"]:
        if annee not in tabAnnee:
            tabAnnee.append(annee)
    for element in tabAnnee:
        listAnnee.append(element)
        moyenneRegion.append(dfQualite.loc[lambda ligne:ligne["Annee"]==element].loc[lambda ligne:ligne["Region"]==region,"Moyenne Annuel"].mean())
        Region.append(region)
df=pd.DataFrame({"Annee":listAnnee,"MoyenneRegion":moyenneRegion,"Region":Region})

df=pd.merge(df,dfPopulation,on=["Annee","Region"],how="inner")

df=pd.merge(df,dfProduction,on=["Annee","Region"],how="inner")
df=pd.merge(df,dfImmatriculations,on=["Annee","Region"],how="inner")
df.to_csv("../Csv/CsvFinal.csv",sep=";")



"""


Evolution des ventes de véhicules électrique par région



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




"""

Partie Map 

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




















