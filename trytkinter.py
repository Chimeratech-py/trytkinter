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
from threading import Thread

def slicePersonal(li):
    if len(li) > 4:
        firstLi = li[0:4]
        secondLi = li[4:]
        
        return str(firstLi) + " \n" + str(secondLi)
    else:
        return str(li)

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
    
    #referencePOSlist = ['DET', 'VERB', 'DET', 'NOUN', 'ADP']
    #candidatePOSlist = ['DET', 'DET', 'NOUN', 'VERB', 'ADP']
    
    #2 out 5 matching
    
    returnDictionary = {'grs': 0,'correctly placed tags': []}
    
    #counter is for looping
    #correctcounter counts the number of correctly placed tags
    counter = 0
    correctcounter = 0
    candidateLength = len(candidatePOSlist)
        
    #if-else statement logic: Count the number of correctly 
    # placed tags by incrementing correctcounter variable everytime a matching POS tag is found across the candidate text and reference text
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
            
    #Calculating the final score. Mistakes is calculated by subtracting the correctcounter from the length of the candidate text
    mistakes = candidateLength - correctcounter
    #partial is calculated by bleu score divided by the candidate length
    partial = netscore/candidateLength
    #deduction is calculated by mistakes times the partial
    deduction = mistakes*partial
    #grossscore is the final score, which is the bleu score minus the deduction  
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
        
        def vocab_clicked(func,samplesize):
            Thread(target=run_vocab_thread,args=(func,samplesize)).start()
        def onmtVocab(samplesize):
            os.chdir('Collab files')
            os.system(r'onmt_build_vocab -config en_tl.yaml -n_sample ' + str(samplesize))
            # textwidget.configure(state='normal')
            # with open('vocabInfo.txt','r') as file:
            #     t = file.read()
            
            # time.sleep(5)
            # textwidget.insert(tk.INSERT, t)
            
            # textwidget.configure(state='disabled')
            
            # os.chdir('Collab files')
            # returned_value = os.system(r'cmd /k onmt_build_vocab -config en_tl.yaml -n_sample 10000')
            # print('returned value: ', returned_value)
            
        def run_vocab_thread(func,samplesize):
            popup = tk.Toplevel()
            tk.Label(popup, text="Building the vocabulary").grid(row=0,column=0)

            processing_bar = ttk.Progressbar(popup, orient='horizontal', mode='indeterminate')
            processing_bar.grid(row=1,column=0)
            
            processing_bar.start(interval=10)
            print('vocab', 'started')
            func(samplesize)
            processing_bar.stop()
            print('vocab', 'stopped')
            
            popup.destroy()
        
        def onmtTrain():            
            try:
                #ensure_command()
                os.system(r'onmt_train -config en_tl.yaml 1>opennmt.log 2>&1')
            except AttributeError:
                tk.messagebox.showerror("Attribute error",  "Incompatible system requirements")
            ##returned_value = os.system(r'cmd /k onmt_train -config en_tl.yaml')
            ##print('returned value: ', returned_value)
        
        def train_clicked(func):
            Thread(target=run_train_thread,args=[func]).start()
        
        def run_train_thread(func):
            popup = tk.Toplevel()
            tk.Label(popup, text="Training data").grid(row=0,column=0)

            processing_bar = ttk.Progressbar(popup, orient='horizontal', mode='indeterminate')
            processing_bar.grid(row=1,column=0)
            
            processing_bar.start(interval=10)
            print('train', 'started')
            func()
            processing_bar.stop()
            print('train', 'stopped')
            
            popup.destroy()
        
        self.modelPtFile = None
        self.origTlFile = None
        
        def updTrans(textwidget):
            tk.messagebox.showinfo("Upload file",  "Select a model pytorch file")
            modelDir = fd.askopenfilename(filetypes=[("Pytorch files", "*.pt")])
            self.modelPtFile = os.path.split(modelDir)[1]
            
            tk.messagebox.showinfo("Upload file",  "Select a text file written in Tagalog")
            origDir = fd.askopenfilename(filetypes=[("Tagalog text files", "*.tl")])
            self.origTlFile = os.path.split(origDir)[1]
            
            with open(self.origTlFile,'r') as file:
                origLines = file.read()
            
            textwidget.configure(state='normal')
            textwidget.delete('1.0',tk.END)
            textwidget.insert(tk.INSERT, origLines)
            textwidget.configure(state='disabled')
            
            if self.modelPtFile and self.origTlFile:
                self.btn_translate["state"] = tk.NORMAL
            
        def onmtTranslate(pytorchFile,tlFile,outputFilename):
            os.system(r'onmt_translate -model ' + pytorchFile + ' -src ' + tlFile + ' -output ' + outputFilename + '.txt -verbose')
            
        def run_translate_thread(name, func,pytorchFile,tlFile,outputFilename):
            popup = tk.Toplevel()
            tk.Label(popup, text="File being translated").grid(row=0,column=0)

            processing_bar = ttk.Progressbar(popup, orient='horizontal', mode='indeterminate')
            processing_bar.grid(row=1,column=0)
            
            processing_bar.start(interval=10)
            print(name, 'started')
            func(pytorchFile,tlFile,outputFilename)
            processing_bar.stop()
            print(name, 'stopped')
            
            popup.destroy()
            
            with open(outputFilename + '.txt','r') as file:
                transLines = file.read()
                
            transLines = transLines.replace('<unk>', 'unknown')
            
            with open(outputFilename + '.txt','w') as file:
                file.write(transLines)
                
            self.translated_text_area.configure(state='normal')
            self.translated_text_area.delete('1.0',tk.END)
            self.translated_text_area.insert(tk.INSERT, transLines)
            self.translated_text_area.configure(state='disabled')
            
        def run_thread(name, func,pytorchFile,tlFile,outputFilename):
            Thread(target=run_translate_thread, args=(name, func,pytorchFile,tlFile,outputFilename)).start()
            
        def translate_clicked(textwidget,pytorchFile,tlFile):          
            outputFilename = AS('File name', 'What would you like to name your output file?')  
            
            outputFilename = outputFilename.replace(' ','-')
            if outputFilename == '':
                tk.messagebox.showerror("No name entered",  "No name entered. Please try again.")
            else:
                
                run_thread('translate', onmtTranslate, pytorchFile,tlFile,outputFilename)
                
            
            #os.system(r'onmt_translate -model ' + pytorchFile + ' -src ' + tlFile + ' -output ' + outputFilename + '.txt -verbose')
                
            
        
        self.button_tab1_Fr = tk.Frame(self.tab1)
        self.button_tab1_Fr.grid(row=2,column=1, pady=20,sticky=tk.E)
        
        self.btn_upload_tab1 = ttk.Button(self.button_tab1_Fr, text = "Upload", command=lambda:updTrans(self.text_area))
        self.btn_upload_tab1.grid(row=0,column=2)
        self.btn_translate = ttk.Button(self.button_tab1_Fr, text="Translate", command=lambda: translate_clicked(self.translated_text_area,self.modelPtFile,self.origTlFile))
        self.btn_translate.grid(row=0,column=3)
        self.btn_translate["state"] = tk.DISABLED
        
        # self.btn_vocab = ttk.Button(self.button_tab1_Fr,text="Build Vocab",command=lambda: vocab_clicked(onmtVocab,10000))
        # self.btn_vocab.grid(row = 0, column= 0)
        
        # self.btn_train = ttk.Button(self.button_tab1_Fr, text="Train", command=lambda: train_clicked(onmtTrain))
        # self.btn_train.grid(row=0, column = 1)
        
        def ensure_command():
            time.sleep(99999)
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
        
        standardtab2LabelFont = 'Times New Roman',11
        self.linesLbl = ttk.Label(self.logFr, text = 'Line ? of ?', font=standardtab2LabelFont)
        self.linesLbl.grid(row = 0, column = 0, sticky=tk.W)
        self.bleu_lbl = ttk.Label(self.logFr, text = 'Standard bleu score: ', font=standardtab2LabelFont)
        self.bleu_lbl.grid(row = 1, column = 0, sticky=tk.W)
        self.avgBleu_lbl = ttk.Label(self.logFr, text = 'Average bleu score so far: ', font=standardtab2LabelFont)
        self.avgBleu_lbl.grid(row = 2, column=0,sticky=tk.W)
        self.gross_lbl = ttk.Label(self.logFr, text = 'Structure sensitive Bleu score: ', font=standardtab2LabelFont)
        self.gross_lbl.grid(row = 3, column = 0, sticky=tk.W)
        self.avgStruct_lbl = ttk.Label(self.logFr,text = 'Average Structure sensitive Bleu score so far: ', font=standardtab2LabelFont)
        self.avgStruct_lbl.grid(row=4,column=0,sticky=tk.W)
        self.corr_lbl = ttk.Label(self.logFr, text = f'Correctly placed POS tags:', font=standardtab2LabelFont)
        self.corr_lbl.grid(row = 5, column= 0, sticky=tk.W )
        self.compare_lbl = ttk.Label(self.logFr, text = f'Number of correctly placed tags:', font=standardtab2LabelFont)
        self.compare_lbl.grid(row = 6, column =0, sticky=tk.W)
        
        
        
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
        
        self.refFileName = ''
        self.candFileName = ''
        
        self.xCoord = []
        self.xCoordCounter = 1
        self.bleuY = []
        self.grossY = []
        
        self.candLineList = []
        self.correctlyPlacedPOSY = []
        
        def Upload(textwidgets):
            self.refLineList = []
            self.xCoord = []
            self.xCoordCounter = 1
            self.bleuY = []
            self.grossY = []
            self.candLineList = []
            self.lineCounter = 1
            
            tk.messagebox.showinfo("Upload file",  "Select a reference text file")
            
            refDir = fd.askopenfilename(filetypes=[("Text files", "*.txt")])
            self.refFileName = os.path.split(refDir)[1]
            
            with open(self.refFileName, 'r') as reFileLines:
                c = 0
                for line in reFileLines:
                    self.refLineList.append(line)
                    c+=1
                self.numOfLines = c
                    
            textwidgets[0].configure(state='normal')
            textwidgets[0].delete("1.0","end")
            refPOS = str(getPOS(self.nlp(self.refLineList[0])))
            textwidgets[0].insert(tk.INSERT,self.refLineList[0] + "\n " + refPOS)
            textwidgets[0].configure(state='disabled')
            
            tk.messagebox.showinfo("Upload file",  "Select a candidate text file")
            
            candDir = fd.askopenfilename(filetypes=[("Text files", "*.txt")])
            self.candFileName = os.path.split(candDir)[1]
            
            with open(self.candFileName,'r') as candFileLines:
                for line in candFileLines:
                    self.candLineList.append(line)

            textwidgets[1].configure(state='normal')
            textwidgets[1].delete("1.0","end")
            candPOS = str(getPOS(self.nlp(self.candLineList[0])))
            textwidgets[1].insert(tk.INSERT,self.candLineList[0] + "\n " + candPOS)
            textwidgets[1].configure(state='disabled')
            
            counterLocal = 0
            while counterLocal < len(self.refLineList):
                bleuSc = sentence_bleu(list(self.refLineList[counterLocal]),list(self.candLineList[counterLocal]), weights=(1,0,0,0))
                self.bleuY.append(bleuSc)
                grossSc = structure_evaluation(self.nlp(self.refLineList[counterLocal]),self.nlp(self.candLineList[counterLocal]),bleuSc)
                self.grossY.append(grossSc['grs'])
                self.correctlyPlacedPOSY.append(grossSc['correctly placed tags'])
                self.xCoord.append(self.xCoordCounter)
                self.xCoordCounter+=1
                counterLocal+=1
            
            format_bleuSc = "{:.2f}".format(self.bleuY[0])
            format_grossSc = "{:.2f}".format(self.grossY[0])
            
            correctlyPOSstr = slicePersonal(self.correctlyPlacedPOSY[0])                                                        

            updateEvalLabels(1,str(self.numOfLines),str(format_bleuSc),str(format_bleuSc),str(format_grossSc),str(format_grossSc),correctlyPOSstr,compare_POS(self.nlp(self.refLineList[0]),self.nlp(self.candLineList[0])))
            self.evalBtn["state"] = tk.NORMAL
            self.lastBtn["state"] = tk.NORMAL
            self.prevBtn["state"] = tk.NORMAL
            
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
        
        def prevEval():
            try:
                self.lineCounter-=1
                self.counter-=1
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
                
                format_bleuSc = "{:.2f}".format(self.bleuY[self.counter])
                avgBleu = "{:.2f}".format(sum(self.bleuY[:self.lineCounter])/self.lineCounter) 
                
                format_grossSc = "{:.2f}".format(self.grossY[self.counter])
                avgStructBleu = "{:.2f}".format(sum(self.grossY[:self.lineCounter])/self.lineCounter)
               
                correctlyPOSstr = slicePersonal(self.correctlyPlacedPOSY[self.counter])
               
                
                updateEvalLabels(str(self.lineCounter),str(self.numOfLines),str(format_bleuSc),str(avgBleu),str(format_grossSc),str(avgStructBleu),correctlyPOSstr,compare_POS(self.nlp(self.refLineList[self.counter]),self.nlp(self.candLineList[self.counter])))
                showGraph()
                
            except IndexError:
                self.calTextarea.configure(state='normal')
                self.calTextarea.delete('1.0',tk.END)
                self.calTextarea.configure(state='disable')
                tk.messagebox.showinfo("information",  "Reached end of text file")
                
        self.prevBtn = ttk.Button(self.buttonFr, text = "Previous", command=lambda: prevEval())
        self.prevBtn["state"] = tk.DISABLED
        self.prevBtn.grid(row=1,column = 0)
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
                
                format_bleuSc = "{:.2f}".format(self.bleuY[self.counter])
                avgBleu = "{:.2f}".format(sum(self.bleuY[:self.lineCounter])/self.lineCounter) 
                
                format_grossSc = "{:.2f}".format(self.grossY[self.counter])
                avgStructBleu = "{:.2f}".format(sum(self.grossY[:self.lineCounter])/self.lineCounter)
               
                correctlyPOSstr = slicePersonal(self.correctlyPlacedPOSY[self.counter])
               
                
                updateEvalLabels(str(self.lineCounter),str(self.numOfLines),str(format_bleuSc),str(avgBleu),str(format_grossSc),str(avgStructBleu),correctlyPOSstr,compare_POS(self.nlp(self.refLineList[self.counter]),self.nlp(self.candLineList[self.counter])))
                showGraph()
            except IndexError:
                self.calTextarea.configure(state='normal')
                self.calTextarea.delete('1.0',tk.END)
                self.calTextarea.configure(state='disable')
                tk.messagebox.showinfo("information",  "Reached end of text file")
        
            
        self.evalBtn = ttk.Button(self.buttonFr, text = "Next", command=lambda: nextEval())
        self.evalBtn["state"] = tk.DISABLED
        self.evalBtn.grid(row=2,column = 0)
        
        
        def skipLines():
            try:
                lineCounter = 0
                bleuScoresList = []
                structBleuScoresList = []
                
                AvgBleu = 0
                AvgStructBleu = 0
                
                for i in range(len(self.refLineList)):
                    bleuSc = sentence_bleu(list(self.refLineList[lineCounter]), list(self.candLineList[lineCounter]), weights=(1, 0, 0, 0))
                    bleuScoresList.append(bleuSc)
                    grossSc = structure_evaluation(self.nlp(self.refLineList[lineCounter]), self.nlp(self.candLineList[lineCounter]),bleuSc)
                    structBleuScoresList.append(grossSc['grs'])
                    
                    lineCounter+=1
                
                AvgBleu = sum(bleuScoresList)/len(bleuScoresList)
                AvgBleu = "{:.2f}".format(AvgBleu)
                AvgStructBleu = sum(structBleuScoresList)/len(structBleuScoresList)
                AvgStructBleu = "{:.2f}".format(AvgStructBleu)
                
                tk.messagebox.showinfo("Averages",  f"Bleu: {AvgBleu} \nStructure Sensitive Bleu: {AvgStructBleu}")
            except FileNotFoundError:
                tk.messagebox.showerror("Error","No files uploaded")             
            
        #self.skipBtn = ttk.Button(self.buttonFr, text = "Show average", command=lambda: skipLines())
        #self.skipBtn.grid(row=2,column=0)
        
        def skipToLast():
            self.lineCounter = len(self.refLineList)
            self.counter = self.lineCounter - 1
            #Should counter also update?       
            self.refTextarea.configure(state='normal')
            self.refTextarea.delete('1.0',tk.END)
            refPOS = str(getPOS(self.nlp(self.refLineList[-1])))
            self.refTextarea.insert(tk.INSERT,self.refLineList[-1] + "\n" + refPOS)
            self.refTextarea.configure(state='disable')
            
            self.calTextarea.configure(state='normal')
            self.calTextarea.delete('1.0',tk.END)
            candPOS = str(getPOS(self.nlp(self.candLineList[-1])))
            self.calTextarea.insert(tk.INSERT,self.candLineList[-1] + "\n" + candPOS)
            self.calTextarea.configure(state='disabled')
            
            bleuSc = sentence_bleu(list(self.refLineList[-1]), list(self.candLineList[-1]), weights=(1, 0, 0, 0))
            format_bleuSc = "{:.2f}".format(bleuSc)
            
            avgBleu = "{:.2f}".format(sum(self.bleuY)/len(self.bleuY)) 
                
            grossSc = structure_evaluation(self.nlp(self.refLineList[-1]), self.nlp(self.candLineList[-1]),bleuSc)
            format_grossSc = "{:.2f}".format(grossSc['grs'])
            
            
            avgStructBleu = "{:.2f}".format(sum(self.grossY)/len(self.grossY))
            
                
            correctlyPOSstr = slicePersonal(grossSc['correctly placed tags'])
        
            updateEvalLabels(str(self.numOfLines),str(self.numOfLines),str(format_bleuSc),str(avgBleu),str(format_grossSc),str(avgStructBleu),correctlyPOSstr,compare_POS(self.nlp(self.refLineList[-1]),self.nlp(self.candLineList[-1])))
            showGraph()
        
        self.lastBtn = ttk.Button(self.buttonFr, text="Skip to Last", command = lambda: skipToLast())
        self.lastBtn["state"] = tk.DISABLED
        self.lastBtn.grid(row=3,column=0)
        
            
        ##self.reftxt = ttk.Label(self.tab2, text = self.ref_being_evaluated)
        ##self.reftxt.place(relx=0.5, rely=0.5,anchor='center')
        
        def updateEvalLabels(line_number,total_lines,std_bleu_score,avg_std_bleu,struct_bleu_score,avg_struct_bleu,correct_lbls,compared_lbls):
            self.linesLbl["text"] = f"Line {line_number} of {total_lines}"
            self.bleu_lbl["text"] = f"Standard bleu score: {std_bleu_score}"
            self.avgBleu_lbl["text"] = f"Average bleu score so far: {avg_std_bleu}"
            self.gross_lbl["text"] = f"Structure sensitive Bleu score: {struct_bleu_score}"
            self.avgStruct_lbl["text"] = f"Average Structure sensitive Bleu score so far: {avg_struct_bleu}"
            self.corr_lbl["text"] = f"Correctly placed POS tags: {correct_lbls}"
            self.compare_lbl["text"] = f"Number of correctly placed tags: {compared_lbls}"
            
        
        def showGraph():
            f = Figure(figsize=(3,3),dpi=85)
            a = f.add_subplot(111)
            a.plot(self.xCoord[:self.lineCounter], self.bleuY[:self.lineCounter], label = "bleu Score")
            a.plot(self.xCoord[:self.lineCounter], self.grossY[:self.lineCounter], label = "SS Bleu Score")
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
        
        remindLbl = ttk.Label(self.tab3, text = 'Reminder: Make sure that a translated text file and reference text file are both already present', font = standardtab3LblFont)
        remindLbl.grid(row = 0, column = 0, sticky=tk.W)
        
        remindLbl2 = ttk.Label(self.tab3, text = ' before proceeding to the evaluation phase', font = standardtab3LblFont)
        remindLbl2.grid(row = 1, column = 0, sticky=tk.W)
        
        transInstructionLbl = ttk.Label(self.tab3, text = 'Translation phase', font = standardtab3LblFont)
        transInstructionLbl.grid(row = 2, column = 0, sticky=tk.W)
        
        step1Lbl = ttk.Label(self.tab3, text = 'Step 1: Click the translate button', font = standardtab3LblFont)
        step1Lbl.grid(row = 3, column = 0, sticky=tk.W)
        
        step2Lbl = ttk.Label(self.tab3, text = 'Step 2: You will be prompted to select a model. Only .pt (PyTorch) files are accepted', font = standardtab3LblFont)
        step2Lbl.grid(row = 4, column = 0, sticky=tk.W)
        
        step3Lbl = ttk.Label(self.tab3, text = 'Step 3: Next, select an input text file. The file should be in Filipino language. Only .txt files are accepted', font = standardtab3LblFont)
        step3Lbl.grid(row = 5, column = 0, sticky=tk.W)
        
        step4Lbl = ttk.Label(self.tab3, text = 'Step 4: Enter the name of the output file', font = standardtab3LblFont)
        step4Lbl.grid(row = 6, column = 0, sticky=tk.W)
        
        spaceLbl = ttk.Label(self.tab3, text = ' ')
        spaceLbl.grid(row = 7, column = 0, sticky = tk.W)
        
        evalInstructionLbl = ttk.Label(self.tab3, text = 'Evaluation phase', font = standardtab3LblFont)
        evalInstructionLbl.grid(row = 8, column = 0, sticky = tk.W)
        
        stepE1Lbl = ttk.Label(self.tab3, text = 'Step 1: Click the upload button', font = standardtab3LblFont)
        stepE1Lbl.grid(row = 9, column = 0, sticky = tk.W)
        
        stepE2Lbl = ttk.Label(self.tab3, text = 'Step 2: Select the reference text file. Only .txt files are accepted', font = standardtab3LblFont)
        stepE2Lbl.grid(row = 10, column = 0, sticky = tk.W)
        
        stepE3Lbl = ttk.Label(self.tab3, text = 'Step 3: Select the candidate text file. Only .txt files are accepted', font = standardtab3LblFont)
        stepE3Lbl.grid(row = 11, column = 0, sticky = tk.W)
        
        stepE4Lbl = ttk.Label(self.tab3, text = 'Step 4: The scores along with other information are now displayed. Click the next button to \nevaluate the next line until the end of the text file', font = standardtab3LblFont)
        stepE4Lbl.grid(row = 12, column = 0, sticky = tk.W)
        
        ##4th tab
        ##POS tags list
        
        self.tab4 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab4, text="POS labels")
        
        self.posLabelFr = tk.Frame(self.tab4)
        self.posLabelFr.grid(row=0,column=0,padx=20,pady=20)
        
        posHeaderLbl = ttk.Label(self.posLabelFr, text = 'POS', font = standardtab3LblFont)
        posHeaderLbl.grid(row = 0, column = 0)
        
        descHeaderLbl = ttk.Label(self.posLabelFr,text = 'DESCRIPTION', font = standardtab3LblFont)
        descHeaderLbl.grid(row=0,column=1)
        
        exHeaderLbl = ttk.Label(self.posLabelFr,text = 'EXAMPLES', font = standardtab3LblFont)
        exHeaderLbl.grid(row=0,column=2)
        
        tags_list = ['ADJ','ADP','ADV','AUX','CONJ','CCONJ','DET','INTJ','NOUN','NUM','PART','PRON','PROPN','PUNCT','SCONJ','SYM','VERB','X','SPACE']
        desc_list = ['adjective','adposition','adverb','auxiliary','conjunction','coordinating conjunction','determiner','interjection','noun','numeral','particle','pronoun','proper noun','punctuation','subordinating conjunction','symbol','verb','other','space']
        examples_list = ['*big, old, green','*in, to, during*','*very, where, there*'
                         ,'	*is, has (done), will (do), should (do)*','	*and, or, but*','*and, or, but*','*a, an, the*','*psst, ouch, bravo, hello*','	*girl, cat, tree, air, beauty*','*1, 2017, one, seventy-seven, IV, MMXIV*'
                         ,'*’s, not,*','	*I, you, he, she, myself, themselves, somebody*','	*Mary, John, London, NATO, HBO*','	*., (, ), ?*','*if, while, that*','*$, %, §, ©, +, −*','	*run, runs, running, eat, ate, eating*'
                         ,'*sfpksdpsxmsa*',''
                         ]

        tags_rows = []
        desc_rows = []
        examples_rows = []
        
        tags_counter=0
        tags_rowcount=1
        for i in tags_list:
            tags_rows.append(ttk.Label(self.posLabelFr, text=i, font = standardtab3LblFont))
            tags_rows[tags_counter].grid(row=tags_rowcount,column=0)
            tags_counter+=1
            tags_rowcount+=1
            
        desc_counter=0
        desc_rowcount=1
        for i in desc_list:
            desc_rows.append(ttk.Label(self.posLabelFr, text=i, font = standardtab3LblFont))
            desc_rows[desc_counter].grid(row=desc_rowcount,column=1)
            desc_counter+=1
            desc_rowcount+=1
            
        examples_counter=0
        examples_rowcount=1
        for i in examples_list:
            examples_rows.append(ttk.Label(self.posLabelFr, text=i, font = standardtab3LblFont))
            examples_rows[examples_counter].grid(row=examples_rowcount,column=2)
            examples_counter+=1
            examples_rowcount+=1
            
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
