import logging
import colorlog
import os
from dotenv import load_dotenv

# Configurar el logger
class Logger:
    logger = None
    def setup_logger(cls):
        if cls.logger is None:
            cls.logger = logging.getLogger() # Se crea un objeto de la clase Logging de la biblioteca logging
            # Para crearlo es necesario hacerlo a través del método getLogger().
            cls.logger.setLevel(10) # Se establece el nivel más bajo de los logs en DEBUG.
            # Por defecto, el nivel más bajo es INFO. Si no se especifica esta línea, 
            # Los niveles más bajos que INFO no se mostrarán. 
            # Los valores de los niveles son:
            #    CRITICAL: 50
            #    ERROR: 40
            #    WARNING: 30
            #    INFO: 20
            #    DEBUG: 10

            # Creamos un formateador de color y fecha a partir de la clase ColoredFormatter de la librería colorlog
            formatter = colorlog.ColoredFormatter(
                "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
                datefmt = "%d-%m-%Y %H:%M:%S", # Formato de fecha español
                log_colors = {
                    'DEBUG': 'blue',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red,bg_yellow',
                },
                reset = True,
                style = '%'
            )
            # Los colores de la librería colorlog son:
            #   black
            #   red
            #   green
            #   yellow
            #   blue
            #   purple
            #   cyan
            #   white
            # Además se permite el modificador bold_ para obtener letra negrita.
            # Para los colores de fondo se puede usar la terminación ,bg_ segida del color, 
            # como en el ejemplo de CRITICAL.
            # Para más combinaciones de colores se tendría que usar una librería más especializada, 
            # como termcolor, o colorama.
            
            # Para la salida en fichero las combinaciones de colores son más límitadas, 
            # y sólo quedan bien si se aplican al nivel de log.
            
            load_dotenv() # Cargamos las variables de entorno
            log_file_path = os.getenv('LOG_FILE_PATH', 'loggin.log') # La ruta del archivo de logs
            output = int(os.getenv('OUTPUT', 0)) # La dirección de salida de los logs
            # 0 = archivo
            # 1 = terminal
            # 2 = archivo y terminal
            if output == 0 or output == 2:
                # Crear un controlador de archivo para el registro
                file_handler = logging.FileHandler(log_file_path)
                file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
                # Agregar el controlador de archivo al logger
                cls.logger.addHandler(file_handler)
            if output == 1 or output == 2:
                # Crear un controlador de consola para el registro en color.
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                # Agregar el controlador de consola al logger
                cls.logger.addHandler(console_handler)

    @classmethod
    def debug(cls, msg):
        cls.setup_logger(cls)
        cls.logger.debug(msg)

    @classmethod
    def info(cls, msg):
        cls.setup_logger(cls)
        cls.logger.info(msg)

    @classmethod
    def warning(cls, msg):
        cls.setup_logger(cls)
        cls.logger.warning(msg)

    @classmethod
    def error(cls, msg):
        cls.setup_logger(cls)
        cls.logger.error(msg)

    @classmethod
    def critical(cls, msg):
        cls.setup_logger(cls)
        cls.logger.critical(msg)


# Ejemplos de registros
# Logger.debug("Esto es un mensaje de depuración")
# Logger.info("Esto es un mensaje de información")
# Logger.warning("Esto es un mensaje de advertencia")
# Logger.error("Esto es un mensaje de error")
# Logger.critical("Esto es un mensaje crítico")
