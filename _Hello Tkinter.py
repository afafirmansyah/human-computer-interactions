import tkinter as tk

# Membuat jendela utama
root = tk.Tk()
root.title("Contoh Tkinter")

# Membuat label
label = tk.Label(root, text="Halo, Tkinter!")
label.pack()

# Memulai loop utama aplikasi
root.mainloop()
