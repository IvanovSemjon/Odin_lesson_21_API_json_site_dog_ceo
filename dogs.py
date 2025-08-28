from tkinter import *
from tkinter import messagebox as mb
import requests
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import ttk
from tkinter import Toplevel
from typing import Optional


def get_dog_image() -> Optional[str]:
    """Получает URL случайного изображения собаки из API.
    
    Returns:
        str: URL изображения или None при ошибке
    """
    try:
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        response.raise_for_status()
        data = response.json()
        return data["message"]
    except Exception as e:
        mb.showerror("Ошибка!", f"Ошибка при получении изображения: {e}")
        return None
    

def show_image() -> None:
    """Загружает и отображает изображение собаки во вкладке."""
    image_url = get_dog_image()
    if image_url:
        try:
            # ВНИМАНИЕ: Загрузка изображения по внешнему URL
            response = requests.get(image_url, stream=True, timeout=10)
            response.raise_for_status()
            
            image_data = BytesIO(response.content)
            img = Image.open(image_data)
            
            # Получаем размеры из пользовательского ввода
            img_size = (int(width_spinbox.get()), int(height_spinbox.get()))
            img.thumbnail(img_size)
            img = ImageTk.PhotoImage(img)
            
            # Создаем новую вкладку
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=f"Картинка № {notebook.index('end')+1}")
            
            lb = ttk.Label(tab, image=img)
            lb.pack(padx=10, pady=10)
            lb.image = img  # Предотвращаем удаление сборщиком мусора
            
        except Exception as e:
           mb.showerror("Ошибка!", f"Ошибка при загрузке изображения: {e}")
    
    progress.stop()


def load_image() -> None:
    """Запускает процесс загрузки изображения с прогресс-баром."""
    progress['value'] = 0
    progress.start(30)
    # Запускаем загрузку в отдельном потоке для лучшей отзывчивости
    window.after(100, show_image)


def clear_tabs() -> None:
    """Очищает все вкладки с изображениями."""
    tabs = notebook.tabs()
    for tab in tabs:
        notebook.forget(tab)


# Создание главного окна
window = Tk()
window.title("Картинки с собачками")
window.geometry("360x420")

# Фрейм для кнопок
button_frame = Frame(window)
button_frame.pack(pady=10)

Button(button_frame, text="Загрузить изображение", command=load_image).pack(side='left', padx=(0, 10))
Button(button_frame, text="Очистить вкладки", command=clear_tabs).pack(side='left')

# Прогресс-бар
progress = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=10)

# Настройки размера изображения
size_frame = Frame(window)
size_frame.pack(pady=10)

ttk.Label(size_frame, text="Ширина: ").pack(side='left', padx=(10, 0))
width_spinbox = ttk.Spinbox(size_frame, from_=200, to=500, increment=50, width=5)
width_spinbox.pack(side='left', padx=(0, 10))
width_spinbox.set(300)

ttk.Label(size_frame, text="Высота: ").pack(side='left', padx=(10, 0))
height_spinbox = ttk.Spinbox(size_frame, from_=200, to=500, increment=50, width=5)
height_spinbox.pack(side='left', padx=(0, 10))
height_spinbox.set(300)

# Окно для отображения изображений
toplevel_window = Toplevel(window)
toplevel_window.title("Изображения собачек")

# Виджет для вкладок с изображениями
notebook = ttk.Notebook(toplevel_window)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

window.mainloop()