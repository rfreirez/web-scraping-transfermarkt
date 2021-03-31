# coding: utf-8

# In[1]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
#import builtwith
#import urllib3
#import whois
import csv
from datetime import datetime
import time


# In[2]:



url_page="https://www.transfermarkt.es/spieler-statistik/wertvollstemannschaften/marktwertetop"


# In[3]:


response = requests.get(url=url_page,
                            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
response.elapsed.seconds
soup = BeautifulSoup(response.content, "html.parser")


# In[4]:

precio_jugador = []
nombre_equipo=[]
nombre=[]
fecha_nacimiento=[]
fut={}
titulos=[]
ranking= set()
jugador=[]
posicion=[]
Edad=[]
Nacionalidad=[]
Altura=[]
Club=[]
Valor_mercado=[]

# In[5]:


#yw1 > table > tbody > tr.odd.selected > td.no-border-links.hauptlink
for link in soup.find_all('div',class_='pager'):
    for link_pag in link.find_all('a'):
        url_page="https://www.transfermarkt.es"+link_pag.attrs["href"]
        response_pagina = requests.get(url=url_page,
                            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        soup_pagina = BeautifulSoup(response_pagina.content, "html.parser")
        time.sleep(3)
        #print(url_page)
        contEquipos = 0
        for link_equipo in soup_pagina.find_all('td', class_= 'no-border-links hauptlink'):
            for equipo in link_equipo.find_all('a',class_='vereinprofil_tooltip'):
                url_equipo="https://www.transfermarkt.es"+equipo.attrs["href"]
                response_equipo = requests.get(url=url_equipo,
                            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
                soup_equipo = BeautifulSoup(response_equipo.content, "html.parser")
                for n_equipo in soup_equipo('h1', itemprop="name"):
                    nombre_eq=n_equipo.text
                    nombre_eq=nombre_eq.replace('\n', '')
                time.sleep(2)
                print(url_equipo)
                for jugador in soup_equipo.find_all('span',class_="hide-for-small"):
                    for jugador_link in jugador.find_all('a',class_='spielprofil_tooltip'):
                        url_jugador="https://www.transfermarkt.es"+jugador_link.attrs["href"]
                        response_jugador = requests.get(url=url_jugador,
                            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
                        soup_jugador = BeautifulSoup(response_jugador.content, "html.parser")
                        time.sleep(1)
                        getTagPrecioJugador = soup_jugador.find('div',class_="right-td")
                        if getTagPrecioJugador:
                            precio_jugador.append(getTagPrecioJugador.text.strip().replace("\n", ""))
                        else:
                            precio_jugador.append("0")
                        for nombrej in soup_jugador.find_all("h1"):
                            nombre_equipo.append(nombre_eq)
                            print("**** Nombre Equipo " + str(nombre_equipo[len(nombre_equipo)-1]))
                            nombre_jugador=nombrej.text
                            #print(nombre_jugador)
                            nombre.append(nombre_jugador)
                            print("Nombre Jugador " + str(nombre[len(nombre) - 1]))
                            print("Precio " + str(precio_jugador[len(precio_jugador) - 1]))
                        for fec in soup_jugador.find_all("span",itemprop="birthDate"):
                            fecha_nac=fec.text.split()
                            edad=fecha_nac[1].replace('(', '')
                            edad=edad.replace(')', '')
                            #print(fecha_nac[0],edad)
                            fecha_nacimiento.append(fecha_nac[0])
                            print("Fecha Nacimiento " + str(fecha_nacimiento[len(fecha_nacimiento) - 1]))
                            Edad.append(edad)
                            print("Edad " + str(Edad[len(Edad) - 1]))
                        for natio in soup_jugador.find_all("span",itemprop="nationality"):
                            Nacionalidad.append(natio.text)
                            print("Nacionalidad " + str(Nacionalidad[len(Nacionalidad) - 1]))
                        # Busca altura
                        tagAltura = soup_jugador.find_all("span",itemprop="height")
                        if len(tagAltura) > 0:
                            for alt in tagAltura:
                                Altura.append(alt.text)
                                print("Altura " + str(Altura[len(Altura) - 1]))
                        else:
                            Altura.append("")
                            print("Altura " + str(Altura[len(Altura) - 1]))
                        # Busca posicion
                        paraPosicion = soup_jugador.find("div", class_="auflistung")
                        posicion.append(paraPosicion.br.text.strip())
                        print("posicion " + str(posicion[len(posicion) - 1]))
                        # for pos in soup_jugador.find_all("span",class_="dataItem"):
                        #     #print(pos)
                        #     if pos.text=="Posición:":
                        #         a=1
                        #         for x in soup_jugador.find_all("span",class_="dataValue"):
                        #             a=a+1
                        #             if a==6:
                        #                 posicion.append(x.text.strip())
                        #                 print("posicion " + str(posicion[len(posicion) - 1]))
                        # Integra con Página de rendimiento
