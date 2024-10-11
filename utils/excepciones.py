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

        trazas = []
        excepcion_actual = excepcion
        trazas.append(f"Se produjo una excepción:\nExcepción: {str(excepcion_actual)}")
        
        causa_raiz = ManejoExcepciones._obtener_causa_mas_profunda(excepcion_actual)
        if causa_raiz:
            trazas.append("\nCausa raíz:")
            trazas.append(causa_raiz)

        trazas.append("\nTraceback (última llamada más reciente):")
        while excepcion_actual:
            tb = traceback.extract_tb(excepcion_actual.__traceback__)

            if tb:
                traza = tb[0]
                trazas.append(f'  File "{traza.filename}", line {traza.lineno}, in {traza.name}\n    {traza.line}')
                
            excepcion_actual = excepcion_actual.__cause__

        return "\n".join(trazas)


    @staticmethod
    def _obtener_causa_mas_profunda(excepcion: Exception) -> str:

        """
        Recorre la cadena de causas encadenadas para obtener la excepción más profunda.

        Parámetros:
            excepcion (Exception): La excepción inicial.

        Salida:
            str: El mensaje formateado de la excepción más profunda.
        """

        excepcion_causa = excepcion.__cause__
        causa_mas_profunda = None
        
        while excepcion_causa:
            causa_mas_profunda = excepcion_causa
            excepcion_causa = excepcion_causa.__cause__

        if causa_mas_profunda:
            return f"{type(causa_mas_profunda).__name__}: {str(causa_mas_profunda)}"
        
        return ""
