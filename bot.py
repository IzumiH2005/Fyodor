import asyncio
import traceback
from typing import NoReturn, Optional

from telegram import Update, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)
from telegram.error import TelegramError
from config import TELEGRAM_TOKEN
from gemini_handler import GeminiHandler
from image_handler import ImageHandler
from logger_config import logger

class FyodorBot:
    """Bot Telegram imitant Fyodor Dostoevsky"""

    def __init__(self) -> None:
        """Initialise le bot avec ses handlers"""
        self.gemini = GeminiHandler()
        self.image_handler = ImageHandler()

    def _send_message_with_retry(
        self, 
        update: Update, 
        text: str, 
        max_retries: int = 3,
        retry_delay: float = 1.0
    ) -> bool:
        """
        Envoie un message avec système de retry

        Args:
            update: L'update Telegram
            text: Le texte à envoyer
            max_retries: Nombre maximum de tentatives
            retry_delay: Délai entre les tentatives en secondes

        Returns:
            bool: True si envoi réussi, False sinon
        """
        for attempt in range(max_retries):
            try:
                update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
                return True
            except TelegramError as e:
                logger.warning(f"Tentative {attempt + 1}/{max_retries} échouée: {e}")
                if attempt < max_retries - 1:
                    asyncio.sleep(retry_delay)
                continue
        return False

    def start_command(
        self, 
        update: Update, 
        context: CallbackContext
    ) -> None:
        """Gère la commande /start"""
        welcome_message = "*ajuste son ushanka* Que souhaitez-vous ?"
        try:
            self._send_message_with_retry(update, welcome_message)
            logger.info(f"Nouvelle conversation démarrée avec {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Erreur lors de la commande start: {e}")
            self._send_message_with_retry(update, "*silence calculateur*")

    def handle_message(
        self, 
        update: Update, 
        context: CallbackContext
    ) -> None:
        """Gère les messages reçus"""
        if not update.message or not update.message.text:
            return

        try:
            # Obtention de la réponse de Gemini
            response = self.gemini.get_response(update.message.text)

            # Envoi de la réponse
            message_sent = self._send_message_with_retry(update, response)
            if not message_sent:
                logger.error("Impossible d'envoyer la réponse après plusieurs tentatives")
                return

            # Gestion des images
            if self.image_handler.should_send_image():
                try:
                    image_url = self.image_handler.get_random_image()
                    update.message.reply_photo(photo=image_url)
                except TelegramError as e:
                    logger.error(f"Erreur lors de l'envoi de l'image: {e}")

            logger.info(f"Réponse envoyée à {update.effective_user.id}")

        except Exception as e:
            logger.error(f"Erreur lors du traitement du message: {e}")
            self._send_message_with_retry(
                update,
                "*silence calculateur*"
            )

    def error_handler(
        self, 
        update: Optional[object], 
        context: CallbackContext
    ) -> None:
        """Gère les erreurs de manière plus détaillée"""
        logger.error(f"Exception lors du traitement d'une update: {context.error}")

        try:
            # Récupération des détails de l'erreur
            if context.error:
                tb_list = traceback.format_exception(
                    None, 
                    context.error, 
                    context.error.__traceback__
                )
                tb_string = "".join(tb_list)
                logger.error(f"Traceback complet:\n{tb_string}")

            # Notification à l'utilisateur si possible
            if update and isinstance(update, Update) and update.effective_message:
                update.effective_message.reply_text(
                    "Une erreur est survenue... *regarde au loin avec dédain*",
                    parse_mode=ParseMode.MARKDOWN
                )
        except Exception as e:
            logger.error(f"Erreur dans le gestionnaire d'erreurs: {e}")

def main():
    """Point d'entrée principal du bot"""
    try:
        # Initialisation du bot
        bot = FyodorBot()

        # Configuration de l'updater
        updater = Updater(TELEGRAM_TOKEN)
        dispatcher = updater.dispatcher

        # Ajout des handlers
        dispatcher.add_handler(CommandHandler("start", bot.start_command))
        dispatcher.add_handler(
            MessageHandler(
                Filters.text & ~Filters.command,
                bot.handle_message
            )
        )
        dispatcher.add_error_handler(bot.error_handler)

        # Démarrage du bot
        logger.info("Démarrage du bot Fyodor...")
        updater.start_polling()
        updater.idle()

    except Exception as e:
        logger.critical(f"Erreur fatale lors du démarrage du bot: {e}")
        raise

if __name__ == "__main__":
    main()