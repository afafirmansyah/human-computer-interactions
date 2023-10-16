import tkinter
from tkdial import Meter

def update_dial_value():
    # Mengambil nilai integer dari kotak teks
    nilai = int(entry.get())

    # Memastikan nilai berada dalam rentang yang valid (misalnya antara 0 dan 100)
    if 0 <= nilai <= 100:
        dial.set(nilai)
    else:
        print("Nilai harus berada antara 0 dan 100")

root = tkinter.Tk()

# Membuat Meter (Dial)
dial = Meter(root)
dial.pack(padx=10, pady=10)

# Membuat kotak teks untuk memasukkan nilai
entry = tkinter.Entry(root)
entry.pack(pady=10)

# Tombol untuk memperbarui nilai pada Dial
update_button = tkinter.Button(root, text="Perbarui", command=update_dial_value)
update_button.pack()

root.mainloop()
