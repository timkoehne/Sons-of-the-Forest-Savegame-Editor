import tkinter as tk
from tkinter import ttk
from TkSearchableCombobox import TkSearchableCombobox
from SavefileLoader import SavefileLoader, SETTINGS
from TkVerticalScrolledFrame import TkVerticalScrolledFrame
import math


class TkWorldTab(tk.Frame):
    def __init__(self, saveFileLoader: SavefileLoader):
        super().__init__()
        
        self.saveFileLoader = saveFileLoader
        
        self.mainFrame = TkVerticalScrolledFrame(self)
        self.mainFrame.pack(expand=True, fill="both")
        self.mainFrame.interior.grid_columnconfigure(2, weight=1)
        
        tk.Label(self.mainFrame.interior, text="Setting").grid(column=0, row=0, padx=5, pady=5)
        tk.Label(self.mainFrame.interior, text="Status").grid(column=1, row=0, padx=5, pady=5)
        tk.Label(self.mainFrame.interior, text="Setting").grid(column=3, row=0, padx=5, pady=5)
        tk.Label(self.mainFrame.interior, text="Status").grid(column=4, row=0, padx=5, pady=5)
        
        tk.Label(self.mainFrame.interior, text="Day").grid(column=0, row=1, padx=5, pady=5, sticky="e")
        tk.Label(self.mainFrame.interior, text="Hour").grid(column=0, row=2, padx=5, pady=5, sticky="e")
        tk.Label(self.mainFrame.interior, text="Minutes").grid(column=0, row=3, padx=5, pady=5, sticky="e")
        
        self.dayVar = tk.IntVar(self)
        self.dayEntry = tk.Entry(self.mainFrame.interior, text="Day", textvariable=self.dayVar).grid(column=1, row=1, padx=5, pady=5)
        self.hourVar = tk.IntVar(self)
        self.hourEntry = tk.Entry(self.mainFrame.interior, text="Hour", textvariable=self.hourVar).grid(column=1, row=2, padx=5, pady=5)
        self.minuteVar = tk.IntVar(self)
        self.minuteEntry = tk.Entry(self.mainFrame.interior, text="Minutes", textvariable=self.minuteVar).grid(column=1, row=3, padx=5, pady=5)
        self.saveFileLoader.setTime(self.setTime)
        
        tk.Label(self.mainFrame.interior, text="Kelvin is").grid(column=0, row=4, padx=5, pady=5, sticky="e")
        tk.Label(self.mainFrame.interior, text="Virginia is").grid(column=0, row=5, padx=5, pady=5, sticky="e")

        self.kelvinStatusVar = tk.StringVar(self)
        self.kelvinStatus = TkSearchableCombobox(self.mainFrame.interior, width=15, textvariable=self.kelvinStatusVar)
        self.kelvinStatus['values'] = ["alive", "dead"]
        self.kelvinStatusVar.set("alive" if self.saveFileLoader.isKelvinAlive() else "dead")
        self.kelvinStatus['state'] = 'readonly'
        self.kelvinStatus.bind("<<ComboboxSelected>>", self.kelvinComboboxSelected)
        self.kelvinStatus.bind("<MouseWheel>", self.comboboxScroll) 
        self.kelvinStatus.bind("<KeyRelease>", self.kelvinStatus.popup_key_pressed)
        self.kelvinStatus.grid(column=1, row=4, ipadx=5, ipady=5, padx=5, pady=5)
        
        self.virginiaStatusVar = tk.StringVar(self)
        self.virginiaStatus = TkSearchableCombobox(self.mainFrame.interior, width=15, textvariable=self.virginiaStatusVar)
        self.virginiaStatus['values'] = ["alive", "dead"]
        self.virginiaStatusVar.set("alive" if self.saveFileLoader.isVirginiaAlive() else "dead")
        self.virginiaStatus['state'] = 'readonly'
        self.virginiaStatus.bind("<<ComboboxSelected>>", self.virginiaComboboxSelected)
        self.virginiaStatus.bind("<MouseWheel>", self.comboboxScroll) 
        self.virginiaStatus.bind("<KeyRelease>", self.kelvinStatus.popup_key_pressed)
        self.virginiaStatus.grid(column=1, row=5, ipadx=5, ipady=5, padx=5, pady=5)
        
        self.settingVars = []
        self.settingCombobox = []
        
        
        firstPosition = 6
        rowLength = math.ceil((len(SETTINGS) + firstPosition)/2)
        ttk.Separator(self.mainFrame.interior, orient="vertical").grid(column=2, row=0, rowspan=rowLength+1, sticky="ns")
        firstRow = rowLength - firstPosition
        for index, settingTitle in enumerate(SETTINGS):
            if index <= firstRow:
                x = 0
                y = index % rowLength
            else:
                x = 3
                y = index - rowLength
            
            tk.Label(self.mainFrame.interior, text=settingTitle).grid(column=0+x, row=firstPosition+y, padx=5, pady=5, sticky="e")
            self.settingVars.append(tk.StringVar(self))
            self.settingCombobox.append(TkSearchableCombobox(self.mainFrame.interior, width=15, 
                                                             textvariable=self.settingVars[index]))
            self.settingCombobox[index]['values'] = SETTINGS[settingTitle].options
            self.settingVars[index].set(self.saveFileLoader.getSetting(settingTitle))
            self.settingCombobox[index]['state'] = 'readonly'
            
            self.settingCombobox[index].bind("<<ComboboxSelected>>", 
                                             lambda event, s=settingTitle, v=self.settingVars[index]: self.setSetting(s, v))
            self.settingCombobox[index].bind("<MouseWheel>", self.comboboxScroll) 
            self.settingCombobox[index].bind("<KeyRelease>", self.settingCombobox[index].popup_key_pressed)
            self.settingCombobox[index].grid(column=1+x, row=firstPosition+y, ipadx=5, ipady=5, padx=5, pady=5)
    
    def setTime(self, day: int, hour: int, minute: int):
        
        self.dayVar.set(str(day))
        self.hourVar.set(str(hour))
        self.minuteVar.set(str(minute))
    
    def setCrashsite(self, event):
        self.saveFileLoader.setCrashsite(self.crashsiteVar.get())
        
    def setDifficulty(self, event):
        self.saveFileLoader.setDifficulty(self.difficultyVar.get())
    
    def setSetting(self, setting, valueVar):
        self.saveFileLoader.setSetting(setting, valueVar.get())
    
    def comboboxScroll(self, event):
        self.mainFrame._onMousewheel(event)
        return "break"
    
    def kelvinComboboxSelected(self, event):
        if self.kelvinStatusVar.get() == "alive": 
            self.saveFileLoader.revive(kelvin=True)
            print("Kelvin was revived")
        else: 
            self.saveFileLoader.kill(kelvin=True)
            print("Kelvin was killed")
        
    def virginiaComboboxSelected(self, event):
        if self.virginiaStatusVar.get() == "alive": 
            self.saveFileLoader.revive(virginia=True)
            print("Virginia was revived")
        else: 
            self.saveFileLoader.kill(virginia=True)
            print("Virginia was killed")