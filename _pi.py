import paho.mqtt.client as mqtt
import tkinter as tk
from ttkbootstrap.widgets import Meter
from ttkbootstrap.widgets import Treeview
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter
import json
import time
from tkinter import Menu, messagebox
from datetime import datetime
import threading
import matplotlib.pyplot as plt

# Maksimum dan minimum nilai yang diizinkan untuk setiap topik
max_temp_1 = 100  # Atur sesuai kebutuhan
min_temp_1 = 0  # Atur sesuai kebutuhan
max_temp_2 = 100  # Atur sesuai kebutuhan
min_temp_2 = 0  # Atur sesuai kebutuhan
max_press_1 = 100  # Atur sesuai kebutuhan
min_press_1 = 0  # Atur sesuai kebutuhan
max_press_2 = 100  # Atur sesuai kebutuhan
min_press_2 = 0  # Atur sesuai kebutuhan

emergency_active = False

# Fungsi untuk mengaktifkan atau menonaktifkan mode Emergency
def toggle_emergency():
    global emergency_active
    if emergency_active:
        # Matikan mode Emergency
        toggle_emergency_button.configure(text="Emergency Release", bg="green")
        emergency_active = False
        # Matikan koneksi MQTT
        client.disconnect()
        messagebox.showinfo("Emergency Mode", "Emergency Mode telah diaktifkan. Koneksi MQTT telah diputus.")
        temp_1_max_entry.config(state='disabled')
        temp_1_min_entry.config(state='disabled')
        temp_2_max_entry.config(state='disabled')
        temp_2_min_entry.config(state='disabled')
        press_1_max_entry.config(state='disabled')
        press_1_min_entry.config(state='disabled')
        press_2_max_entry.config(state='disabled')
        press_2_min_entry.config(state='disabled')
        update_button.config(state='disabled')
    else:
        # Aktifkan mode Emergency
        toggle_emergency_button.configure(text="Emergency Button", bg="red")
        emergency_active = True
        # Sambungkan kembali ke MQTT
        mqtt_thread = threading.Thread(target=connect_mqtt)
        mqtt_thread.daemon = True
        mqtt_thread.start()
        messagebox.showwarning("Emergency Mode", "Emergency Mode telah dimatikan. Koneksi MQTT telah dihidupkan kembali.")
        # Aktifkan semua widget dan meter
        temp_1_max_entry.config(state='normal')
        temp_1_min_entry.config(state='normal')
        temp_2_max_entry.config(state='normal')
        temp_2_min_entry.config(state='normal')
        press_1_max_entry.config(state='normal')
        press_1_min_entry.config(state='normal')
        press_2_max_entry.config(state='normal')
        press_2_min_entry.config(state='normal')
        update_button.config(state='normal')


def set_column_width(col_name, width):
    aktivitas_alarm_treeview.column(col_name, width=width)

def on_column_width_resize(event):
    for col_name in ("Time", "Topic", "Value", "Threshold"):
        width = aktivitas_alarm_treeview.column(col_name, 'width')
        set_column_width(col_name, width)

