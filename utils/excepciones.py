# utils/excepciones.py

import traceback

class ExcepcionBase(Exception):

    """
    Clase base para excepciones en el proyecto.
    
    Parámetros:
        mensaje (str): Mensaje de error descriptivo.
    
    Salida:
        None
    """

    def __init__(self, mensaje):
        super().__init__(mensaje)


class ExcepcionScrapping(ExcepcionBase):

    """
    Excepción lanzada cuando ocurre un error en el proceso de scrapping.
    
    Parámetros:
        url (str): URL de la página donde ocurrió el error.
        mensaje (str): Mensaje de error descriptivo. Por defecto es "Error durante el scraping de la página".

    Salida:
        None
    """

    def __init__(self, url, mensaje="Error durante el scraping de la página"):
        self.url = url
        self.mensaje = f"{mensaje}: {url}"
        super().__init__(self.mensaje)


class ExcepcionBaseDeDatos(ExcepcionBase):

    """
    Excepción lanzada cuando ocurre un error en las operaciones de base de datos.
    
    Parámetros:
        consulta_sql (str): Consulta SQL que causó el error.
        mensaje (str): Mensaje de error descriptivo. Por defecto es "Error durante la operación de base de datos".

    Salida:
        None
    """

    def __init__(self, consulta_sql, mensaje="Error durante la operación de base de datos"):
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

    def __init__(self, mensaje="Error de conexión o configuración de la base de datos"):
        super().__init__(mensaje)



class ExcepcionConfiguracion(ExcepcionBase):

    """
    Excepción lanzada cuando hay un problema con la configuración del proyecto.

    Parámetros:
        clave (str): Clave de configuración que causó el error.
        mensaje (str): Mensaje de error descriptivo. Por defecto es "Error en la configuración".
    
    Salida:
        None
    """
    
    def __init__(self, clave, mensaje="Error en la configuración"):
        self.clave = clave
        self.mensaje = f"{mensaje}: {clave}"
        super().__init__(self.mensaje)


class ExcepcionLogging(ExcepcionBase):
   
    """
    Excepción lanzada cuando ocurre un error en la configuración del logging.
    
    Parámetros:
        mensaje (str): Mensaje descriptivo del error.

    Salida:
        None
    """

    def __init__(self, mensaje="Error en la configuración de logging"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class ManejoExcepciones:
    
    @staticmethod
    def formatear_trazas_excepciones(e: Exception) -> str:

        """
        Formatea las trazas de una excepción encadenada, colocando primero el mensaje de la excepción más interna.
        
        Parámetros:
            e (Exception): La excepción principal.
            
        Salida:
            str: La cadena formateada con las trazas de la excepción.
        """

        trazas = []

        excepcion_actual = e
        ultima_excepcion = excepcion_actual

        while excepcion_actual:
            tb = traceback.extract_tb(excepcion_actual.__traceback__)

            if tb:
                traza = tb[0]
                trazas.append(f"File \"{traza.filename}\", line {traza.lineno}, in {traza.name}: {traza.line}")

            ultima_excepcion = f"{type(excepcion_actual).__name__}: {str(excepcion_actual)}"
            excepcion_actual = excepcion_actual.__cause__

        trazas.append(f"Excepción: {str(ultima_excepcion)}")
        trazas.reverse()

        return "\n".join(trazas)