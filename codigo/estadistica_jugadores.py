# coding: utf-8

# In[1]:

import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
#import builtwith
#import urllib3
#import whois
import csv
from datetime import datetime
#from datetime import date
import time
import re
# Variables Rendimiento
from rendimiento_jugadores import RendimientoScraper

vec_nroalineado, vec_valoracionpromedio, vec_totalgoles, vec_pasesgol, vec_autogol, vec_minutosjugados, vec_porteriaimbatida = [],[],[],[],[],[],[],

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
            # if contEquipos != 8:
            #     contEquipos = contEquipos + 1
            #     continue
            for equipo in link_equipo.find_all('a',class_='vereinprofil_tooltip'):
                # if contEquipos != 18:
                #     contEquipos = contEquipos + 1
                #     continue
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
                            #print("Precio Manolo 1",getTagPrecioJugador.text.strip())
                            l_precio=re.split(" ",getTagPrecioJugador.text.strip().replace("\n", ""))
                            if l_precio[1]=="mill.":
                                precio=float(l_precio[0].replace(",","."))
                            elif l_precio[1]=="mil":
                                precio=round(float(l_precio[0].replace(",","."))/1000,2)
                            precio_jugador.append(precio)
                            #precio_jugador.append(getTagPrecioJugador.text.strip().replace("\n", ""))
                            #print("Precio Manolo " + str(precio_jugador[len(precio_jugador) - 1]))
                        else:
                            precio_jugador.append("0")
                        for nombrej in soup_jugador.find_all("h1"):
                            nombre_equipo.append(nombre_eq)
                            print("**** Nombre Equipo " + str(nombre_equipo[len(nombre_equipo)-1]))
                            nombre_jugador=nombrej.text
                            #print(nombre_jugador)
                            nombre.append(nombre_jugador)
                            #print("Nombre Jugador " + str(nombre[len(nombre) - 1]))
                            
                        for fec in soup_jugador.find_all("span",itemprop="birthDate"):
                            fecha_nac=fec.text.split()
                            edad=fecha_nac[1].replace('(', '')
                            edad=edad.replace(')', '')
                            fecha=fecha_nac[0]
                            #print("Fecha Nacimiento ",fecha,"tipo",type(fecha))
                            fecha=datetime.strptime(fecha, "%d/%m/%Y")
                            #print("Fecha Nacimiento ",fecha,"tipo",type(fecha))
                            fecha_nacimiento.append(fecha)
                            #fecha_nacimiento.append(fecha_nac[0])
                            #print("Fecha Nacimiento " + str(fecha_nacimiento[len(fecha_nacimiento) - 1]))
                            Edad.append(edad)
                            print("Edad " + str(Edad[len(Edad) - 1]))
                        for natio in soup_jugador.find_all("span",itemprop="nationality"):
                            Nacionalidad.append(natio.text)
                            print("Nacionalidad " + str(Nacionalidad[len(Nacionalidad) - 1]))
                        # Busca altura
                        tagAltura = soup_jugador.find_all("span",itemprop="height")
                        if len(tagAltura) > 0:
                            for alt in tagAltura:
                                altura=alt.text.replace(" m","")
                                altura=float(altura.replace(",","."))
                                Altura.append(altura)
                                #Altura.append(alt.text.replace(" m",""))
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
                        linkRendimiento = soup_jugador.find("div", {"class": ["leistungsdatenHeadline flexCenter"]})
                        if linkRendimiento:
                            urlRendimiento = linkRendimiento.select("a")[0]['href']
                            # Instancia Clase para extración de rendimiento con selenium
                            try:
                                objRendimientoScraper = RendimientoScraper(urlRendimiento, posicion[len(posicion)-1])
                                nroalineado, valoracionpromedio, totalgoles, pasesgol, autogol, \
                                minutosjugados, porteriaimbatida = objRendimientoScraper.navegando()
                                vec_nroalineado.append(nroalineado)
                                vec_valoracionpromedio.append(valoracionpromedio)
                                vec_totalgoles.append(totalgoles)
                                vec_pasesgol.append(pasesgol)
                                vec_autogol.append(autogol)
                                vec_porteriaimbatida.append(porteriaimbatida)
                                vec_minutosjugados.append(minutosjugados)
                            except Exception as e:
                                #print(e)
                                vec_nroalineado.append("0")
                                vec_valoracionpromedio.append("0")
                                vec_totalgoles.append("0")
                                vec_pasesgol.append("0")
                                vec_autogol.append("0")
                                vec_porteriaimbatida.append("0")
                                vec_minutosjugados.append("0")
                        else:
                            vec_nroalineado.append("0")
                            vec_valoracionpromedio.append("0")
                            vec_totalgoles.append("0")
                            vec_pasesgol.append("0")
                            vec_autogol.append("0")
                            vec_porteriaimbatida.append("0")
                            vec_minutosjugados.append("0")

                        data_frame_navigate = pd.DataFrame(
                            {
                                'NombreEquipo': nombre_equipo,
                                'NombreJugador': nombre,
                                'PrecioJugador': precio_jugador,
                                'FechaNacimiento': fecha_nacimiento,
                                'Edad': Edad,
                                'Nacionalidad': Nacionalidad,
                                'Altura': Altura,
                                'Posicion': posicion,
                                'PartidosJugados': vec_nroalineado,
                                'ValoracionPromedio': vec_valoracionpromedio,
                                'TotalGoles': vec_totalgoles,
                                'TotalPasesGol': vec_pasesgol,
                                'TotalGolesRecibidos': vec_autogol,
                                'PorteriaImbatida': vec_porteriaimbatida,
                                'MinutosJugados': vec_minutosjugados,

                            }, columns=['NombreEquipo', 'NombreJugador', 'PrecioJugador', 'FechaNacimiento', 'Edad', 'Nacionalidad', 'Altura', 'Posicion', 'PartidosJugados', 'ValoracionPromedio', 'TotalGoles', 'TotalPasesGol', 'TotalGolesRecibidos', 'PorteriaImbatida', 'MinutosJugados']
                        )
                        data_frame_navigate.to_csv('../dataset/estadisticas-futbolistas.csv', index=False, encoding="UTF-8")
        print("contEquipos " + str(contEquipos))
        if contEquipos > 0:
            break
        contEquipos = contEquipos + 1
