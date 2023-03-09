import json
import tkinter as tk
from tkinter import ttk
from ItemIdLoader import ItemIdLoader
from SavefileLoader import SavefileLoader
from TkInventoryTab import TkInventoryTab
from TkSaveLoadTab import TkSaveLoadTab
from TkSettingsTab import TkSettingsTab
from TkWorldTab import TkWorldTab

def createUiElements():
    
    tabsystem = ttk.Notebook(window)
    
    inventoryTab = TkInventoryTab(itemIdLoader, inventoryLoader)
    settingsTab = TkSettingsTab(inventoryTab)
    worldTab = TkWorldTab(savefileLoader)
    saveFileTab = TkSaveLoadTab(savefileLoader, inventoryTab, worldTab)
    
    tabsystem.add(saveFileTab, text="saveFile")
    tabsystem.add(worldTab, text="World")
    tabsystem.add(inventoryTab, text="Inventory")
    tabsystem.add(settingsTab, text="Settings")
    
    tabsystem.pack(expand=1, fill="both")

itemIdLoader = ItemIdLoader()
itemIdLoader.loadIds()

savefileLoader = SavefileLoader(itemIdLoader)


inventoryLoader = savefileLoader.inventoryLoader

window = tk.Tk()
window.title("SotF Inventory Editor")
window.geometry("600x350")
createUiElements()




window.mainloop()