from telethon import TelegramClient, events
import logging
import sys

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Данные приложения (получите их на https://my.telegram.org)
api_id = 29845701           # замените на ваш api_id
api_hash = '599f6d661ec1537655deb02e1e301c4a'  # замените на ваш api_hash

# Используем userbot (авторизация обычного аккаунта)
client = TelegramClient('user_session', api_id, api_hash)

# ID групп (замените на актуальные)
source_group_id = -1002491838028  # Исходная группа
target_groups = [-1002251806398]   # Целевая группа

# Список ключевых слов для фильтрации сообщений
KEYWORDS = ['кран', 'аренда']

@client.on(events.NewMessage(chats=source_group_id))
async def message_handler(event):
    """Обрабатывает сообщения из исходной группы:
       - Если сообщение содержит одно из ключевых слов, пересылает его без служебного заголовка.
       - Поддерживает текстовые сообщения и сообщения с медиа (фото, документы и т.п.)."""
    try:
        msg_text = event.message.message or ''
        # Проверяем наличие хотя бы одного ключевого слова (без учёта регистра)
        if any(key.lower() in msg_text.lower() for key in KEYWORDS):
            logger.info(f"Сообщение с ключевым словом обнаружено от {event.sender_id}: {msg_text}")

            # Если сообщение содержит медиа, отправляем его как файл с подписью
            if event.message.media:
                for target in target_groups:
                    try:
                        # Отправляем файл с оригинальным текстом в качестве подписи (caption)
                        await client.send_file(target, event.message.media, caption=msg_text)
                        logger.info(f"Медиа сообщение отправлено в группу {target} без пересылки.")
                    except Exception as err:
                        logger.error(f"Ошибка при отправке медиа в группу {target}: {err}")
            else:
                # Если просто текстовое сообщение – отправляем новый текст
                for target in target_groups:
                    try:
                        await client.send_message(target, msg_text)
                        logger.info(f"Текстовое сообщение отправлено в группу {target} без пересылки.")
                    except Exception as err:
                        logger.error(f"Ошибка при отправке текста в группу {target}: {err}")
        else:
            logger.info("Сообщение не содержит ключевых слов – пересылка не производится.")
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")

async def main():
    await client.start()
    logger.info("Userbot запущен и ожидает сообщений...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Userbot остановлен")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
    finally:
        sys.exit(0)
