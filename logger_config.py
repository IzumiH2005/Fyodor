import logging
import sys

def setup_logger():
    # Configuration du logger
    logger = logging.getLogger('fyodor_bot')
    logger.setLevel(logging.INFO)
    
    # Handler pour la console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Format du log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Ajout du handler au logger
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()
