# -*- coding: utf-8 -*-
"""
This is a simple project to process data series of the study:
    Effect of Ischemic Preconditioning on Local Oxigenation of Lower Limbs
    Ribeiro, G.G.S., Bresser, M., Deotti, A., Marocolo, M.
    Physiology and Human Performance Research Group - UFJF

    Created on Fri Nov  9 20:12:19 2018
    @author: Antonio Iyda Paganelli antonioiyda@gmail.com
    
    Version 1:  Plain python routines.
    Version 2:  Incorporated a TK graphical interface.
"""

import matplotlib
matplotlib.use("TkAgg")

import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import tkinter as tk

FONT_LARGE  = ("Verdana", 12)
FONT_SIMPLE = ('Verdana','10','bold')

class Conf():
    def __init__(self, filename, rate, iTime, oTime, rTime, number):
        self.filename = filename
        self.rate = rate
        self.iTime = iTime
        self.oTime = oTime
        self.rTime = rTime
        self.number = number
        self.Tserie = np.array([])
        self.Aserie = np.array([])
        self.Oserie = np.array([])
        self.Rserie = np.array([])
        
        self.configured = False
        
    def setSeries(self, Tserie, Aserie, Oserie, Rserie):
        self.Tserie = Tserie
        self.Aserie = Aserie
        self.Oserie = Oserie
        self.Rserie = Rserie
        self.configured = True
        
    def setConfigured(self, value):
        self.configured = value
     
        
class MainWindow(tk.Tk):    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "UFJF - Department of Physiology - @iyda collaboration")
        
        container = tk.Frame(self)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)        

        self.frames = {}
                        
        for F in (StartPage, ReportPage, GraphsPage):
            frame = F(container, self)            
            self.frames[F] = frame            
            frame.grid(row=0, column=0, sticky=tk.NSEW)
        
        self.show_frame(StartPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]        
        frame.tkraise()
        
    def exit(self):
        global app
        app.destroy()
        

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Configuration Page", font=FONT_LARGE)
        label.grid(pady=10, padx=10, row=0, columnspan=4)
        
        tk.Label(self, text="Filename:", font=FONT_SIMPLE).grid(row=1)
        self.Filename = tk.Entry(self, width=30, font=FONT_SIMPLE)
        self.Filename.insert(tk.END, "Tabela de Dados - 3 Min.csv")
        self.Filename.focus_force()
        self.Filename.grid(row=1, column=1)

        tk.Label(self, text="Sampling Rate:", font=FONT_SIMPLE).grid(row=2)
        self.SamplingRate = tk.Entry(self, width=5, font=FONT_SIMPLE, justify=tk.RIGHT)
        self.SamplingRate.insert(tk.END, "12")
        self.SamplingRate.grid(row=2, column=1, sticky=tk.W)
        
        tk.Label(self, text="Initial time (min):", font=FONT_SIMPLE).grid(row=3, column=0)
        self.InitialTime = tk.Entry(self, width=5, font=FONT_SIMPLE, justify=tk.RIGHT)
        self.InitialTime.insert(tk.END, "5")
        self.InitialTime.grid(row=3, column=1, sticky=tk.W)
        
        tk.Label(self, text="Occlusion time (min):", font=FONT_SIMPLE).grid(row=4, column=0)
        self.OcclusionTime = tk.Listbox(self, height=3, justify=tk.RIGHT, 
                                        font=FONT_SIMPLE, selectmode=tk.SINGLE)
        for item in ["3", "5", "7"]:
            self.OcclusionTime.insert(tk.END, item)
        self.OcclusionTime.grid(row=4, column=1, sticky=tk.W)
        
        tk.Label(self, text="Reperfusion time (min):", font=FONT_SIMPLE).grid(row=5, column=0)
        self.ReperfusionTime = tk.Entry(self, width=5, font=FONT_SIMPLE, justify=tk.RIGHT)
        self.ReperfusionTime.insert(tk.END, "5")
        self.ReperfusionTime.grid(row=5, column=1, sticky=tk.W)

        tk.Label(self, text="Number of occlusions:", font=FONT_SIMPLE).grid(row=6, column=0)
        self.NumOcclusions = tk.Entry(self, width=5, font=FONT_SIMPLE, justify=tk.RIGHT)
        self.NumOcclusions.insert(tk.END, "4")
        self.NumOcclusions.grid(row=6, column=1, sticky=tk.W)

        self.status = tk.Label(self, text="None", font=FONT_SIMPLE)
        self.status.grid(row=7, columnspan=2)

        button1 = tk.Button(self, text="Save Configuration", command=self.doSave)
        button1.grid(row=8, column=0)

        button2 = tk.Button(self, text="Run Report", 
                            command=lambda:controller.show_frame(ReportPage))
        button2.grid(row=8, column=1, padx=10, pady=10)
        
        button3 = tk.Button(self, text="Run Graphs", 
                            command=lambda:controller.show_frame(GraphsPage))
        button3.grid(row=8, column=2, padx=10, pady=10)
        
        button4 = tk.Button(self, text="Exit", 
                            command=lambda:controller.exit())
        button4.grid(row=8, column=3, padx=10, pady=10)

    def doSave(self):   
        conf.setConfigured(False)
        conf.filename = self.Filename.get()
        conf.rate = int(self.SamplingRate.get())
        conf.iTime = int(self.InitialTime.get())        
        items = self.OcclusionTime.curselection()
        times = [3,5,7]
        for i in items:
            conf.oTime = times[i]

        conf.rTime = int(self.ReperfusionTime.get())
        conf.number = int(self.NumOcclusions.get())        
        self.status["text"] = "Saved."

        
class ReportPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Report Page", font=FONT_LARGE)
        label.grid(row=0, pady=10, padx=10)
        
        self.TLeft = tk.Text(self, height=20, width=80)
        self.TLeft.grid(row=1, column=0, pady=10, padx=5)
        S = tk.Scrollbar(self, command=self.TLeft.yview)
        S.grid(row=1, column=1)
        self.TLeft['yscrollcommand'] = S.set

        self.TRight = tk.Text(self, height=20, width=80)
        self.TRight.grid(row=1, column=2, pady=10, padx=5)
        S2 = tk.Scrollbar(self, command=self.TRight.yview)
        S2.grid(row=1, column=3)
        self.TLeft['yscrollcommand'] = S2.set

        self.Status = tk.Label(self, text="")
        self.Status.grid(row=2, columnspan=2)

        button1 = tk.Button(self, text="Run", command=self.Run)
        button1.grid(row=3, column=0, padx=10, pady=10)

        button1 = tk.Button(self, text="Back", 
                            command=lambda:controller.show_frame(StartPage))
        button1.grid(row=3, column=1)


    def Run(self):        
        if not self.PrepareData():
            return
                
        text = PrintMeanSeries(conf.Oserie, "Tabela de Oclusões - Média das Amostras")
        self.TLeft.insert(tk.END, text)
        
        text = PrintMeanSeries(conf.Rserie, "Tabela de Reperfusões - Média das Amostras")        
        self.TRight.insert(tk.END, text)
                
        text = PrintInitialFinalValues(conf.Aserie[1], conf.Aserie[-1])
        self.TLeft.insert(tk.END, text)
        
    def PrepareData(self):
        #Directory = "D:\\anton\\Documents\\03 - PUC\\Doutorado\\00 - UFJF\\Oclusão\\Dados Projeto IPC - Estatística\\"
        Directory = ""
        print("\n\n####  {0}  #####\n\n".format(conf.filename))
        TimeSeries = np.zeros(0)      # Sampling time series
        averageSeries = np.zeros(0)   # Average per sample (line)
        meanOccl = np.zeros(0)
        meanReper = np.zeros(0)
        
        TimeSeries, averageSeries =  ReadFile(Directory, conf.filename)
        
        if len(TimeSeries) > 0:
            meanOccl = ExtractMeanSeries(averageSeries, conf.iTime, conf.oTime, conf.rTime)
            meanReper = ExtractMeanSeries(averageSeries, conf.iTime+conf.oTime, 
                                          conf.rTime, conf.oTime)
        else:
            self.Status['text'] = "Error: file not found"
            return False
            
        conf.setSeries(TimeSeries, averageSeries, meanOccl, meanReper)
        return True

class GraphsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page", font=FONT_LARGE)
        label.grid(row=0, pady=10, padx=10)

        self.Status = tk.Label(self, text="", font=FONT_LARGE)
        self.Status.grid(row=1, columnspan=2)

        button1 = tk.Button(self, text="Run", 
                            command=self.doGraph)
        button1.grid(row=2, column=1, pady=10)


        button2 = tk.Button(self, text="Back", 
                            command=lambda:controller.show_frame(StartPage))
        button2.grid(row=2, column=2, pady=10)
        
    def doGraph(self):
        if not conf.configured:
            ReportPage.PrepareData(self)
        
        if len(conf.Tserie) == 0:
            print("GraphsPage " + conf.filename)
            return
                        
        totalSerie = np.hstack((conf.Tserie, np.vstack(conf.Aserie)))
        self.PlotGraph(totalSerie,
              "Resultados" + conf.filename,
              "% Oxigenação muscular local",
              "Tempo (s)", 3, 0,
              np.arange(0,4500,500))
        
        totalSerie = None
        
        self.PlotGraph(conf.Oserie[0:,],
                  "Oclusão",
                  "% Oxigenação muscular local",
                  "Tempo (s)", 3, 1,
                  np.arange(0,450,50),
                  np.arange(20,90,10),
                  False)
        
        self.PlotGraph(conf.Rserie[0:15,],
                  "Reperfusão",
                  "% Oxigenação muscular local",
                  "Tempo (s)", 3, 2,
                  np.arange(0,80,10),
                  np.arange(20,90,10),
                  False,
                  True)
        
    #
    # Plots a graph on a canvas on screen.
    #    
    def PlotGraph(self, serie, title, ylabel, xlabel,  p_row, p_col,
              xscale, 
              yscale=[0, 20, 40, 60, 80, 100],
              lastIsMean=True,
              plotBestFit=False):
    
        time = (len(serie)-1) * (60/conf.rate)
        time = np.arange(0,time, (60/conf.rate))
    
        lin,col = np.shape(serie)    

        f = Figure(figsize=(4.5,4.5), dpi=100)
        a = f.add_subplot(111)
        
        a.set_title(title)
        a.set_ylabel(ylabel)
        a.set_xlabel(xlabel)

        if lastIsMean:
            a.plot(time, serie[1:,0:-1], alpha=0.3)
            a.plot(time, serie[1:, col-1], 'k')
        else:        
            a.plot(time, serie[1:,], alpha=0.7)
            
            if plotBestFit:
                mMeans = np.zeros(0)
                for l in range(lin):
                    mMeans = np.append(mMeans, np.mean(serie[l:l+1,]))
                
                mMeans = mMeans[1:]
                
                # finds where changes are minimum.
                # inclination tends to go horizontal
                diffs = np.diff(mMeans)
                diffs = np.nonzero(abs(diffs) < 0.8)
                dP = diffs[0][0]           # deflection point
                fit = np.polyfit(time[0:dP], mMeans[0:dP], 1)
                fit_fn = np.poly1d(fit)
                a.plot(time[0:dP], mMeans[0:dP], time[0:dP], fit_fn(time[0:dP]), 
                         '--k', linewidth=2.5)
                
                if dP < 2:
                    dP = 0
                else:
                    dP = dP-2
                    
                fit = np.polyfit(time[dP:], mMeans[dP:], 1)
                fit_fn = np.poly1d(fit)
                a.plot(time[dP:], mMeans[dP:], time[dP:], fit_fn(time[dP:]), 
                         '--k', linewidth=2.5)
    
        #plt.scatter(time, serie[1:], marker="|")
        a.set_yticks(yscale)
        a.set_xticks(xscale)
        
        canvas = FigureCanvasTkAgg(f, self)        
        #NavigationToolbar2TkAgg(canvas, self)
        #toolbar.update()
        #canvas._tkcanvas.grid(row=p_row, column=p_col )
        canvas.show()
        canvas.get_tk_widget().grid(row=p_row, column=p_col)

