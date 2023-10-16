import paho.mqtt.client as mqtt
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Fungsi yang dipanggil saat pesan diterima
def on_message(client, userdata, message):
    pesan_baru = message.payload.decode()
    
    # Mengupdate Meter berdasarkan nilai pesan yang diterima
    try:
        nilai_meter = int(pesan_baru)
        meter.configure(amountused=nilai_meter)
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

# Menghubungkan ke broker MQTT
connect_mqtt()

# Mulai loop untuk menerima pesan
client.loop_start()

# Memulai aplikasi Tkinter
root.mainloop()
