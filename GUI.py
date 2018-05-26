from tkinter import *

from tkinter import messagebox
import os

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageTk

top = Tk()
top.grid()
top.geometry("300x300")

i=0

payload=''
payloads=os.listdir("payloads")
try:
   payloads.remove('.DS_Store')
except:
   pass

var = StringVar()
label = Label( top, textvariable = var, relief = RAISED )
var.set(str(payloads[i]))
payload=str(payloads[i])
label.pack()

def runPayload():
    global payload
    os.system('python3 fusee-launcher.py payloads/'+payload)

def decrement():
    global i
    global label
    global var
    global payload
    i-=1
    if i<0:
        i=len(payloads)-1
    var.set(str(payloads[i]))
    payload=str(payloads[i])
    label.pack()
    
def increment():
    global i
    global label
    global label2
    global var
    global payload
    i+=1
    if i>len(payloads)-1:
        i=0
    var.set(str(payloads[i]))
    payload=str(payloads[i])
    label.pack()

A = Button(top, text = "<", command = decrement)
#A.place(x = 75,y = 150)
A.place(relx=0.25, rely=0.5, anchor=W)
#A.grid(row=0, column=0)
#A.pack(side=LEFT)
B = Button(top, text = "Run", command = runPayload)
#B.place(x = 150,y = 150)
B.place(relx=0.5, rely=0.5, anchor=CENTER)
#B.grid(row=2, column=2)
#B.pack(side=CENTER)
C = Button(top, text = ">", command = increment)
#C.place(x = 225,y = 150)
C.place(relx=0.75, rely=0.5, anchor=E)
#C.grid(row=3, column=3)
#C.pack(side=RIGHT)
top.mainloop()
