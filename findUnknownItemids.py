import json
import tkinter as tk
from tkinter import ttk

class KnownItem:
    def __init__(self, id: int, name: str):
        self.id = int(id)
        self.name = name
        
    def __eq__(self, anotherId):
        return self.id == anotherId

def loadKnownItemIds():
    global knownItemIds
    with open("itemIds.txt", "r") as file:
        knownItemIds = []
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            knownItemIds.append(KnownItem(line.split(":")[0], line.split(":")[1]))

def findIdFromName(name: str):
    global knownItemIds
    for item in knownItemIds:
        if item.name == name:
            return item

def isKnownId(itemId: int):
    global knownItemIds
    return any(item == itemId for item in knownItemIds)

def listInventory():
    global inventory
    for item in inventory:
        print("Item %s exists %d times" %(item["ItemId"], item["TotalCount"]))

def setAmount(itemId: int, amount: int):
    print(f"Setting item amount of {itemId} to {amount}")
    for item in inventory:
        if item["ItemId"] == itemId:
            item["TotalCount"] = amount
            return
    #item not in inventory yet. adding
    inventory.append({'ItemId': itemId, 'TotalCount': amount, 'UniqueItems': []})
        
def getAmount(itemId: int) -> int:
    for item in inventory:
        if item["ItemId"] == itemId:
            return item["TotalCount"]
    return 0
        
def loadInventory():
    global playerSaveData
    global entireInventoryData
    global inventory
    with open("PlayerInventorySaveData.json", "r") as file:
        playerSaveData = json.loads(file.read())
    entireInventoryData = json.loads(playerSaveData["Data"]["PlayerInventory"])
    inventory = entireInventoryData["ItemInstanceManagerData"]["ItemBlocks"]
    print("Inventory loaded")
        
def saveInventory():
    global playerSaveData
    global entireInventoryData
    global inventory
    
    playerSaveData["Data"]["PlayerInventory"] = json.dumps(entireInventoryData)
    strPlayerSaveData = json.dumps(playerSaveData)
    
    with open("test.json", "w") as file:
        file.write(strPlayerSaveData)
    print("Inventory saved")


def addItem():
    itemId = findIdFromName(selectedItem.get())
    currentAmount = getAmount(itemId)
    setAmount(itemId.id, currentAmount + int(amountText.get("1.0")))
    refreshInventoryText()
    saveInventory()

def refreshInventoryText():
    global inventory
    inventoryText.delete("1.0", tk.END)
    inventoryText.insert("1.0", json.dumps(inventory, indent=4))

loadKnownItemIds()
loadInventory()
# setAmount(414, 3)
# saveInventory()


window = tk.Tk()
window.title("SOTF Inventory Editor")
window.geometry("800x400")

#create user combobox
possibleItems = [item.name for item in knownItemIds]
selectedItem = tk.StringVar(window)
selectedItem.set(possibleItems[0])
itemCombobox = ttk.Combobox(window, textvariable=selectedItem)
itemCombobox['values'] = possibleItems
itemCombobox['state'] = 'readonly'
itemCombobox.pack()



addButton = tk.Button(window, text="Add Item to Inventory", command=addItem)
addButton.pack()

amountLabel = ttk.Label(window, text="Amount")
amountLabel.pack()
amountText = tk.Text(window, height=1)
amountText.pack()

inventoryLabel = ttk.Label(window, text="Inventory")
inventoryLabel.pack()
inventoryText = tk.Text(window)
inventoryText.pack()
refreshInventoryText()


window.mainloop()

# for item in inventory:
#     if not isKnown(item["ItemId"]):
#         print("Currently unknown ItemId: %d is %dx in inventory" % (item["ItemId"], item["TotalCount"]))