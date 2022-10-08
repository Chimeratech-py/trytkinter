from tkinter import *
from weakref import ref
from nltk.translate.bleu_score import sentence_bleu
import spacy

def getPOS(inputtext):
    c = 0
    POSlist = []
    for token in inputtext:
        POSlist.append(token.pos_)
        c+=1
    return POSlist

##structure evaluation phase, it takes 3 arguments, which are the referencetxt, or translated text according to human judgement,
##candidatetxt, or translated text from the machine translation algorithm, and the netscore, which is the score output
##of standard BLEU
##The percentage of incorrectly placed parts-of-speech tags are then deducted from the netscore 
def structure_evaluation(referencetxt,candidatetxt,netscore):
    referencePOSlist = getPOS(referencetxt)
    candidatePOSlist = getPOS(candidatetxt)
    
    #referencePOSlist = ['DET', 'VERB', 'DET', 'NOUN']
    #candidatePOSlist = ['DET', 'DET', 'NOUN', 'VERB']
    
    
    counter = 0
    correctcounter = 0
    candidateLength = len(candidatePOSlist)
        
    if(len(referencePOSlist)>candidateLength):
        while(len(referencePOSlist) > counter):
            if(referencePOSlist[counter]==candidatePOSlist[counter]):
                correctcounter+=1
            counter+=1        
    else:
        while(candidateLength > counter):
            if(referencePOSlist[counter]==candidatePOSlist[counter]):
                correctcounter+=1
            counter+=1  
            
   
    mistakes = candidateLength - correctcounter
    
    partial = netscore/candidateLength
    
    deduction = mistakes*partial
       
    grossscore = netscore - deduction
    
    return grossscore
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
        re_list = []
        with open('reference.txt',mode='r') as re:
            for line in re:
                re_list.append(line)
        
        reftxt = re_list[0]
        subframe = Frame(master, background="blue")
        reflbl = Label(subframe, text = "Reference Text")
        reflbl.place(relx=0.5,anchor=N)
        subject = Label(subframe, text = reftxt)
        subject.place(relx=0.5, rely=0.5,anchor=CENTER)
        subframe.pack(expand = True, fill = BOTH, side=LEFT)
        
        candtxt = ''
        ca_list = []
        with open('candidate.txt',mode='r') as f:
            for line in f:
                ca_list.append(line)
                
        candtxt = ca_list[1]
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
