from tkinter import *
from tkinter import messagebox as mb
import requests
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import ttk
from tkinter import Toplevel


def get_dog_image():
    try:
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        response.raise_for_status()
        data = response.json()
        return data["message"]
    except Exception as e:
        mb.showerror("Ошибка!", f"Ошибка при получении изображения -->  {e}")
        return None
    

def show_image():
    image_url = get_dog_image()
    if image_url:
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            image_data = BytesIO(response.content)
            img = Image.open(image_data)
            img_size = (int(width_spinbox.get()), int(height_spinbox.get()))
            img.thumbnail(img_size)
            img = ImageTk.PhotoImage(img)
            new_window = Toplevel(window)
            new_window.title("Случайное изображение")
            lb = ttk.Label(new_window, image=img)
            lb.pack(pady=10)
            lb.image = img
        except Exception as e:
           mb.showerror("Ошибка!", f"Ошибка при загрузке изображения -->  {e}")
    progress.stop()   


def prog():
    progress['value'] = 0
    progress.start(30)
    window.after(3000, show_image)


window = Tk()
window.title("Картинки с собачками")
window.geometry("360x420")

label = Label()
label.pack(pady=10)

button = Button(text="Загрузить изображение", command=prog)
button.pack(pady=10)

progress = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=10)

width_lable = ttk.Label(text="Ширина: ")
width_lable.pack(side='left', padx=(10, 0))
width_spinbox = ttk.Spinbox(from_=200, to=500, increment=50, width=5)
width_spinbox.pack(side='left', padx=(0, 10))

height_lable = ttk.Label(text="Высота: ")
height_lable.pack(side='left', padx=(10, 0))
height_spinbox = ttk.Spinbox(from_=200, to=500, increment=50, width=5)
height_spinbox.pack(side='left', padx=(0, 10))


window.mainloop()