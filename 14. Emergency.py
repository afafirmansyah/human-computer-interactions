import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import threading

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
        set_meter_value(nilai_meter)

        # Periksa apakah nilai melebihi 70
        if nilai_meter > 70 and not emergency_mode:
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

# Fungsi untuk mengaktifkan atau menonaktifkan mode darurat
def toggle_emergency_mode():
    global emergency_mode
    if emergency_mode:
        emergency_mode = False
        enable_widgets()
        emergency_button.configure(text="Emergency Off")
    else:
        emergency_mode = True
        disable_widgets()
        emergency_button.configure(text="Emergency On")

# Fungsi untuk menonaktifkan widget
def disable_widgets():
    meter_frame.pack_forget()
    notification_tree.pack_forget()

# Fungsi untuk mengaktifkan kembali widget
def enable_widgets():
    meter_frame.pack()
    notification_tree.pack()

# Fungsi untuk mengatur nilai meter
def set_meter_value(value):
    meter["value"] = value

# Inisialisasi mode darurat
emergency_mode = False

# Membuat klien MQTT
client = mqtt.Client()
client.on_message = on_message

# Membuat jendela Tkinter
root = tk.Tk()
root.title("Penerima Pesan MQTT")

# Membuat Frame untuk Meter widget
meter_frame = ttk.Frame(root)
meter_frame.pack()

# Membuat Label untuk Meter widget
meter_label = ttk.Label(meter_frame, text="Meter Widget:")
meter_label.pack()

# Membuat Progress Bar sebagai Meter
meter = ttk.Progressbar(meter_frame, mode="determinate", length=200)
meter.pack()


# Membuat Treeview untuk tabel notifikasi
notification_tree = ttk.Treeview(root, columns=("Notification",), show="headings")
notification_tree.heading("Notification", text="Notification")
notification_tree.pack()

# Membuat tombol "Emergency"
emergency_button = ttk.Button(root, text="Emergency Off", command=toggle_emergency_mode)
emergency_button.pack()

# Menghubungkan ke broker MQTT
connect_mqtt()

# Mulai loop untuk menerima pesan
client.loop_start()

# Memulai aplikasi Tkinter
root.mainloop()
