# utils/fecha_utils.py

from datetime import datetime, timedelta
from utils.excepciones import ExcepcionFecha
import re

def limpiar_fecha(fecha: str) -> str:

    """
    Elimina los sufijos "st", "nd", "rd", "th" de una cadena de fecha.

    Parámetro:
        fecha (str): Cadena que contiene una fecha con sufijos.

    Salida:
        str: Cadena de fecha sin sufijos.

    Lanza:
        ExcepcionFecha: Si la cadena de fecha es inválida.
    """

    try:

        return re.sub(r'(\d+)(st|nd|rd|th)', r'\1', fecha)

    except Exception as e:
        raise ExcepcionFecha(f"Error al limpiar la fecha {fecha}")


def convertir_a_datetime(fecha: str, formato: str) -> datetime:

    """
    Convierte una cadena de fecha en un objeto datetime usando un formato dado.

    Parámteros:
        fecha (str): Cadena de fecha a convertir.
        formato (str): Formato en que se espera la fecha (ej. "%d %B %Y").

    Returns:
        datetime: Objeto datetime correspondiente a la fecha dada.

    Raises:
        ExcepcionFecha: Si la conversión a datetime falla.
    """

    try:
        return datetime.strptime(fecha, formato)

    except ValueError as e:
        raise ExcepcionFecha(f"Formato de fecha inválido: {str(e)}")


def sumar_dias_a_fecha(fecha: str, dias: int, formato: str) -> str:

    """
    Suma una cantidad de días a una fecha dada y devuelve la nueva fecha en el mismo formato.

    Parámetros:
        fecha (str): Cadena de fecha original.
        dias (int): Número de días a sumar.
        formato (str): Formato de la fecha original y la fecha de salida.

    Salida:
        str: Cadena de la nueva fecha con los días sumados en el mismo formato.

    Lazza:
        ExcepcionFecha: Si ocurre un error al procesar la fecha.
    """

    try:
        fecha_dt = convertir_a_datetime(fecha, formato)
        nueva_fecha_dt = fecha_dt + timedelta(days=dias)

        return nueva_fecha_dt.strftime(formato)

    except Exception as e:
        raise ExcepcionFecha(f"Error al sumar días a la fecha {fecha}") from e


def completar_anyo(fecha: str, anyo: int = None) -> str:

        """
        Completa la fecha agregando el año actual si no se proporciona.

        Parámetros:
            fecha (str): Cadena de fecha que puede no incluir el año.
            anyo (int, opcional): Año a usar si la fecha no incluye uno. Si no se proporciona, se usa el año actual.

        Salida:
            str: Cadena de fecha con el año agregado si faltaba.

        Lanza:
            ExcepcionFecha: Si la fecha no es válida o no puede procesarse.
        """

        try:
            if anyo is None:
                anyo = datetime.now().year
            
            partes_fecha = fecha.split(" ")
            
            if len(partes_fecha) == 2:
                fecha = f"{fecha} {anyo}"

            return fecha

        except Exception as e:
            raise ExcepcionFecha(f"Error al completar el año en la fecha {fecha}") from e


def convertir_formato_fecha(fecha_str: str, formato_actual: str, formato_nuevo: str) -> str:

    """
    Convierte una fecha de un formato dado a otro.

    Ejemplo:
        14 August 2024 en formato "%d %B %Y"
        Se tranforma en:
            14-08-2024 00:00:00 en formato "%d-%m-%Y %H:%M:%S"

    Parámetros:
        fecha_str (str): Fecha en formato de cadena.
        formato_actual (str): Formato actual de la fecha en la cadena de entrada.
        formato_nuevo (str): Formato deseado para la salida.

    Salida:
        str: La fecha convertida al nuevo formato.
    """

    try:
        fecha_dt = datetime.strptime(fecha_str, formato_actual)

        return fecha_dt.strftime(formato_nuevo)

    except Exception as e:
        raise ExcepcionFecha(f"Error al convertir el formato de la fecha {fecha_str}") from e