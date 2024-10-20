# scripts/subprocesos/scrapping_obtener_grupos_competiciones.py

import os
from typing import List, Dict, Optional
from .scrapping_base import ScrappingBase
from utils import string_utils
from utils.excepciones import ExcepcionScrapping

class ObtenerGruposCompeticiones(ScrappingBase):

    def __init__(self) -> None:

        """
        Inicializa la clase de obtención de grupos de competiciones.

        Parámetros:
            None

        Salida:
            None

        Lanza:
            ExcepcionScrapping: Si ocurre algún error al inicializar la clase.
        """

        try:
            super().__init__()
        
        except ExcepcionScrapping as es:
            raise ExcepcionScrapping(f"Error al inicializar el proceso obtención de grupos de competiciones") from es


    def ejecutar(self) -> List[Dict[str, str]]:

        """
        Obtiene los grupos de competiciones desde la página de Velogames después del encabezado 'All Contests'.

        Parámetros: 
            Ninguno.

        Salida:
            list: Lista de diccionarios con información sobre los grupos de competiciones (nombre, genero y URL).

        Lanza:
            ExcepcionScrapping: Si ocurre algún error durante el proceso de obtención de competiciones.
        """

        try:
            self.logger.info("Iniciando la obtención de grupos de competiciones...")
            self._cargar_valores_configuracion()
            soup = self.obtener_soup_pagina(self.url_velogames)
            h1_todas_competiciones = self._encontrar_encabezado_todas_competiciones(soup)

            if h1_todas_competiciones:
                competiciones = self._extraer_grupos_competiciones(h1_todas_competiciones)
                self.logger.info(f"Se encontraron {len(competiciones)} competiciones.")
                return competiciones

            else:
                self.logger.warning("No se encontró el encabezado de competiciones con 'All Contests'.")
                return []

        except Exception as e:
            raise ExcepcionScrapping(f"Error en el proceso de obtención de grupos de competiciones") from e


    def _cargar_valores_configuracion(self) -> None:

        """
        Carga en variables los valores del archivo de configuración.

        Parámetros: 
            Ninguno.

        Lanza:
            ExcepcionScrapping: Si ocurre algún error al cargar las configuraciones.
        """

        nombre_subproceso = os.path.splitext(os.path.basename(__file__))[0]

        try:
            self.url_velogames = self.obtener_valor_config_proceso(nombre_subproceso, "url_velogames")
            self.clase_h1_all_contests = self.obtener_valor_config_proceso(nombre_subproceso, "clase_h1_all_contests")
            self.texto_all_contests = self.obtener_valor_config_proceso(nombre_subproceso, "texto_all_contests")
            self.texto_eliminar_competiciones = self.obtener_valor_config_proceso(nombre_subproceso, "texto_eliminar_competiciones")
            self.palabras_femenino = self.obtener_valor_config_proceso(nombre_subproceso, "palabras_femenino")
            self.clases_enlace_competiciones = self.obtener_valor_config_proceso(nombre_subproceso, "clases_enlace_competiciones")

        except Exception as e:
            raise ExcepcionScrapping(f"Error al cargar los valores de configuración de '{nombre_subproceso}'") from e


    def _encontrar_encabezado_todas_competiciones(self, soup) -> Optional[object]:

        """
        Busca el encabezado 'All Contests' en la página para identificar la sección correcta.

        Parámetros:
            soup (BeautifulSoup): Objeto BeautifulSoup de la página.

        Salida:
            Optional[object]: El objeto h1 correspondiente si se encuentra, None en caso contrario.
        """

        try:
            h1_elements = soup.select(self.clase_h1_all_contests)

            for h1 in h1_elements:
                if string_utils.comparar_cadenas_ignorando_case(h1.text.strip(), self.texto_all_contests):
                    return h1

            return None

        except Exception as e:
            raise ExcepcionScrapping(f"Error al buscar '{self.texto_all_contests}' en {self.url_velogames}") from e


    def _extraer_grupos_competiciones(self, h1_todas_competiciones: object) -> List[Dict[str, str]]:

        """
        Extrae la lista de competiciones a partir del encabezado 'All Contests'.

        Parámetros:
            h1_todas_competiciones (BeautifulSoup): El encabezado h1 de la sección 'All Contests'.

        Salida:
            list: Lista de diccionarios con la información de cada competición (nombre, género, URL).

        Lanza:
            ExcepcionScrapping: Si ocurre algún error al extraer las competiciones.
        """

        try:
            self.logger.info("Extrayendo grupos de competiciones...")
            competiciones = []

            for a in h1_todas_competiciones.find_all_next('a', class_=self.clases_enlace_competiciones):
                nombre_competicion = self.limpiar_nombre_competicion(a.text, self.texto_eliminar_competiciones.split(','))
                url_competicion = a['href']
                genero_competicion = self._determinar_genero_competicion(nombre_competicion,
                                                                         self.palabras_femenino.split(","))

                competiciones.append({'nombre': nombre_competicion,
                    'genero': genero_competicion,
                    'url': url_competicion
                })
                self.logger.info(f"Competición encontrada: {nombre_competicion}, Género: {genero_competicion}, URL: {url_competicion}")

            return competiciones

        except Exception as e:
            raise ExcepcionScrapping(f"Error al extraer los grupos de competciones de {self.url_velogames}") from e


    def _determinar_genero_competicion(self, nombre_competicion: str, palabras_identificador_femenino: List[str]) -> str:

        """
        Determina el género de la competición basándose en palabras clave femeninas.

        Parámetros:
            nombre_competicion (str): Nombre de la competición.
            palabras_identificador_femenino (list): Lista de palabras clave que identifican competiciones femeninas.

        Salida:
            str: 'femenino' o 'masculino' según las palabras clave.
        """

        try:
            self.logger.debug(f"nombre_competicion: {nombre_competicion}")
            if string_utils.contiene_cualquier_subcadena(nombre_competicion, palabras_identificador_femenino):
                self.logger.debug(f"nombre_competicion FEMENINO")
                return 'femenino'
            
            self.logger.debug("MASCULINO")

            return 'masculino'

        except Exception as e:
            raise ExcepcionScrapping(f"Error al determinar el género de '{nombre_competicion}'") from e