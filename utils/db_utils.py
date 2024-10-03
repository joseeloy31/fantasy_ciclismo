import mysql.connector
from utils.properties_utils import leer_properties, obtener_property

def obtener_conexion(ruta_properties):

    # Obtiene una conexión a la base de datos usando los valores de config.properties.
    #
    # Parámetros:
    # ruta_properties (str): Ruta al archivo de configuración .properties.
    #
    # Retorno:
    # mysql.connector.connection: Conexión a la base de datos.

    propiedades = leer_properties(ruta_properties)
    
    conexion = mysql.connector.connect(
        host=obtener_property(propiedades, 'database', 'host'),
        database=obtener_property(propiedades, 'database', 'name'),
        user=obtener_property(propiedades, 'database', 'user'),
        password=obtener_property(propiedades, 'database', 'password'),
        port=obtener_property(propiedades, 'database', 'port')
    )
    
    return conexion