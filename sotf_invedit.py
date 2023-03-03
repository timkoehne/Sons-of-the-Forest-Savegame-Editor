import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as tkfiledialog
from tkinter import messagebox as tkmessagebox
import os
from KnownItem import KnownItem
from TkEditJsonDialog import TkEditJsonDialog
from ItemIdLoader import ItemIdLoader

def reloadItemIds():
    itemIdLoader.loadIdsFromGamefiles()
    itemCombobox['values'] = sorted([item.name for item in itemIdLoader.getIds()])
          
def listInventory():
    for item in inventory:
        print("Item %s exists %d times" %(item["ItemId"], item["TotalCount"]))

def listboxSelect(index: int):
    inventoryListbox.selection_set(index)
    inventoryListbox.activate(index)
    inventoryListbox.see(index)

def setAmount():
    global inventory
    
    if selectedItem.get() in possibleItems: 
        itemId = itemIdLoader.findIdFromName(selectedItem.get())
    else:
        itemId = int(selectedItem.get().split("-")[-1])
        
    amount =  int(amountEntry.get())
    print(f"Setting item {itemIdLoader.findNameFromId(itemId)} (id {itemId}) to amount {amount}")
    found = False
    for index, item in enumerate(inventory):
        if item["ItemId"] == itemId:
            found = True
            item["TotalCount"] = amount
            listboxSelect(index)
    if not found:      
            inventory.append({'ItemId': itemId, 'TotalCount': amount, 'UniqueItems': []})
            #itemIndex = possibleItems.index(selectedItem.get())
            #listboxSelect(itemIndex)
            
    refreshInventoryText()
        
def getAmount(itemId: int) -> int:
    for item in inventory:
        if item["ItemId"] == itemId:
            return item["TotalCount"]
    return 0
        
def loadInventory():
    global playerdataFilepath
    global playerSaveData
    global entireInventoryData
    global inventory
    
    filetypes = (
    ('json file', '*.json'),
    ('All files', '*.*')
    )
    playerdataFilepath = tkfiledialog.askopenfilename(title="Select PlayerInventorySaveData.json", 
                                          initialdir=f"C:/Users/{os.getlogin()}/AppData/LocalLow/Endnight/SonsOfTheForest/Saves/", 
                                          filetypes=filetypes)
    
    with open(playerdataFilepath, "r") as file:
        playerSaveData = json.loads(file.read())
    entireInventoryData = json.loads(playerSaveData["Data"]["PlayerInventory"])
    inventory = entireInventoryData["ItemInstanceManagerData"]["ItemBlocks"]
    refreshInventoryText()
    print("Inventory loaded")
        
def saveInventory():
    entireInventoryData["ItemInstanceManagerData"]["ItemBlocks"] = inventory
    playerSaveData["Data"]["PlayerInventory"] = json.dumps(entireInventoryData)
    strPlayerSaveData = json.dumps(playerSaveData)
     
    filetypes = (
    ('json file', '*.json'),
    ('All files', '*.*')
    )
    savefilepath = tkfiledialog.asksaveasfilename(title="Save Inventory as...", 
                                          initialdir=playerdataFilepath, 
                                          filetypes=filetypes)
    with open(savefilepath, "w") as file:
        file.write(strPlayerSaveData)
        print("Inventory saved")

def refreshInventoryText():
    global inventory
    selected = inventoryListbox.curselection()
    yview = inventoryListbox.yview()
    inventoryListbox.delete(0, tk.END)
    inventory = sorted(inventory, key=lambda item: itemIdLoader.findNameFromId(item["ItemId"]))
    
    for index, item in enumerate(inventory):
        name = itemIdLoader.findNameFromId(item["ItemId"])
        amount = item["TotalCount"]
        inventoryListbox.insert(index+1, name + " " + str(amount) + "x")
    for s in selected:
        listboxSelect(s)
    inventoryListbox.yview_moveto(yview[0])

def viewItemJson(event):
    if inventoryListbox.curselection():
        selectedIndex = inventoryListbox.curselection()[0]
        selectedId = inventory[selectedIndex]["ItemId"]
        selectedName = itemIdLoader.findNameFromId(selectedId)
    
        result = TkEditJsonDialog(window, title=selectedName, 
                                    text=json.dumps(inventory[selectedIndex], indent=4)).show()
        try:
            result = json.loads(result)
            
            if inventory[selectedIndex] != result:
                print(f"Item {selectedName} ({selectedId}) was changed")
        except ValueError:
            tkmessagebox.showerror("Json Format Error", 
                                   "Change could not be saved since it was not in json format.")
        else:
            inventory[selectedIndex] = result
            refreshInventoryText()

