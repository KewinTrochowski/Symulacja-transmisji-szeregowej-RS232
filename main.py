import tkinter as tk
from tkinter import ttk

root = tk.Tk()
style = ttk.Style()

# Ustawienie motywu
style.theme_use('vista')  # Przykład: 'clam', 'alt', 'default', 'classic' itp.

label = ttk.Label(root, text="To jest etykieta")
label.pack()

button = ttk.Button(root, text="Kliknij mnie")
button.pack()

root.mainloop()
