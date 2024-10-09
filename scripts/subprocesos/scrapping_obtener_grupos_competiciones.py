# scripts/subprocesos/scrapping_obtener_grupos_competiciones.py

from .scrapping_base import ScrappingBase
from utils import string_utils
from utils.excepciones import ExcepcionScrapping, ExcepcionConfiguracion

class ObtenerGruposCompeticiones(ScrappingBase):

    def __init__(self, ruta_config, logger, proceso):

        """
        Inicializa la clase de obtención de grupos de competiciones.

        Parámetros:
            ruta_config (str): Ruta al archivo de configuración.
            logger (logging): Gestor de log.
            proceso (str): Nombre del proceso.

        Salida:
            None

        Lanza:
            ExcepcionScrapping: Si ocurre algún error al inicializar la clase base de scrapping.
        """

        try:
            super().__init__(ruta_config, logger, proceso)
        
        except ExcepcionScrapping as es:
            raise ExcepcionScrapping(f"Error al inicializar el proceso '{proceso}': {str(es)}") from es


    def ejecutar(self):

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
            self.logger.info("Iniciando la obtención de competiciones...")
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
            raise ExcepcionScrapping(f"Error al ejecutar el proceso de obtención de competiciones: {str(e)}") from e


    def _cargar_valores_configuracion(self):

        """
        Carga en variables los valores del archivo de configuración.

        Parámetros: 
            Ninguno.

        Lanza:
            ExcepcionScrapping: Si ocurre algún error al cargar las configuraciones.
        """

        try:
            self.url_velogames = self.obtener_valor_config("scrapping_ogc", "url_velogames")
            self.clase_h1_all_contests = self.obtener_valor_config("scrapping_ogc", "clase_h1_all_contests")
            self.texto_all_contests = self.obtener_valor_config("scrapping_ogc", "texto_all_contests")
            self.etiqueta_enlace_competiciones = self.obtener_valor_config("scrapping_ogc", "etiqueta_enlace_competiciones")
            self.texto_eliminar_competiciones = self.obtener_valor_config("scrapping_ogc", "texto_eliminar_competiciones")
            self.palabras_identificador_femenino = self.obtener_valor_config("scrapping_ogc", "palabras_identificador_femenino")
            self.clases_enlace_competiciones = self.obtener_valor_config("scrapping_ogc", "clases_enlace_competiciones")

        except ExcepcionConfiguracion as ec:
            raise ExcepcionScrapping(f"Error al cargar valores de configuración: {str(ec)}") from ec


    def _encontrar_encabezado_todas_competiciones(self, soup):

        """
        Busca el encabezado 'All Contests' en la página para identificar la sección correcta.

        Parámetros:
            soup (BeautifulSoup): Objeto BeautifulSoup de la página.

        Salida:
            h1: El objeto h1 correspondiente si se encuentra, None en caso contrario.
        """

        try:
            h1_elements = soup.select(self.clase_h1_all_contests)

            for h1 in h1_elements:
                if string_utils.comparar_cadenas_ignorando_case(h1.text.strip(), self.texto_all_contests):
                    return h1

            return None

        except Exception as e:
            raise ExcepcionScrapping(f"Error al buscar el encabezado 'All Contests': {str(e)}") from e


    def _extraer_grupos_competiciones(self, h1_todas_competiciones):

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

            for a in h1_todas_competiciones.find_all_next(self.etiqueta_enlace_competiciones, class_=self.clases_enlace_competiciones):
                nombre_competicion = self._limpiar_nombre_competicion(a.text, self.texto_eliminar_competiciones)
                url_competicion = a['href']
                genero_competicion = self._determinar_genero_competicion(nombre_competicion, self.palabras_identificador_femenino)

                competiciones.append({
                    'nombre': nombre_competicion,
                    'genero': genero_competicion,
                    'url': url_competicion
                })
                self.logger.info(f"Competición encontrada: {nombre_competicion}, Género: {genero_competicion}, URL: {url_competicion}")

            return competiciones

        except Exception as e:
            raise ExcepcionScrapping(f"Error al extraer grupos de competiciones: {str(e)}") from e


    def _limpiar_nombre_competicion(self, nombre, texto_eliminar_competiciones):

        """
        Elimina el texto inicial innecesario del nombre de la competición.

        Parámetros:
            nombre (str): Nombre original de la competición.
            texto_eliminar_competiciones (str): Texto que se debe eliminar al inicio.

        Salida:
            str: Nombre limpio de la competición.
        """

        try:
            if string_utils.comparar_cadenas_ignorando_case(nombre[:len(texto_eliminar_competiciones)], texto_eliminar_competiciones):
                return nombre[len(texto_eliminar_competiciones):].strip()

            return nombre.strip()

        except Exception as e:
            raise ExcepcionScrapping(f"Error al limpiar el nombre de la competición: {str(e)}") from e


    def _determinar_genero_competicion(self, nombre_competicion, palabras_identificador_femenino):

        """
        Determina el género de la competición basándose en palabras clave femeninas.

        Parámetros:
            nombre_competicion (str): Nombre de la competición.
            palabras_identificador_femenino (list): Lista de palabras clave que identifican competiciones femeninas.

        Salida:
            str: 'femenino' o 'masculino' según las palabras clave.
        """

        try:
            if string_utils.contiene_cualquier_subcadena(nombre_competicion, palabras_identificador_femenino):
                return 'femenino'

            return 'masculino'

        except Exception as e:
            raise ExcepcionScrapping(f"Error al determinar el género de la competición: {str(e)}") from e