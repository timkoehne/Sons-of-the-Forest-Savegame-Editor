import tkinter as tk
from TkSearchableCombobox import TkSearchableCombobox
from SavefileLoader import SavefileLoader, SETTINGS
from TkVerticalScrolledFrame import TkVerticalScrolledFrame


class TkWorldTab(tk.Frame):
    def __init__(self, saveFileLoader: SavefileLoader):
        super().__init__()
        
        self.saveFileLoader = saveFileLoader
        
        
        mainFrame = TkVerticalScrolledFrame(self)
        mainFrame.pack(expand=True, fill="both")
        
        
        tk.Label(mainFrame.interior, text="Setting").grid(column=0, row=0, padx=5, pady=5)
        tk.Label(mainFrame.interior, text="Status").grid(column=1, row=0, padx=5, pady=5)
        
        

        tk.Label(mainFrame.interior, text="Kelvin is").grid(column=0, row=1, padx=5, pady=5)
        tk.Label(mainFrame.interior, text="Virginia is").grid(column=0, row=2, padx=5, pady=5)

        self.kelvinStatusVar = tk.StringVar(self)
        self.kelvinStatus = TkSearchableCombobox(mainFrame.interior, width=15, textvariable=self.kelvinStatusVar)
        self.kelvinStatus['values'] = ["alive", "dead"]
        self.kelvinStatusVar.set("alive" if self.saveFileLoader.isKelvinAlive() else "dead")
        self.kelvinStatus['state'] = 'readonly'
        self.kelvinStatus.bind("<<ComboboxSelected>>", self.kelvinComboboxSelected)
        self.kelvinStatus.bind("<KeyRelease>", self.kelvinStatus.popup_key_pressed)
        self.kelvinStatus.grid(column=1, row=1, ipadx=5, ipady=5, padx=5, pady=5)
        
        self.virginiaStatusVar = tk.StringVar(self)
        self.virginiaStatus = TkSearchableCombobox(mainFrame.interior, width=15, textvariable=self.virginiaStatusVar)
        self.virginiaStatus['values'] = ["alive", "dead"]
        self.virginiaStatusVar.set("alive" if self.saveFileLoader.isVirginiaAlive() else "dead")
        self.virginiaStatus['state'] = 'readonly'
        self.virginiaStatus.bind("<<ComboboxSelected>>", self.virginiaComboboxSelected)
        self.virginiaStatus.bind("<KeyRelease>", self.kelvinStatus.popup_key_pressed)
        self.virginiaStatus.grid(column=1, row=2, ipadx=5, ipady=5, padx=5, pady=5)
        
        self.settingVars = []
        self.settingCombobox = []
        for index, settingTitle in enumerate(SETTINGS):
            tk.Label(mainFrame.interior, text=settingTitle).grid(column=0, row=3+index, padx=5, pady=5)
            self.settingVars.append(tk.StringVar(self))
            self.settingCombobox.append(TkSearchableCombobox(mainFrame.interior, width=15, 
                                                             textvariable=self.settingVars[index]))
            self.settingCombobox[index]['values'] = SETTINGS[settingTitle].options
            self.settingVars[index].set(self.saveFileLoader.getSetting(settingTitle))
            self.settingCombobox[index]['state'] = 'readonly'
            
            self.settingCombobox[index].bind("<<ComboboxSelected>>", 
                                             lambda event, s=settingTitle, v=self.settingVars[index]: self.setSetting(s, v))
            self.settingCombobox[index].bind("<KeyRelease>", self.settingCombobox[index].popup_key_pressed)
            self.settingCombobox[index].grid(column=1, row=3+index, ipadx=5, ipady=5, padx=5, pady=5)
    
    def setCrashsite(self, event):
        self.saveFileLoader.setCrashsite(self.crashsiteVar.get())
        
    def setDifficulty(self, event):
        self.saveFileLoader.setDifficulty(self.difficultyVar.get())
    
    def setSetting(self, setting, valueVar):
        self.saveFileLoader.setSetting(setting, valueVar.get())
    
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