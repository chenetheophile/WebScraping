# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 21:45:08 2022

@author: chene
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
site=['https://aqicn.org/map/france/en/',"https://e.infogram.com/d106e364-d435-4e45-8a64-e059d8f4d5e8?parent_url=https%3A%2F%2Fwww.automobile-propre.com%2Fdossiers%2Fchiffres-vente-immatriculations-france%2F&src=embed#async_embed"]
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
        # villeAScrap=["Paris"]
        for nom in villeAScrap:
            time1=time.perf_counter()
            recherche=driver.find_element(By.ID,'full-page-search-input')
            time.sleep(2)
            recherche.send_keys(nom)
            time.sleep(3)
            recherche.location_once_scrolled_into_view
            time.sleep(3)
            driver.find_element(By.ID,'searchResults').find_element(By.TAG_NAME,'a').click()
            time.sleep(2)
            driver.find_element(By.ID,'h1header3').location_once_scrolled_into_view
            time.sleep(2)
            donneeshistorique=driver.find_element(By.CLASS_NAME,'historical-yearly-data')
            time.sleep(2)
            Annee=donneeshistorique.find_elements(By.CLASS_NAME,'year-divider')
            marqueurAnnee=[]
            time.sleep(2)
            ligneTab=donneeshistorique.find_elements(By.TAG_NAME,'tr')
            time.sleep(2)
            for element in Annee:
                marqueurAnnee.append(element.text)
            time.sleep(1)
            anneeDic={}
            diction={}
            for i in range(len(ligneTab)-1,-1,-1):  
                    if ligneTab[i].get_attribute('class')=="year-divider":
                        diction[ligneTab[i].text]=(anneeDic)
                        Pollutiondelair[nom.split(" ")[0]]=diction
                        anneeDic={}
                    else:
                        mois=[]
                        carre=ligneTab[i].find_elements(By.CLASS_NAME,'squares')
                        time.sleep(1)
                        for element in carre:
                            text=element.find_elements(By.TAG_NAME,'text')
                            for balise in text:
                                if balise.text!="-" and balise.text!="-":
                                    mois.append(balise.text)
                        labelmois=ligneTab[i].find_element(By.TAG_NAME,'td').text
                        if labelmois!="-" and labelmois!="" :
                            anneeDic[labelmois]=mois
            temps=(time.perf_counter()-time1)
            print('nombre de seconde pour '+nom+':'+str(temps))
            
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
            if ville in ['Saint-Denis','Orleans','Besancon','Rouen','Amiens','Mulhouse','Angers','Brest','Poitier','Montpellier','Saint-etienne','Nice']:
                iter+=1
        df=pd.DataFrame({'Annee':AnneeList,'Region':RegionList,'Ville':VilleList,"Moyenne Annuel":MoyenneList}).to_csv("Pollution2.csv",sep=";")

"""

Partie Merge Donnée

"""
dfProduction=pd.read_csv("parc-region-annuel-production-filiere.csv",sep=";")
dfProduction=dfProduction.drop(["Code INSEE région","Géo-shape région","Géo-point région"],axis=1)
dfProduction=dfProduction.fillna(0)

dfImmatriculations=pd.read_csv("ImmatriculationsTypeEnergieRegion.csv",sep=";")
print(dfImmatriculations.info())

dfPopulation=pd.read_csv("région_habitant.csv",sep=";")

Population=[]

dfQualite=pd.read_csv("Pollution2.csv",sep=";")
nomRegion=["Ile-de-France","Centre-Val de Loire","Bourgogne-Franche-Comte","Normandie","Hauts-de-France","Grand Est",
                "Pays de la Loire","Bretagne","Nouvelle-Aquitaine","Occitanie","Auvergne-Rhone-Alpes","Provence-Alpes-Cote d'Azur","Corse"]
moyenneRegion=[]
Region=[]
listAnnee=[]
for region in nomRegion:
    tabAnnee=[]
    for annee in dfQualite.loc[lambda ligne:ligne['Region']==region]["Annee"]:
        if annee not in tabAnnee:
            tabAnnee.append(annee)
    for element in tabAnnee:
        listAnnee.append(element)
        moyenneRegion.append(dfQualite.loc[lambda ligne:ligne['Annee']==element].loc[lambda ligne:ligne['Region']==region,'Moyenne Annuel'].mean())
        Region.append(region)

df=pd.DataFrame({'Annee':listAnnee,'MoyenneRegion':moyenneRegion,'Region':Region})
print(df.count())
df=pd.merge(df,dfPopulation,on=["Annee","Region"],how='inner')
df=pd.merge(df,dfProduction,on=["Annee","Region"],how='inner')
df=pd.merge(df,dfImmatriculations,on=["Annee","Region"],how='inner')
print(df.to_csv("Donneefusionner.csv",sep=";"))