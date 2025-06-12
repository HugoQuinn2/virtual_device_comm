import logging
import colorlog

# Crear logger
logger = logging.getLogger("SerialDeviceSimulator")
logger.setLevel(logging.DEBUG)

# Crear handler para consola con color
console_handler = logging.StreamHandler()
formatter = colorlog.ColoredFormatter(
    fmt="%(log_color)s[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    log_colors={
        'DEBUG':    'purple',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }
)
console_handler.setFormatter(formatter)

# Agregar handler si aún no está
if not logger.handlers:
    logger.addHandler(console_handler)
