import paho.mqtt.client as mqtt
import tkinter as tk
from ttkbootstrap.widgets import Meter
from tkinter import Menu, messagebox
from datetime import datetime
import threading
from PIL import Image
Image.CUBIC = Image.BICUBIC

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
            check_threshold("Temperature 1", nilai_meter, min_temp_1, max_temp_1)
        elif topic == "ubd/mti/temp_2":
            temp_2_meter.configure(amountused=nilai_meter)
            check_threshold("Temperature 2", nilai_meter, min_temp_2, max_temp_2)
        elif topic == "ubd/mti/press_1":
            press_1_meter.configure(amountused=nilai_meter)
            check_threshold("Pressure 1", nilai_meter, min_press_1, max_press_1)
        elif topic == "ubd/mti/press_2":
            press_2_meter.configure(amountused=nilai_meter)
            check_threshold("Pressure 2", nilai_meter, min_press_2, max_press_2)
    except ValueError:
        pass

# Fungsi untuk memeriksa apakah nilai melebihi batasan dan mengubah warna font
def check_threshold(topic, nilai, batasan_min, batasan_max):
    if nilai < batasan_min:
        messagebox.showwarning("Below Minimum Threshold", f"Nilai {topic} di bawah batasan minimum: {nilai} < {batasan_min}", icon="error")
    elif nilai > batasan_max:
        messagebox.showwarning("Above Maximum Threshold", f"Nilai {topic} di atas batasan maksimum: {nilai} > {batasan_max}", icon="error")

# Fungsi untuk menghubungkan ke broker MQTT
def connect_mqtt():
    mqtt_broker = "broker.hivemq.com"
    mqtt_port = 1883
    topics = ["ubd/mti/temp_1", "ubd/mti/temp_2", "ubd/mti/press_1", "ubd/mti/press_2"]

    client.connect(mqtt_broker, mqtt_port)
    for topic in topics:
        client.subscribe(topic)
    client.loop_forever()

# Fungsi untuk mengganti mode tampilan antara gauge
def change_view_mode(mode):
    if mode == "gauge":
        gauge_frame.pack()  # Menampilkan frame tampilan gauge

# Membuat klien MQTT
client = mqtt.Client()
client.on_message = on_message

# Membuat jendela Tkinter
root = tk.Tk()
root.title("Human Computer Interactions")


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
    metersize=180,
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
    metersize=180,
    padding=5,
    amountused=0,
    metertype="semi",
    subtext="temp_2 (°C)",
    interactive=True,
)
temp_2_meter.grid(row=0, column=1)

press_1_meter = Meter(
    gauge_frame,
    metersize=180,
    padding=5,
    amountused=0,
    metertype="semi",
    subtext="press_1 (bar)",
    interactive=True,
)
press_1_meter.grid(row=0, column=2)

press_2_meter = Meter(
    gauge_frame,
    metersize=180,
    padding=5,
    amountused=0,
    metertype="semi",
    subtext="press_2 (bar)",
    interactive=True,
)
press_2_meter.grid(row=0, column=3)

# Memulai utas MQTT dalam utas terpisah
mqtt_thread = threading.Thread(target=connect_mqtt)
mqtt_thread.daemon = True
mqtt_thread.start()

# Memulai aplikasi Tkinter
root.mainloop()
