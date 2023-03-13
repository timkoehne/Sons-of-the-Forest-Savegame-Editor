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
        tk.Label(self.mainFrame.interior, text="Time").grid(column=0, row=2, padx=5, pady=5, sticky="e")
    
        self.dayFrame = tk.Frame(self.mainFrame.interior)
        self.dayFrame.grid(column=1, row=1, padx=5, pady=5, sticky="ew")
        self.dayVar = tk.IntVar(self)
        self.dayEntry = tk.Entry(self.dayFrame, textvariable=self.dayVar, width=5)
        self.dayEntry.bind("<KeyRelease>", self.checkDayEntry)
        self.dayEntry.pack(side="left", ipadx=2, ipady=2, padx=5)
        self.dayButton = tk.Button(self.dayFrame, text="Set", command=self.setDay)
        self.dayButton["state"] = "disabled"
        self.dayButton.pack(side="left", ipadx=2, ipady=2)
        
        self.timeFrame = tk.Frame(self.mainFrame.interior)
        self.timeFrame.grid(column=1, row=2, padx=5, pady=5, sticky="ew")
        self.timeVar = tk.StringVar(self)
        self.timeEntry = tk.Entry(self.timeFrame, textvariable=self.timeVar, width=5)
        self.timeEntry.bind("<KeyRelease>", self.checkTimeEntry)
        self.timeEntry.pack(side="left", ipadx=2, ipady=2, padx=5)
        self.timeButton = tk.Button(self.timeFrame, text="Set", command=self.setTime)
        self.timeButton["state"] = "disabled"
        self.timeButton.pack(side="left", ipadx=2, ipady=2)
        
        self.saveFileLoader.entrySetTimeAndDayCallback(self.entrySetTimeAndDay)
        
        firstPosition = 3 #number of grid rows that are manually added before
        self.initSettings(firstPosition)
    
    def initSettings(self, firstPosition):
        self.settingVars = []
        self.settingCombobox = []
        
        rowLength = math.floor((len(SETTINGS) + firstPosition)/2)
        ttk.Separator(self.mainFrame.interior, orient="vertical").grid(column=2, row=0, rowspan=rowLength+1, sticky="ns")
        
        for index, settingTitle in enumerate(SETTINGS):
            x, y = findXY(index, firstPosition, rowLength)
            
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
    
    def checkTimeEntry(self, event=None):
        time = self.timeVar.get()
        if time == self.saveFileLoader.getTime():
            self.timeButton["state"] = "disabled"
        else:
            self.timeButton["state"] = "normal"
        pass
    
    def checkDayEntry(self, event=None):
        day = self.dayVar.get()
        if day == self.saveFileLoader.getDay():
            self.dayButton["state"] = "disabled"
        else:
            self.dayButton["state"] = "normal"
        pass
    
    def setTime(self):
        print(f"Setting time to {self.timeVar.get()}")
        self.saveFileLoader.setTime(self.timeVar.get())
        self.checkTimeEntry()
        
    def setDay(self):
        print(f"Setting day to {self.dayVar.get()}")
        currentSeason = self.saveFileLoader.getSetting("CurrentSeason")
        self.saveFileLoader.setDay(self.dayVar.get())
        self.checkDayEntry()
        self.saveFileLoader.setSeason(currentSeason)
    
    def entrySetTimeAndDay(self, day: int, hour: int, minute: int):
        self.dayVar.set(day)
        self.timeVar.set(str(hour) + ":" + str(minute))
    
    def setCrashsite(self, event):
        self.saveFileLoader.setCrashsite(self.crashsiteVar.get())
        
    def setDifficulty(self, event):
        self.saveFileLoader.setDifficulty(self.difficultyVar.get())
    
    def setSetting(self, setting, valueVar):
        self.saveFileLoader.setSetting(setting, valueVar.get())
    
    def refreshSettings(self):
        self.saveFileLoader.entrySetTimeAndDayCallback(self.entrySetTimeAndDay)
        for index, settingTitle in enumerate(SETTINGS):
            self.settingVars[index].set(self.saveFileLoader.getSetting(settingTitle))
    
    def comboboxScroll(self, event):
        self.mainFrame._onMousewheel(event)
        return "break"
    
def findXY(index, firstPosition, rowLength):
    firstRow = rowLength - firstPosition
    if index <= firstRow:
        x = 0
        y = index % rowLength
    else:
        x = 3
        y = index - rowLength
    return x,y