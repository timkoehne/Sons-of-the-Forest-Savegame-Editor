from KnownItem import KnownItem
import regex
import os
from tkinter import filedialog as tkfiledialog

class ItemIdLoader: 
    
    def __init__(self) -> None:
        self.itemIds = []

    def loadIdsFromFile(self):
        with open("itemIds.txt", "r") as file:
            self.itemIds = []
            lines = file.readlines()
            for line in lines:
                id, name = line.strip().split(":")
                self.itemIds.append(KnownItem(id, name))

    def loadIdsFromGamefiles(self, sotfInstallDir=None):
        if sotfInstallDir is None:
            sotfInstallDir = tkfiledialog.askdirectory(
                title="Select Sons of the Forest installation location")
        
        path = sotfInstallDir + "/SonsOfTheForest_Data/resources.assets"
        self.itemIds = []
        
        print("Extracting Item Ids...")
        with open(path, "rb",) as file:
            content = file.readlines()
            numLines = len(content)
            pattern = regex.compile("[0-9a-zA-Z]+ ID\(\d+\)")
            for index, line in enumerate(content):
                if index % (numLines//10) == 0:
                    print(f"{round(index / numLines * 100)}%")
                matchesInLine = pattern.findall(str(line))
            
                for match in matchesInLine:
                    name, id = match.split(" ")
                    name = name.removeprefix("x00")
                    id = id[3:-1]
                    
                    
                    self.itemIds.append(KnownItem(id, name))
                    
        print(f"Done. Found {len(self.itemIds)} Ids.")
         
    def loadIds(self, sotfInstallDir=None):
        if sotfInstallDir is None and os.path.exists("itemIds.txt"):
            self.loadIdsFromFile()
            if self.itemIds == []:
                self.loadIdsFromGamefiles(sotfInstallDir)
        else:
            self.loadIdsFromGamefiles(sotfInstallDir)
            
    def saveIds(self, sotfInstallDir=None):
        with open("itemIds.txt", "w") as file:
            for index, item in enumerate(self.itemIds, 1):
                file.write(str(item.id) + " : " + item.name)
                if index < len(self.itemIds):
                    file.write("\n")
            print("Save complete.")
    
    def getIds(self):
        return self.itemIds
        
    def findNameFromId(self, id: int) -> str:
        for item in self.itemIds:
            if item.id == id:
                return item.name
        return f"?-UnknownId-{id}"

    def findItemFromId(self, id: int) -> KnownItem:
        for item in self.item:
            if item.id == id:
                return item
    
            return self.itemIds
        
    def findIdFromName(self, name: str) -> int:
        for item in self.itemIds:
            if item.name == name:
                return item.id

    def isKnownId(self, itemId: int):
        return any(item == itemId for item in self.itemIds)

        