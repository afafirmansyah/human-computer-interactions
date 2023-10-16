import paho.mqtt.client as mqtt
import tkinter as tk

# Fungsi yang dipanggil saat pesan diterima
def on_message(client, userdata, message):
    pesan_baru = message.payload.decode()
    pesan_label.config(text=pesan_baru)

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

# Membuat label untuk menampilkan pesan
pesan_label = tk.Label(root, text="", wraplength=300)
pesan_label.pack(padx=10, pady=10)

# Menghubungkan ke broker MQTT
connect_mqtt()

# Mulai loop untuk menerima pesan
client.loop_start()

# Memulai aplikasi Tkinter
root.mainloop()
