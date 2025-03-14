import argparse

from term_colors import TClr
from open_aep_file import open_aep_file
from download_from_yandex_disk import download_from_yandex_disk
from unpack_archive import unzip_to_destination, find_and_move_all_files

if __name__ == "__main__":

    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument('unpack_path', type=str, help='Путь распаковки архива')
    args = parser.parse_args()

    # Укажите путь к вашему ChromeDriver
    chrome_driver_path = "chromedriver.exe"  # Убедитесь, что chromedriver.exe находится в той же папке, что и скрипт

    # Запрашиваем у пользователя публичную ссылку на Яндекс.Диск
    public_url = input("Введите публичную ссылку на Яндекс.Диск: ")

    # Вызов функции
    zip_file_path = download_from_yandex_disk(public_url, chrome_driver_path)

    if zip_file_path:
        print(f"Скачанный файл находится по пути: {zip_file_path}")
    else:
        print(f"{TClr.CRED}Скачивание не удалось. Завершение скрипта.{TClr.CEND}")
        exit()

    # Распаковка архива и получение пути к распакованной папке
    unpack_to = args.unpack_path
    extracted_folder = unzip_to_destination(zip_file_path, unpack_to)

    if extracted_folder:
        # Перемещаем все файлы из распакованной папки в саму себя (для структурирования)
        find_and_move_all_files(extracted_folder)
        print(f"Распакованный архив находится по пути: {extracted_folder}")
        # Открываем файл .aep в распакованной папке
        open_aep_file(extracted_folder)
    else:
        print(f"{TClr.CRED}Распаковка не удалась. Завершение скрипта.{TClr.CEND}")
        exit()

    print(f"{TClr.CGREEN}Скрипт успешно завершился.{TClr.CEND}")