import pyautogui
import pydirectinput
import keyboard
import time
import threading
import os
import sys
import pygetwindow as gw  # Не забудь: pip install pygetwindow
from pystray import Icon, Menu, MenuItem
from PIL import Image

# Авто-определение путей
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_IMAGE = os.path.join(BASE_DIR, 'target.png')
ICON_IMAGE = os.path.join(BASE_DIR, 'icon.png')

# Настройка заголовка окна
GAME_WINDOW_TITLE = 'Doomsday' # Бот будет искать окно, где есть это слово

is_running = True
is_paused = False

def bot_logic():
    global is_running, is_paused
    while is_running:
        # 1. Если нажата пауза в трее — отдыхаем
        if is_paused:
            time.sleep(1)
            continue
            
        try:
            # 2. Получаем активное окно
            active_win = gw.getActiveWindow()
            
            # 3. Проверяем: существует ли окно и есть ли в его названии "Doomsday"
            # .lower() нужен, чтобы не зависеть от больших/маленьких букв
            if active_win and GAME_WINDOW_TITLE.lower() in active_win.title.lower():
                
                # Если игра активна — ищем кнопку
                location = pyautogui.locateOnScreen(TARGET_IMAGE, confidence=0.8)
                
                if location:
                    x, y = pyautogui.center(location)
                    pydirectinput.moveTo(int(x), int(y))
                    time.sleep(0.2)
                    pydirectinput.click()
                    time.sleep(5) 
                else:
                    time.sleep(1)
            else:
                # Если окно игры НЕ активно — ничего не делаем и ждем 2 секунды
                time.sleep(2)
                
        except Exception:
            # Если произошла ошибка (например, окно закрылось), ждем и пробуем снова
            time.sleep(2)

def toggle_pause(icon, item):
    global is_paused
    is_paused = not is_paused

def stop_bot(icon, item):
    global is_running
    is_running = False
    icon.stop()
    os._exit(0)

def setup_tray():
    if os.path.exists(ICON_IMAGE):
        image = Image.open(ICON_IMAGE)
    else:
        image = Image.new('RGB', (32, 32), color=(0, 255, 0))

    menu = Menu(
        MenuItem('Пауза / Старт', toggle_pause, checked=lambda item: is_paused),
        MenuItem('Выход', stop_bot)
    )
    icon = Icon("DoomsdayBot", image, "Doomsday Bot Active", menu)
    
    thread = threading.Thread(target=bot_logic, daemon=True)
    thread.start()
    icon.run()

if __name__ == "__main__":
    setup_tray()