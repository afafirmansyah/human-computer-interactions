import tkinter
from tkdial import Jogwheel, Meter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

# Fungsi untuk mengupdate grafik setiap detik
def update_plot():
    # Setel nilai Meter sesuai dengan nilai Jogwheel
    dial.set(knob.get())
    
    # Tambahkan nilai saat ini ke dalam daftar nilai
    values.append(knob.get())
    
    # Hapus nilai yang sudah melebihi 20 data terbaru
    if len(values) > 20:
        values.pop(0)
    
    # Update grafik
    ax.clear()
    ax.plot(range(len(values)), values, marker='o', linestyle='-')
    ax.set_xlabel('Waktu (detik)')
    ax.set_ylabel('Nilai')
    canvas.draw()
    
    # Jadwalkan pembaruan berikutnya setelah 1 detik
    root.after(1000, update_plot)

root = tkinter.Tk()
root.title("Grafik Nilai Jogwheel")

# Buat Jogwheel dan Meter
knob = Jogwheel(root)
knob.grid(row=0, column=0)

dial = Meter(root)
dial.grid(row=0, column=1, padx=10, pady=10)

# Inisialisasi daftar nilai dengan nilai awal dari Jogwheel
values = [knob.get()]

# Buat subplot untuk grafik
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlabel('Waktu (detik)')
ax.set_ylabel('Nilai')

# Tampilkan grafik dalam jendela Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=1, column=0, columnspan=2)

# Fungsi untuk memulai pembaruan plot
def start_update():
    # Jadwalkan pembaruan pertama setelah 1 detik
    root.after(1000, update_plot)

# Mulai pembaruan plot saat aplikasi dimulai
start_update()

root.mainloop()
