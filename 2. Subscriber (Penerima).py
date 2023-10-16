import paho.mqtt.client as mqtt

# Fungsi yang dipanggil saat pesan diterima
def on_message(client, userdata, message):
    print(f"Pesan diterima di topik '{message.topic}': {message.payload.decode()}")

# Pengaturan broker MQTT
mqtt_broker = "broker.hivemq.com"
mqtt_port = 1883

# Membuat klien MQTT
client = mqtt.Client()
client.on_message = on_message

# Menghubungkan klien ke broker
client.connect(mqtt_broker, mqtt_port)

# Berlangganan ke topik
topic = "ubd/mti/temperature"
client.subscribe(topic)

# Mulai loop untuk menerima pesan
client.loop_forever()
