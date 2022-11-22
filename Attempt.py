from tkinter import *
from unittest import skip
from weakref import ref
from nltk.translate.bleu_score import sentence_bleu
import spacy

class Window:
    def __init__(self, master):
        self.counter = 0
        subframe = Frame(master, background="blue")
        self.reflbl = Label(subframe, text = "Reference Text")
        self.reflbl.place(relx=0.5,anchor=N)
        
    
        
        self.btn_next = Button(subframe,text="Next",command =self.update)
        self.btn_next.place(relx=0.5, rely=0.8, anchor = CENTER)
        
        subframe.pack(expand=True, fill=BOTH, side=LEFT)
        
        
        self.ca_list = []
        with open('candidate.txt',mode='r') as fr:
            for line in fr:
                self.ca_list.append(line)
                  
    def update(self):
        temp = self.ca_list[self.counter]
        self.reflbl["text"] = temp
        self.counter+=1

        # if temp: # there was text in file
        #     Tk.after(1000, self.update)
        # else:
        #     print('Probably end of file')
        #     self.f.close()
        #     self.f = None # so you can open again
            
        
root = Tk()
root.geometry('300x200')
window = Window(root)

root.mainloop()  

