import random
from config import FYODOR_IMAGES
from logger_config import logger

class ImageHandler:
    def __init__(self):
        self.message_counter = 0
        self.next_image_interval = self._generate_new_interval()
    
    def _generate_new_interval(self) -> int:
        """Génère un nouvel intervalle aléatoire entre 3 et 8"""
        return random.randint(3, 8)
    
    def should_send_image(self) -> bool:
        """Détermine si une image doit être envoyée"""
        self.message_counter += 1
        
        if self.message_counter >= self.next_image_interval:
            self.message_counter = 0
            self.next_image_interval = self._generate_new_interval()
            return True
        return False
    
    def get_random_image(self) -> str:
        """Retourne une URL d'image aléatoire"""
        try:
            image_url = random.choice(FYODOR_IMAGES)
            logger.info(f"Image sélectionnée: {image_url}")
            return image_url
        except Exception as e:
            logger.error(f"Erreur lors de la sélection d'image: {e}")
            return FYODOR_IMAGES[0]  # Image par défaut en cas d'erreur
