# Импорт всех виджетов из tkinter
from tkinter import *
# Импорт модуля для диалоговых окон
from tkinter import messagebox as mb
# Импорт библиотеки для HTTP-запросов
import requests
# Импорт библиотек для работы с изображениями
from PIL import Image, ImageTk
# Импорт для работы с байтовыми данными
from io import BytesIO
# Импорт стилизованных виджетов
from tkinter import ttk
# Импорт для создания дополнительных окон
from tkinter import Toplevel


def get_dog_image():
    """Функция для получения URL случайного изображения собаки из API"""
    try:
        # Отправляем GET-запрос к API для получения случайного изображения собаки
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        # Проверяем успешность HTTP-запроса
        response.raise_for_status()
        # Преобразуем ответ в JSON формат
        data = response.json()
        # Выводим полученные данные в консоль для отладки
        print(data)
        print(data["message"])
        print(data["status"])
        # Возвращаем URL изображения из ответа API
        return data["message"]
    except Exception as e:
        # Показываем окно с ошибкой при неудачном запросе
        mb.showerror("Ошибка!", f"Ошибка при получении изображения -->  {e}")
        return None
    

def show_image():
    """Функция для загрузки и отображения изображения собаки"""
    # Получаем URL изображения собаки
    image_url = get_dog_image()
    if image_url:
        try:
            # Загружаем изображение по URL с потоковой передачей
            response = requests.get(image_url, stream=True)
            # Проверяем успешность загрузки изображения
            response.raise_for_status()
            # Создаем объект BytesIO из содержимого ответа
            image_data = BytesIO(response.content)
            # Открываем изображение с помощью PIL
            img = Image.open(image_data)
            # Получаем размеры из spinbox виджетов
            img_size = (int(width_spinbox.get()), int(height_spinbox.get()))
            # Изменяем размер изображения с сохранением пропорций
            img.thumbnail(img_size)
            # Преобразуем изображение в формат для tkinter
            img = ImageTk.PhotoImage(img)
            # Создаем новую вкладку в notebook
            tab = ttk.Frame(notebook)
            # Добавляем вкладку с нумерацией
            notebook.add(tab, text=f"Картинка № {notebook.index('end')+1}")
            # Создаем Label для отображения изображения во вкладке
            lb = ttk.Label(tab, image=img)
            # Размещаем Label во вкладке с отступами
            lb.pack(padx=10, pady=10)
            # Сохраняем ссылку на изображение для предотвращения удаления сборщиком мусора
            lb.image = img
        except Exception as e:
           # Показываем окно с ошибкой при неудачной загрузке изображения
           mb.showerror("Ошибка!", f"Ошибка при загрузке изображения -->  {e}")
    # Останавливаем анимацию прогресс-бара
    progress.stop()   


def prog():
    """Функция для запуска процесса загрузки с прогресс-баром"""
    # Сбрасываем значение прогресс-бара на 0
    progress['value'] = 0
    # Запускаем анимацию прогресс-бара с интервалом 30мс
    progress.start(30)
    # Запускаем функцию show_image через 3 секунды
    window.after(3000, show_image)


# Создаем главное окно приложения
window = Tk()
# Устанавливаем заголовок главного окна
window.title("Картинки с собачками")
# Устанавливаем размер окна
window.geometry("360x420")

# Создаем пустой Label (не используется в текущей версии)
label = Label()
# Размещаем Label с вертикальным отступом
label.pack(pady=10)

# Создаем кнопку для загрузки изображения
button = Button(text="Загрузить изображение", command=prog)
# Размещаем кнопку с вертикальным отступом
button.pack(pady=10)

# Создаем горизонтальный прогресс-бар длиной 300 пикселей
progress = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")  
# Размещаем прогресс-бар с вертикальным отступом
progress.pack(pady=10)

# Создаем метку для поля ширины
width_lable = ttk.Label(text="Ширина: ")
# Размещаем метку слева с горизонтальным отступом
width_lable.pack(side='left', padx=(10, 0))
# Создаем spinbox для выбора ширины изображения (от 200 до 500 с шагом 50)
width_spinbox = ttk.Spinbox(from_=200, to=500, increment=50, width=5)
# Размещаем spinbox слева с горизонтальным отступом
width_spinbox.pack(side='left', padx=(0, 10))
# Устанавливаем значение по умолчанию для ширины
width_spinbox.set(300)

# Создаем метку для поля высоты
height_lable = ttk.Label(text="Высота: ")
# Размещаем метку слева с горизонтальным отступом
height_lable.pack(side='left', padx=(10, 0))
# Создаем spinbox для выбора высоты изображения (от 200 до 500 с шагом 50)
height_spinbox = ttk.Spinbox(from_=200, to=500, increment=50, width=5)
# Размещаем spinbox слева с горизонтальным отступом
height_spinbox.pack(side='left', padx=(0, 10))
# Устанавливаем значение по умолчанию для высоты
height_spinbox.set(300) 

# Создаем дополнительное окно верхнего уровня для отображения изображений
toplevel_window = Toplevel(window)
# Устанавливаем заголовок дополнительного окна
toplevel_window.title("Изображение собачек")

# Создаем виджет notebook для вкладок с изображениями
notebook = ttk.Notebook(toplevel_window)
# Размещаем notebook с заполнением всего пространства и отступами
notebook.pack(fill='both', expand=True, padx=10, pady=10)


# Запускаем главный цикл обработки событий приложения
window.mainloop()