def comboboxSelected(event):
    selectedId = itemIdLoader.findIdFromName(selectedItem.get())
    found = False
    for index, item in enumerate(inventory):
        if item["ItemId"] == selectedId:
            listboxSelect(index)
            amountSetText(item["TotalCount"])
            found = True
            
    if not found:
        amountSetText(str(1))
        
def amountSetText(text: str):
    amountEntry.delete(0, tk.END)
    amountEntry.insert(tk.END, text)

def listboxSelected(event):
    if inventoryListbox.curselection():
        selectedIndex = inventoryListbox.curselection()
        selectedId = inventory[selectedIndex[0]]["ItemId"]
        selectedName = itemIdLoader.findNameFromId(selectedId)
        itemCombobox.set(selectedName)
        amountSetText(inventory[selectedIndex[0]]["TotalCount"])

def createUiElements():
    global inventoryListbox
    global amountEntry
    global itemCombobox
    global possibleItems
    global selectedItem
    
    #left part of ui
    addItemFrame = tk.Frame(window)
    addItemFrame.pack(expand=True, fill="both", side="left", padx=10, pady=10)
    possibleItems = [item.name for item in itemIdLoader.getIds()]
    selectedItem = tk.StringVar(addItemFrame)
    selectedItem.set(possibleItems[0])
    itemCombobox = ttk.Combobox(addItemFrame, textvariable=selectedItem)
    itemCombobox['values'] = possibleItems
    itemCombobox['state'] = 'readonly'
    itemCombobox.bind("<<ComboboxSelected>>", comboboxSelected)
    itemCombobox.pack(ipadx=5, ipady=5, padx=5, pady=5)
    amountFrame = tk.Frame(addItemFrame)
    amountFrame.pack(ipadx=5, ipady=5, padx=5, pady=5)
    amountLabel = ttk.Label(amountFrame, text="Amount")
    amountLabel.pack(side="left")
    amountEntry = tk.Entry(amountFrame)
    amountSetText(str(1))
    amountEntry.pack(side="right")
    addButton = tk.Button(addItemFrame, text="Set Amount", 
                          command=setAmount)
    addButton.pack(ipadx=5, ipady=5, padx=5, pady=5)
    
    knownItemsFrame = tk.Frame(addItemFrame)
    knownItemsFrame.pack(side="bottom")
    
    reloadKnownItemsButton = tk.Button(knownItemsFrame, text="Reload Item Ids", command=reloadItemIds)
    reloadKnownItemsButton.pack(side="left", ipadx=5, ipady=5, padx=5, pady=5)
    saveKnownItemsButton = tk.Button(knownItemsFrame, text="Save Item Ids", command=itemIdLoader.saveIds)
    saveKnownItemsButton.pack(side="left", ipadx=5, ipady=5, padx=5, pady=5)

    #right part of ui
    inventoryFrame = tk.Frame(window)
    inventoryFrame.pack(expand=True, fill="both", side="right", padx=10, pady=10)
    inventoryLabel = ttk.Label(inventoryFrame, text="Inventory")
    inventoryLabel.pack(side="top")
    saveLoadFrame = tk.Frame(inventoryFrame)
    saveLoadFrame.pack(side="bottom", padx=5, pady=5)
    loadButton = tk.Button(saveLoadFrame, text="Load Inventory", 
                           command=loadInventory)
    loadButton.pack(side="left", padx=5, ipadx=5, ipady=5)
    saveButton = tk.Button(saveLoadFrame, text="Save Inventory", 
                           command=saveInventory)
    saveButton.pack(side="left", padx=5, ipadx=5, ipady=5)
    inventoryScrollbar = tk.Scrollbar(inventoryFrame)
    inventoryScrollbar.pack(side="right", fill="y")
    inventoryListbox = tk.Listbox(inventoryFrame, yscrollcommand=inventoryScrollbar.set)
    inventoryListbox.pack(side="left", expand=True, fill="both")
    inventoryListbox.bind("<Double-1>", viewItemJson)
    inventoryListbox.bind("<<ListboxSelect>>", listboxSelected)
    inventoryScrollbar.config(command=inventoryListbox.yview)
    
    comboboxSelected("")
    refreshInventoryText()

itemIdLoader = ItemIdLoader()
itemIdLoader.loadIds()
    
inventory = []

window = tk.Tk()
window.title("SotF Inventory Editor")
window.geometry("700x350")
createUiElements()

window.mainloop()