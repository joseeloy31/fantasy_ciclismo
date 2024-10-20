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


def contiene_subcadena(cadena: str, cadena_buscar: list) -> bool:

    """
    Verifica si una cadena está contenida en otra.
    
    Parámetros:
        cadena (str): Cadena en la que buscar.
        cadena_buscar (list): Cadena que buscar dentro de la cadena principal.
    
    Salida:
        bool: True si las cadena a buscar está contenida en la cadena principal, False en caso contrario.
    """

    cadena = cadena.lower()

    if cadena_buscar.lower() in cadena:
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
    nuevo_nombre = nuevo_nombre.replace(".properties", "")

    return f"{nuevo_nombre}.properties"


def completar_url(url: str) -> str:

    """
    Completa la URL en caso de que le falte el esquema HTTP o HTTPS.

    Parámetros:
        url (str): URL parcial o completa de la competición.

    Salida:
        str: URL completa con el esquema correcto.
    """

    if url.startswith('//'):
        return f'https:{url}'

    return url


def eliminar_subcadena_ignorando_case(cadena_principal: str, subcadena: str) -> str:
    
    """
    Elimina la primera aparición de la subcadena de la cadena principal ignorando mayúsculas y minúsculas.

    Parámetros:
        cadena_principal (str): La cadena de la que se eliminará la subcadena.
        subcadena (str): La subcadena que se desea eliminar.

    Salida:
        str: La cadena resultante después de eliminar la subcadena.
    """

    posicion = cadena_principal.lower().find(subcadena.lower())
    
    if posicion != -1:
        return cadena_principal[:posicion] + cadena_principal[posicion + len(subcadena):]
    
    return cadena_principal


import re

def sustituir_cadena_con_marcador(cadena_principal: str, texto_sustituir: str, texto_reemplazo: str, marcador: str = "yyyy") -> str:

    """
    Sustituye el texto de la cadena principal, manteniendo el valor del marcador 
    y colocando un prefijo antes de él. El marcador se define como parámetro para flexibilidad.

    Parámetros:
        cadena_principal (str): La cadena original donde se hará la sustitución.
        texto_sustituir (str): El texto que contiene el patrón de sustitución con un marcador.
        texto_reemplazo (str): El texto que reemplazará la cadena original, también con el marcador.
        marcador (str): El marcador que representa la variable a capturar y reemplazar.

    Salida:
        str: La cadena con la sustitución realizada.
    """
    
    patron = texto_sustituir.replace(marcador, r"(.+?)")
    match = re.search(patron, cadena_principal, flags=re.IGNORECASE)
    
    if match:
        valor_capturado = match.group(1)
        texto_reemplazado = texto_reemplazo.replace(marcador, valor_capturado)
        
        return re.sub(patron, texto_reemplazado, cadena_principal, flags=re.IGNORECASE).strip()
    
    return cadena_principal