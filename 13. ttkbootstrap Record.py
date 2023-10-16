import paho.mqtt.client as mqtt
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from tkinter import ttk as ttk2  # Import ttk as ttk2 for Treeview
from datetime import datetime

# Inisialisasi data untuk tabel notifikasi
notifications = []  # Simpan notifikasi

# Fungsi untuk menambahkan notifikasi ke tabel
def add_notification(notification):
    notifications.append(notification)
    # Hapus notifikasi lama jika lebih dari 10 notifikasi
    if len(notifications) > 10:
        notifications.pop(0)
    update_notification_table()

# Fungsi untuk mengupdate tabel notifikasi
def update_notification_table():
    notification_tree.delete(*notification_tree.get_children())
    for notification in notifications:
        notification_tree.insert("", "end", values=(notification,))

# Fungsi yang dipanggil saat pesan diterima
def on_message(client, userdata, message):
    pesan_baru = message.payload.decode()
    
    # Mengupdate Meter berdasarkan nilai pesan yang diterima
    try:
        nilai_meter = int(pesan_baru)
        meter.configure(amountused=nilai_meter)
        
        # Periksa apakah nilai melebihi 70
        if nilai_meter > 70:
            # Tambahkan notifikasi ke tabel
            waktu_sekarang = datetime.now().strftime('%H:%M:%S')
            notification = f"{waktu_sekarang} - Temperature: {nilai_meter}°C"
            add_notification(notification)
            
    except ValueError:
        pass

# Fungsi untuk menghubungkan ke broker MQTT
def connect_mqtt():
    mqtt_broker = "broker.hivemq.com"
    mqtt_port = 1883
    topic = "ubd/mti/temperature"

    client.connect(mqtt_broker, mqtt_port)
    client.subscribe(topic)

# Membuat klien MQTT
client = mqtt.Client()
client.on_message = on_message

# Membuat jendela Tkinter
root = tk.Tk()
root.title("Penerima Pesan MQTT")

# Membuat Meter widget
meter = ttk.Meter(
    metersize=180,
    padding=5,
    amountused=0,  # Nilai awal Meter
    metertype="semi",
    subtext="°Celcius",
    interactive=True,
)
meter.pack()

# Membuat Treeview untuk tabel notifikasi
notification_tree = ttk2.Treeview(root, columns=("Notification",), show="headings")
notification_tree.heading("Notification", text="Notification")
notification_tree.pack()

# Menghubungkan ke broker MQTT
connect_mqtt()

# Mulai loop untuk menerima pesan
client.loop_start()

# Memulai aplikasi Tkinter
root.mainloop()
