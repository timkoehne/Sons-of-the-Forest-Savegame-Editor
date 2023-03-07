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
    
    def loadInventory(self, savefilePath):
        self.playerdataFilepath = savefilePath
        print("Loading Inventory...")
        
        with open(savefilePath, "r") as file:
            self.playerSaveData = json.loads(file.read())
        self.entireInventoryData = json.loads(self.playerSaveData["Data"]["PlayerInventory"])
        self.inventory = sorted(self.entireInventoryData["ItemInstanceManagerData"]["ItemBlocks"], 
                                key=lambda item: self.itemIdLoader.findNameFromId(item["ItemId"]))
        print("loaded", len(self.inventory), "items")
        
    def saveInventory(self, savefilePath):
        self.entireInventoryData["ItemInstanceManagerData"]["ItemBlocks"] = self.inventory
        self.playerSaveData["Data"]["PlayerInventory"] = json.dumps(self.entireInventoryData)
        strPlayerSaveData = json.dumps(self.playerSaveData)
        
        with open(savefilePath, "w") as file:
            file.write(strPlayerSaveData)
            print("Inventory saved")

    def listInventory(self):
        for item in self.inventory:
            print("Item %s exists %d times" %(item["ItemId"], item["TotalCount"]))
            
    def setAmount(self, selectedItem, amount):
        
        if selectedItem in [item["name"] for item in self.itemIdLoader.getIds()]: 
            itemId = self.itemIdLoader.findIdFromName(selectedItem)
        else:
            itemId = int(selectedItem.split("-")[-1])
            
        allUniqueItems = []
        singleUniqueItem = self.itemIdLoader.findEntryFromId(itemId)["UniqueItems"]
        for x in range(0, amount):                
            allUniqueItems.append(singleUniqueItem)
            
        print(f"Setting item {self.itemIdLoader.findNameFromId(itemId)} (id {itemId}) to amount {amount}")
        found = False
        for index, item in enumerate(self.inventory):
            if str(item["ItemId"]) == str(itemId):
                found = True
                
                if amount == 0:
                    self.inventory.pop(index)
                
                
                if amount == 0:
                    self.inventory.pop(index)
                
                item["TotalCount"] = amount
                item["UniqueItems"] = allUniqueItems
                
        if not found:      
                self.inventory.append({'ItemId': itemId, 'TotalCount': amount, 'UniqueItems': allUniqueItems})
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
    
    def findItemFromId(self, id):
        for item in self.inventory:
            if str(item["ItemId"]) == str(id):
                return item
            
    def containsId(self, id):
        for item in self.inventory:
            if str(item["ItemId"]) == str(id):
                return True
        return False
    
    def deleteFromInventory(self, selectionIndexTuple):
            it = iter(self.inventory)
            for index, i in enumerate(it):
                if index in selectionIndexTuple:
                    self.inventory.pop(index)