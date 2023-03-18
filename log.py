from loguru import logger


logger.add(
    "./logfiles/file.log",
    level="INFO",
    format="{time} {level} {message}",
    rotation="16 MB",
    compression="zip"
)
