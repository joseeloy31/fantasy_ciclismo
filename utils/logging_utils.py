# utils/logging_utils.py

from logging.handlers import RotatingFileHandler
from utils.properties_utils import leer_properties, obtener_property
from utils.excepciones import ExcepcionConfiguracion, ExcepcionLogging
import logging
import os

# Constantes
CTE_NIVELES_LOGGING = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

def _cargar_configuracion_logging(ruta_config, nombre_config):

    """
    Método privado para cargar la configuración de logging desde un archivo de properties.

    Parámetros:
        ruta_config (str): Ruta del fichero de configuración del log.
        nombre_config (str): Nombre del fichero de configuración del log.

    Salida:
        tuple: (directorio_logs, tamanyo_maximo_mb, archivos_rotativos, nivel_archivo, nivel_consola)
    
    Lanza:
        ExcepcionLogging: Si ocurre algún error en la configuración de logging.
    """

    try:
        fichero_config = leer_properties(f"{ruta_config}{nombre_config}")

        directorio_logs = obtener_property(fichero_config, 'logging', 'dir', default='logs')
        tamanyo_maximo_mb = int(obtener_property(fichero_config, 'logging', 'max_size_mb', default=1)) * 1024 * 1024
        archivos_rotativos = int(obtener_property(fichero_config, 'logging', 'backup_count', default=10))
        nivel_archivo = CTE_NIVELES_LOGGING.get(obtener_property(fichero_config, 'logging', 'nivel_archivo', default='DEBUG'))
        nivel_consola = CTE_NIVELES_LOGGING.get(obtener_property(fichero_config, 'logging', 'nivel_consola', default='INFO'))

        return directorio_logs, tamanyo_maximo_mb, archivos_rotativos, nivel_archivo, nivel_consola

    except KeyError as ke:
        raise ExcepcionLogging(f"Error al leer la clave '{ke.args[0]}' del archivo '{nombre_config}'") from ke

    except ExcepcionConfiguracion as ec:
        raise ExcepcionLogging(f"Error en la configuración: {str(ec)}") from ec
    
    except Exception as e:
        raise ExcepcionLogging(f"Error al cargar la configuración de logging: {str(e)}") from e


def inicializar_logging(ruta_config, nombre_config, proceso):

    """
    Inicializa el sistema de logging con salidas tanto a archivo como a consola.

    Parámetros:
        ruta_config (str): Ruta del fichero de configuración del log.
        nombre_config (str): Nombre del fichero de configuración del log.
        proceso (str): Nombre del proceso que llama a la inicialización del log.

    Salida:
        logging.Logger: Objeto de logger configurado.
    
    Lanza:
        ExcepcionLogging: Si ocurre algún error en la configuración de logging.
    """

    try:
        directorio_logs, tamanyo_maximo_mb, archivos_rotativos, nivel_archivo, nivel_consola = _cargar_configuracion_logging(ruta_config, nombre_config)
        ruta_log = _generar_ruta_log(directorio_logs, proceso)
        logger = _configurar_logger(proceso, nivel_archivo, nivel_consola, ruta_log, tamanyo_maximo_mb, archivos_rotativos)

        return logger

    except ExcepcionLogging as el:
        raise el

    except Exception as e:
        raise ExcepcionLogging(f"Error al configurar el logging: {str(e)}") from e


def _generar_ruta_log(directorio_logs, proceso):
    
    """
    Genera la ruta del archivo de log y crea el directorio si no existe.

    Parámetros:
        directorio_logs (str): Directorio donde se almacenarán los logs.
        proceso (str): Nombre del proceso que genera el log.

    Salida:
        str: Ruta completa del archivo de log.
    
    Lanza:
        ExcepcionLogging: Si ocurre un error al generar la ruta del log.
    """

    try:
        os.makedirs(directorio_logs, exist_ok=True)
        nombre_archivo_log = f"{proceso}.log"
 
        return os.path.join(directorio_logs, nombre_archivo_log)
 
    except Exception as e:
        raise ExcepcionLogging(f"Error al generar la ruta del log para el proceso '{proceso}': {str(e)}") from e


def _configurar_logger(proceso, nivel_archivo, nivel_consola, ruta_log, tamanyo_maximo_mb, archivos_rotativos):
 
    """
    Configura el logger con handlers para archivo y consola.

    Parámetros:
        proceso (str): Nombre del proceso que genera el log.
        nivel_archivo (int): Nivel de logging para el archivo.
        nivel_consola (int): Nivel de logging para la consola.
        ruta_log (str): Ruta del archivo de log.
        tamanyo_maximo_mb (int): Tamaño máximo del archivo de log en bytes.
        archivos_rotativos (int): Número de archivos de log rotativos.

    Salida:
        logging.Logger: Objeto de logger configurado.

    Lanza:
        ExcepcionLogging: Si ocurre un error al configurar el logger.
    """
 
    try:
        formato_log = logging.Formatter('%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        logger = logging.getLogger(proceso)
        logger.setLevel(min(nivel_archivo, nivel_consola))

        archivo_handler = _crear_handler_archivo(ruta_log, tamanyo_maximo_mb, archivos_rotativos, nivel_archivo, formato_log)
        consola_handler = _crear_handler_consola(nivel_consola, formato_log)

        logger.addHandler(archivo_handler)
        logger.addHandler(consola_handler)

        return logger

    except ExcepcionLogging as el:
        raise el

    except Exception as e:
        raise ExcepcionLogging(f"Error al configurar el logger para el proceso '{proceso}': {str(e)}") from e

def _crear_handler_archivo(ruta_log, tamanyo_maximo_mb, archivos_rotativos, nivel_archivo, formato_log):

    """
    Crea un handler para el logging en archivo.

    Parámetros:
        ruta_log (str): Ruta del archivo de log.
        tamanyo_maximo_mb (int): Tamaño máximo del archivo de log en bytes.
        archivos_rotativos (int): Número de archivos de log rotativos.
        nivel_archivo (int): Nivel de logging para el archivo.
        formato_log (logging.Formatter): Formato del log.

    Salida:
        logging.Handler: Handler configurado para el logging en archivo.

    Lanza:
        ExcepcionLogging: Si ocurre un error al crear el handler de archivo.
    """

    try:
        archivo_handler = RotatingFileHandler(filename=ruta_log, maxBytes=tamanyo_maximo_mb, backupCount=archivos_rotativos)
        archivo_handler.setLevel(nivel_archivo)
        archivo_handler.setFormatter(formato_log)

        return archivo_handler

    except Exception as e:
        raise ExcepcionLogging(f"Error al crear el handler de archivo para '{ruta_log}': {str(e)}") from e


def _crear_handler_consola(nivel_consola, formato_log):

    """
    Crea un handler para el logging en consola.

    Parámetros:
        nivel_consola (int): Nivel de logging para la consola.
        formato_log (logging.Formatter): Formato del log.

    Salida:
        logging.Handler: Handler configurado para el logging en consola.

    Lanza:
        ExcepcionLogging: Si ocurre un error al crear el handler de consola.
    """

    try:
        consola_handler = logging.StreamHandler()
        consola_handler.setLevel(nivel_consola)
        consola_handler.setFormatter(formato_log)

        return consola_handler

    except Exception as e:
        raise ExcepcionLogging(f"Error al crear el handler de consola: {str(e)}") from e