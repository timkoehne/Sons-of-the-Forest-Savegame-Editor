import regex
import os
import json
from tkinter import filedialog as tkfiledialog

class ItemIdLoader: 
    
    def __init__(self) -> None:
        self.itemIds = []

    def loadIdsFromFile(self):
        with open("itemIds.json", "r") as file:
            self.itemIds = json.loads(file.read())

    def loadIdsFromGamefiles(self, sotfInstallDir=None):
        if sotfInstallDir is None:
            sotfInstallDir = tkfiledialog.askdirectory(
                title="Select Sons of the Forest installation location")
        
        path = sotfInstallDir + "/SonsOfTheForest_Data/resources.assets"
        
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
                    
                    if not self.isKnownId(id):
                        print(f"{id} is not a known id")
                        self.itemIds.append({
                            "id" : id, 
                            "name" : name, 
                            "max" : 1,
                            "UniqueItems" : {}
                        })
                    
        print(f"Done. Found {len(self.itemIds)} Ids.")
         
    def loadIds(self, sotfInstallDir=None):
        if sotfInstallDir is None and os.path.exists("itemIds.json"):
            self.loadIdsFromFile()
            if self.itemIds == []:
                self.loadIdsFromGamefiles(sotfInstallDir)
        else:
            self.loadIdsFromGamefiles(sotfInstallDir)
            
    def saveIds(self, sotfInstallDir=None):
        self.itemIds.sort(key=lambda item: item["name"])
        with open("itemIds.json", "w") as file:
            file.write(json.dumps(self.itemIds, indent=4))
            print("Save complete.")
    
    def getIds(self):
        return self.itemIds
        
    def findNameFromId(self, id: int) -> str:
        for item in self.itemIds:
            if item["id"] == str(id):
                return item["name"]
        return f"?-UnknownId-{id}"
        
    def findIdFromName(self, name: str) -> str:
        for item in self.itemIds:
            if item["name"] == name:
                return item["id"]

    def findEntryFromName(self, name: str):
        for item in self.itemIds:
            if item["name"] == name:
                return item
            
    def findEntryFromId(self, id: str):
        for item in self.itemIds:
            if str(item["id"]) == str(id):
                return item


    def isKnownId(self, itemId: str):
        found = False
        for item in self.itemIds:
            if item["id"] == itemId:
                found = True
        return found

        