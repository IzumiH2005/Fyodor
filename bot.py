import asyncio
import traceback
import os
from typing import Optional, Union

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from telegram.constants import ParseMode
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

    async def _send_message_with_retry(
        self, 
        update: Update, 
        text: str, 
        max_retries: int = 3,
        retry_delay: float = 1.0
    ) -> bool:
        """Envoie un message avec système de retry"""
        for attempt in range(max_retries):
            try:
                await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN_V2)
                return True
            except TelegramError as e:
                logger.warning(f"Tentative {attempt + 1}/{max_retries} échouée: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                continue
        return False

    async def start_command(
        self, 
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Gère la commande /start"""
        welcome_message = "*observe silencieusement* Que souhaitez\-vous ?"
        try:
            await self._send_message_with_retry(update, welcome_message)
            logger.info(f"Nouvelle conversation démarrée avec {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Erreur lors de la commande start: {e}")
            await self._send_message_with_retry(update, "*observe silencieusement*")

    async def handle_message(
        self, 
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Gère les messages reçus"""
        if not update.message or not update.message.text:
            return

        try:
            # Afficher l'action de frappe
            await update.message.chat.send_action('typing')

            # Obtention de la réponse de Gemini
            response = self.gemini.get_response(update.message.text)

            # Échapper les caractères spéciaux pour Markdown V2
            response = response.replace('-', '\-').replace('.', '\.').replace('!', '\!')

            # Envoi de la réponse
            message_sent = await self._send_message_with_retry(update, response)
            if not message_sent:
                logger.error("Impossible d'envoyer la réponse après plusieurs tentatives")
                return

            # Gestion des images
            if self.image_handler.should_send_image():
                try:
                    image_path = self.image_handler.get_random_image()
                    if image_path and os.path.exists(image_path):
                        with open(image_path, 'rb') as photo:
                            await update.message.reply_photo(photo=photo)
                    else:
                        logger.warning(f"Image non trouvée ou invalide: {image_path}")
                except TelegramError as e:
                    logger.error(f"Erreur lors de l'envoi de l'image: {e}")
                except Exception as e:
                    logger.error(f"Erreur inattendue lors de l'envoi de l'image: {e}")

            logger.info(f"Réponse envoyée à {update.effective_user.id}")

        except Exception as e:
            logger.error(f"Erreur lors du traitement du message: {e}")
            await self._send_message_with_retry(
                update,
                "*observe silencieusement*"
            )

    async def error_handler(
        self, 
        update: Optional[Update], 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Gère les erreurs de manière plus détaillée"""
        logger.error(f"Exception lors du traitement d'une update: {context.error}")

        try:
            if context.error:
                tb_list = traceback.format_exception(
                    None, 
                    context.error, 
                    context.error.__traceback__
                )
                tb_string = "".join(tb_list)
                logger.error(f"Traceback complet:\n{tb_string}")

            if update and update.effective_message:
                await update.effective_message.reply_text(
                    "Une erreur est survenue\.\.\. *regarde au loin avec dédain*",
                    parse_mode=ParseMode.MARKDOWN_V2
                )
        except Exception as e:
            logger.error(f"Erreur dans le gestionnaire d'erreurs: {e}")

def main() -> None:
    """Point d'entrée principal du bot"""
    try:
        # Initialisation du bot
        bot = FyodorBot()

        # Création de l'application
        application = Application.builder().token(TELEGRAM_TOKEN).build()

        # Ajout des handlers
        application.add_handler(CommandHandler("start", bot.start_command))
        application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                bot.handle_message
            )
        )
        application.add_error_handler(bot.error_handler)

        # Démarrage du bot
        logger.info("Démarrage du bot Fyodor...")
        application.run_polling()

    except Exception as e:
        logger.critical(f"Erreur fatale lors du démarrage du bot: {e}")
        raise

if __name__ == "__main__":
    main()