import argparse

from pyautogui import doubleClick
from pywinauto import Application
import pyautogui
import time


def run(video_path, save_path):
    # Запуск приложения TitleEditor
    app = Application(backend='win32').start('C:/Program Files/BRAM Technologies/AutoPlay 7/TitleEditor.exe')

    # Подключение к главному окну приложения
    main_window = app.TitleEditor
    main_window.move_window(x=0, y=0, width=800, height=600)

    # Загружаем стандартный tpj
    main_window.menu_select("Файл -> Открыть...")
    tpj_load_dlg = app.window(title='Загрузить шаблон')
    tpj_load_dlg.wait("exists enabled visible ready")
    tpj_load_dlg.Edit.set_edit_text(tpj_path)
    time.sleep(1)
    tpj_load_dlg.wait(wait_for="exists enabled visible ready", timeout=10, retry_interval=0.1)
    tpj_load_dlg.window(title="&Открыть", class_name="Button").click()
    # Ждем когда окно Загрузить шаблон закроется
    tpj_load_dlg.wait_not("exists")
    # Переводим фокус на главное окно
    main_window = app.top_window()

    # Кликаем по видео слою
    pyautogui.click(x=249, y=55)

    main_window.window(control_id=1008, class_name="Button").wait(
        "exists enabled visible ready").click()  # Кнопка "..."
    video_load_dlg = app.window(title='Загрузить изображение')
    video_load_dlg.wait("exists enabled visible ready")
    video_load_dlg.Edit.set_edit_text(video_path)
    time.sleep(1)
    video_load_dlg.wait(wait_for="exists enabled visible ready", timeout=10, retry_interval=0.1)
    video_load_dlg.window(title="&Открыть", class_name="Button").click()  # Кнопка Открыть
    # Ждем когда окно Загрузить изображение закроется
    video_load_dlg.wait_not("exists")
    # Переводим фокус на главное окно
    main_window = app.top_window()
    # Сохраняем tpj
    main_window.menu_select("Файл -> Сохранить как...")
    save_tpj_dlg = app.window(title='Сохранить шаблон')
    save_tpj_dlg.wait("exists enabled visible ready")
    save_tpj_dlg.Edit.set_edit_text(save_path)
    time.sleep(1)
    save_tpj_dlg.wait(wait_for="exists enabled visible ready", timeout=10, retry_interval=0.1)
    save_tpj_dlg.window(control_id=1, class_name="Button").click()  # Кнопка Сохранить
    # Ждем когда окно Загрузить изображение закроется
    save_tpj_dlg.wait_not("exists")
    # Переводим фокус на главное окно
    main_window = app.top_window()
    main_window.wait(wait_for="exists enabled visible ready", timeout=120)
    # Проверяем появилось ли окно замены файла
    if app.window(title='Замена файла').exists():
        raise FileExistsError("Что то пошло не так. Файл уже существует")
    # Ждем конца сохранения
    while app.window(title='Сохранение проекта').exists():
        time.sleep(1)
    app.top_window().maximize()
    # Завершаем приложение
    # app.kill()


if __name__ == "__main__":
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument('video_paths', type=str, nargs='+', help='Пути к файлам .mov')
    args = parser.parse_args()

    tpj_path = 'F:\\PROJECTS\\DKO\\DKO__01_001.tpj'

    project_name = input("Введите название проекта: ")
    project_version = input("Введите версию проекта (по умолчанию - 001): ") or "001"

    for i, video_path in enumerate(args.video_paths, start=1):
        run(video_path, f'C:\\Users\\admin\\Desktop\\DKO_{project_name}_{i:02d}_{project_version}.tpj')
