import tkinter
from tkdial import Jogwheel

app = tkinter.Tk()

knob = Jogwheel(app)
knob.grid()

app.mainloop()