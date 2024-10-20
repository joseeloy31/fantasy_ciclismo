# scripts/subprocesos/scrapping_base.py

from bs4 import BeautifulSoup
import requests
from utils.config import Config
from utils import string_utils
from utils.excepciones import ExcepcionScrapping
from requests.exceptions import RequestException
from typing import Optional, Any

class ScrappingBase:

    def __init__(self) -> None:

        """
        Inicializa la clase base de scrapping.

        Parámetros:
            None

        Salida:
            None

        Lanza:
            ExcepcionScrapping: Si ocurre algún error al inicializar el logger o cargar la configuración.
        """

        try:
            config_instance = Config()
            self.logger = config_instance.obtener_logger()
            self.config_general = config_instance.obtener_fichero_config_general()
            self.config_proceso = config_instance.obtener_fichero_config_proceso()

        except Exception as e:
            raise ExcepcionScrapping(f"Error al inicializar la clase base de Scrapping") from e


    def obtener_valor_config_general(self, seccion: str, clave: str, valor_por_defecto: Optional[Any] = None) -> Any:

        """
        Obtiene el valor de una clave específica del diccionario de configuración general.

        Parámetros:
            seccion (str): Sección del archivo de configuración.
            clave (str): Clave que se desea obtener del diccionario de configuración.
            valor_por_defecto (Any, optional): Valor por defecto si la clave no existe.

        Salida:
            Any: El valor asociado a la clave o el valor por defecto.

        Lanza:
            ExcepcionScrapping: Si ocurre un error al leer el valor de configuración.
        """

        try:            
            clave_compuesta = f"{seccion}.{clave}"
            return self.config_general.get(clave_compuesta, valor_por_defecto)

        except Exception as e:
            raise ExcepcionScrapping(f"Error inesperado leer la propiedad '{clave}' de la sección {seccion}") from e


    def obtener_valor_config_proceso(self, seccion: str, clave: str, valor_por_defecto: Optional[Any] = None) -> Any:

        """
        Obtiene el valor de una clave específica del diccionario de configuración del proceso.

        Parámetros:
            seccion (str): Sección del archivo de configuración.
            clave (str): Clave que se desea obtener del diccionario de configuración.
            valor_por_defecto (Any, optional): Valor por defecto si la clave no existe.

        Salida:
            Any: El valor asociado a la clave o el valor por defecto.

        Lanza:
            ExcepcionScrapping: Si ocurre un error al leer el valor de configuración.
        """

        try:            
            clave_compuesta = f"{seccion}.{clave}"
            return self.config_proceso.get(clave_compuesta, valor_por_defecto)

        except Exception as e:
            raise ExcepcionScrapping(f"Error inesperado leer la propiedad '{clave}' de la sección {seccion}") from e


    def obtener_soup_pagina(self, url: str) -> BeautifulSoup:

        """
        Realiza la solicitud HTTP y convierte el contenido de la página a un objeto BeautifulSoup.

        Parámetros:
            url (str): URL de la página a la que se hará la solicitud.

        Salida:
            BeautifulSoup: Objeto BeautifulSoup con el contenido de la página.

        Lanza:
            ExcepcionScrapping: Si ocurre un error al realizar la solicitud HTTP.
        """

        try:
            self.logger.info(f"Realizando la solicitud a: {url}")
            response = requests.get(url)
            response.raise_for_status()

            return BeautifulSoup(response.text, 'html.parser')

        except RequestException as re:
            raise ExcepcionScrapping(f"Error al realizar la solicitud HTTP a {url}") from re

        except Exception as e:
            raise ExcepcionScrapping(f"Error inesperado al obtener contenido de la página {url}") from e


    def limpiar_nombre_competicion(self, nombre_competicion: str, textos_eliminar: list[str]) -> str:

        """
        Elimina textos como VELOGAMES o Fantasy de las competiciones.

        Parámetros:
            nombre_competicion (str): Nombre original de la competición.
            textos_eliminar (list[str]): Lista de textos que se deben eliminar al inicio.

        Salida:
            str: Nombre limpio de la competición.
        """

        try:
            for texto_eliminar in textos_eliminar:
                
                if string_utils.contiene_subcadena(nombre_competicion, texto_eliminar):
                    nombre_competicion = string_utils.eliminar_subcadena_ignorando_case(nombre_competicion, texto_eliminar)

            return nombre_competicion.strip()

        except Exception as e:
            raise ExcepcionScrapping(f"Error al limpiar el nombre de la competición {nombre_competicion}") from e