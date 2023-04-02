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
    for tab in tabsystem.tabs()[1:]:
        tabsystem.forget(tab)
    
    inventoryTab = TkInventoryTab(itemIdLoader, inventoryLoader)
    worldTab = TkWorldTab(savefileLoader)
    npcTab = TkNPCTab(savefileLoader)
    playerTab = TkPlayerTab(savefileLoader)
    teleportTab = TkTeleportTab(savefileLoader, npcTab, playerTab)
    settingsTab = TkSettingsTab(inventoryTab, savefileLoader, teleportTab)
    tabsystem.add(worldTab, text="World")
    tabsystem.add(playerTab, text="Player")
    tabsystem.add(inventoryTab, text="Inventory")
    tabsystem.add(teleportTab, text="Teleport")
    tabsystem.add(npcTab, text="NPCs")
    tabsystem.add(settingsTab, text="Settings")

itemIdLoader = ItemIdLoader()
itemIdLoader.loadIds()

savefileLoader = SavefileLoader(itemIdLoader)
inventoryLoader = savefileLoader.inventoryLoader

window = tk.Tk()
window.title("SotF Inventory Editor")
window.geometry("600x460")


tabsystem = ttk.Notebook(window)
saveFileTab = TkSaveLoadTab(savefileLoader, createUiElements)

tabsystem.add(saveFileTab, text="saveFile")

tabsystem.pack(expand=1, fill="both")


window.mainloop()