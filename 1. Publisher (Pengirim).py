import paho.mqtt.publish as publish
import time
import random

# Pengaturan broker MQTT
mqtt_broker = "broker.hivemq.com"
mqtt_port = 1883

# Topik untuk mengirim pesan
topic = "ubd/mti/temperature"

# Jeda waktu antara pengiriman pesan (dalam detik)
interval = 1

while True:
    # Membuat angka acak dari 0 hingga 100
    angka_acak = random.randint(0, 100)
    
    # Mengirim angka acak sebagai pesan
    pesan = str(angka_acak)
    publish.single(topic, pesan, hostname=mqtt_broker, port=mqtt_port)
    
    # Menunggu sebelum mengirim pesan lagi
    time.sleep(interval)
