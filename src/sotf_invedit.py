import json
import tkinter as tk
from tkinter import ttk
from ItemIdLoader import ItemIdLoader
from SavefileLoader import SavefileLoader
from TkInventoryTab import TkInventoryTab
from TkSaveLoadTab import TkSaveLoadTab
from TkSettingsTab import TkSettingsTab
from TkWorldTab import TkWorldTab
from TkTeleportTab import TkTeleportTab

def createUiElements():
    
    tabsystem = ttk.Notebook(window)
    
    inventoryTab = TkInventoryTab(itemIdLoader, inventoryLoader)
    worldTab = TkWorldTab(savefileLoader)
    teleportTab = TkTeleportTab(savefileLoader)
    saveFileTab = TkSaveLoadTab(savefileLoader, inventoryTab, worldTab)
    settingsTab = TkSettingsTab(inventoryTab, savefileLoader, teleportTab)
    
    tabsystem.add(saveFileTab, text="saveFile")
    tabsystem.add(worldTab, text="World")
    tabsystem.add(inventoryTab, text="Inventory")
    tabsystem.add(teleportTab, text="Teleport")
    tabsystem.add(settingsTab, text="Settings")
    
    tabsystem.pack(expand=1, fill="both")

itemIdLoader = ItemIdLoader()
itemIdLoader.loadIds()

savefileLoader = SavefileLoader(itemIdLoader, 
                                "C:/Users/Tim/AppData/LocalLow/Endnight/SonsOfTheForest/Saves/76561198042133385/SinglePlayer/1445249876")
inventoryLoader = savefileLoader.inventoryLoader

window = tk.Tk()
window.title("SotF Inventory Editor")
window.geometry("600x350")
createUiElements()




window.mainloop()