# scripts/cron_actualizar_calendario.py

from utils.logging_utils import inicializar_logging
from scripts.subprocesos import scrapping_obtener_grupos_competiciones
import os

# Constantes
CTE_RUTA_CONFIG = "src/config/"
CTE_NOMBRE_CONFIG_PROPERTIES = "config.properties"

def main():

    proceso = os.path.splitext(os.path.basename(__file__))[0]
    logger = inicializar_logging(CTE_RUTA_CONFIG, CTE_NOMBRE_CONFIG_PROPERTIES, proceso)
    conexion = None

    try:
        objeto_competiciones = scrapping_obtener_grupos_competiciones.ObtenerGruposCompeticiones(CTE_RUTA_CONFIG, logger, proceso)
        grupo_competiciones = objeto_competiciones.ejecutar()
        
        # Aquí continuaría la lógica para actualizar el calendario.
        # ...
        
    except Exception as e:
        logger.exception(e)
    
    finally:
        if conexion:
            #conexion.close()
            logger.info("Conexión a la base de datos cerrada.")


if __name__ == "__main__":
    main()