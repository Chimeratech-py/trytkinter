from tkinter import *
from unittest import skip
from weakref import ref
from nltk.translate.bleu_score import sentence_bleu
import spacy

def getPOS(inputtext):
    c = 0
    POSlist = []
    for token in inputtext:
        if token.pos_ != 'SPACE':
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
            try:
                if(candidatePOSlist[counter]==referencePOSlist[counter]):
                    correctcounter+=1
            except:
                skip
            finally:    
                counter+=1 
                   
    else:
        while(candidateLength > counter):
            try:
                if(referencePOSlist[counter]==candidatePOSlist[counter]):
                    correctcounter+=1
            except:
                skip
            finally:
                counter+=1  
            
   
    mistakes = candidateLength - correctcounter
    
    partial = netscore/candidateLength
    
    deduction = mistakes*partial
       
    grossscore = netscore - deduction
    
    return grossscore

def compare_POS(referencetxt, candidatetxt):
    referencePOSlist = getPOS(referencetxt)
    candidatePOSlist = getPOS(candidatetxt)
    
    counter = 0
    correctcounter = 0
    candidateLength = len(candidatePOSlist)
        
    if(len(referencePOSlist)>candidateLength):
        while(len(referencePOSlist) > counter):
            try:
                if(candidatePOSlist[counter]==referencePOSlist[counter]):
                    correctcounter+=1
            except:
                skip
            finally:    
                counter+=1 
                   
    else:
        while(candidateLength > counter):
            try:
                if(referencePOSlist[counter]==candidatePOSlist[counter]):
                    correctcounter+=1
            except:
                skip
            finally:
                counter+=1  
                
    return f'{correctcounter} of {len(referencePOSlist)} and {str(referencePOSlist)}'
    



class Window:
    def __init__(self, master):
        reftxt = ''
        re_list = []
        with open('reference.txt',mode='r') as re:
            for line in re:
                re_list.append(line)
                
        nlp = spacy.load('en_core_web_sm')
        
        pos_list = getPOS(nlp(re_list[0]))
        c=0
        #reftxt = ' '.join([str(word) for word in pos_list])
        reftxt = re_list[c]
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
        
        
        candtxt = ca_list[c]
        subframe2 = Frame(master, background="red")
        candlbl = Label(subframe2, text="Candidate Text")
        candlbl.place(relx=0.5,anchor=N)
        message = Label(subframe2, text= candtxt)
        message.place(relx=0.5, rely=0.5,anchor=CENTER) 
        
        bleuscore = sentence_bleu(list(reftxt), list(candtxt), weights=(0, 0, 0, 0))
        
        gross = structure_evaluation(nlp(reftxt),nlp(candtxt), bleuscore)
        bleu_lbl = Label(subframe2, text = 'standard bleu score: ' + str(bleuscore))
        bleu_lbl.place(relx=0.5, rely=0.7,anchor=CENTER)
        gross_lbl = Label(subframe2, text = 'Structure sensitive Bleu score: ' + str(gross))
        gross_lbl.place(relx=0.5, rely=0.8, anchor = CENTER)
        compare_lbl = Label(subframe2, text = f'Correctly placed POS tags: {compare_POS(nlp(reftxt), nlp(candtxt))}')
        compare_lbl.place(relx=0.5, rely=0.9, anchor = CENTER)
        subframe2.pack(expand=True, fill=BOTH, side=LEFT)
        
        def nextLine(z):
            z+=1
            print(z)
            reftxt = re_list[z]
            candtxt = ca_list[z]
            subject.config(text=reftxt)
            message.config(text=candtxt)
            
        btn_next = Button(subframe,text="Next",command =nextLine(c))
        btn_next.place(relx=0.5, rely=0.8, anchor = CENTER)
        
            
root = Tk()
root.geometry('300x200')
window = Window(root)

root.mainloop()  
