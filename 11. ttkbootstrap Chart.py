import paho.mqtt.client as mqtt
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
from datetime import datetime


# Inisialisasi data untuk plotting
nilai_meter_list = deque(maxlen=10)  # Simpan 20 nilai terakhir
waktu_list = deque(maxlen=10)  # Simpan waktu terkait dengan nilai

# Fungsi yang dipanggil saat pesan diterima
def on_message(client, userdata, message):
    pesan_baru = message.payload.decode()
    
    # Mengupdate Meter dan data plotting berdasarkan nilai pesan yang diterima
    try:
        nilai_meter = int(pesan_baru)
        meter.configure(amountused=nilai_meter)
        nilai_meter_list.append(nilai_meter)
        
        # Simpan waktu saat ini
        waktu_sekarang = datetime.now().strftime('%H:%M:%S')
        waktu_list.append(waktu_sekarang)
        
        # Plot nilai-meter dengan waktu pada sumbu X
        ax.clear()
        ax.plot(waktu_list, nilai_meter_list)
        ax.set_xlabel('Time')
        ax.set_ylabel('Temperature (°C)')
        ax.tick_params(axis='x', rotation=25)
        canvas.draw()
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
    padding=0,
    amountused=0,  # Nilai awal Meter
    metertype="semi",
    subtext="°Celcius",
    interactive=True,
)
meter.pack()

# Membuat plot grafik
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Menghubungkan ke broker MQTT
connect_mqtt()

# Mulai loop untuk menerima pesan
client.loop_start()

# Memulai aplikasi Tkinter
root.mainloop()
