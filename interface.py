import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

window = tk.Tk()

label = tk.Label(window, text="Ingrese el código fuente:")
label.pack(padx=10, pady=5)

text_input = tk.Text(window, height=10, width=40)
text_input.pack(padx=10, pady=5)

table = ttk.Treeview(window, columns=("Token", "Clasificación"), show="headings")
table.heading("Token", text="Token")
table.heading("Clasificación", text="Clasificación")
table.pack(padx=10, pady=10)

classify_button = tk.Button(window, text="Clasificar Tokens", command=classify_tokens)
classify_button.pack(padx=10, pady=5)

classify_button1 = tk.Button(window, text="Analizar", command=parse_code)
classify_button1.pack(padx=10, pady=5)

text_sintactico = tk.Text(window, height=10, width=40)
text_sintactico.pack(padx=10, pady=5)

restaurar_button = tk.Button(window, text="Restaurar Todo", command=restaurar_todo)
restaurar_button.pack(padx=10, pady=5)

window.mainloop()
