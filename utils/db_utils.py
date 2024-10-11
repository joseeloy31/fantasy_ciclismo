# utils/db_utils.py

import mysql.connector
from mysql.connector import connection
from utils.properties_utils import leer_properties, obtener_property
from utils.excepciones import ExcepcionConexionBaseDeDatos

def obtener_conexion(ruta_properties: str) -> connection:

    """
    Obtiene una conexión a la base de datos usando los valores de un archivo de configuración .properties.

    Parámetros:
        ruta_properties (str): Ruta al archivo de configuración .properties
                               que contiene las credenciales
                               y parámetros de la base de datos.

    Salida:
        mysql.connector.connection: Objeto de conexión a la base de datos.

    Lanza:
        ExcepcionConexionBaseDeDatos: Si ocurre algún error al intentar conectarse a la base de datos,
                                      como problemas con el archivo de configuración o MySQL.
    """

    try:
        propiedades = leer_properties(ruta_properties)

        conexion = mysql.connector.connect(
            host=obtener_property(propiedades, 'database', 'host'),
            database=obtener_property(propiedades, 'database', 'name'),
            user=obtener_property(propiedades, 'database', 'user'),
            password=obtener_property(propiedades, 'database', 'password'),
            port=obtener_property(propiedades, 'database', 'port')
        )
        
        return conexion

    except FileNotFoundError as fnfe:
        raise ExcepcionConexionBaseDeDatos(f"El archivo de configuración '{ruta_properties}' no fue encontrado") from fnfe

    except KeyError as ke:
        raise ExcepcionConexionBaseDeDatos(f"Falta una clave requerida en el archivo de configuración: {ke.args[0]}") from ke

    except mysql.connector.Error as mce:
        raise ExcepcionConexionBaseDeDatos(f"Error de conexión a MySQL") from mce

    except Exception as e:
        raise ExcepcionConexionBaseDeDatos(f"Error inesperado al intentar conectarse a la base de datos") from e
