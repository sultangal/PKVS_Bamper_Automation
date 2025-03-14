import zipfile
import os
import shutil

from term_colors import TClr


def unzip_to_destination(zip_path, unpack_to):

    # Проверяем, существует ли архив с таким же именем
    if not os.path.exists(zip_path):
        print(f"Архив {zip_path} не существует.")
        print("Распаковка отменена.")
        return None  # Завершаем выполнение функции

    # Определяем имя папки, которая будет создана после распаковки
    archive_name = os.path.splitext(os.path.basename(zip_path))[0]
    extracted_folder = os.path.join(unpack_to, archive_name)

    # Проверяем, существует ли папка с таким же именем
    if os.path.exists(extracted_folder):
        print(f"Папка {extracted_folder} уже существует.")
        print("Распаковка отменена.")
        return None  # Завершаем выполнение функции

    # Распаковка архива
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(unpack_to)
        print(f"Архив {zip_path} распакован в {unpack_to}")

    # Удаляем архив после успешной распаковки
    try:
        os.remove(zip_path)
        print(f"Архив {zip_path} успешно удален.")
    except Exception as e:
        print(f"{TClr.CYELLOW}Не удалось удалить архив {zip_path}. Причина: {e}{TClr.CEND}")

    # Проверяем, что папка создана
    if os.path.exists(extracted_folder):
        print(f"Папка после распаковки: {extracted_folder}")
        return extracted_folder
    else:
        print(f"Папка {extracted_folder} не найдена.")
        return None

def find_and_move_all_files(dir):
    # Проходим по всем папкам и подпапкам в dir
    for root, dirs, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, file)
            target_path = os.path.join(dir, file)

            # Перемещаем файл
            shutil.move(file_path, target_path)
            print(f"Файл {file} перемещен в {dir}")