import tkinter as tk
from tkinter import ttk
from TkInventoryTab import TkInventoryTab


class TkSettingsTab(tk.Frame):
    def __init__(self, inventoryTab: TkInventoryTab):
        super().__init__()

        reloadKnownItemsButton = tk.Button(self, text="Reload Item Ids", command=inventoryTab.reloadItemIds)
        reloadKnownItemsButton.pack(ipadx=5, ipady=5, padx=5, pady=5)
        saveKnownItemsButton = tk.Button(self, text="Save Item Ids", command=inventoryTab.itemIdLoader.saveIds)
        saveKnownItemsButton.pack(ipadx=5, ipady=5, padx=5, pady=5)