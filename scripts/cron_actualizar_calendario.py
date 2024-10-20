# scripts/cron_actualizar_calendario.py

from scripts.subprocesos.scrapping_desglosar_grupos_competiciones import DesglosarGruposCompeticiones
from scripts.subprocesos.scrapping_obtener_grupos_competiciones import ObtenerGruposCompeticiones
from utils.config import Config
from utils.excepciones import ManejoExcepciones
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
    config = Config(ruta_config=CTE_RUTA_CONFIG, nombre_config=CTE_NOMBRE_CONFIG_PROPERTIES, proceso=proceso)

    logger = config.obtener_logger()
    logger.info("Iniciado proceso de actualización del calendario de competiciones")
    conexion = None

    try:
        objeto_competiciones = ObtenerGruposCompeticiones()
        grupos_competiciones = objeto_competiciones.ejecutar()

        objeto_desglose_competiciones = DesglosarGruposCompeticiones(grupos_competiciones)
        grupos_competiciones_desglosados = objeto_desglose_competiciones.ejecutar()

        # Al final del proceso, luego de haber llenado self.resultados
        log_mensaje = "\n"

        for grupos_competiciones in grupos_competiciones_desglosados:
            log_mensaje += f"Nombre: {grupos_competiciones['nombre']}\n"
            log_mensaje += f"Género: {grupos_competiciones['genero']}\n"
            log_mensaje += f"URL: {grupos_competiciones['url']}\n"
            log_mensaje += f"Tipo de Grupo: {grupos_competiciones['tipo_grupo']}\n"

            desglose = grupos_competiciones.get('desglose_grupo_competiciones')
            if desglose:
                log_mensaje += "Desglose de Competiciones:\n"
                if grupos_competiciones['tipo_grupo'] == 'grupo_vueltas':  # Para vueltas por etapas
                    for competicion in desglose:
                        log_mensaje += f"  - Competición: {competicion['descripcion']}\n"
                        log_mensaje += f"    - URL: {competicion['url']}\n"
                        log_mensaje += f"    - Número de Etapas: {competicion['numero_etapas']}\n"
                        log_mensaje += f"    - Tipo de Vuelta: {competicion['tipo_vuelta']}\n"
                        log_mensaje += f"    - Fecha de Inicio: {competicion['fecha_inicio']}\n"
                        log_mensaje += f"    - Fecha de Fin: {competicion['fecha_fin']}\n"
                else:  # Para grupos de clásicas
                    for competicion in desglose:
                        log_mensaje += f"  - Clásica: {competicion['numero_clasica']}\n"
                        log_mensaje += f"    - Fecha: {competicion['fecha_clasica']}\n"
                        log_mensaje += f"    - Nombre: {competicion['nombre_clasica']}\n"
                        log_mensaje += f"    - Categoría: {competicion['categoria']}\n"
            
            log_mensaje += "\n"  # Línea en blanco para separar cada resultado

        # Imprime el mensaje completo con logger.debug
        logger.info(log_mensaje)

        # Aquí continuaría la lógica para actualizar el calendario.
        # ...

    except Exception as e:
        trazas_error = ManejoExcepciones.formatear_trazas_excepciones(e)
        logger.error(trazas_error)

    finally:
        logger.info("Finalizado proceso de actualización del calendario de competiciones")


if __name__ == "__main__":
    main()