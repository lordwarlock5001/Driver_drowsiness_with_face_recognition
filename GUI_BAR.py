import tkinter as tk
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageTk, Image
import os
from tkinter import messagebox
root=None
def gen_bar(name):
    if os.path.exists("re/user_files/"+name+".csv"):
        data = pd.read_csv("re/user_files/"+name+".csv")
        # data.set_index("name")
        data.fillna("Unknown", inplace=True)
        gb = data.groupby("name")
        gb = gb.sum()
        print(gb)
        l = gb.index.values
        s = gb['hours'].tolist()
        print(s)
        plt.bar(l, s)
        plt.title("Driving time of various users")
        plt.xlabel("Users")
        plt.ylabel("Hours")
        plt.savefig("temp.png")
        plt.show()
        img = Image.open("temp.png")
        img = img.resize((700, 500), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        imgl = tk.Label(root,image=img)
        imgl.pack()
    else:
        messagebox.showinfo(title="sample",message="Report/data is not available")
def bar_chart():
    root = tk.Toplevel()
    title=tk.Label(root,text="Report Page(Bar chart)")
    title.pack()
    hint_date=tk.Label(root,text="dd-mm-yyyy please fill in this format")
    hint_date.pack()
    date=tk.Entry(root)
    date.pack()
    btn=tk.Button(root,text="Genrate",command=lambda :gen_bar(date.get()))
    btn.pack()
    root.mainloop()