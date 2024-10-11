# utils/string_utils.py

def comparar_cadenas_ignorando_case(cadena1: str, cadena2: str) -> bool:

    """
    Compara dos cadenas de texto sin tener en cuenta las mayúsculas o minúsculas.
    
    Parámetros:
        cadena1 (str): Primera cadena a comparar.
        cadena2 (str): Segunda cadena a comparar.
    
    Salida:
        bool: True si las cadenas son iguales sin tener en cuenta mayúsculas/minúsculas, False en caso contrario.
    """

    return cadena1.strip().lower() == cadena2.strip().lower()


def contiene_cualquier_subcadena(cadena: str, subcadenas: list) -> bool:

    """
    Verifica si una cadena contiene cualquiera de las subcadenas dadas.
    
    Parámetros:
        cadena (str): Cadena en la que buscar.
        subcadenas (list): Lista de subcadenas a buscar dentro de la cadena principal.
    
    Salida:
        bool: True si alguna de las subcadenas está contenida en la cadena, False en caso contrario.
    """

    cadena = cadena.lower()

    for subcadena in subcadenas:

        if subcadena.lower() in cadena:
            return True

    return False


def obtener_nombre_properties_proceso(nombre_proceso: str,
                                      prefijo_proceso: str = 'cron',
                                      prefijo_properties: str = 'scrapping') -> str:

    """
    Convierte el prefijo del proceso en un nombre de archivo .properties.
    
    Ejemplo: 
        'cron' se convierte en 'scrapping',
        y devuelve 'scrapping_actualizar_calendario.properties'
        para un proceso llamado 'cron_actualizar_calendario'.
    
    Parámetros:
        nombre_proceso (str): El nombre del proceso (ej. 'actualizar_calendario').
        prefijo_proceso (str, optional): El prefijo a buscar ysustituir (ej. 'cron').Default es 'cron'.
        prefijo_properties (str, optional): El prefijo a utilizar en lugar del anterior (ej. 'scrapping'). Default es 'scrapping'.
    
    Salida:
        str: El nombre de archivo para el log del scrapping.
    """

    nuevo_nombre = nombre_proceso.replace(prefijo_proceso, prefijo_properties)
    return f"{nuevo_nombre}.properties"