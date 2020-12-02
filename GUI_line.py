from tkinter import messagebox

import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import os
def get_chart_user(date):
    if os.path.exists("re/drowsiness_files/"+date+".csv"):
        data=pd.read_csv("re/drowsiness_files/"+date+".csv")
        data.fillna("Unknown",inplace=True)
        gb=data.groupby("name")
        su=gb.sum()
        l=list(su.index.values)
        user=[]
        for i in l:
            user.append(gb.get_group(i))
            grb=gb.get_group(i)
            grb.plot(x="time", y="EAR", rot=45, title=i)
        plt.show()
    else:
        messagebox.showinfo(title="sample", message="Report/data is not available")
def bar_chart():
    root = tk.Toplevel()
    title=tk.Label(root,text="Report Page(Line chart)")
    title.pack()
    hint_date=tk.Label(root,text="dd-mm-yyyy please fill in this format")
    hint_date.pack()
    date=tk.Entry(root)
    date.pack()
    btn=tk.Button(root,text="Genrate",command=lambda :get_chart_user(date.get()))
    btn.pack()
    root.mainloop()