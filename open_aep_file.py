import os
import subprocess

def open_aep_file(folder_path):
    # Ищем файл с расширением .aep в указанной папке
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".aep"):
                aep_file_path = os.path.join(root, file)
                print(f"Найден файл .aep: {aep_file_path}")

                # Открываем файл с помощью программы по умолчанию
                try:
                    if os.name == 'nt':  # Для Windows
                        os.startfile(aep_file_path)
                    elif os.name == 'posix':  # Для macOS и Linux
                        subprocess.run(
                            ["open", aep_file_path] if os.uname().sysname == "Darwin" else ["xdg-open", aep_file_path])
                    print(f"Файл {aep_file_path} успешно открыт.")
                    return
                except Exception as e:
                    print(f"Ошибка при открытии файла: {e}")
                    return

    print(f"Файл с расширением .aep не найден в {folder_path}.")