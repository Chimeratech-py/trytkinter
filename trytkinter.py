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
    
    returnDictionary = {'grs': 0,'correctly placed tags': []}
    
    counter = 0
    correctcounter = 0
    candidateLength = len(candidatePOSlist)
        
    if(len(referencePOSlist)>candidateLength):
        while(len(referencePOSlist) > counter):
            try:
                if(candidatePOSlist[counter]==referencePOSlist[counter]):
                    returnDictionary['correctly placed tags'].append(f'{candidatePOSlist[counter]} {counter}')
                    correctcounter+=1
            except:
                skip
            finally:    
                counter+=1 
                   
    else:
        while(candidateLength > counter):
            try:
                if(referencePOSlist[counter]==candidatePOSlist[counter]):
                    returnDictionary['correctly placed tags'].append(f'{candidatePOSlist[counter]} {counter}')
                    correctcounter+=1
            except:
                skip
            finally:
                counter+=1  
            
   
    mistakes = candidateLength - correctcounter
    
    partial = netscore/candidateLength
    
    deduction = mistakes*partial
       
    grossscore = netscore - deduction
    
    returnDictionary['grs'] = grossscore
    
    return returnDictionary

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
                
    return f'{correctcounter} of {len(referencePOSlist)}'
    



class Window:
    def __init__(self, master):
        self.nlp = spacy.load('en_core_web_sm')
        
        self.counter=0
        
        self.ref_list = []
        with open('reference.txt',mode='r') as re:
            for line in re:
                self.ref_list.append(line)
        
        self.ca_list = []
        with open('candidate.txt',mode='r') as f:
            for line in f:
                self.ca_list.append(line)
                
        self.ref_being_evaluated = self.ref_list[self.counter]
        self.cand_being_evaluated = self.ca_list[self.counter]
                
        
        
        
        
        #reftxt = ' '.join([str(word) for word in pos_list])
        
        subframe = Frame(master, background="blue")
        self.reflbl = Label(subframe, text = "Reference Text")
        self.reflbl.place(relx=0.5,anchor=N)
        self.reftxt = Label(subframe, text = self.ref_being_evaluated)
        self.reftxt.place(relx=0.5, rely=0.5,anchor=CENTER)
        subframe.pack(expand = True, fill = BOTH, side=LEFT)
        
        
        
        
        
       
        subframe2 = Frame(master, background="red")
        self.candlbl = Label(subframe2, text="Candidate Text")
        self.candlbl.place(relx=0.5,anchor=N)
        self.candtxt = Label(subframe2, text= self.cand_being_evaluated)
        self.candtxt.place(relx=0.5, rely=0.5,anchor=CENTER) 
        
        bleuscore = sentence_bleu(list(self.ref_being_evaluated), list(self.cand_being_evaluated), weights=(1, 0, 0, 0))
        
        dictOutput = structure_evaluation(self.nlp(self.ref_being_evaluated),self.nlp(self.cand_being_evaluated), bleuscore)
        
        self.bleu_lbl = Label(subframe2, text = 'standard bleu score: ' + str(bleuscore))
        self.bleu_lbl.place(relx=0.5, rely=0.6,anchor=CENTER)
        self.gross_lbl = Label(subframe2, text = 'Structure sensitive Bleu score: ' + str(dictOutput['grs']))
        self.gross_lbl.place(relx=0.5, rely=0.7, anchor = CENTER)
        self.corr_lbl = Label(subframe2, text = f'Correctly placed POS tags:' +  str(dictOutput['correctly placed tags']))
        self.corr_lbl.place(relx=0.5, rely=0.8, anchor = CENTER)
        self.compare_lbl = Label(subframe2, text = f'Number of correctly placed tags: {compare_POS(self.nlp(self.ref_being_evaluated), self.nlp(self.cand_being_evaluated))}')
        self.compare_lbl.place(relx=0.5, rely=0.9, anchor = CENTER)
        subframe2.pack(expand=True, fill=BOTH, side=LEFT)
        
        self.btn_next = Button(subframe,text="Next",command =self.updateTexts)
        self.btn_next.place(relx=0.5, rely=0.8, anchor = CENTER)
        
    def updateTexts(self):
        self.ref_being_evaluated = self.ref_list[self.counter]
        self.cand_being_evaluated = self.ca_list[self.counter]
        self.reftxt["text"] = self.ref_being_evaluated
        self.candtxt["text"] = self.cand_being_evaluated
        internal_bleu_score = sentence_bleu(list(self.ref_being_evaluated), list(self.cand_being_evaluated), weights=(1, 0, 0, 0))
        self.bleu_lbl["text"] = 'standard bleu score: ' + str(internal_bleu_score)
        internalDictOutput = dictOutput = structure_evaluation(self.nlp(self.ref_being_evaluated),self.nlp(self.cand_being_evaluated), internal_bleu_score)
        self.gross_lbl["text"] = 'Structure sensitive Bleu score: ' + str(internalDictOutput['grs'])
        self.corr_lbl["text"] = f'Correctly placed POS tags:' + str(internalDictOutput['correctly placed tags'])
        self.compare_lbl["text"] = f'Number of correctly placed tags: {compare_POS(self.nlp(self.ref_being_evaluated), self.nlp(self.cand_being_evaluated))}'
        self.counter+=1
        
        # self.c+=1 
        # print(self.c)
        # reftxt = re_list[self.c]
        # candtxt = ca_list[self.c]
        # self.subject.config(text=reftxt)
        # self.message.config(text=candtxt)
            
        
        
            
root = Tk()
root.geometry('300x200')
window = Window(root)

root.mainloop()  
