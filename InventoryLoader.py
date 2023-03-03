import json
import os
from tkinter import filedialog as tkfiledialog
from ItemIdLoader import ItemIdLoader

jsonFiletypes = (
    ('json file', '*.json'),
    ('All files', '*.*')
)

class InventoryLoader:
    def __init__(self, itemIdLoader: ItemIdLoader) -> None:
        self.inventory = []
        self.playerSaveData = []
        self.entireInventoryData = []
        self.itemIdLoader = itemIdLoader
        self.playerdataFilepath = ""
        self.loadInventory(True)
    
    def loadInventory(self, loadDefaultInventory=False):
        if loadDefaultInventory:
            path = "defaultInventory.json"
        else:
            path = tkfiledialog.askopenfilename(title="Select PlayerInventorySaveData.json", 
                                            initialdir=f"C:/Users/{os.getlogin()}/AppData/LocalLow/Endnight/SonsOfTheForest/Saves/", 
                                            filetypes=jsonFiletypes)
            self.playerdataFilepath = path
        
        with open(path, "r") as file:
            self.playerSaveData = json.loads(file.read())
        self.entireInventoryData = json.loads(self.playerSaveData["Data"]["PlayerInventory"])
        self.inventory = sorted(self.entireInventoryData["ItemInstanceManagerData"]["ItemBlocks"], 
                                key=lambda item: self.itemIdLoader.findNameFromId(item["ItemId"]))
        print("Inventory loaded")
        
    def saveInventory(self):
        self.entireInventoryData["ItemInstanceManagerData"]["ItemBlocks"] = self.inventory
        self.playerSaveData["Data"]["PlayerInventory"] = json.dumps(self.entireInventoryData)
        strPlayerSaveData = json.dumps(self.playerSaveData)
        
        if self.playerdataFilepath == "":
            initialDir = f"C:/Users/{os.getlogin()}/AppData/LocalLow/Endnight/SonsOfTheForest/Saves/"
        else:
            initialDir = self.playerdataFilepath
                
        savefilepath = tkfiledialog.asksaveasfilename(title="Save Inventory as...", 
                                                initialdir=initialDir, 
                                                filetypes=jsonFiletypes)
        
        with open(savefilepath, "w") as file:
            file.write(strPlayerSaveData)
            print("Inventory saved")

    def listInventory(self):
        for item in self.inventory:
            print("Item %s exists %d times" %(item["ItemId"], item["TotalCount"]))
            
    def setAmount(self, selectedItem, amount):
        if selectedItem in [item.name for item in self.itemIdLoader.getIds()]: 
            itemId = self.itemIdLoader.findIdFromName(selectedItem)
        else:
            itemId = int(selectedItem.split("-")[-1])
            
        print(f"Setting item {self.itemIdLoader.findNameFromId(itemId)} (id {itemId}) to amount {amount}")
        found = False
        for index, item in enumerate(self.inventory):
            if item["ItemId"] == itemId:
                found = True
                item["TotalCount"] = amount
        if not found:      
                self.inventory.append({'ItemId': itemId, 'TotalCount': amount, 'UniqueItems': []})
                self.inventory.sort(key=lambda item: self.itemIdLoader.findNameFromId(item["ItemId"]))
            
    def getAmount(self, itemId: int) -> int:
        for item in self.inventory:
            if item["ItemId"] == itemId:
                return item["TotalCount"]
        return 0
    
    def findIndexInInventory(self, itemName):
        for index, item in enumerate(self.inventory):
            if itemName == self.itemIdLoader.findNameFromId(item["ItemId"]):
                return index
        return -1