# Fungsi untuk mengganti batasan maksimum dan minimum
def update_max_min_values():
    global max_temp_1, min_temp_1, max_temp_2, min_temp_2, max_press_1, min_press_1, max_press_2, min_press_2
    try:
        max_temp_1 = int(temp_1_max_entry.get())
        min_temp_1 = int(temp_1_min_entry.get())
        max_temp_2 = int(temp_2_max_entry.get())
        min_temp_2 = int(temp_2_min_entry.get())
        max_press_1 = int(press_1_max_entry.get())
        min_press_1 = int(press_1_min_entry.get())
        max_press_2 = int(press_2_max_entry.get())
        min_press_2 = int(press_2_min_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Masukkan angka yang valid untuk nilai maksimum dan minimum.")
        return
    messagebox.showinfo("Success", "Nilai maksimum dan minimum telah diperbarui.")

# Fungsi yang dipanggil saat pesan diterima
def on_message(client, userdata, message):
    pesan_baru = message.payload.decode()
    topic = message.topic
    
    # Mengupdate Meter berdasarkan nilai pesan yang diterima
    try:
        nilai_meter = int(pesan_baru)
        if topic == "ubd/mti/temp_1":
            temp_1_meter.configure(amountused=nilai_meter)
            update_chart(temp_ax, temp_data, "temp", topic, nilai_meter)
            check_threshold("Temperature 1", nilai_meter, min_temp_1, max_temp_1)
        elif topic == "ubd/mti/temp_2":
            temp_2_meter.configure(amountused=nilai_meter)
            update_chart(temp_ax, temp_data, "temp", topic, nilai_meter)
            check_threshold("Temperature 2", nilai_meter, min_temp_2, max_temp_2)
        elif topic == "ubd/mti/press_1":
            press_1_meter.configure(amountused=nilai_meter)
            update_chart(press_ax, press_data, "press", topic, nilai_meter)
            check_threshold("Pressure 1", nilai_meter, min_press_1, max_press_1)
        elif topic == "ubd/mti/press_2":
            press_2_meter.configure(amountused=nilai_meter)
            update_chart(press_ax, press_data, "press", topic, nilai_meter)
            check_threshold("Pressure 2", nilai_meter, min_press_2, max_press_2)
    except ValueError:
        pass

# Fungsi untuk memeriksa apakah nilai melebihi batasan dan mengubah warna font
def check_threshold(topic, nilai, batasan_min, batasan_max):
    if nilai < batasan_min:
        messagebox.showwarning("Below Minimum Threshold", f"Nilai {topic} di bawah batasan minimum: {nilai} < {batasan_min}", icon="error")
        # Catat aktivitas alarm
        catat_aktivitas_alarm(topic, nilai, batasan_min, "red")  # Warna merah
    elif nilai > batasan_max:
        messagebox.showwarning("Above Maximum Threshold", f"Nilai {topic} di atas batasan maksimum: {nilai} > {batasan_max}", icon="error")
        # Catat aktivitas alarm
        catat_aktivitas_alarm(topic, nilai, batasan_max, "blue")  # Warna biru


# Fungsi untuk mencatat aktivitas alarm dengan warna teks yang sesuai
def catat_aktivitas_alarm(topic, nilai, batasan, warna):
    waktu_sekarang = datetime.now().strftime('%H:%M:%S')
    
    # Masukkan data di bagian atas Treeview
    aktivitas_alarm_treeview.insert("", 0, values=(waktu_sekarang, topic, nilai, batasan), tags=(warna,))
    
    # Jika terdapat lebih dari 10 item, hapus item yang lebih lama
    if len(aktivitas_alarm_treeview.get_children()) > 10:
        aktivitas_alarm_treeview.delete(aktivitas_alarm_treeview.get_children()[-1])



# Fungsi untuk menghubungkan ke broker MQTT
def connect_mqtt():
    mqtt_broker = "broker.hivemq.com"
    mqtt_port = 1883
    topics = ["ubd/mti/temp_1", "ubd/mti/temp_2", "ubd/mti/press_1", "ubd/mti/press_2"]

    client.connect(mqtt_broker, mqtt_port)
    for topic in topics:
        client.subscribe(topic)
    client.loop_forever()

# Fungsi untuk mengupdate data pada grafik
def update_chart(ax, data, data_type, topic, value):
    if topic not in data:
        data[topic] = []
    
    data[topic].append((time.time(), value))
    if len(data[topic]) > max_data_points:
        data[topic].pop(0)
    
    ax.clear()
    for topic, data_points in data.items():
        x, y = zip(*data_points)
        ax.plot(x, y, label=topic)
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.legend(loc='upper right')
    ax.xaxis.set_major_formatter(FuncFormatter(format_time))
    canvas.draw()

# Fungsi untuk memformat waktu sebagai "H:M:S"
def format_time(value, tick_number):
    return datetime.fromtimestamp(value).strftime('%H:%M:%S')

# Fungsi untuk mengganti mode tampilan antara gauge, chart, dan alarm
def change_view_mode(mode):
    if mode == "gauge":
        chart_frame.pack_forget()  # Menghilangkan frame tampilan chart
        alarm_frame.pack_forget()  # Menghilangkan frame tampilan alarm
        gauge_frame.pack()  # Menampilkan frame tampilan gauge
    elif mode == "chart":
        gauge_frame.pack_forget()  # Menghilangkan frame tampilan gauge
        alarm_frame.pack_forget()  # Menghilangkan frame tampilan alarm
        chart_frame.pack()  # Menampilkan frame tampilan chart
    else:
        gauge_frame.pack_forget()  # Menghilangkan frame tampilan gauge
        chart_frame.pack_forget()  # Menghilangkan frame tampilan chart
        alarm_frame.pack()  # Menampilkan frame tampilan alarm

# Membuat klien MQTT
client = mqtt.Client()
client.on_message = on_message

# Membuat jendela Tkinter
root = tk.Tk()
root.title("Human Computer Interactions")
root.geometry("640x480")  # Mengatur resolusi menjadi 640x480

# Fungsi untuk menambahkan menu toolbar
menu = Menu(root)
root.config(menu=menu)

# Membuat menu "View"
view_menu = Menu(menu)
menu.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Gauge", command=lambda: change_view_mode("gauge"))
view_menu.add_command(label="Chart", command=lambda: change_view_mode("chart"))
view_menu.add_command(label="Alarm", command=lambda: change_view_mode("alarm"))

# Membuat frame untuk tampilan gauge
gauge_frame = tk.Frame(root)
gauge_frame.pack()

# Membuat Entry untuk pengguna memasukkan nilai maksimum dan minimum
temp_1_max_label = tk.Label(gauge_frame, text="Max Temp 1")
temp_1_max_label.grid(row=1, column=0)
temp_1_max_entry = tk.Entry(gauge_frame)
temp_1_max_entry.grid(row=2, column=0)

temp_1_min_label = tk.Label(gauge_frame, text="Min Temp 1")
temp_1_min_label.grid(row=3, column=0)
temp_1_min_entry = tk.Entry(gauge_frame)
temp_1_min_entry.grid(row=4, column=0)

# Menambahkan entri untuk nilai maksimum dan minimum lainnya
temp_2_max_label = tk.Label(gauge_frame, text="Max Temp 2")
temp_2_max_label.grid(row=1, column=1)
temp_2_max_entry = tk.Entry(gauge_frame)
temp_2_max_entry.grid(row=2, column=1)

temp_2_min_label = tk.Label(gauge_frame, text="Min Temp 2")
temp_2_min_label.grid(row=3, column=1)
temp_2_min_entry = tk.Entry(gauge_frame)
temp_2_min_entry.grid(row=4, column=1)

press_1_max_label = tk.Label(gauge_frame, text="Max Press 1")
press_1_max_label.grid(row=1, column=2)
press_1_max_entry = tk.Entry(gauge_frame)
press_1_max_entry.grid(row=2, column=2)

press_1_min_label = tk.Label(gauge_frame, text="Min Press 1")
press_1_min_label.grid(row=3, column=2)
press_1_min_entry = tk.Entry(gauge_frame)
press_1_min_entry.grid(row=4, column=2)

press_2_max_label = tk.Label(gauge_frame, text="Max Press 2")
press_2_max_label.grid(row=1, column=3)
press_2_max_entry = tk.Entry(gauge_frame)
press_2_max_entry.grid(row=2, column=3)

press_2_min_label = tk.Label(gauge_frame, text="Min Press 2")
press_2_min_label.grid(row=3, column=3)
press_2_min_entry = tk.Entry(gauge_frame)
press_2_min_entry.grid(row=4, column=3)

empty_label = tk.Label(gauge_frame, text="", width=10)
empty_label.grid(row=5, column=0)

update_button = tk.Button(gauge_frame, text="Update Max/Min Values", command=update_max_min_values)
update_button.grid(row=6, column=1, columnspan=2, sticky="nsew")

empty_label = tk.Label(gauge_frame, text="", width=10)
empty_label.grid(row=7, column=0)

# Tambahkan tombol Toggle Emergency
toggle_emergency_button = tk.Button(gauge_frame, text="Emergency Button", command=toggle_emergency)
toggle_emergency_button.grid(row=8, column=1, columnspan=2, sticky="nsew")

empty_label = tk.Label(gauge_frame, text="", width=10)
empty_label.grid(row=9, column=0)


# Membuat Meter widget
temp_1_meter = Meter(
    gauge_frame,
    metersize=150,
    padding=5,
    amountused=0,
    metertype="semi",
    subtext="temp_1 (°C)",
    interactive=True,
)
temp_1_meter.grid(row=0, column=0)

# Menambahkan Meter untuk nilai maksimum dan minimum lainnya
temp_2_meter = Meter(
    gauge_frame,
    metersize=150,
    padding=5,
    amountused=0,
    metertype="semi",
    subtext="temp_2 (°C)",
    interactive=True,
)
temp_2_meter.grid(row=0, column=1)

press_1_meter = Meter(
    gauge_frame,
    metersize=150,
    padding=5,
    amountused=0,
    metertype="semi",
    subtext="press_1 (bar)",
    interactive=True,
)
press_1_meter.grid(row=0, column=2)

press_2_meter = Meter(
    gauge_frame,
    metersize=150,
    padding=5,
    amountused=0,
    metertype="semi",
    subtext="press_2 (bar)",
    interactive=True,
)
press_2_meter.grid(row=0, column=3)

# Membuat frame untuk tampilan chart
chart_frame = tk.Frame(root)
chart_frame.pack(fill="both", expand=True)  # Mengisi dan memperluas frame ke seluruh jendela

# Konfigurasi grafik
max_data_points = 10
temp_data = {}
press_data = {}

fig = Figure(figsize=(8, 4), dpi=100)  # Sesuaikan ukuran dan dpi sesuai dengan frame

temp_ax = fig.add_subplot(211)
temp_ax.set_title("Temperature")

press_ax = fig.add_subplot(212)
press_ax.set_title("Pressure")

# Atur jarak antara subplot
fig.subplots_adjust(hspace=0.5)  # Sesuaikan angka sesuai dengan kebutuhan

canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill="both", expand=True)  # Mengisi dan memperluas canvas ke seluruh frame


