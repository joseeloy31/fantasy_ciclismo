# scripts/subprocesos/scrapping_desglosar_grupos_competiciones.py

import os
from .scrapping_base import ScrappingBase
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
from utils import fecha_utils, string_utils
from utils.excepciones import ExcepcionScrapping

class DesglosarGruposCompeticiones(ScrappingBase):

    def __init__(self, competiciones: list[dict]) -> None:

        """
        Inicializa la clase de obtención de grupos de competiciones.

        Parámetros:
            competiciones (list[dict]): Lista de grupos de competiciones.

        Salida:
            None

        Lanza:
            ExcepcionScrapping: Si ocurre algún error al inicializar la clase base de scrapping.
        """

        super().__init__()
        self.competiciones = competiciones
        self.resultados = []


    def ejecutar(self) -> list[dict]:

        """
        Procesa cada una de las competiciones y las clasifica en grupo de vueltas o clásicas.

        Recorre las competiciones, hace scrapping de cada URL para determinar si es un grupo de vueltas
        o un grupo de clásicas. Busca excepciones en las que una competición dentro de grupo de vueltas
        debe ser tratada como un nuevo grupo de clásicas (sucede con las clásicas de primevera femeninas).

        Parámetros:
            None

        Salida:
            list[dict]: Lista de competiciones procesadas con su tipo de grupo (grupo_vueltas o grupo_clasicas).
        """

        self.logger.info("Iniciando el desglose de los grupos de competiciones...")
        self._cargar_valores_configuracion()
        
        for competicion in self.competiciones:
            nombre = competicion['nombre']
            genero = competicion['genero']
            url = string_utils.completar_url(competicion['url'])
            self.logger.info(f"Procesando competición: {nombre} ({genero})")

            try:
                soup = self.obtener_soup_pagina(url)
                tipo_grupo = self._determinar_tipo_grupo(soup)
                excepcion_clasicas_femeninas = self._buscar_excepcion_clasicas_femeninas(soup, genero)
                desglose_grupo_competiciones = self._extraer_info_grupo(soup, tipo_grupo, url, excepcion_clasicas_femeninas)
                self._agregar_grupo(competicion, tipo_grupo, desglose_grupo_competiciones)

            except Exception as e:
                raise ExcepcionScrapping(f"Error al procesar la competición '{nombre}'") from e

        self.logger.info("Desglose de grupos de competiciones finalizado.")

        return self.resultados


    def _agregar_grupo(self, competicion, tipo_grupo, desglose_grupo_competiciones):

        """
        Agrega un grupo de competiciones a la lista de resultados.

        Parámetros:
            competicion (dict): Un diccionario que contiene información sobre la competición, 
                                incluyendo 'nombre' y 'genero'.
            tipo_grupo (str): El tipo de grupo de la competición.
            desglose_grupo_competiciones (dict): Información detallada del desglose del grupo 
                                                de competiciones.

        Salida:
            None: Este método no retorna ningún valor, simplemente agrega el resultado a la lista.
        """

        self.resultados.append({
            'nombre': competicion['nombre'],
            'genero': competicion['genero'],
            'url': string_utils.completar_url(competicion['url']),
            'tipo_grupo': tipo_grupo,
            'desglose_grupo_competiciones': desglose_grupo_competiciones
        })


    def _cargar_valores_configuracion(self) -> None:

        """
        Carga en variables los valores del archivo de configuración.

        Parámetros:
            None

        Salida:
            None

        Lanza:
            ExcepcionScrapping: Si ocurre algún error al cargar las configuraciones.
        """

        nombre_subproceso = os.path.splitext(os.path.basename(__file__))[0]

        try:
            self.tipo_grupo_vueltas = self.obtener_valor_config_proceso(nombre_subproceso, "tipo_grupo_vueltas")
            self.tipo_grupo_clasicas = self.obtener_valor_config_proceso(nombre_subproceso, "tipo_grupo_clasicas")
            self.tipo_gran_vuelta = self.obtener_valor_config_proceso(nombre_subproceso, "tipo_gran_vuelta")
            self.tipo_vuelta_menor = self.obtener_valor_config_proceso(nombre_subproceso, "tipo_vuelta_menor")

            self.clase_competicion = self.obtener_valor_config_proceso(nombre_subproceso, "clase_competicion")
            self.clase_grupo_vueltas = self.obtener_valor_config_proceso(nombre_subproceso, "clase_grupo_vueltas")

            self.cadena_clasicas_femeninas = self.obtener_valor_config_proceso(nombre_subproceso, "cadena_clasicas_femeninas")
 
            self.texto_sustituir_tour_masculino = self.obtener_valor_config_proceso(nombre_subproceso,
                                                                          "texto_sustituir_tour_masculino")
            self.texto_sustituir_tour_femenino = self.obtener_valor_config_proceso(nombre_subproceso,
                                                                                   "texto_sustituir_tour_femenino")
            self.textos_eliminar_competicion = self.obtener_valor_config_proceso(nombre_subproceso, "textos_eliminar_competicion")
            
            self.clases_enlace_competiciones = self.obtener_valor_config_proceso(nombre_subproceso, "clases_enlace_competiciones")
            self.clases_fecha_vuelta_x_etapas = self.obtener_valor_config_proceso(nombre_subproceso, "clases_fecha_vuelta_x_etapas")

            self.formato_fecha_vuelta_x_etapas = self.obtener_valor_config_proceso(nombre_subproceso, "formato_fecha_vuelta_x_etapas")
            self.formato_fecha_clasica = self.obtener_valor_config_proceso(nombre_subproceso, "formato_fecha_clasica")
            self.formato_fecha_generico = self.obtener_valor_config_general("fechas", "formato_generico")

            self.numero_etiqueta_fecha_vuelta_x_etapas = int(self.obtener_valor_config_proceso(nombre_subproceso,
                                                                                       "numero_etiqueta_fecha_vuelta_x_etapas"))

            self.url_info_detalle = self.obtener_valor_config_proceso(nombre_subproceso, "url_info_detalle")
            
            self.clase_tabla_etapas = self.obtener_valor_config_proceso(nombre_subproceso, "clase_tabla_etapas")
            
            self.cadenas_no_contar_etapa = self.obtener_valor_config_proceso(nombre_subproceso, "cadenas_no_contar_etapa")
            self.numero_etapas_gran_vuelta = int(self.obtener_valor_config_proceso(nombre_subproceso, "numero_etapas_gran_vuelta"))
            self.jornadas_descanso_gran_vuelta = int(self.obtener_valor_config_proceso(nombre_subproceso, "jornadas_descanso_gran_vuelta"))

            self.columna_numero_clasica = int(self.obtener_valor_config_proceso(nombre_subproceso, "columna_numero_clasica"))
            self.columna_fecha_clasica = int(self.obtener_valor_config_proceso(nombre_subproceso, "columna_fecha_clasica"))
            self.columna_nombre_clasica = int(self.obtener_valor_config_proceso(nombre_subproceso, "columna_nombre_clasica"))
            self.columna_categoria_clasica = int(self.obtener_valor_config_proceso(nombre_subproceso, "columna_categoria_clasica"))

        except Exception as e:
            raise ExcepcionScrapping(f"Error al cargar los valores de configuración de '{nombre_subproceso}'") from e


    def _determinar_tipo_grupo(self, soup: BeautifulSoup) -> str:

        """
        Determina si la competición es un grupo de vueltas o un grupo de clásicas.

        Parámetros:
            soup (BeautifulSoup): Objeto BeautifulSoup que contiene el HTML de la página scrappeada.

        Salida:
            str: Retorna 'grupo_vueltas' si es un grupo de vueltas, de lo contrario retorna 'grupo_clasicas'.
        """

        try:

            if self._es_grupo_vueltas(soup):
                return self.tipo_grupo_vueltas

            else:
                return self.tipo_grupo_clasicas

        except ExcepcionScrapping as e:
            raise ExcepcionScrapping(f"No ha sido posible determinar el tipo grupo de competciones") from e


    def _es_grupo_vueltas(self, soup: BeautifulSoup) -> bool:

        """
        Determina si una competición es grupo de vueltas o grupo de clásicas.

        Busca el primer <div class="postcontent"> y verifica si contiene un <span class="race">,
        lo que indica que es un grupo de vueltas. Si no encuentra dicho span, asume que es un grupo de clásicas.

        Parámetros:
            soup (BeautifulSoup): Objeto BeautifulSoup que contiene el HTML de la página scrappeada.

        Salida:
            bool: True si es un grupo de vueltas, False si es un grupo de clásicas.

        Lanza:
            ExcepcionScrapping: Si no se encuentran las etiquetas para determinar si es grupo de vueltas o grupo de clásicas.
        """

        postcontent = soup.find('div', class_=self.clase_competicion)

        if postcontent is None:
            raise ExcepcionScrapping(f"No fue posible encontrar 'div' con clase '{self.clase_competicion}'")

        if postcontent.find('span', class_=self.clase_grupo_vueltas):
            return True

        else:
            return False


    def _extraer_url_descripcion_y_fecha_inicio_vuelta(self, postcontent: BeautifulSoup) -> Dict[str, str]:

        """
        Extrae la URL, descripcion y fecha de inicio de la competición.

        Parámetros:
            postcontent (BeautifulSoup): Objeto que contiene el HTML de la competición.

        Salida:
            dict: Diccionario con los datos de la competición (fecha_inicio, nombre_competicion, url).
        
        Lanza:
            ExcepcionScrapping: Si ocurre un error al extraer los datos.
        """

        try:
            etiquetas_tipo_fecha = postcontent.find_all('span')
            etiqueta_fecha_inicio = etiquetas_tipo_fecha[self.numero_etiqueta_fecha_vuelta_x_etapas - 1]
            fecha_inicio_completa = fecha_utils.completar_anyo(etiqueta_fecha_inicio.text.strip().split('\n')[0])
            fecha_inicio_limpia = fecha_utils.limpiar_fecha(fecha_inicio_completa)
            fecha_inicio = fecha_utils.convertir_formato_fecha(fecha_inicio_limpia,
                                                               self.formato_fecha_vuelta_x_etapas,
                                                               self.formato_fecha_generico)

            h2_tag = postcontent.find('h2')
            nombre_competicion = self._ajustar_nombre_competicion(h2_tag.text)

            hiperenlace = postcontent.find('a', class_=self.clases_enlace_competiciones)
            url = string_utils.completar_url(hiperenlace['href']) if hiperenlace else ""

            return {
                'url': url,
                'descripcion': nombre_competicion,
                'fecha_inicio': fecha_inicio
            }

        except Exception as e:
            raise ExcepcionScrapping(f"Error al extraer (url, descripción, fecha de inicio) de una vuelta por etapas") from e


    def _obtener_numero_etapas_fecha_fin_tipo_vuelta(self, url: str, fecha_inicio: str) -> Tuple[int, str, str]:

        """
        Obtiene el número de etapas y calcula la fecha de fin de la competición.
        Si la competición es una gran vuelta, se le suman 2 días a la fecha de fin.

        Parámetros:
            url (str): URL de la página de la competición.
            fecha_inicio (str): Fecha de inicio de la competición.

        Salida:
            tuple: Número de etapas, fecha de fin calculada y tipo de vuelta.

        Lanza:
            ExcepcionScrapping: Si ocurre un error al obtener el número de etapas.
        """

        try:
            url_etapas = url + self.url_info_detalle
            soup_etapas = self.obtener_soup_pagina(url_etapas)
            numero_etapas = self._obtener_numero_etapas(soup_etapas)
            
            tipo_vuelta = self._determinar_tipo_vuelta(numero_etapas)
            jornadas_descanso = self.jornadas_descanso_gran_vuelta if tipo_vuelta == self.tipo_gran_vuelta else 0
            fecha_fin = fecha_utils.sumar_dias_a_fecha(fecha_inicio,
                                                       numero_etapas - 1 + jornadas_descanso,
                                                       self.formato_fecha_generico)
        
            return numero_etapas, fecha_fin, tipo_vuelta

        except Exception as e:
            raise ExcepcionScrapping(f"Error al obtener (número de etapas, fecha de fin, tipo de vuelta)") from e


    def _obtener_numero_etapas(self, soup_etapas) -> int:

        """
        Obtiene el número de etapas de una vuelta, se excluyen aquellas
        filas que contienen las palabras "NULL" o "End-Of-Tour".

        Parámetros:
            soup_etapas (BeautifulSoup): Objeto BeautifulSoup que contiene la página de las etapas.

        Salida:
            int: Número de etapas válidas.
        """

        try:
            tabla_etapas = soup_etapas.find('table', class_=self.clase_tabla_etapas)
            if tabla_etapas:
                etapas = tabla_etapas.find('tbody').find_all('tr')
                numero_etapas = len([etapa for etapa in etapas 
                                    if not string_utils.contiene_cualquier_subcadena(etapa.get_text().strip(),
                                                                                     self.cadenas_no_contar_etapa.split(','))])
            
            else:
                numero_etapas = 0

            return numero_etapas

        except Exception as e:
            raise ExcepcionScrapping(f"Error al obtener el núemero de etapas") from e


    def _determinar_tipo_vuelta(self, numero_etapas: int) -> str:

        """
        Determina el tipo de vuelta según el número de etapas.

        Parámetros:
            numero_etapas (int): Número de etapas en la vuelta.

        Salida:
            str: Tipo de vuelta ('gran_vuelta' o 'vuelta_menor').
        """

        if numero_etapas == self.numero_etapas_gran_vuelta:
            return self.tipo_gran_vuelta
        
        else:
            return self.tipo_vuelta_menor


    def _extraer_info_vueltas(self, soup: BeautifulSoup, ignorar_primera_competicion: list) -> list:

        """
        Procesa todas las competiciones dentro del objeto soup, obteniendo su información básica y detalles,
        ignorando las competiciones que están en la lista de excepciones.

        Parámetros:
            soup (BeautifulSoup): Objeto BeautifulSoup que contiene el HTML de las competiciones.
            ignorar_primera_competicion (list): Ignora la primera competición (excepción de clásicas femeninas).

        Salida:
            list: Una lista de diccionarios donde cada diccionario contiene:
                - 'url' (str): La URL de la competición.
                - 'descripcion' (str): El nombre de la competición.
                - 'numero_etapas' (int): El número de etapas de la vuelta.
                - 'tipo_vuelta' (str): Gran vuelta o vuelta por etapas.
                - 'fecha_inicio' (str): La fecha de inicio de la vuelta.
                - 'fecha_fin' (str): La fecha de fin la vuelta.

        Lanza:
            ExcepcionScrapping: Si ocurre un error al procesar las competiciones.
        """
        
        vueltas: list = []
        
        try:
            postcontents = soup.find_all('div', class_='postcontent')

            if ignorar_primera_competicion:
                postcontents = postcontents[1:]

            for postcontent in postcontents:
                datos_vuelta = self._extraer_url_descripcion_y_fecha_inicio_vuelta(postcontent)
                numero_etapas, fecha_fin, tipo_vuelta = self._obtener_numero_etapas_fecha_fin_tipo_vuelta(datos_vuelta['url'],
                                                                                                          datos_vuelta['fecha_inicio'])

                vueltas.append(self._crear_vuelta(datos_vuelta, numero_etapas, tipo_vuelta, fecha_fin))

            return vueltas

        except Exception as e:
            raise ExcepcionScrapping(f"Error al extraer información de una vueltas por etapas") from e


    def _crear_vuelta(self, datos_vuelta: dict, numero_etapas: int, tipo_vuelta: str, fecha_fin: str) -> dict:
    
        """
        Crea un diccionario que representa una vuelta.

        Parámetros:
            datos_vuelta (dict): Un diccionario que contiene información sobre la vuelta,
                                 incluyendo 'url', 'descripcion' y 'fecha_inicio'.
            numero_etapas (int): Número de etapas de la vuelta.
            tipo_vuelta (str): Tipo de vuelta 'gran_vuelta' o 'vuelta_menor'.
            fecha_fin (str): Fecha de fin de la vuelta.

        Salida:
            None: Este método no retorna ningún valor, simplemente agrega el resultado a la lista.
        """

        return {
            'url': datos_vuelta['url'],
            'descripcion': datos_vuelta['descripcion'],
            'numero_etapas': numero_etapas,
            'tipo_vuelta': tipo_vuelta,
            'fecha_inicio': datos_vuelta['fecha_inicio'],
            'fecha_fin': fecha_fin
        }


    def _buscar_excepcion_clasicas_femeninas(self, soup: BeautifulSoup, genero: str) -> list[dict]:

        """
        Busca excepciones que convierten una competición de vueltas en una nueva competición de clásicas.

        Busca dentro del primer <div class="postcontent"> si el texto del <h2> contiene "FANTASY WOMENS CLASSICS".
        Si encuentra este texto, extrae el nombre y la URL de la nueva competición.

        Parámetros:
            soup (BeautifulSoup): Objeto BeautifulSoup que contiene el HTML de la página scrappeada.
            genero (str): Género de la competición actual (masculino o femenino).

        Salida:
            list[dict]: Lista de nuevas competiciones detectadas, en formato de diccionarios.
        """

        nuevas_competiciones = []
        postcontent = soup.find('div', class_=self.clase_competicion)

        if postcontent is not None:
            h2_tag = postcontent.find('h2')

            if h2_tag and string_utils.contiene_subcadena(h2_tag.text, self.cadena_clasicas_femeninas):
                nombre_competicion = self.limpiar_nombre_competicion(h2_tag.text, self.textos_eliminar_competicion.split(','))
                hiperenlace = postcontent.find('a', class_=self.clases_enlace_competiciones)
                url = hiperenlace['href'] if hiperenlace else ""

                nuevas_competiciones.append({
                    'nombre': nombre_competicion,
                    'genero': genero,
                    'url': string_utils.completar_url(url),
                    'tipo_grupo': self.tipo_grupo_vueltas
                })

        return nuevas_competiciones


    def _extraer_info_grupo(self, soup, tipo_grupo: str, url: str, excepcion_clasicas_femeninas: bool) -> dict:

        """
        Extrae la información del grupo de competiciones según el tipo de grupo (vueltas o clásicas).

        Parámetros:
            soup (BeautifulSoup): El objeto BeautifulSoup que contiene el HTML de la página.
            tipo_grupo (str): El tipo de grupo de competición (vueltas o clásicas).
            url (str): URL de la página a la que se está haciendo el scrapping.
            excepcion_clasicas_femeninas (bool): Indica si se aplica la excepción para clásicas femeninas.

        Salida:
            dict: Diccionario con la información desglosada del grupo de competiciones.

        Lanza:
            ExcepcionScrapping: Si ocurre algún error durante la extracción de la información.
        """

        if tipo_grupo == self.tipo_grupo_vueltas:
            return self._extraer_info_vueltas(soup, excepcion_clasicas_femeninas)

        elif tipo_grupo == self.tipo_grupo_clasicas:
            return self._extraer_info_clasicas(url)

        else:
            raise ExcepcionScrapping(f"Tipo de grupo no reconocido: {tipo_grupo}")


    def _extraer_info_clasicas(self, url: str) -> list:

        """
        Extrae la información de un grupo de clásicas a partir de una URL de la página.

        Parámetros:
            url (str): URL de la página a la que se está haciendo el scrapping.

        Salida:
            list: Lista de diccionarios con la información de cada clásica (número, fecha, nombre, categoría).

        Lanza:
            ExcepcionScrapping: Si ocurre algún error durante la extracción de la información.
        """

        try:
            url_clasicas_grupo = url + self.url_info_detalle
            soup_clasicas = self.obtener_soup_pagina(url_clasicas_grupo)
            tabla = soup_clasicas.find('table')

            if not tabla:
                raise ExcepcionScrapping(f"No se pudo encontrar la tabla de clásicas en la página en {url_clasicas_grupo}")

            clasicas: list = []

            for fila in tabla.find_all('tr')[1:]:
                columnas = fila.find_all('td')

                numero_clasica = columnas[self.columna_numero_clasica].get_text(strip=True)
                fecha_clasica = columnas[self.columna_fecha_clasica].get_text(strip=True)
                fecha_clasica_formato = fecha_utils.convertir_formato_fecha(fecha_clasica,
                                                                            self.formato_fecha_clasica,
                                                                            self.formato_fecha_generico)

                numero_clasica = self._corregir_numero_clasica(numero_clasica, fecha_clasica_formato)

                nombre_clasica = columnas[self.columna_nombre_clasica].get_text(strip=True)
                categoria = columnas[self.columna_categoria_clasica].get_text(strip=True)[-1]

                clasicas.append(self._crear_clasica(numero_clasica, fecha_clasica_formato, nombre_clasica, categoria))

            return clasicas

        except Exception as e:
            raise ExcepcionScrapping(f"Error al extraer la información de clásicas de {url_clasicas_grupo}") from e


    def _crear_clasica(self, numero_clasica: int, fecha_clasica: str, nombre_clasica: str, categoria: str) -> dict:

        """
        Crea un diccionario que representa una clásica.

        Parámetros:
            numero_clasica (int): El número de la clásica.
            fecha_clasica (str): La fecha de la clásica en formato adecuado.
            nombre_clasica (str): El nombre de la clásica.
            categoria (str): La categoría de la clásica.

        Salida:
            dict: Un diccionario que representa la clásica.
        """
        
        return {
            'numero_clasica': numero_clasica,
            'fecha_clasica': fecha_clasica,
            'nombre_clasica': nombre_clasica,
            'categoria': categoria
        }


    def _corregir_numero_clasica(self, numero_clasica: str, fecha_clasica: str) -> str:

        """
        Corrige el número de la clásica si contiene información extra, como la fecha.
        
        A veces, el HTML mal formado puede mezclar varias columnas, y el contenido de `numero_clasica`
        puede incluir la fecha de la clásica, causando que tenga más información de la necesaria.
        Este método corrige esa situación.

        Parámetros:
            numero_clasica (str): El número de la clásica que posiblemente contiene información extra.
            fecha_clasica (str): La fecha de la clásica, que podría estar accidentalmente dentro del número.

        Retorna:
            str: El número corregido de la clásica, sin información extra.

        Ejemplo:
            Si tenemos:
            - numero_clasica: '12024-03-02 11:00:00Strade Bianche'
            - fecha_clasica: '2024-03-02 11:00:00'

            El método corregirá `numero_clasica` a '1' quitando la fecha y cualquier otro texto que no pertenezca al número.
        """

        if string_utils.contiene_subcadena(numero_clasica, fecha_clasica):
            numero_clasica = numero_clasica.split(fecha_clasica)[0].strip()

        return numero_clasica


    def _ajustar_nombre_competicion(self, nombre_competicion: str) -> str:
        
        """
        Aplica las sustituciones y elimina los textos innecesarios en el nombre de la competición.

        Parámetros:
            nombre_competicion (str): Nombre original de la competición.

        Salida:
            str: Nombre de la competición después de aplicar las sustituciones y limpiezas.
        """

        try:
            texto_sustituir_tour_masculino = self.texto_sustituir_tour_masculino.split(',')
            texto_sustituir_tour_femenino = self.texto_sustituir_tour_femenino.split(',')
            textos_eliminar = self.textos_eliminar_competicion.split(',')

            nombre_competicion = string_utils.sustituir_cadena_con_marcador(
                nombre_competicion,
                texto_sustituir_tour_masculino[0],
                texto_sustituir_tour_masculino[1],
                '@yyyy@'
            )

            nombre_competicion = string_utils.sustituir_cadena_con_marcador(
                nombre_competicion,
                texto_sustituir_tour_femenino[0],
                texto_sustituir_tour_femenino[1],
                '@yyyy@'
            )

            nombre_competicion = self.limpiar_nombre_competicion(nombre_competicion, textos_eliminar)

            return nombre_competicion

        except Exception as e:
            raise ExcepcionScrapping(f"Error al ajustar el nombre de la competición '{nombre_competicion}'") from e