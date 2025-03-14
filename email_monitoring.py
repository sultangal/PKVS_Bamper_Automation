import imaplib
import email
import re
from email.header import decode_header

# Настройки почтового ящика
EMAIL = ''
PASSWORD = ''  # Замените на пароль приложения, если используется 2FA
IMAP_SERVER = 'outlook.office365.com'

# Тема письма, которую мы ищем
TARGET_SUBJECT = 'Важная тема'

# Регулярное выражение для поиска ссылки на Яндекс.Диск
YANDEX_DISK_URL_PATTERN = r'https://disk\.yandex\.ru/d/[a-zA-Z0-9_-]+'

def decode_mime_header(header):
    """Декодирует заголовок письма."""
    decoded = decode_header(header)
    return ''.join([text.decode(encoding or 'utf-8') if isinstance(text, bytes) else text for text, encoding in decoded])

def fetch_emails():
    """Получает письма с почтового ящика и ищет ссылку на Яндекс.Диск."""
    try:
        # Подключаемся к серверу
        print(f"Подключение к серверу {IMAP_SERVER}...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        print("Подключение успешно.")

        # Логинимся
        print(f"Авторизация пользователя {EMAIL}...")
        mail.login(EMAIL, PASSWORD)
        print("Авторизация успешна.")

        # Выбираем папку "входящие"
        mail.select('inbox')
        print("Папка 'inbox' выбрана.")

        # Ищем все непрочитанные письма
        status, messages = mail.search(None, 'UNSEEN')
        if status != 'OK':
            print("Ошибка при поиске писем.")
            return

        for mail_id in messages[0].split():
            # Получаем письмо
            status, msg_data = mail.fetch(mail_id, '(RFC822)')
            if status != 'OK':
                print(f"Ошибка при получении письма {mail_id}.")
                continue

            # Парсим письмо
            msg = email.message_from_bytes(msg_data[0][1])
            subject = decode_mime_header(msg['Subject'])

            # Проверяем тему письма
            if subject == TARGET_SUBJECT:
                # Ищем ссылку на Яндекс.Диск в теле письма
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True).decode()
                        match = re.search(YANDEX_DISK_URL_PATTERN, body)
                        if match:
                            print(f"Найдена ссылка на Яндекс.Диск: {match.group(0)}")
                        else:
                            print("Ссылка на Яндекс.Диск не найдена.")

    except imaplib.IMAP4.error as e:
        print(f"Ошибка IMAP: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Закрываем соединение
        if 'mail' in locals():
            mail.logout()
            print("Соединение закрыто.")

if __name__ == '__main__':
    fetch_emails()