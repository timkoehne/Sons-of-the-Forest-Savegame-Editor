import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tkmessagebox
from TkEditJsonDialog import TkEditJsonDialog
from ItemIdLoader import ItemIdLoader
from InventoryLoader import InventoryLoader

def reloadItemIds():
    itemIdLoader.loadIdsFromGamefiles()
    itemCombobox['values'] = sorted([item["name"] for item in itemIdLoader.getIds()])

def listboxSelect(index: int):
    inventoryListbox.selection_set(index)
    inventoryListbox.activate(index)
    inventoryListbox.see(index)

def setAmount():
    selected = selectedItem.get()
    amount = int(amountEntry.get())
    inventoryLoader.setAmount(selected, amount)
    
    listboxSelect(inventoryLoader.findIndexInInventory(selected))
    refreshInventoryList()

def refreshInventoryList():
    selected = inventoryListbox.curselection()
    yview = inventoryListbox.yview()
    inventoryListbox.delete(0, tk.END)
    
    for index, item in enumerate(inventoryLoader.inventory):
        name = itemIdLoader.findNameFromId(item["ItemId"])
        amount = item["TotalCount"]
        inventoryListbox.insert(index+1, name + " " + str(amount) + "x")
    for s in selected:
        listboxSelect(s)
    inventoryListbox.yview_moveto(yview[0])

def loadInventory():
    inventoryLoader.loadInventory()
    refreshInventoryList()

def saveInventory():
    inventoryLoader.saveInventory()

def viewItemJson(event):
    if inventoryListbox.curselection():
        selectedIndex = inventoryListbox.curselection()[0]
        selectedId = inventoryLoader.inventory[selectedIndex]["ItemId"]
        selectedName = itemIdLoader.findNameFromId(selectedId)
    
        result = TkEditJsonDialog(window, title=selectedName, 
                                    text=json.dumps(inventoryLoader.inventory[selectedIndex], indent=4)).show()
        try:
            result = json.loads(result)
            
            if inventoryLoader.inventory[selectedIndex] != result:
                print(f"Item {selectedName} ({selectedId}) was changed")
        except ValueError:
            tkmessagebox.showerror("Json Format Error", 
                                   "Change could not be saved since it was not in json format.")
        else:
            inventoryLoader.inventory[selectedIndex] = result
            refreshInventoryList()

def comboboxSelected(event):
    selectedId = itemIdLoader.findIdFromName(selectedItem.get())
    for index, item in enumerate(inventoryLoader.inventory):
        if item["ItemId"] == selectedId:
            listboxSelect(index)
            
    amountSetKnownItem(itemIdLoader.findEntryFromId(selectedId))

def amountSetKnownItem(item):
    amountEntry.delete(0, tk.END)
    
    if inventoryLoader.containsId(item["id"]):
        amountEntry.insert(tk.END, inventoryLoader.findItemFromId(item["id"])["TotalCount"])
    else:
        amountEntry.insert(tk.END, "1")
        
    maxLabel.config(text=f'max {itemIdLoader.findEntryFromId(item["id"])["max"]}')

def listboxSelected(event):
    if inventoryListbox.curselection():
        selectedIndex = inventoryListbox.curselection()
        selectedId = inventoryLoader.inventory[selectedIndex[0]]["ItemId"]
        selectedName = itemIdLoader.findNameFromId(selectedId)
        itemCombobox.set(selectedName)
        amountSetKnownItem(itemIdLoader.findEntryFromId(selectedId))
        
def createUiElements():
    global inventoryListbox
    global amountEntry
    global itemCombobox
    global possibleItems
    global selectedItem
    global maxLabel
    
    #left part of ui
    addItemFrame = tk.Frame(window)
    addItemFrame.pack(expand=True, fill="both", side="left", padx=10, pady=10)
    possibleItems = [item["name"] for item in itemIdLoader.getIds()]
    selectedItem = tk.StringVar(addItemFrame)
    selectedItem.set(possibleItems[0])
    itemCombobox = ttk.Combobox(addItemFrame, textvariable=selectedItem, width=30)
    itemCombobox['values'] = possibleItems
    itemCombobox['state'] = 'readonly'
    itemCombobox.bind("<<ComboboxSelected>>", comboboxSelected)
    itemCombobox.pack(ipadx=5, ipady=5, padx=5, pady=5)
    amountFrame = tk.Frame(addItemFrame)
    amountFrame.pack(ipadx=5, ipady=5, padx=5, pady=5)
    amountLabel = ttk.Label(amountFrame, text="Amount")
    amountLabel.pack(side="left")
    amountEntry = tk.Entry(amountFrame, width="8")
    amountEntry.pack(side="left")
    maxLabel = ttk.Label(amountFrame, text="max 1", width=10)
    maxLabel.pack(side="right")
    amountSetKnownItem(itemIdLoader.itemIds[0])
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
    refreshInventoryList()

itemIdLoader = ItemIdLoader()
itemIdLoader.loadIds()

inventoryLoader = InventoryLoader(itemIdLoader)

window = tk.Tk()
window.title("SotF Inventory Editor")
window.geometry("700x350")
createUiElements()

window.mainloop()