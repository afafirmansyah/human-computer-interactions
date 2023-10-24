import paho.mqtt.client as mqtt
import tkinter as tk
from tkdial import Meter

# Fungsi yang dipanggil saat pesan diterima
def on_message(client, userdata, message):
    pesan_baru = message.payload.decode()
    try:
        nilai = float(pesan_baru)
        if 0 <= nilai <= 100:
            dial.set(nilai)
        else:
            print("Nilai harus berada antara 0 dan 100")
    except ValueError:
        print("Pesan MQTT harus berupa nilai numerik")

# Fungsi untuk menghubungkan ke broker MQTT
def connect_mqtt():
    mqtt_broker = "broker.hivemq.com"
    mqtt_port = 1883
    topic = "ubd/mti/temp_1"

    client.connect(mqtt_broker, mqtt_port)
    client.subscribe(topic)

# Membuat klien MQTT
client = mqtt.Client()
client.on_message = on_message

# Membuat jendela Tkinter
root = tk.Tk()
root.title("Penerima Pesan MQTT")

# Membuat Meter (Dial)
dial = Meter(root)
dial.pack(padx=10, pady=10)

# Menghubungkan ke broker MQTT
connect_mqtt()

# Mulai loop untuk menerima pesan
client.loop_start()

# Memulai aplikasi Tkinter
root.mainloop()
