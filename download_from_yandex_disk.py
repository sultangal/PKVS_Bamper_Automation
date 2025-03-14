import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from term_colors import TClr


def download_from_yandex_disk(public_url, chrome_driver_path):

    download_folder = os.path.join(os.getcwd(), "downloads")
    # Создаем папку для скачивания, если она не существует
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Очищаем папку скачивания перед началом скачивания
    for file_name in os.listdir(download_folder):
        file_path = os.path.join(download_folder, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Удаляем файл или символическую ссылку
            elif os.path.isdir(file_path):
                os.rmdir(file_path)  # Удаляем пустую папку
        except Exception as e:
            print(f"Ошибка при удалении {file_path}: {e}")

    # Настройки для Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Открыть браузер в полном окне
    options.add_argument("--headless=new")  # Попробуйте этот режим, если используете Chrome 109+
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("prefs", {
        "download.default_directory": download_folder,  # Указываем папку для скачивания
        "download.prompt_for_download": False,  # Отключаем запрос на подтверждение скачивания
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # Инициализация драйвера
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Открываем страницу Яндекс.Диска
        driver.get(public_url)

        # Ждем, пока страница загрузится и появится кнопка "Скачать всё"
        wait = WebDriverWait(driver, 20)

        # Извлекаем название папки из элемента на странице
        folder_name_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//h1[@class='js-prevent-mouse-selection']"))
        )
        folder_name = folder_name_element.text.strip()

        # Формируем ожидаемое имя файла
        expected_zip_name = f"{folder_name}.zip"
        expected_zip_path = os.path.join(download_folder, expected_zip_name)

        # Ищем кнопку "Скачать всё" по классам и тексту
        try:
            download_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'download-button') and .//span[contains(text(), 'Скачать всё')]]"))
            )
        except:
            print(f"{TClr.CRED}Кнопка 'Скачать всё' не найдена. Возможно ссылка не корректна или файл удален с Яндекс Диска или по ссылке находится не папка а отдельный файл.{TClr.CEND}")
            return None  # Завершаем выполнение функции

        # Нажимаем кнопку "Скачать всё"
        download_button.click()

        # Ждем, пока файл скачается
        print(f"Ожидание завершения скачивания файла {expected_zip_name}...")

        # Проверяем, завершилось ли скачивание
        start_time = time.time()
        timeout = 600  # Максимальное время ожидания скачивания (10 минут)
        while True:
            # Проверяем, появился ли файл с ожидаемым именем
            if os.path.exists(expected_zip_path):
                print(f"Скачивание завершено! Найден файл: {expected_zip_name}")
                return expected_zip_path  # Возвращаем полный путь к файлу

            # Проверяем, не превышено ли время ожидания
            if time.time() - start_time > timeout:
                print("Время ожидания скачивания истекло.")
                return None

            time.sleep(2)  # Проверяем каждые 2 секунды

    except:
        print(f"{TClr.CRED}Ошибка при скачивании.{TClr.CEND}")
        return None

    finally:
        # Закрываем браузер
        driver.quit()