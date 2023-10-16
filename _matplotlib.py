import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import datetime

# Fungsi untuk membuat data contoh (data waktu dan nilai)
def generate_sample_data():
    dates = [datetime.date(2023, 10, 1) + datetime.timedelta(days=i) for i in range(10)]
    values = [20, 25, 30, 28, 35, 40, 38, 45, 50, 48]
    return dates, values

# Fungsi untuk membuat grafik garis
def create_line_chart():
    # Ambil data contoh
    dates, values = generate_sample_data()

    # Buat objek Figure dari Matplotlib
    fig = Figure(figsize=(8, 5))

    # Tambahkan axes (sumbu) ke dalam objek Figure
    ax = fig.add_subplot(111)

    # Buat grafik garis dengan data waktu
    ax.plot(dates, values, marker='o', linestyle='-', color='b', label='Data')

    # Konfigurasi sumbu-x dengan format tanggal
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(DateFormatter("%m-%d"))

    # Atur judul dan label sumbu
    ax.set_title("Grafik Time Series")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Nilai")

    # Tambahkan legenda
    ax.legend()

    # Buat aplikasi Tkinter
    root = tk.Tk()
    root.title("Grafik Time Series")

    # Buat frame Tkinter untuk menampung chart
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Buat canvas Tkinter untuk menampilkan chart Matplotlib
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # Mulai aplikasi Tkinter
    root.mainloop()

# Panggil fungsi untuk membuat grafik garis
create_line_chart()
