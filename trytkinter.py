import tkinter as tk
from tkinter import ttk
from unittest import skip
from weakref import ref
from nltk.translate.bleu_score import sentence_bleu
import spacy
import tkinter.scrolledtext as st
import os
import subprocess
import time
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy
from tkinter.simpledialog import askstring as AS

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
    



# class fr2(tk.Frame):
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
        self.reftxt.place(relx=0.5, rely=0.5,anchor='center')
        subframe.pack(expand = True, fill = BOTH, side=LEFT)
        
        
        
        
        
       
        subframe2 = ttk.Frame(master, background="red")
        self.candlbl = ttk.Label(subframe2, text="Candidate Text")
        self.candlbl.place(relx=0.5,anchor=N)
        self.candtxt = ttk.Label(subframe2, text= self.cand_being_evaluated)
        self.candtxt.place(relx=0.5, rely=0.5,anchor=CENTER) 
        
        bleuscore = sentence_bleu(list(self.ref_being_evaluated), list(self.cand_being_evaluated), weights=(1, 0, 0, 0))
        
        dictOutput = structure_evaluation(self.nlp(self.ref_being_evaluated),self.nlp(self.cand_being_evaluated), bleuscore)
        
        self.bleu_lbl = ttk.Label(subframe2, text = 'standard bleu score: ' + str(bleuscore))
        self.bleu_lbl.place(relx=0.5, rely=0.6,anchor=CENTER)
        self.gross_lbl = ttk.Label(subframe2, text = 'Structure sensitive Bleu score: ' + str(dictOutput['grs']))
        self.gross_lbl.place(relx=0.5, rely=0.7, anchor = CENTER)
        self.corr_lbl = ttk.Label(subframe2, text = f'Correctly placed POS tags:' +  str(dictOutput['correctly placed tags']))
        self.corr_lbl.place(relx=0.5, rely=0.8, anchor = CENTER)
        self.compare_lbl = ttk.Label(subframe2, text = f'Number of correctly placed tags: {compare_POS(self.nlp(self.ref_being_evaluated), self.nlp(self.cand_being_evaluated))}')
        self.compare_lbl.place(relx=0.5, rely=0.9, anchor = CENTER)
        subframe2.pack(expand=True, fill=BOTH, side=LEFT)
        
        self.btn_next = ttk.Button(subframe,text="Next",command =self.updateTexts)
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
            
