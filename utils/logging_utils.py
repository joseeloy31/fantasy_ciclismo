import logging
import os
from logging.handlers import RotatingFileHandler
from utils.properties_utils import leer_properties, obtener_property

def inicializar_logging(ruta_properties, proceso):

    # Inicializa el sistema de logging utilizando las propiedades del archivo config.properties.
    # 
    # Parámetros:
    # ruta_properties (str): Ruta al archivo de configuración .properties.
    # proceso (str): Nombre del proceso (puede ser un script o componente) para usarlo en el archivo de log correspondiente.
    # 
    # Retorno:
    # logging.Logger: Logger configurado con el sistema de rotación de archivos.

    propiedades = leer_properties(ruta_properties)

    directorio_logs = obtener_property(propiedades, 'logging', 'dir', default='logs')
    tamaño_maximo_mb = int(obtener_property(propiedades, 'logging', 'max_size_mb', default=1)) * 1024 * 1024
    archivos_rotativos = int(obtener_property(propiedades, 'logging', 'backup_count', default=10))

    if not os.path.exists(directorio_logs):
        os.makedirs(directorio_logs)

    nombre_archivo_log = f"{proceso}.log"
    ruta_log = os.path.join(directorio_logs, nombre_archivo_log)

    logger = logging.getLogger(proceso)
    logger.setLevel(logging.INFO)

    manejador_rotativo = RotatingFileHandler(
        filename=ruta_log,
        maxBytes=tamaño_maximo_mb,
        backupCount=archivos_rotativos
    )

    manejador_rotativo.setFormatter(
        logging.Formatter('%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    )

    logger.addHandler(manejador_rotativo)

    return logger