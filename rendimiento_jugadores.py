from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys, os
import pandas as pd
from selenium.webdriver.chrome.options import Options
import enum
import time

class Posiciones(enum.Enum):
    PORTERO = "Portero"

class ColumnasTablaRendimiento(enum.Enum):
    PARTIDOS_JUGADOS = 4
    PUNTAJE_PROMEDIO = 5
    GOLES = 6
    PASES_GOL = 7
    GOLES_EN_CONTRA = 8
    PARTIDOS_IMBATIDO_PORTERO_Y_TIEMPO_JUGADOR = 9
    TIEMPO_PORTERO = 10


class RendimientoScraper:
    url_principal = 'https://www.transfermarkt.es'
    nroalineado, valoracionpromedio, totalgoles, pasesgol, \
    autogol, minutosjugados, porteriaimbatida = "", "", "", "", "", "", ""

    def __init__(self, path, posicion):
        self.path = path
        self.posicion = posicion

    def limpiarRendimiento(self):
        self.nroalineado, self.valoracionpromedio, \
        self.totalgoles, self.pasesgol, self.autogol, \
        self.minutosjugados, self.porteriaimbatida = "", "", "", "", "", "", ""

    def navegando(self):
        try:
            self.limpiarRendimiento()
            conexion = self.open_conexion_selenium(self.path)
            try:
                selectTag = WebDriverWait(conexion, 5).until(EC.presence_of_element_located((By.NAME, 'saison')))
                print("ok")
            except Exception as e:
                print("Error ...")
                print(e)

            # Selecciona que sean todas las ligas
            selectCompetencia = conexion.find_element_by_name('wettbewerb')
            # Este dropdown tiene un problema que el select tiene el estilo display:none y no se puede acceder
            conexion.execute_script("arguments[0].style.display = 'block';", selectCompetencia)
            # Seleccionamos opcion de todas las competencias
            all_options = selectCompetencia.find_elements_by_tag_name("option")
            for option in all_options:
                option.click()
                break
            # Dropdown de las temporadas seleccionamos todas las temporadas
            selectTagTemporada = conexion.find_element_by_name('saison')
            conexion.execute_script("arguments[0].style.display = 'block';", selectTagTemporada)
            all_options = selectTagTemporada.find_elements_by_tag_name("option")
            #self.recursivo_filtros(conexion, all_options, 0)
            for option in all_options:
                option.click()
                break 
            # Presionamos boton submit para filtrar datos seleccionados
            botonSubmit = conexion.find_element_by_css_selector(
                '#main > div:nth-child(15) > div.large-8.columns > div > div.content > form > div > div > table > tbody > tr:nth-child(6) > td:nth-child(3) > input')
            botonSubmit.click()
            time.sleep(4)
            # GO RENDIMIENTO
            self.rendimiento_jugador(conexion, self.posicion)
            conexion.quit()
            print("nroalineado")
            print(self.nroalineado)
            print("valoracionpromedio")
            print(self.valoracionpromedio)
            print("totalgoles")
            print(self.totalgoles)
            print("pasesgol")
            print(self.pasesgol)
            print("autogol")
            print(self.autogol)
            print("minutosjugados")
            print(self.minutosjugados)
            print("porteriaimbatida")
            print(self.porteriaimbatida)
            return self.nroalineado, \
                   self.valoracionpromedio, self.totalgoles, self.pasesgol, self.autogol, \
                   self.minutosjugados, self.porteriaimbatida


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)


    def rendimiento_jugador(self, conexion, posicion):
        try:
            table_rendimiento = conexion.find_element_by_class_name("items")
            bodyTable = table_rendimiento.find_element(By.TAG_NAME, "tfoot")
            filas = bodyTable.find_elements(By.TAG_NAME, "tr")
            for i, fila in enumerate(filas):
                columnas = fila.find_elements(By.TAG_NAME, "td")
                for j, columna in enumerate(columnas):
                    if j == ColumnasTablaRendimiento.PARTIDOS_JUGADOS.value:
                        self.nroalineado = columna.text.strip().replace("\n", "").replace("-", "")
                        if self.nroalineado == "":
                            self.nroalineado = "0"
                    elif j == ColumnasTablaRendimiento.PUNTAJE_PROMEDIO.value:
                        self.valoracionpromedio = columna.text.strip().replace("\n", "").replace("-", "")
                        if self.valoracionpromedio == "":
                            self.valoracionpromedio = "0"
                    elif j == ColumnasTablaRendimiento.GOLES.value:
                        varTotGoles = columna.text.strip().replace("\n", "").replace("-", "")
                        if varTotGoles == "":
                            self.totalgoles = "0"
                        else:
                            self.totalgoles = columna.text.strip().replace("\n", "").replace("-", "")
                            if self.totalgoles == "":
                                self.totalgoles = "0"
                    elif j == ColumnasTablaRendimiento.PASES_GOL.value:
                        if posicion != Posiciones.PORTERO.value:
                            self.pasesgol = columna.text.strip().replace("\n", "").replace("-", "")
                            if self.pasesgol == "":
                                self.pasesgol = "0"
                        else:
                            self.pasesgol = "0"
                    elif j == ColumnasTablaRendimiento.GOLES_EN_CONTRA.value:
                        if posicion == Posiciones.PORTERO.value:
                            self.autogol = columna.text.strip().replace("\n", "").replace("-", "")
                            if self.autogol == "":
                                self.autogol = "0"
                        else:
                            self.autogol = "0"
                    elif j == ColumnasTablaRendimiento.PARTIDOS_IMBATIDO_PORTERO_Y_TIEMPO_JUGADOR.value:
                        if posicion == Posiciones.PORTERO.value:
                            self.porteriaimbatida = columna.text.strip().replace("\n", "").replace("-", "")
                            if self.porteriaimbatida == "":
                                self.porteriaimbatida = "0"
                        else:
                            self.minutosjugados = columna.text.strip().replace("\n", "").replace("-", "")
                            if self.minutosjugados == "":
                                self.minutosjugados = "0"
                            self.porteriaimbatida = "0"
                    elif j == ColumnasTablaRendimiento.TIEMPO_PORTERO.value:
                        if posicion == Posiciones.PORTERO.value:
                            self.minutosjugados = columna.text.strip().replace("\n", "").replace("-", "")
                            if self.minutosjugados == "":
                                self.minutosjugados = "0"
                        else:
                            self.minutosjugados = "0"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def open_conexion_selenium(self, path):
        try:
            driverexe = 'driver/chromedriver'
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Chrome(driverexe, options=options)
            driver.set_window_size(1920, 1080)
            driver.get(self.url_principal + path)
        except Exception as e:
            print(e)
        finally:
            return driver


if __name__ == "__main__":
    obj = RendimientoScraper("/denis-franchi/leistungsdatendetails/spieler/606576/wettbewerb/FRC/saison/2020", 'Portero')
    obj.navegando()