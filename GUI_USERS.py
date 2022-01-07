import tkinter as tk
import os
import shutil
from PIL import ImageTk, Image

def Update_name(file_name,name,type):
    os.rename(file_name,"re/known/"+name+type)
def Move_file(file_name,name,type):
    shutil.move(file_name,"re/known/"+name+type)
def Users():
    name = []
    img=[]
    mylist = os.listdir("re/known/")
    root=tk.Toplevel()
    title=tk.Label(root,text="Users")
    title.pack()
    j=0



    i=22
    for i in mylist:
        frame=tk.Frame(root)
        frame.pack()
        L=tk.Entry(frame)
        L.insert(0,os.path.splitext(i)[0])
        L.grid(row=1,column=2)
        imgt = Image.open("re/known/"+i)
        imgt = imgt.resize((100, 80), Image.ANTIALIAS)
        img.append(ImageTk.PhotoImage(imgt))
        imgL=tk.Label(frame,image=img[j])
        imgL.grid(row=1,column=1)
        btn=tk.Button(frame,text="Update",command=lambda :Update_name("re/known/"+i,L.get(),os.path.splitext(i)[1]))
        btn.grid(row=1,column=3)
        name.append(os.path.splitext(i)[0])
        j=j+1
    un = os.listdir("re/unknown/")
    for i in un:
        frame=tk.Frame(root)
        frame.pack()
        L=tk.Entry(frame)
        L.insert(0,os.path.splitext(i)[0])
        L.grid(row=1,column=2)
        imgt = Image.open("re/unknown/" + i)
        imgt = imgt.resize((100, 80), Image.ANTIALIAS)
        img.append(ImageTk.PhotoImage(imgt))
        imgL = tk.Label(frame, image=img[j])
        imgL.grid(row=1,column=1)
        btn=tk.Button(frame,text="Update",command=lambda :Move_file("re/unknown/"+i,L.get(),os.path.splitext(i)[1]))
        btn.grid(row=1,column=3)
        j=j+1
        name.append(os.path.splitext(i)[0])

    root.mainloop()