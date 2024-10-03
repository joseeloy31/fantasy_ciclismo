import configparser

def leer_properties(ruta_properties):
    
    # Lee un archivo .properties y devuelve un objeto ConfigParser con las propiedades cargadas.
    # 
    # Parámetros:
    # ruta_properties (str): Ruta del archivo .properties.
    #
    # Retorno:
    # configparser.ConfigParser: Objeto con las propiedades.

    config = configparser.ConfigParser()
    config.read(ruta_properties)
    return config

def obtener_property(propiedades, seccion, clave, default=None):

    # Obtiene el valor de una propiedad del archivo de configuración.
    # 
    # Parámetros:
    # propiedades (ConfigParser): Objeto con las propiedades cargadas.
    # seccion (str): Sección del archivo de configuración de donde se obtiene la propiedad.
    # clave (str): Clave de la propiedad a obtener.
    # default (any): Valor por defecto a retornar si la clave no existe.
    # 
    # Retorno:
    # str: Valor de la propiedad o el valor por defecto si no existe.

    return propiedades.get(seccion, clave, fallback=default)