# Menambahkan empty label di bawah press_ax
empty_label = tk.Label(chart_frame, text="", height=1)
empty_label.pack()

# Membuat frame untuk tampilan alarm
alarm_frame = tk.Frame(root)

# Membuat Treeview untuk merekam aktivitas alarm
aktivitas_alarm_treeview = Treeview(alarm_frame, columns=("Time", "Topic", "Value", "Threshold"))

# Mengonfigurasi tag dengan warna
aktivitas_alarm_treeview.tag_configure("red", foreground="red")
aktivitas_alarm_treeview.tag_configure("blue", foreground="blue")

# Kemudian mengaitkan tag ke Treeview
aktivitas_alarm_treeview.tag_bind("red", sequence="<<TreeviewSelect>>", callback=lambda event: aktivitas_alarm_treeview.item(aktivitas_alarm_treeview.selection(), tags="red"))
aktivitas_alarm_treeview.tag_bind("blue", sequence="<<TreeviewSelect>>", callback=lambda event: aktivitas_alarm_treeview.item(aktivitas_alarm_treeview.selection(), tags="blue"))

aktivitas_alarm_treeview.heading("Time", text="Time")
aktivitas_alarm_treeview.heading("Topic", text="Topic")
aktivitas_alarm_treeview.heading("Value", text="Value")
aktivitas_alarm_treeview.heading("Threshold", text="Threshold")
aktivitas_alarm_treeview.pack()


# Mengatur lebar awal kolom Treeview
aktivitas_alarm_treeview.column("Time", width=100)
aktivitas_alarm_treeview.column("Topic", width=100)
aktivitas_alarm_treeview.column("Value", width=100)
aktivitas_alarm_treeview.column("Threshold", width=100)

aktivitas_alarm_treeview.pack()

# Mengatur rata tengah untuk semua kolom Treeview
for col in ("Time", "Topic", "Value", "Threshold"):
    aktivitas_alarm_treeview.column(col, anchor="center")
    aktivitas_alarm_treeview.heading(col, text=col, anchor="center")

# Mengizinkan pengguna untuk mengatur lebar kolom secara dinamis
aktivitas_alarm_treeview.bind("<Motion>", on_column_width_resize)
    

# Memulai dengan tampilan gauge
change_view_mode("gauge")

# Memulai utas MQTT dalam utas terpisah
mqtt_thread = threading.Thread(target=connect_mqtt)
mqtt_thread.daemon = True
mqtt_thread.start()

# Memulai aplikasi Tkinter
root.mainloop()
