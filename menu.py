from tkinter import *
import threading
from turtle import width
from ursina.prefabs.first_person_controller import FirstPersonController
import os

def stop():
    root.destroy()
    exit(0)

root=Tk()

root.geometry("800x500")
root.minsize(800, 500)
root.title("  PhyGame 1.2")

canvas=Canvas(root, 
    bg="#23272e", 
    width=800,
    height=500
)

top=canvas.create_rectangle(
    0, 0, 
    root.maxsize()[0], 80,
    outline="black", 
    fill="#1c1c1c"
)

root.update()

Tt=canvas.create_text(
    root.winfo_width()/2, 40, 
    text="PhyGame", 
    font=('Helvetica 25 bold'), 
    fill="white"
)

param=canvas.create_window(
    root.winfo_width()/2+320, 40, 
    window=Button(root, 
        font=("Arial", 15), 
        relief="flat", 
        borderwidth=0, 
        bg="#1e2227", 
        width=7, 
        highlightthickness=1, 
        highlightbackground='black', 
        fg="white", 
        text="Param"
    )
)

def STG():
    But1B['bg']="#1a1d21"
    But2B['bg']="#1e2227"
    But3B['bg']="#1e2227"

def HTG():
    But1B['bg']="#1e2227"
    But2B['bg']="#1a1d21"
    But3B['bg']="#1e2227"

def GI():
    But1B['bg']="#1e2227"
    But2B['bg']="#1e2227"
    But3B['bg']="#1a1d21"

But1B=Button(root, 
    font=("Arial", 20), 
    relief="flat", borderwidth=0, 
    bg="#1a1d21", 
    width=round(root.winfo_width()/49), 
    height=1, 
    highlightthickness=1, 
    highlightbackground='black', 
    fg="white", 
    text="Start Game",
    command=STG
)

But2B=Button(root, 
    font=("Arial", 20), 
    relief="flat", borderwidth=0, 
    bg="#1e2227", 
    width=round(root.winfo_width()/49), 
    height=1, 
    highlightthickness=1, 
    highlightbackground='black', 
    fg="white", 
    text="Host Game",
    command=HTG
)

But3B=Button(root, 
    font=("Arial", 20), 
    relief="flat", borderwidth=0, 
    bg="#1e2227", 
    width=round(root.winfo_width()/49), 
    height=1, 
    highlightthickness=1, 
    highlightbackground='black', 
    fg="white", 
    text="Game Infos",
    command=GI
)

But1=canvas.create_window(
    ((root.winfo_width()*(1/3))-root.winfo_width()/6), 107,
    window=But1B
)

But2=canvas.create_window(
    ((root.winfo_width()*(2/3))-root.winfo_width()/6), 107, 
    window=But2B
)

But3=canvas.create_window(
    ((root.winfo_width()*(3/3))-root.winfo_width()/6), 107, 
    window=But3B
)

Auto=canvas.create_window(
    root.winfo_width()/2-150, root.winfo_height()/2, 
    window=Button(root, 
        font=("Arial", 20),
        relief="flat", 
        borderwidth=0, 
        bg="#1e2227", 
        width=15, 
        highlightthickness=1, 
        highlightbackground='black', 
        fg="white", 
        text="Publics Servers"
    )
)

Manual=canvas.create_window(
    root.winfo_width()/2+150, root.winfo_height()/2, 
    window=Button(root, 
        font=("Arial", 20), 
        relief="flat", 
        borderwidth=0, 
        bg="#1e2227", 
        width=15, 
        highlightthickness=1, 
        highlightbackground='black', 
        fg="white", 
        text="Manual Servers"
    )
)



GPage=canvas.create_window(2, 80, anchor="nw", width=root.winfo_width()-5, height=root.winfo_height()-82)

def act():
    while 1:
        root.update()
        canvas.itemconfigure(GPage, width=root.winfo_width()-5, height=root.winfo_height()-122)
        canvas.coords(Auto, root.winfo_width()/2-150, root.winfo_height()/2)
        canvas.coords(Manual, root.winfo_width()/2+150, root.winfo_height()/2)
        canvas.coords(param, root.winfo_width()/2+320, canvas.coords(param)[1])
        canvas.coords(Tt, root.winfo_width()/2, canvas.coords(Tt)[1])
        canvas.coords(But1, (root.winfo_width()*(1/3))-root.winfo_width()/6, canvas.coords(But1)[1])
        canvas.coords(But2, (root.winfo_width()*(2/3))-root.winfo_width()/6, canvas.coords(But2)[1])
        canvas.coords(But3, (root.winfo_width()*(3/3))-root.winfo_width()/6, canvas.coords(But3)[1])
        But1B['width']=round(root.winfo_width()/49)
        But2B['width']=round(root.winfo_width()/49)
        But3B['width']=round(root.winfo_width()/49)
    
t=threading.Thread(target=act)
t.setDaemon(True)
t.start()

canvas.pack(expand=True, fill="both")
root.protocol("WM_DELETE_WINDOW", stop)
root.mainloop()