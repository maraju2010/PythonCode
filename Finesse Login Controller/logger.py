

fileConfig('ConfigProperty.ini')
logger = logging.getLogger(__name__)

def get_logger():
    print(logger)
    return logger
