import tkinter
from tkdial import Jogwheel, Meter

def update_meter_value(event):
    # Fungsi ini akan dipanggil ketika nilai Jogwheel berubah
    # Setel nilai Meter sesuai dengan nilai Jogwheel
    dial.set(knob.get())

root = tkinter.Tk()

# Buat Jogwheel dan Meter
knob = Jogwheel(root)
knob.grid(row=0, column=0)

dial = Meter(root)
dial.grid(row=0, column=1, padx=10, pady=10)

# Hubungkan perubahan nilai Jogwheel ke fungsi update_meter_value
knob.bind("<Motion>", update_meter_value)

root.mainloop()
