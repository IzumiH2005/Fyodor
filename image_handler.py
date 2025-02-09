import random
import os
from config import FYODOR_IMAGES
from logger_config import logger

class ImageHandler:
    def __init__(self):
        self.message_counter = 0
        self.next_image_interval = self._generate_new_interval()

    def _generate_new_interval(self) -> int:
        """Génère un nouvel intervalle aléatoire entre 5 et 10"""
        return random.randint(5, 10)

    def should_send_image(self) -> bool:
        """Détermine si une image doit être envoyée"""
        self.message_counter += 1

        if self.message_counter >= self.next_image_interval:
            self.message_counter = 0
            self.next_image_interval = self._generate_new_interval()
            return True
        return False

    def get_random_image(self) -> str:
        """Retourne un chemin d'image aléatoire"""
        try:
            image_path = random.choice(FYODOR_IMAGES)
            # Vérifier que le fichier existe
            if not os.path.exists(image_path):
                logger.error(f"Image non trouvée: {image_path}")
                return None

            logger.info(f"Image sélectionnée: {image_path}")
            return image_path

        except Exception as e:
            logger.error(f"Erreur lors de la sélection d'image: {e}")
            return None