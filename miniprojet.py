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

site=['https://aqicn.org/map/france/fr/',"https://e.infogram.com/d106e364-d435-4e45-8a64-e059d8f4d5e8?parent_url=https%3A%2F%2Fwww.automobile-propre.com%2Fdossiers%2Fchiffres-vente-immatriculations-france%2F&src=embed#async_embed"]
driver = webdriver.Firefox()
ImmatriculationsElectrique={}
Pollutiondelair={}
for url in site:
    driver.get(url)
    time.sleep(2)
    if url is site[0]:
        # ville=['Paris','Marseille','Lyon','Toulouse','Nice','Nantes','Montpellier','Strasbourg','Bordeaux','Lille','Rennes',
        #         'Reims','Toulouse','Saint-Étienne','Le Havre', 'Grenoble', 'Dijon','Angers','Saint-Denis','Villeurbanne',
        #         'Nîmes','Clermont-Ferrand','Aix-en-Provence','Le Mans','Brest','Tours','Amiens','Limoges','Annecy',
        #         'Boulogne-Billancourt','Perpignan','Metz','Besançon','Orléans','Rouen','Montreuil','Argenteuil',
        #         'Mulhouse','Caen',	'Nancy','Saint-Paul','Roubaix','Tourcoing',	'Nanterre','Vitry-sur-Seine','Nouméa',
        #         'Créteil','Avignon','Poitiers','Aubervilliers','Asnières-sur-Seine','Aulnay-sous-Bois']
        ville=['Paris','Marseille','Lyon Centre','Toulouse','Nice','Nantes','Montpellier','Strasbourg est','Talence','Lille fives','Rennes']
        for nom in ville:
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
            annee={}
            diction={}
            for i in range(len(ligneTab)-1,-1,-1):  
                    if ligneTab[i].get_attribute('class')=="year-divider":
                        diction[ligneTab[i].text]=(annee)
                        Pollutiondelair[nom]=diction
                        annee={}
                    else:
                        mois=[]
                        carre=ligneTab[i].find_elements(By.CLASS_NAME,'squares')
                        time.sleep(1)
                        for element in carre:
                            text=element.find_elements(By.TAG_NAME,'text')
                            for balise in text:
                                mois.append(balise.text)
                        annee[ligneTab[i].find_element(By.TAG_NAME,'td').text]=mois
            temps=(time.perf_counter()-time1)
            print('nombre de seconde pour '+nom+':'+str(temps))
        pd.DataFrame(Pollutiondelair).to_csv("Pollution.csv",sep=";")
    else:
        annee=[]
        menu=Select(driver.find_element(By.TAG_NAME,"select"))
        opt=menu.options
        for op in opt:
            annee.append(op.text)
        options=len(menu.options)
        for i in range(options):
            valeur={}
            driver.find_element_by_css_selector("div[class='igc-tab-switcher igc-tab-switcher__left']").click()
            time.sleep(5)
            mois=driver.find_element(By.CLASS_NAME,'igc-graph-group').find_elements(By.TAG_NAME,'text')
            labelMois=driver.find_element(By.CLASS_NAME,'igc-x-axis-text').find_elements(By.TAG_NAME,'text')
            for j in range(len(mois)):
                valeur[labelMois[j].text]=mois[j].text
            ImmatriculationsElectrique[annee[options-i-1]]=(valeur)
        pd.DataFrame(ImmatriculationsElectrique).to_csv('Immat.csv',sep=";",encoding='utf-8')
        