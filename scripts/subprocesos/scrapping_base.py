# scripts/subprocesos/scrapping_base.py

from bs4 import BeautifulSoup
import requests
from utils import properties_utils, string_utils
from utils.excepciones import ExcepcionLogging, ExcepcionConfiguracion, ExcepcionScrapping
from requests.exceptions import RequestException

class ScrappingBase:

    def __init__(self, ruta_config, logger, nombre_proceso):

        """
        Inicializa la clase base de scrapping.

        Parámetros:
            ruta_config (str): Ruta general de los archivos de configuración.
            logger (logging): Gestor de log.
            nombre_proceso (str): Nombre del proceso que se está ejecutando (para el log).

        Salida:
            None

        Lanza:
            ExcepcionScrapping: Si ocurre algún error al inicializar el logger o cargar la configuración.
        """

        try:
            self.config = self.cargar_configuracion_competiciones(ruta_config, nombre_proceso)
            self.logger = logger
            self.nombre_proceso = nombre_proceso

        except ExcepcionLogging as el:
            raise ExcepcionScrapping(f"Error al inicializar el logging en {nombre_proceso}: {str(el)}") from el

        except ExcepcionConfiguracion as ec:
            raise ExcepcionScrapping(f"Error al cargar las propiedades en {nombre_proceso}: {str(ec)}") from ec

        except Exception as e:
            raise ExcepcionScrapping(f"Error inesperado al inicializar {nombre_proceso}: {str(e)}") from e


    def cargar_configuracion_competiciones(self, ruta_config, nombre_proceso):

        """
        Carga el archivo de configuración y devuelve un diccionario con claves
        del tipo 'seccion.propiedad' y valores asociados.

        Parámetros:
            ruta_config (str): Ruta al archivo de configuración.
            nombre_proceso (str): Nombre del proceso que se está ejecutando (para el log).

        Salida:
            dict: Diccionario con las claves y valores de la configuración.

        Lanza:
            ExcepcionScrapping: Si ocurre un error al cargar las configuraciones.
        """

        try:
            nombre_properties = string_utils.obtener_nombre_properties_proceso(f"{ruta_config}{nombre_proceso}")
            config = properties_utils.leer_properties(nombre_properties)
            configuracion_dict = {}

            for seccion in config:
                for clave, valor in config[seccion].items():
                    clave_formateada = f"{seccion}.{clave}"
                    configuracion_dict[clave_formateada] = valor

            self.logger.info(f"Configuración cargada exitosamente desde {nombre_properties}")
            return configuracion_dict

        except ExcepcionConfiguracion as ec:
            raise ExcepcionScrapping(f"Error al leer propiedades desde {nombre_proceso}: {str(ec)}") from ec

        except Exception as e:
            raise ExcepcionScrapping(f"Error inesperado al cargar configuraciones para {nombre_proceso}: {str(e)}") from e


    def obtener_valor_config(self, seccion, clave, valor_por_defecto=None):

        """
        Obtiene el valor de una clave específica del diccionario de configuración.

        Parámetros:
            seccion (str): Sección del archivo de configuración.
            clave (str): Clave que se desea obtener del diccionario de configuración.
            valor_por_defecto (Any, optional): Valor por defecto si la clave no existe.

        Salida:
            Any: El valor asociado a la clave o el valor por defecto.
        """

        clave_compuesta = f"{seccion}.{clave}"
        return self.config.get(clave_compuesta, valor_por_defecto)


    def obtener_soup_pagina(self, url):

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
            raise ExcepcionScrapping(url=url, mensaje=f"Error al realizar la solicitud HTTP a {url}: {str(re)}") from re

        except Exception as e:
            raise ExcepcionScrapping(f"Error inesperado al obtener contenido de la página {url}: {str(e)}") from e