# Reads data series and store them into:
# averageSeries = a vector with the average value of all participants per time.
# TimeSeries = a matrix with time (lines) versus participant (column)
# each cell has the captured variable value for time-participant.
def ReadFile(Directory, Filename):
    averageSeries = np.zeros(0)
    TimeSeries = np.zeros(0)
    
    if len(Filename) == 0:
        print("ReadFile: no defined filename")
        return [], []
        
    Name = Directory + Filename
    
    with open(Name, 'rt') as f:        
        for line in f:
            line = line[:-1]
            line = line.split(",")
            line = [float(i) for i in line]
            line = np.array(line)
            
            # Calculates average of the line (time record).
            averageSeries = np.append(averageSeries, np.mean(line))            
            TimeSeries = np.append(TimeSeries, line)
    f.close()
    
    # Transform vector into matrix
    numLines = len(averageSeries)
    numCol = int(len(TimeSeries) / numLines)
    TimeSeries = np.reshape(TimeSeries, (numLines, numCol))

    return TimeSeries, averageSeries

# Extracts mean series based on initial time (Itime), occlusion time (Otime)
# and interval time time (IntTime).
def ExtractMeanSeries(serie, Itime, Otime, Inttime):
    ini = Itime * conf.rate
    means = np.zeros(0)
    
    # for each occlusion calculates mean series
    i = 1
    while(i <= conf.number):
        #print(ini, ini+(Otime*12), Otime)
        temp = serie[ini:ini+(Otime*conf.rate)+1]
               
        if i == 1:
            means = np.vstack(temp)
        else:
            temp = np.vstack(temp)
            means = np.hstack((means, temp))
        
        ini = ini + (Otime*conf.rate) + (Inttime * conf.rate)
        i += 1
    
    return means

def PrintMeanSeries(series, title):
    text = "{0:^50}\n".format(title)
    text += '{0:^8}'.format('Tempo (s)')
    
    lin, col = np.shape(series)
    
    for i in range(col):
        text += "   Serie-{0:1d} ".format(i+1)

    text += "\n"
     
    for i in range(lin):
        text += "{0:^8}".format(i*5)
        
        for value in series[i]:
            text += "{0:>11.4f}".format(value)
            
        text += "\n"
    
    text += "\n\tMinimum   Maximal Mean-diff Max-diff Min-diff values of series\n"
    
    for i in range(col):
        text += "Serie-{0:d} {1:8.4f} {2:8.4f} {3:8.4f}  {4:8.4f} {5:8.4f}\n".format(i,
                np.min(series[:,i]), np.max(series[:,i]),
                np.mean(np.diff(series[:,i])),
                np.max(np.diff(series[:,i])),
                np.min(np.diff(series[:,i])))
    text += "\ndiff - means differences between each following sampling record.\n"
    text += "For instance: value(time-5s) - value(time-10s)\n"
    
    return text

        
def PrintInitialFinalValues(ini, final):
    text = "\n\nValores de Oxigenação - Protocolo\n"
    text += "Valor Inicial - Valor Final\n"
    text += "{0:^12.4f} - {1:^12.4f}\n".format(ini, final)

    return text


conf = Conf("", 12, 5, 3, 5, 4)   
app = MainWindow()
app.mainloop()