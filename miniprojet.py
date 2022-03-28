# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 21:45:08 2022

@author: chene
"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv

site=['https://aqicn.org/map/france/fr/','https://www.automobile-propre.com/dossiers/chiffres-vente-immatriculations-france/']
driver = webdriver.Firefox()
ImmatriculationsElectrique=[]
Pollutiondelair=[]
for url in site:
    driver.get(url)
    time.sleep(2)
    if url is site[0]:
        ville=['Paris','Marseille','Lyon','Toulouse','Nice','Nantes','Montpellier','Strasbourg','Bordeaux','Lille','Rennes',
                'Reims','Toulouse','Saint-Étienne','Le Havre', 'Grenoble', 'Dijon','Angers','Saint-Denis','Villeurbanne',
                'Nîmes','Clermont-Ferrand','Aix-en-Provence','Le Mans','Brest','Tours','Amiens','Limoges','Annecy',
                'Boulogne-Billancourt','Perpignan','Metz','Besançon','Orléans','Rouen','Montreuil','Argenteuil',
                'Mulhouse','Caen',	'Nancy','Saint-Paul','Roubaix','Tourcoing',	'Nanterre','Vitry-sur-Seine','Nouméa',
                'Créteil','Avignon','Poitiers','Aubervilliers','Asnières-sur-Seine','Aulnay-sous-Bois']
        for nom in ville:
            time1=time.perf_counter()
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
            Annee=donneeshistorique.find_elements_by_class_name('year-divider')
            marqueurAnnee=[]
            time.sleep(2)
            ligneTab=donneeshistorique.find_elements_by_tag_name('tr')
            time.sleep(2)
            for element in Annee:
                marqueurAnnee.append(element.text)
            time.sleep(2)
            annee=[]
            for i in range(len(ligneTab)):  
                    if ligneTab[i].get_attribute('class')=="year-divider":
                        print(ligneTab[i].text)
                        Pollutiondelair.append(annee)
                        annee=[]
                    else:
                        carre=ligneTab[i].find_elements_by_class_name('squares')
                        time.sleep(1)
                        for element in carre:
                            text=element.find_elements_by_tag_name('text')
                            time.sleep(1)
                            for balise in text:
                                annee.append(balise.text)
            temps=(time.perf_counter()-time1)
            print('nombre de seconde pour une ville:'+str(temps))
    else:
        menu=Select(driver.find_element_by_tag_name("select"))
        options=len(menu.options)
        for i in range(options):
            valeur=[]
            driver.find_element_by_css_selector("div[class='igc-tab-switcher igc-tab-switcher__left']").click()
            time.sleep(4)
            mois=driver.find_element_by_class_name('igc-graph-group').find_elements_by_tag_name('text')
            for i in range(len(mois)):
                valeur.append(mois[i].text)
            ImmatriculationsElectrique.append(valeur)