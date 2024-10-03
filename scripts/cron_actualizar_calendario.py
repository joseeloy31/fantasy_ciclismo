from utils import db_utils, logging_utils
import os
import logging

def main():

    ruta_properties = os.path.join(os.path.dirname(__file__), '../config/config.properties')
    proceso = os.path.splitext(os.path.basename(__file__))[0]

    logger = logging_utils.inicializar_logging(ruta_properties, proceso)
    logger.info("Sistema de logging inicializado correctamente.")
    
    conexion = None
    try:
        conexion = db_utils.obtener_conexion(ruta_properties)
        logger.info("Conexión a la base de datos exitosa.")
        
        # Aquí iría la lógica para actualizar el calendario.
        # ...
        
    except Exception as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
    
    finally:
        if conexion:
            conexion.close()
            logger.info("Conexión a la base de datos cerrada.")

if __name__ == "__main__":
    main()