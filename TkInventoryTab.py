import tkinter as tk
from tkinter import ttk
from TkSearchableCombobox import TkSearchableCombobox
from ItemIdLoader import ItemIdLoader
from InventoryLoader import InventoryLoader
from tkinter import messagebox as tkmessagebox
from tkinter import messagebox as tkmessagebox
from TkEditJsonDialog import TkEditJsonDialog
import json

class TkInventoryTab(tk.Frame):
    def __init__(self, itemIdLoader: ItemIdLoader, inventoryLoader: InventoryLoader):
        super().__init__()
        
        self.itemIdLoader = itemIdLoader
        self.inventoryLoader = inventoryLoader
        
        self.initUi()
        
    def initUi(self):
        # left
        self.addItemFrame = tk.Frame(self)
        self.addItemFrame.pack(side="left")
        self.possibleItems = [item["name"] for item in self.itemIdLoader.getIds()]
        self.selectedItem = tk.StringVar(self)
        self.selectedItem.set(self.possibleItems[0])
        self.itemCombobox = TkSearchableCombobox(self.addItemFrame, textvariable=self.selectedItem, width=30)
        self.itemCombobox['values'] = self.possibleItems
        self.itemCombobox['state'] = 'readonly'
        self.itemCombobox.bind("<<ComboboxSelected>>", self.comboboxSelected)
        self.itemCombobox.bind("<KeyRelease>", self.itemCombobox.popup_key_pressed)
        self.itemCombobox.pack(ipadx=5, ipady=5, padx=5, pady=5)
        self.amountFrame = tk.Frame(self.addItemFrame)
        self.amountFrame.pack(ipadx=5, ipady=5, padx=5, pady=5)
        self.amountLabel = ttk.Label(self.amountFrame, text="Amount")
        self.amountLabel.pack(side="left")
        self.amountEntry = tk.Entry(self.amountFrame, width="8")
        self.amountEntry.pack(side="left")
        self.maxLabel = ttk.Label(self.amountFrame, text="max 1", width=10)
        self.maxLabel.pack(side="right")
        self.amountSetKnownItem(self.itemIdLoader.itemIds[0])
        self.addButton = tk.Button(self.addItemFrame, text="Set Amount", command=self.setAmount)
        self.addButton.pack(ipadx=5, ipady=5, padx=5, pady=5)
        
        # right
        self.inventoryLabel = ttk.Label(self, text="Inventory")
        self.inventoryLabel.pack(side="top")
        self.inventoryScrollbar = tk.Scrollbar(self)
        self.inventoryScrollbar.pack(side="right", fill="y", pady=5)
        self.inventoryListbox = tk.Listbox(self, yscrollcommand=self.inventoryScrollbar.set)
        self.inventoryListbox.pack(side="right", expand=True, fill="both", pady=5)
        self.inventoryListbox.bind("<Double-1>", self.viewItemJson)
        self.inventoryListbox.bind("<<ListboxSelect>>", self.listboxSelected)
        self.inventoryListbox.bind("<KeyRelease>", self.inventoryKeyPressed)
        self.inventoryScrollbar.config(command=self.inventoryListbox.yview)
        
        self.comboboxSelected("")
        self.refreshInventoryList()
        
    def setAmount(self):
        selected = self.selectedItem.get()
        amount = int(self.amountEntry.get())
        
        self.inventoryLoader.setAmount(selected, amount)
        
        self.listboxSelect(self.inventoryLoader.findIndexInInventory(selected))
        self.refreshInventoryList()
        
    def listboxSelected(self, event):
        if self.inventoryListbox.curselection():
            selectedIndex = self.inventoryListbox.curselection()
            selectedId = self.inventoryLoader.inventory[selectedIndex[0]]["ItemId"]
            selectedName = self.itemIdLoader.findNameFromId(selectedId)
            self.itemCombobox.set(selectedName)
            self.amountSetKnownItem(self.itemIdLoader.findEntryFromId(selectedId))
            
    def comboboxSelected(self, event):
        selectedId = self.itemIdLoader.findIdFromName(self.selectedItem.get())
        for index, item in enumerate(self.inventoryLoader.inventory):
            if str(item["ItemId"]) == str(selectedId):
                self.listboxSelect(index)
                
        self.amountSetKnownItem(self.itemIdLoader.findEntryFromId(selectedId))

    def amountSetKnownItem(self, item):
        self.amountEntry.delete(0, tk.END)
        
        if self.inventoryLoader.containsId(item["id"]):
            self.amountEntry.insert(tk.END, self.inventoryLoader.findItemFromId(item["id"])["TotalCount"])
        else:
            self.amountEntry.insert(tk.END, "1")
            
        self.maxLabel.config(text=f'max {self.itemIdLoader.findEntryFromId(item["id"])["max"]}')

    def inventoryKeyPressed(self, event):
        if event.keysym == "Delete":
            selection = self.inventoryListbox.curselection()
            self.inventoryLoader.deleteFromInventory(selection)
            self.refreshInventoryList()

    def listboxSelect(self, index: int):
        self.inventoryListbox.selection_set(index)
        self.inventoryListbox.activate(index)
        self.inventoryListbox.see(index)
        
    def viewItemJson(self, event):
        if self.inventoryListbox.curselection():
            selectedIndex = self.inventoryListbox.curselection()[0]
            selectedId = self.inventoryLoader.inventory[selectedIndex]["ItemId"]
            selectedName = self.itemIdLoader.findNameFromId(selectedId)
        
            result = TkEditJsonDialog(self, title=selectedName, 
                                        text=json.dumps(self.inventoryLoader.inventory[selectedIndex], indent=4)).show()
            try:
                result = json.loads(result)
                
                if self.inventoryLoader.inventory[selectedIndex] != result:
                    print(f"Item {selectedName} ({selectedId}) was changed")
            except ValueError:
                tkmessagebox.showerror("Json Format Error", 
                                    "Change could not be saved since it was not in json format.")
            else:
                self.inventoryLoader.inventory[selectedIndex] = result
                self.refreshInventoryList()

    def reloadItemIds(self):
        self.itemIdLoader.loadIdsFromGamefiles()
        self.possibleItems = sorted([item["name"] for item in self.itemIdLoader.getIds()])
        self.itemCombobox['values'] = self.possibleItems

    def refreshInventoryList(self):
        selected = self.inventoryListbox.curselection()
        yview = self.inventoryListbox.yview()
        self.inventoryListbox.delete(0, tk.END)
        
        for index, item in enumerate(self.inventoryLoader.inventory):
            name = self.itemIdLoader.findNameFromId(item["ItemId"])
            amount = item["TotalCount"]
            self.inventoryListbox.insert(index+1, name + " " + str(amount) + "x")
        for s in selected:
            self.listboxSelect(s)
        self.inventoryListbox.yview_moveto(yview[0])
