import traceback

class ExcepcionBase(Exception):

    """
    Clase base para excepciones en el proyecto.
    
    Parámetros:
        mensaje (str): Mensaje de error descriptivo.
    
    Salida:
        None
    """

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)


class ExcepcionScrapping(ExcepcionBase):

    """
    Excepción lanzada cuando ocurre un error en el proceso de scrapping.
    
    Parámetros:
        mensaje (str): Mensaje de error descriptivo. Por defecto es "Error durante el scraping de la página".

    Salida:
        None
    """

    def __init__(self, mensaje: str = "Error durante el scraping de la página") -> None:
        super().__init__(mensaje)


class ExcepcionBaseDeDatos(ExcepcionBase):

    """
    Excepción lanzada cuando ocurre un error en las operaciones de base de datos.
    
    Parámetros:
        consulta_sql (str): Consulta SQL que causó el error.
        mensaje (str): Mensaje de error descriptivo. Por defecto es "Error durante la operación de base de datos".

    Salida:
        None
    """

    def __init__(self, consulta_sql: str, mensaje: str = "Error durante la operación de base de datos") -> None:
        self.consulta_sql = consulta_sql
        self.mensaje = f"{mensaje}: {consulta_sql}"
        super().__init__(self.mensaje)


class ExcepcionConexionBaseDeDatos(ExcepcionBase):

    """
    Excepción lanzada cuando ocurre un error al establecer la conexión o cargar la configuración de la base de datos.
    
    Parámetros:
        mensaje (str): Mensaje de error descriptivo.
    
    Salida:
        None
    """

    def __init__(self, mensaje: str = "Error de conexión o configuración de la base de datos") -> None:
        super().__init__(mensaje)


class ExcepcionProperties(ExcepcionBase):

    """
    Excepción lanzada cuando hay un problema al leer archivos de properties.

    Parámetros:
        mensaje (str): Mensaje de error descriptivo. Por defecto es "Error en tratamiento de archivo de propiedades".
    
    Salida:
        None
    """
    
    def __init__(self, mensaje: str = "Error en la tratemiento de archivo de propiedades") -> None:
        super().__init__(mensaje)


class ExcepcionLogging(ExcepcionBase):
   
    """
    Excepción lanzada cuando ocurre un error en la configuración del logging.
    
    Parámetros:
        mensaje (str): Mensaje descriptivo del error.

    Salida:
        None
    """

    def __init__(self, mensaje: str = "Error en la configuración de logging") -> None:
        self.mensaje = mensaje
        super().__init__(self.mensaje)


import traceback

import traceback

class ManejoExcepciones:

    @staticmethod
    def formatear_trazas_excepciones(excepcion: Exception) -> str:

        """
        Formatea la traza de una excepción mostrando la causa raíz y las trazas de la excepción encadenada.

        Parámetros:
            excepcion (Exception): La excepción principal.

        Salida:
            str: La cadena formateada con el mensaje detallado de la excepción.
        """

        mensajes_excepciones, trazas_traceback, causa_mas_profunda_tipo, causa_mas_profunda_mensaje = ManejoExcepciones._recopilar_excepciones_y_trazas(excepcion)
        
        trazas = ["\nSe produjo una excepción:"]
    
        for mensaje in mensajes_excepciones[:-1]:
            trazas.append(f"  >> {mensaje}")

        if causa_mas_profunda_tipo and causa_mas_profunda_mensaje:
            trazas.append("\nCausa raíz:")
            trazas.append(f"{causa_mas_profunda_tipo}: {causa_mas_profunda_mensaje}")

        trazas.append("\nTraceback (última llamada más reciente):")
        trazas.extend(trazas_traceback)

        return "\n".join(trazas)

    @staticmethod
    def _recopilar_excepciones_y_trazas(excepcion: Exception) -> tuple:

        """
        Recorre la cadena de excepciones y almacena los mensajes de error, las trazas del traceback,
        y obtiene la causa más profunda.

        Parámetros:
            excepcion (Exception): La excepción principal.

        Salida:
            tuple: Cuatro elementos:
                - Lista con los mensajes de las excepciones
                - Lista con las trazas del traceback
                - Tipo de la causa más profunda
                - Mensaje de la causa más profunda
        """

        mensajes_excepciones = []
        trazas_traceback = []
        causa_mas_profunda_tipo = None
        causa_mas_profunda_mensaje = None
        excepcion_actual = excepcion

        while excepcion_actual:
            tipo_excepcion = type(excepcion_actual).__name__
            mensaje_excepcion = str(excepcion_actual)
            mensajes_excepciones.append(mensaje_excepcion)
            tb = traceback.extract_tb(excepcion_actual.__traceback__)

            if tb:
                traza = tb[0]
                trazas_traceback.append(f'  File "{traza.filename}", line {traza.lineno}, in {traza.name}\n    {traza.line}')

            causa_mas_profunda_tipo = tipo_excepcion
            causa_mas_profunda_mensaje = mensaje_excepcion
            excepcion_actual = excepcion_actual.__cause__

        return mensajes_excepciones, trazas_traceback, causa_mas_profunda_tipo, causa_mas_profunda_mensaje