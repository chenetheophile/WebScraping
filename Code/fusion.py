# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 11:16:11 2022

@author: chene
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