class Display:
    def __init__(self):
        self.root = tk.Tk()
        
        self.root.geometry('900x600')
        self.root.resizable(False,False)
        self.root.title("Structure Sensitive BLEU")
        
        self.tabControl = ttk.Notebook(self.root)
        
        
        ##1ST TAB
        ##TRANSLATION 
        ##STAGE
        
        self.tab1 = ttk.Frame(self.tabControl)
        
        #self.tab1.columnconfigure(0, weight=1)
        #self.tab1.columnconfigure(1, weight=2)
        
        self.tabControl.add(self.tab1, text="Translation")
        
        self.tab1origLbl = ttk.Label(self.tab1, text = "Original Text")
        self.tab1origLbl.grid(row=0,column=0, padx=20, pady=20)
        
        self.tab2transLbl = ttk.Label(self.tab1, text = "Translated Text")
        self.tab2transLbl.grid(row=0,column=1)
        
        self.text_area = st.ScrolledText(self.tab1,
                            width = 50, 
                            height = 24, 
                            font = ("Times New Roman",
                                    12))
        # self.text_area.grid(row = 0, column = 0, rowspan= 3)
        self.text_area.grid(row = 1, column = 0, padx=20)
        self.text_area.configure(state ='disabled')
        
        self.translated_text_area = st.ScrolledText(self.tab1, width = 50, height = 24, font = ("Times New Roman", 12))
        self.translated_text_area.grid(row = 1, column = 1)
        self.translated_text_area.configure(state='disabled')
        
        def buildVocab(textwidget):
            textwidget.configure(state='normal')
            with open('vocabInfo.txt','r') as file:
                t = file.read()
            
            time.sleep(5)
            textwidget.insert(tk.INSERT, t)
            
            textwidget.configure(state='disabled')
            
            # os.chdir('Collab files')
            # returned_value = os.system(r'cmd /k onmt_build_vocab -config en_tl.yaml -n_sample 10000')
            # print('returned value: ', returned_value)
            
        # self.btn_vocab = ttk.Button(self.tab1,text="Build Vocab",command=lambda: buildVocab(self.text_area))
        # self.btn_vocab.grid(row = 0, column= 1)
        
        def onmtTrain(textwidget):
            textwidget.configure(state='normal')
            beginProcessWindow = tk.Toplevel(self.tab2)
            beginProcessWindow.geometry("750x250")
            beginProcessWindow.title("Process")
            tk.Label(beginProcessWindow, text = "Beginning process...", font=('Times New Roman',15)).place(x=150,y=80)
            self.root.after(5000, beginProcessWindow.destroy)
            
            textwidget.delete('1.0',tk.END)
            textwidget.insert(tk.INSERT, 'training successful')
            textwidget.configure(state='disabled')
            ##returned_value = os.system(r'cmd /k onmt_train -config en_tl.yaml')
            ##print('returned value: ', returned_value)
        
        # self.btn_train = ttk.Button(self.tab1, text="Train", command=lambda: onmtTrain(self.text_area))
        # self.btn_train.grid(row=1, column = 1)
        
        def onmtTranslate(textwidget, secondtextwidget):
            tk.messagebox.showinfo("",  "Select a model pytorch file")
            modelDir = fd.askopenfilename()
            modelPt = os.path.split(modelDir)[1]
            
            tk.messagebox.showinfo("",  "Select a text file written in Tagalog")
            origDir = fd.askopenfilename()
            origTl = os.path.split(origDir)[1]
                      
            outputFilename = AS('File name', 'What would you like to name your output file?')  
            sysCmd = os.system(r'onmt_translate -model ' + modelPt + ' -src ' + origTl + ' -output ' + outputFilename + '.txt -verbose')
            
            with open(origTl,'r') as file:
                origLines = file.read()
                
            with open('candOut.txt','r') as file:
                transLines = file.read()
                
            textwidget.configure(state='normal')
            textwidget.delete('1.0',tk.END)
            textwidget.insert(tk.INSERT, origLines)
            textwidget.configure(state='disabled')
            
            secondtextwidget.configure(state='normal')
            secondtextwidget.delete('1.0',tk.END)
            secondtextwidget.insert(tk.INSERT, transLines)
            secondtextwidget.configure(state='disabled')
            
        self.btn_translate = ttk.Button(self.tab1, text="Translate", command=lambda:onmtTranslate(self.text_area,self.translated_text_area))
        self.btn_translate.grid(row=2, column = 1, pady=20,sticky=tk.E)
        
        ##2ND TAB
        ##FOR EVALUATION
        ##STAGE
        ##
        ##
        ##
        
        
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2, text="Evaluation")
        
        self.nlp = spacy.load('en_core_web_sm')
        
        self.tab2.columnconfigure(0, weight = 2)
        self.tab2.columnconfigure(1, weight = 2)
        self.tab2.columnconfigure(2, weight = 1)
        
        
            
        #graph
        # self.f = Figure(figsize=(3,3),dpi=85)
        
        # a = self.f.add_subplot(111)
        # a.plot([1,2,3,4,5],[0.89,0.56,0.56,0.22,0.17],label="bleu Score")
        # a.plot([1,2,3,4,5],[0.1,0.56,0.43,0.16,0.1],label = "gross Score")
        # a.legend()
        # canvas = FigureCanvasTkAgg(self.f,self.tab2)
        # canvas.draw()
        # canvas.get_tk_widget().grid(row=0,column = 1)
        
        ##labels
        
        #self.origLbl = ttk.Label(self.tab2, text = "Original Text")
        #self.origLbl.grid(row=1,column=0)
        
        self.reflbl = ttk.Label(self.tab2, text = "Reference Text")
        self.reflbl.grid(row=1,column=0)
        
        self.caLbl = ttk.Label(self.tab2, text = "Candidate Text")
        self.caLbl.grid(row=1, column=1)
        
        ##text areas
        #self.origTextarea = st.ScrolledText(self.tab2, width = 20, height = 10, font = ("Times New Roman", 12))
        #self.origTextarea.grid(row = 2, column = 0, rowspan=4)
        
        self.refTextarea = st.ScrolledText(self.tab2, font = ("Times New Roman",7))
        self.refTextarea.grid(row=2,column=0, rowspan=4)
        
        self.calTextarea = st.ScrolledText(self.tab2, font = ("Times New Roman",7))
        self.calTextarea.grid(row=2,column=1, rowspan=4)
        
        self.logFr = tk.Frame(self.tab2, height = 317, width = 580)
        self.logFr.grid(row=0, column = 0, sticky=tk.W)
        ##eval data labels
        self.numOfLines = 0
        self.lineCounter = 1
        
        standardtab2LabelFont = 'Times New Roman',14
        self.linesLbl = ttk.Label(self.logFr, text = 'line ? of ?', font=standardtab2LabelFont)
        self.linesLbl.grid(row = 0, column = 0, sticky=tk.W)
        self.bleu_lbl = ttk.Label(self.logFr, text = 'standard bleu score: ', font=standardtab2LabelFont)
        self.bleu_lbl.grid(row = 1, column = 0, sticky=tk.W)
        self.gross_lbl = ttk.Label(self.logFr, text = 'Structure sensitive Bleu score: ', font=standardtab2LabelFont)
        self.gross_lbl.grid(row = 2, column = 0, sticky=tk.W)
        self.corr_lbl = ttk.Label(self.logFr, text = f'Correctly placed POS tags:', font=standardtab2LabelFont)
        self.corr_lbl.grid(row = 3, column= 0, sticky=tk.W )
        self.compare_lbl = ttk.Label(self.logFr, text = f'Number of correctly placed tags:', font=standardtab2LabelFont)
        self.compare_lbl.grid(row = 4, column =0, sticky=tk.W)
        
        
        
        ##button frame
        self.buttonFr = tk.Frame(self.tab2)
        self.buttonFr.grid(row=1,column=2,rowspan=5,sticky=tk.W)
        
        
        
        
        ##choose text file buttons
        self.origLineList = []
        def chooseOrigText(textwidget):
            origDir = fd.askopenfilename()
            origFileName = os.path.split(origDir)[1]
            
            with open(origFileName,'r') as origFileLines:
                for line in origFileLines:
                    self.origLineList.append(line)
                    
            textwidget.configure(state='normal')
            textwidget.insert(tk.INSERT,self.origLineList[0])
            textwidget.configure(state='disabled')
        
        #self.origBtn = ttk.Button(self.tab2, text="Choose Original text file", command=lambda: chooseOrigText(self.origTextarea))
        #self.origBtn.grid(row=6, column = 0)
    
        self.refLineList = []
        def chooseRefText(textwidget):
            refDir = fd.askopenfilename()
            refFileName = os.path.split(refDir)[1]
            
            with open(refFileName, 'r') as reFileLines:
                for line in reFileLines:
                    self.refLineList.append(line)
                    
            textwidget.configure(state='normal')
            textwidget.insert(tk.INSERT,self.refLineList[0])
            textwidget.configure(state='disabled')
        
        # self.refBtn = ttk.Button(self.tab2, text="Choose Reference text file", command=lambda: chooseRefText(self.refTextarea))
        # self.refBtn.grid(row=6, column = 1)
        
        self.xCoord = []
        self.xCoordCounter = 1
        self.bleuY = []
        self.grossY = []
        
        self.candLineList = []
        def Upload(textwidgets):
            tk.messagebox.showinfo("",  "Select a reference text file")
            
            refDir = fd.askopenfilename()
            refFileName = os.path.split(refDir)[1]
            
            with open(refFileName, 'r') as reFileLines:
                c = 0
                for line in reFileLines:
                    self.refLineList.append(line)
                    c+=1
                self.numOfLines = c
                    
            textwidgets[0].configure(state='normal')
            refPOS = str(getPOS(self.nlp(self.refLineList[0])))
            textwidgets[0].insert(tk.INSERT,self.refLineList[0] + "\n " + refPOS)
            textwidgets[0].configure(state='disabled')
            
            tk.messagebox.showinfo("",  "Select a candidate text file")
            
            candDir = fd.askopenfilename()
            candFileName = os.path.split(candDir)[1]
            
            
            
            with open(candFileName,'r') as candFileLines:
                for line in candFileLines:
                    self.candLineList.append(line)

            textwidgets[1].configure(state='normal')
            candPOS = str(getPOS(self.nlp(self.candLineList[0])))
            textwidgets[1].insert(tk.INSERT,self.candLineList[0] + "\n " + candPOS)
            textwidgets[1].configure(state='disabled')
            
            self.linesLbl["text"] = 'line 1 of ' + str(self.numOfLines)
            
            bleuSc = sentence_bleu(list(self.refLineList[0]), list(self.candLineList[0]), weights=(1, 0, 0, 0))
            format_bleuSc = "{:.2f}".format(bleuSc)
            self.bleu_lbl["text"] = 'standard bleu score: ' + str(format_bleuSc)
            self.bleuY.append(bleuSc)
            
            grossSc = structure_evaluation(self.nlp(self.refLineList[0]), self.nlp(self.candLineList[0]),bleuSc)
            format_grossSc = "{:.2f}".format(grossSc['grs'])
            self.gross_lbl["text"] = 'Structure sensitive Bleu score: ' + str(format_grossSc)
            self.grossY.append(grossSc['grs'])
            
            self.xCoord.append(self.xCoordCounter)
            self.xCoordCounter+=1
            
            self.corr_lbl["text"] = f'Correctly placed POS tags:' + str(grossSc['correctly placed tags'])

            self.compare_lbl["text"] = f'Number of correctly placed tags:' + compare_POS(self.nlp(self.refLineList[0]),self.nlp(self.candLineList[0]))

            
            # a = self.f.add_subplot(111)
            # a.plot(self.xCoord, self.bleuY, label = "bleu Score")
            # a.plot(self.xCoord, self.grossY, label = "gross Score")
            # a.legend()
            
        self.candBtn = ttk.Button(self.buttonFr, text="Upload", command=lambda: Upload([self.refTextarea, self.calTextarea]))
        self.candBtn.grid(row=0, column = 0)
        
        
        
        self.counter = 0
        
        ##eval buttons
        
        def update_line(hl, new_data):
            hl.set_xdata(numpy.append(hl.get_xdata(), new_data))
            hl.set_ydata(numpy.append(hl.get_ydata(), new_data))
            plt.draw()
            
        def nextEval():
            try:
                self.lineCounter+=1
                self.counter+=1
                self.refTextarea.configure(state='normal')
                self.refTextarea.delete('1.0',tk.END)
                refPOS = str(getPOS(self.nlp(self.refLineList[self.counter])))
                self.refTextarea.insert(tk.INSERT,self.refLineList[self.counter] + "\n" + refPOS)
                self.refTextarea.configure(state='disable')
                
                self.calTextarea.configure(state='normal')
                self.calTextarea.delete('1.0',tk.END)
                candPOS = str(getPOS(self.nlp(self.candLineList[self.counter])))
                self.calTextarea.insert(tk.INSERT,self.candLineList[self.counter] + "\n" + candPOS)
                self.calTextarea.configure(state='disabled')

                self.linesLbl["text"] = f'line {str(self.lineCounter)} of {str(self.numOfLines)}'  
                bleuSc = sentence_bleu(list(self.refLineList[self.counter]), list(self.candLineList[self.counter]), weights=(1, 0, 0, 0))
                format_bleuSc = "{:.2f}".format(bleuSc)
                self.bleu_lbl["text"] = 'standard bleu score: ' + str(format_bleuSc)
                self.bleuY.append(bleuSc)
                
                grossSc = structure_evaluation(self.nlp(self.refLineList[self.counter]), self.nlp(self.candLineList[self.counter]),bleuSc)
                format_grossSc = "{:.2f}".format(grossSc['grs'])
                self.gross_lbl["text"] = 'Structure sensitive Bleu score: ' + str(format_grossSc)
                self.grossY.append(grossSc['grs'])
                
                self.xCoord.append(self.xCoordCounter)
                self.xCoordCounter+=1
                
                # a = self.f.add_subplot(111)
                # a.plot(self.xCoord, self.bleuY, label = "bleu Score")
                # a.plot(self.xCoord, self.grossY, label = "gross Score")
                # a.legend()
                
                self.corr_lbl["text"] = f'Correctly placed POS tags:' + str(grossSc['correctly placed tags'])

                self.compare_lbl["text"] = f'Number of correctly placed tags:' + compare_POS(self.nlp(self.refLineList[self.counter]),self.nlp(self.candLineList[self.counter]))
                
                showGraph()
            except IndexError:
                self.calTextarea.configure(state='normal')
                self.calTextarea.delete('1.0',tk.END)
                self.calTextarea.configure(state='disable')
                tk.messagebox.showinfo("!",  "Reached end of text file")
        
            
        self.evalBtn = ttk.Button(self.buttonFr, text = "Next", command=lambda: nextEval())
        self.evalBtn.grid(row=1,column = 0)
        
        
        
        
            
        ##self.reftxt = ttk.Label(self.tab2, text = self.ref_being_evaluated)
        ##self.reftxt.place(relx=0.5, rely=0.5,anchor='center')
        
        def showGraph():
            f = Figure(figsize=(3,3),dpi=85)
            a = f.add_subplot(111)
            a.plot(self.xCoord, self.bleuY, label = "bleu Score")
            a.plot(self.xCoord, self.grossY, label = "SS Bleu Score")
            a.legend()
            
            canvas = FigureCanvasTkAgg(f,self.tab2)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0,column = 1)
            
        
        
        self.tabControl.pack(expand=1, fill="both")
        
        
        ##3rd tab
        ##For instructions
        ##
        ##
        ##
        
        self.tab3 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab3, text="Instructions")
        
        standardtab3LblFont = 'Times New Roman', 12
        transInstructionLbl = ttk.Label(self.tab3, text = 'Translation phase', font = standardtab3LblFont)
        transInstructionLbl.grid(row = 0, column = 0, sticky=tk.W)
        
        step1Lbl = ttk.Label(self.tab3, text = 'Step 1: Click the translate button', font = standardtab3LblFont)
        step1Lbl.grid(row = 1, column = 0, sticky=tk.W)
        
        step2Lbl = ttk.Label(self.tab3, text = 'Step 2: You will be prompted to select a model. Only .pt (PyTorch) files are accepted', font = standardtab3LblFont)
        step2Lbl.grid(row = 2, column = 0, sticky=tk.W)
        
        step3Lbl = ttk.Label(self.tab3, text = 'Step 3: Next, select an input text file. The file should be in Filipino language. Only .txt files are accepted', font = standardtab3LblFont)
        step3Lbl.grid(row = 3, column = 0, sticky=tk.W)
        
        step4Lbl = ttk.Label(self.tab3, text = 'Step 4: Enter the name of the output file', font = standardtab3LblFont)
        step4Lbl.grid(row = 4, column = 0, sticky=tk.W)
        
        spaceLbl = ttk.Label(self.tab3, text = ' ')
        spaceLbl.grid(row = 5, column = 0, sticky = tk.W)
        
        evalInstructionLbl = ttk.Label(self.tab3, text = 'Evaluation phase', font = standardtab3LblFont)
        evalInstructionLbl.grid(row = 6, column = 0, sticky = tk.W)
        
        stepE1Lbl = ttk.Label(self.tab3, text = 'Step 1: Click the upload button', font = standardtab3LblFont)
        stepE1Lbl.grid(row = 7, column = 0, sticky = tk.W)
        
        stepE2Lbl = ttk.Label(self.tab3, text = 'Step 2: Select the reference text file. Only .txt files are accepted', font = standardtab3LblFont)
        stepE2Lbl.grid(row = 8, column = 0, sticky = tk.W)
        
        stepE3Lbl = ttk.Label(self.tab3, text = 'Step 3: Select the candidate text file. Only .txt files are accepted', font = standardtab3LblFont)
        stepE3Lbl.grid(row = 9, column = 0, sticky = tk.W)
        
        stepE4Lbl = ttk.Label(self.tab3, text = 'Step 4: The scores along with other information are now displayed. Click the next button to \nevaluate the next line until the end of the text file', font = standardtab3LblFont)
        stepE4Lbl.grid(row = 10, column = 0, sticky = tk.W)
        
        
        
        self.root.mainloop()
        
        
        
        
        
        
            
# root = tk.Tk()
# root.geometry('300x200')
# tabControl = ttk.Notebook(root)

# tab1 = ttk.Frame(tabControl)
# tab2 = ttk.Frame(tabControl)

# tabControl.add(tab1, text ='Tab 1')
# tabControl.add(tab2, text ='Tab 2')
# tabControl.pack(expand = 1, fill ="both")

# ttk.Label(tab1, 
#           text ="Welcome to \
#           GeeksForGeeks").grid(column = 0, 
#                                row = 0,
#                                padx = 30,
#                                pady = 30)  
          
# root.mainloop()  

display = Display()
