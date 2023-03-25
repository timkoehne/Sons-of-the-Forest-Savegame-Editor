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
from TkNPCTab import TkNPCTab
from TkPlayerTab import TkPlayerTab

def createUiElements():
    
    tabsystem = ttk.Notebook(window)
    
    inventoryTab = TkInventoryTab(itemIdLoader, inventoryLoader)
    worldTab = TkWorldTab(savefileLoader)
    saveFileTab = TkSaveLoadTab(savefileLoader, inventoryTab, worldTab)
    npcTab = TkNPCTab(savefileLoader)
    playerTab = TkPlayerTab(savefileLoader)
    teleportTab = TkTeleportTab(savefileLoader, npcTab, playerTab)
    settingsTab = TkSettingsTab(inventoryTab, savefileLoader, teleportTab)
    
    tabsystem.add(saveFileTab, text="saveFile")
    tabsystem.add(worldTab, text="World")
    tabsystem.add(playerTab, text="Player")
    tabsystem.add(inventoryTab, text="Inventory")
    tabsystem.add(teleportTab, text="Teleport")
    tabsystem.add(npcTab, text="NPCs")
    tabsystem.add(settingsTab, text="Settings")
    
    tabsystem.pack(expand=1, fill="both")

itemIdLoader = ItemIdLoader()
itemIdLoader.loadIds()

savefileLoader = SavefileLoader(itemIdLoader, 
                                "C:/Users/Tim/AppData/LocalLow/Endnight/SonsOfTheForest/Saves/76561198042133385/SinglePlayer/0863039748")
inventoryLoader = savefileLoader.inventoryLoader

window = tk.Tk()
window.title("SotF Inventory Editor")
window.geometry("600x450")
createUiElements()




window.mainloop()