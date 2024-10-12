# scripts/cron_actualizar_calendario.py

from utils.logging_utils import inicializar_logging
from utils.excepciones import ManejoExcepciones
from scripts.subprocesos import scrapping_obtener_grupos_competiciones
import os

# Constantes para la configuración
CTE_RUTA_CONFIG = "src/config/"
CTE_NOMBRE_CONFIG_PROPERTIES = "config.properties"

def main():

    """
    Función principal que se ejecuta al iniciar el script.
    
    Esta función configura el logging, obtiene los grupos de competiciones 
    mediante un proceso de scrapping, y maneja cualquier excepción que 
    pueda ocurrir durante la ejecución.

    Parámetros:
        None
    
    Salida:
        None
    """

    proceso = os.path.splitext(os.path.basename(__file__))[0]
    logger = inicializar_logging(CTE_RUTA_CONFIG, CTE_NOMBRE_CONFIG_PROPERTIES, proceso)
    logger.info("Iniciado proceso de actualización del calendario de competiciones")
    conexion = None

    try:
        objeto_competiciones = scrapping_obtener_grupos_competiciones.ObtenerGruposCompeticiones(CTE_RUTA_CONFIG, logger, proceso)
        grupo_competiciones = objeto_competiciones.ejecutar()
        
        # Aquí continuaría la lógica para actualizar el calendario.
        # ...

    except Exception as e:
        trazas_error = ManejoExcepciones.formatear_trazas_excepciones(e)
        logger.exception(e)
        #logger.error(trazas_error)

    finally:
        logger.info("Finalizado proceso de actualización del calendario de competiciones")


if __name__ == "__main__":
    main()
