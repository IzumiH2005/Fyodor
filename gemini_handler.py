import google.generativeai as genai
from typing import Optional
from config import GEMINI_API_KEY, FYODOR_PERSONA
from logger_config import logger

class GeminiHandler:
    """Gestionnaire des interactions avec l'API Gemini"""

    def __init__(self) -> None:
        """Initialise la connexion avec Gemini et configure le persona"""
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
            self.chat = self.model.start_chat(history=[])
            self._initialize_persona()
            logger.info("GeminiHandler initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de GeminiHandler: {e}")
            raise

    def _initialize_persona(self) -> None:
        """Initialise le persona de Fyodor"""
        try:
            init_prompt = f"{FYODOR_PERSONA}\nRéponds comme ce personnage à partir de maintenant."
            self.chat.send_message(init_prompt)
            logger.info("Persona Fyodor initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du persona: {e}")
            raise

    def get_response(self, user_message: str) -> str:
        """
        Génère une réponse à partir du message de l'utilisateur

        Args:
            user_message: Le message de l'utilisateur

        Returns:
            str: La réponse générée

        Raises:
            Exception: Si une erreur survient lors de la génération
        """
        try:
            # Construction du prompt pour les conversations ordinaires
            prompt = f"""En tant que Fyodor Dostoevsky, réponds à ce message: "{user_message}"
            Rappel pour les conversations ordinaires:
            - Reste bref et direct (1-2 phrases)
            - Garde un ton froid et distant
            - Sois poli mais légèrement condescendant
            - Évite les longues répliques ou les références au manga
            - Tu peux utiliser des petites actions entre *asterisques* si pertinent"""

            # Génération de la réponse
            response = self.chat.send_message(prompt).text
            logger.info(f"Réponse générée avec succès: {response[:50]}...")
            return response

        except Exception as e:
            logger.error(f"Erreur lors de la génération de réponse: {e}")
            return "*observe silencieusement*"

    def reset_chat(self) -> None:
        """Réinitialise la conversation"""
        try:
            self.chat = self.model.start_chat(history=[])
            self._initialize_persona()
            logger.info("Conversation réinitialisée avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la réinitialisation de la conversation: {e}")
            raise