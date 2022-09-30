from tkinter import *

# root = Tk()  

# txt = ''

# with open('reference.txt',mode='r') as f:
#     txt = f.readline()


# myLabel = Label(root, text = txt)

# myLabel.pack()

# canvas = Canvas(root, height = 700, width = 700, bg="#263D42")
# canvas.pack()

# frame = Frame(root, bg="white")
# frame.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.1)

# initiate = Button(root, text="Initiate", padx=10, pady=5, fg="white",  bg="#263D42")

# initiate.pack()
class Window:
    def __init__(self, master):
        reftxt = ''
        with open('reference.txt',mode='r') as f:
            reftxt = f.readline()
        subframe = Frame(master, background="blue")
        reflbl = Label(subframe, text = "Reference Text")
        reflbl.place(relx=0.5,anchor=N)
        subject = Label(subframe, text = reftxt)
        subject.place(relx=0.5, rely=0.5,anchor=CENTER)
        subframe.pack(expand = True, fill = BOTH, side=LEFT)

        candtxt = ''
        with open('candidate.txt',mode='r') as f:
            candtxt = f.readline()

        subframe2 = Frame(master, background="red")
        candlbl = Label(subframe2, text="Candidate Text")
        candlbl.place(relx=0.5,anchor=N)
        message = Label(subframe2, text= candtxt)
        message.place(relx=0.5, rely=0.5,anchor=CENTER)
        subframe2.pack(expand=True, fill=BOTH, side=LEFT)
 
root = Tk()
root.geometry('300x200')
window = Window(root)

root.mainloop()  
