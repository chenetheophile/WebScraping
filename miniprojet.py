# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 21:45:08 2022

@author: chene
"""
# zzzz
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import csv

site=['https://aqicn.org/map/france/fr/','https://www.automobile-propre.com/dossiers/chiffres-vente-immatriculations-france/']
driver = webdriver.Firefox()
ImmatriculationsElectrique=[]
Pollutiondelair=[]
# try:
for url in site:
    driver.get(url)
    time.sleep(1)
    if url is site[0]:
        ville=['Paris','Marseille','Lyon','Toulouse','Nice','Nantes','Montpellier','Strasbourg','Bordeaux','Lille','Rennes',
               'Reims','Toulouse','Saint-Étienne','Le Havre', 'Grenoble', 'Dijon','Angers','Saint-Denis','Villeurbanne',
               'Nîmes','Clermont-Ferrand','Aix-en-Provence','Le Mans','Brest','Tours','Amiens','Limoges','Annecy',
               'Boulogne-Billancourt','Perpignan','Metz','Besançon','Orléans','Rouen','Montreuil','Argenteuil',
               'Mulhouse','Caen',	'Nancy','Saint-Paul','Roubaix','Tourcoing',	'Nanterre','Vitry-sur-Seine','Nouméa',
               'Créteil','Avignon','Poitiers','Aubervilliers','Asnières-sur-Seine','Aulnay-sous-Bois']
        for nom in ville:
            recherche=driver.find_element_by_id('full-page-search-input')
            time.sleep(2)
            recherche.send_keys(nom)
            time.sleep(3)
            recherche.location_once_scrolled_into_view
            time.sleep(2)
            driver.find_element_by_id('searchResults').find_element_by_tag_name('a').click()
            time.sleep(2)
            driver.find_element_by_id('h1header3').location_once_scrolled_into_view
            time.sleep(2)
            donneeshistorique=driver.find_element_by_class_name('historical-yearly-data')
            time.sleep(2)
            ligneTab=donneeshistorique.find_element_by_tag_name('tr')
            time.sleep(2)
            marqueurAnnee=ligneTab.find_element_by_class_name('year-divider')
            time.sleep(2)
            print(ligneTab)
            # for i in range(len(ligneTab)):
            #     if ligneTab[i] in marqueurAnnee:
            #         Pollutiondelair.append([])
            #     else:
            #         ligneDonnee=ligneTab.find_element_by_class_name('squares').find_element_by_tag_name('text')
            #         time.sleep(1)
            #         for element in ligneDonnee:
            #             Pollutiondelair[i].append(element.text)
                    
                
    else:
        menu=driver.find_element_by_class_name("igc-tab-content igc-tab-select")
        time.sleep(1)
        annee=menu.find_element_by_tag_name('option')
        time.sleep(1)
        for element in annee:
            element.click()
            graph=driver.find_element_by_class_name('igc-graph-group')
            time.sleep(1)
            mois=graph.find_element_by_tag_name('text')
            time.sleep(1)
            for i in range(len(mois)):
                ImmatriculationsElectrique.append([])#pas bon je crois
                ImmatriculationsElectrique[i].append(mois[i].text)
# except NoSuchElementException:
#     print(NoSuchElementException())
#     driver.close()