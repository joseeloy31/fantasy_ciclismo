# utils/config.py

import logging
from typing import Dict
import utils.properties_utils as properties_utils
import utils.string_utils as string_utils
import utils.logging_utils as logging_utils
from utils.excepciones import ExcepcionConfig

class Config:

    """
    Clase singleton para manejar la configuración de la aplicación.

    Esta clase se encarga de inicializar el logger y cargar
    la configuración a partir de un archivo de propiedades.

    Atributos:
        logger (logging.Logger): Objeto de logger configurado.
        proceso (str): Nombre del proceso que utiliza esta configuración.
    """

    _instancia = None
    _conexion_bbdd = None


    def __new__(cls, *args, **kwargs) -> 'Config':

        """
        Controla la creación de la instancia singleton de Config.

        Si es la primera vez que se invoca, se espera que se pase la ruta de
        configuración, el nombre del archivo de configuración y el nombre del proceso para inicializar
        la configuración. En llamadas subsecuentes, ya no se requieren los parámetros.

        Parámetros:
            *args: Argumentos posicionales opcionales (no se utilizan en este caso).
            **kwargs: Diccionario de argumentos opcionales. 
                - ruta_config (str): Ruta del directorio de configuración.
                - nombre_config (str): Nombre del archivo de configuración de propiedades.
                - proceso (str): Nombre del proceso que utiliza esta configuración.

        Salida:
            Config: La instancia de Config.

        Lanza:
            ExcepcionConfig: Si faltan los parámetros requeridos en la primera llamada.
        """

        try:
            if cls._instancia is None:
                ruta_config = kwargs.get('ruta_config')
                nombre_config = kwargs.get('nombre_config')
                proceso = kwargs.get('proceso')

                if ruta_config is None or nombre_config is None or proceso is None:
                    raise ExcepcionConfig("Faltan parámetros en la primera llamada a la clase Config")

                cls._instancia = super(Config, cls).__new__(cls)
                cls._instancia._inicializar(ruta_config, nombre_config, proceso)

            return cls._instancia

        except Exception as e:
            raise ExcepcionConfig("Error en la creación del Singleton Config") from e


    def _inicializar(self, ruta_config: str, nombre_config: str, proceso: str) -> None:

        """
        Inicializa el logger y los atributos de la clase.

        Parámetros:
            ruta_config (str): Ruta del directorio de configuración.
            nombre_config (str): Nombre del archivo de configuración de propiedades.
            proceso (str): Nombre del proceso que utiliza esta configuración.

        Salida:
            None

        Lanza:
            ExcepcionConfig: Si ocurre un error al inicializar el logger.
        """

        try:
            self.proceso = proceso
            self.logger = logging_utils.inicializar_logging(ruta_config, nombre_config, proceso)
            self.fichero_config_general = self._inicializar_fichero_config(ruta_config, nombre_config)
            self.fichero_config_proceso = self._inicializar_fichero_config(ruta_config, proceso)

        except Exception as e:
            raise ExcepcionConfig(f"Error al inicializar la configuración de '{proceso}'") from e


    def obtener_logger(self) -> logging.Logger:

        """
        Devuelve el logger configurado.

        Parámetros:
            None

        Salida:
            logging.Logger: El objeto de logger configurado.
        """

        return self.logger


    def obtener_fichero_config_general(self) -> Dict[str, str]:

        """
        Devuelve el diccionario con la configuración general.

        Parámetros:
            None

        Salida:
            dict: Diccionario con las claves y valores de la configuración general.
        """

        return self.fichero_config_general


    def obtener_fichero_config_proceso(self) -> Dict[str, str]:

        """
        Devuelve el diccionario con la configuración específica del proceso.

        Parámetros:
            None

        Salida:
            dict: Diccionario con las claves y valores de la configuración del proceso.
        """

        return self.fichero_config_proceso


    def _inicializar_fichero_config(self, ruta_config: str, nombre_proceso: str) -> Dict[str, str]:

        """
        Carga el archivo de configuración y devuelve un diccionario con claves del tipo 'seccion.propiedad' y valores asociados.

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

        except Exception as e:
            raise ExcepcionConfig(f"Error inesperado al leer el fichero de configuración de '{nombre_proceso}'") from e