import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from PIL import ImageTk, Image
import os
import datetime
import json
from SavefileLoader import SavefileLoader


saveGameModes = ["SinglePlayer", "Multiplayer", "MultiplayerClient"]
manuallySelectLocationText = "Manually select Save Location"
labelFileName = "/label.txt"

class SaveFileEntry:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

class TkSaveLoadTab(tk.Frame):
    def __init__(self, saveFileLoader: SavefileLoader, createUiFunction):
        super().__init__()
        
        self.saveFileLoader = saveFileLoader
        self.createUiFunction = createUiFunction
        
        self.savefileList = []
        self.savefileList.append(SaveFileEntry(manuallySelectLocationText, None))
        
        path = "C:/Users/" + os.getlogin() + "/AppData/LocalLow/Endnight/SonsOfTheForest/Saves/"
        idNumber = os.listdir(path)[0]
        path = path + idNumber + "/"
        for saveGameMode in saveGameModes:
            saveFolder = path + saveGameMode + "/"
            
            #save file names are 10 digit strings
            saveFiles = filter(lambda saveName: len(saveName) == 10 and saveName.isdigit(), os.listdir(saveFolder))
            for saveFile in saveFiles:
                if os.path.isdir(saveFolder + saveFile):
                    #read save file label
                    if os.path.isfile(saveFolder + saveFile + labelFileName):
                        with open(saveFolder + saveFile + labelFileName, "r") as file:
                            name = file.read()
                    else:
                        name = saveFile
                    self.savefileList.append(SaveFileEntry(saveGameMode + " " + name, saveFolder + saveFile))
        
        comboboxFrame = tk.Frame(self)
        comboboxFrame.pack(ipadx=5, ipady=5, padx=5, pady=5)
        self.saveNames = [save.name for save in self.savefileList]
        self.savefileVar = tk.StringVar(self)
        self.savefileVar.set(self.saveNames[0])
        self.saveCombobox = ttk.Combobox(comboboxFrame, textvariable=self.savefileVar, values=self.saveNames, state="readonly", width=50)
        self.saveCombobox.bind("<<ComboboxSelected>>", self.onSaveSelected)
        self.saveCombobox.pack(side="left", ipadx=5, ipady=5, padx=5, pady=5)
        self.renameButton = tk.Button(comboboxFrame, text="Rename", command=self.renameSave, state="disabled")
        self.renameButton.pack(side="left", ipadx=5, ipady=5, padx=5, pady=5)
        
        
        self.lastModifiedVar = tk.StringVar(self)
        lastModified = tk.Label(self, textvariable=self.lastModifiedVar)
        lastModified.pack()
        self.imagePreview = tk.Label(self)
        self.imagePreview.pack()
        
        saveLoadFrame = tk.Frame(self)
        saveLoadFrame.pack(padx=5, pady=5)
        loadButton = tk.Button(saveLoadFrame, text="Load Savefolder", command=self.loadSavefile)
        loadButton.pack(ipadx=5, ipady=5, padx=5, pady=5)
        saveButton = tk.Button(saveLoadFrame, text="Save Savefolder", command=self.saveSavefile)
        saveButton.pack(ipadx=5, ipady=5, padx=5, pady=5)
        
        self.showBackupsVar = tk.StringVar(self)
        showBackups = tk.Label(self, textvariable=self.showBackupsVar)
        showBackups.pack(side="bottom", ipadx=5, ipady=5, padx=5, pady=5)
        self.findNumBackups()
        
    def findNumBackups(self):
        num = 0
        path = "C:/Users/" + os.getlogin() + "/AppData/LocalLow/Endnight/SonsOfTheForest/Saves/"
        idNumber = os.listdir(path)[0]
        path = path + idNumber + "/"
        for saveGameMode in saveGameModes:
            backupFolder = path + saveGameMode + "/Backup/"
            if os.path.isdir(backupFolder):
                num += len(os.listdir(backupFolder))
        self.showBackupsVar.set(f"{num} Backups found")
        
    def renameSave(self):
        oldName = self.savefileVar.get()
        path = self.findSavefileFromName(oldName).path
        newName = simpledialog.askstring("Rename Save", "New Name: ")
        
        if newName is None:
            return
        elif newName == "":
            os.remove(path + labelFileName)
            newName = path.split("/")[-1]
        else:
            with open(path + "/label.txt", "w") as file:
                file.write(newName)
                
        for index, saveFile in enumerate(self.savefileList):
            if saveFile.name == oldName:
                newName = str(oldName).split(" ")[0] + " " + newName
                self.savefileList[index].name = newName
        self.saveNames = [save.name for save in self.savefileList]
        self.savefileVar.set(newName)
        self.saveCombobox.configure(values=self.saveNames)

    def onSaveSelected(self, event=None):
        selectedSaveName = self.savefileVar.get()
        selectedSavePath = self.findSavefileFromName(selectedSaveName).path
        
        if selectedSaveName == manuallySelectLocationText:
            self.renameButton.configure(state="disabled")
            self.lastModifiedVar.set("")
            self.imagePreview.configure(image='')
        elif selectedSaveName.startswith("MultiplayerClient"):
            self.renameButton.configure(state="normal")
            self.lastModifiedVar.set("Last Modified: " + self.readSaveTime(selectedSavePath))
            self.imagePreview.configure(image='')
        else:
            self.renameButton.configure(state="normal")
            self.lastModifiedVar.set("Last Modified: " + self.readSaveTime(selectedSavePath))
            img = ImageTk.PhotoImage(Image.open(selectedSavePath + "/SaveDataThumbnail.png"))
            self.img = img
            self.imagePreview.configure(image=img)
    
    def readSaveTime(self, path) -> str:
        path = path + "/GameStateSaveData.json"
        with open(path, "r") as file:
            saveTimeStr = str(json.loads(json.loads(file.read())["Data"]["GameState"])["SaveTime"])
            saveTimeStr = saveTimeStr[:19] #ignore ms and timezone
            saveTime = datetime.datetime.strptime(saveTimeStr, '%Y-%m-%dT%H:%M:%S')
            return saveTime.strftime("%d %b %Y - %I:%M:%S %p")
    
    def findSavefileFromName(self, name) -> SaveFileEntry:
        for saveFile in self.savefileList:
            if saveFile.name == name:
                return saveFile
        
    def loadSavefile(self):
        currentlySelected = self.findSavefileFromName(self.savefileVar.get())
        self.saveFileLoader.load(currentlySelected.path)
        self.createUiFunction()

    def saveSavefile(self):
        currentlySelected = self.findSavefileFromName(self.savefileVar.get())
        success = self.saveFileLoader.save(currentlySelected.path)
        if success:
            selectedSaveName = self.savefileVar.get()
            selectedSavePath = self.findSavefileFromName(selectedSaveName).path
            self.lastModifiedVar.set("Last Modified: " + self.readSaveTime(selectedSavePath))
            self.findNumBackups()
