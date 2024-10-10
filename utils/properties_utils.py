# utils/properties_utils.py

import configparser
import os
from utils.excepciones import ExcepcionConfiguracion

def leer_properties(ruta_properties):
    
    """
    Lee un archivo .properties y devuelve un objeto ConfigParser con las propiedades cargadas.

    Parámetros:
        ruta_properties (str): Ruta del archivo .properties.

    Salida:
        configparser.ConfigParser: Objeto con las propiedades cargadas.

    Lanza:
        ExcepcionConfiguracion: Si el archivo de propiedades no se encuentra o no se puede leer.
    """

    if not os.path.exists(ruta_properties):
        raise ExcepcionConfiguracion(f"El archivo de propiedades '{ruta_properties}' no existe o no se puede acceder.")

    try:
        config = configparser.ConfigParser()
        config.read(ruta_properties)
        return config

    except Exception as e:
        raise ExcepcionConfiguracion(f"Error al leer el archivo de propiedades: {str(e)}") from e

def obtener_property(propiedades, seccion, clave, default=None):

    """
    Obtiene el valor de una propiedad del archivo de configuración.

    Parámetros:
        propiedades (ConfigParser): Objeto ConfigParser con las propiedades cargadas.
        seccion (str): Sección del archivo de configuración de donde se obtiene la propiedad.
        clave (str): Clave de la propiedad a obtener.
        default (any): Valor por defecto a retornar si la clave no existe. Por defecto es None.

    Salida:
        str: Valor de la propiedad o el valor por defecto si no existe.

    Lanza:
        ExcepcionConfiguracion: Si la sección o clave especificada no existe en el archivo de propiedades
                                y no se proporciona un valor por defecto.
    """

    try:
        return propiedades.get(seccion, clave, fallback=default)
    
    except configparser.NoSectionError:
        raise ExcepcionConfiguracion(f"La sección '{seccion}' no existe en el archivo de propiedades.")
    
    except configparser.NoOptionError:
        raise ExcepcionConfiguracion(f"La clave '{clave}' no existe en la sección '{seccion}'.")