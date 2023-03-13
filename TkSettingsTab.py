import tkinter as tk
from tkinter import ttk
from TkInventoryTab import TkInventoryTab
import HeightMap
from SavefileLoader import SavefileLoader
from HeightMap import HeightMap
from TkTeleportTab import TkTeleportTab
from Misc import *

class TkSettingsTab(tk.Frame):
    
    def __init__(self, inventoryTab: TkInventoryTab, savefileLoader: SavefileLoader, tkTeleportTab: TkTeleportTab):
        super().__init__()
        self.savefileLoader = savefileLoader
        self.tkTeleportTab = tkTeleportTab
        
        #reload item ids
        itemIdFrame = tk.Frame(self, highlightthickness=1, highlightbackground="black")
        itemIdFrame.pack(ipadx=5, ipady=5, padx=5, pady=5)
        reloadKnownItemsButton = tk.Button(itemIdFrame, text="Reload Item Ids", command=inventoryTab.reloadItemIds)
        reloadKnownItemsButton.pack(side="left", ipadx=5, ipady=5, padx=5, pady=5)
        saveKnownItemsButton = tk.Button(itemIdFrame, text="Save Item Ids", command=inventoryTab.itemIdLoader.saveIds)
        saveKnownItemsButton.pack(side="left", ipadx=5, ipady=5, padx=5, pady=5)        

        #heightmap
        heightmapFrame = tk.Frame(self, highlightthickness=1, highlightbackground="black")
        heightmapFrame.pack(ipadx=5, ipady=5, padx=5, pady=5)
        self.selectedHeightmapMethod = tk.StringVar()
        heightmapCombobox = ttk.Combobox(heightmapFrame, textvariable=self.selectedHeightmapMethod, width=15)
        heightmapCombobox['values'] = ["linear", "nearest", "cubic"]
        self.selectedHeightmapMethod.set(heightmapCombobox["values"][0])
        heightmapCombobox['state'] = 'readonly'
        heightmapCombobox.grid(row=0, column=0, ipadx=5, ipady=5, padx=5, pady=5)
        generateHeightmapButton = tk.Button(heightmapFrame, text="Generate Heightmap", command=self.generateHeightmap)
        generateHeightmapButton.grid(row=0, column=1, ipadx=5, ipady=5, padx=5, pady=5)
        self.showPositions = tk.BooleanVar(self)
        showHeightmapBox = tk.Checkbutton(heightmapFrame, text="Show Positions for generating heightmap", variable=self.showPositions, command=self.toggleHeightmapActors)
        showHeightmapBox.grid(row=1, column=0, columnspan=2, ipadx=5, ipady=5, padx=5, pady=5)
        
    def toggleHeightmapActors(self):
        
        #test
        #countNumActors(self.saveFileLoader.actors)
        
        if self.showPositions.get():
            bboxMap = self.tkTeleportTab.canvasMap.getImageBBox()
            positionData = self.savefileLoader.getPositiondataForActorId(HeightMap.ACTORSFORHEIGHTMAP)
            for position in positionData:
                imagePos = transformCoordinatesystemToImage(position, bboxMap)
                self.tkTeleportTab.canvasMap.markPos(imagePos, ICONSIZE, color="yellow")
        else:
            self.tkTeleportTab.canvasMap.deleteOtherMarks()
        
    def generateHeightmap(self):
        positionData = self.savefileLoader.getPositiondataForActorId(HeightMap.ACTORSFORHEIGHTMAP)
        self.tkTeleportTab.heightMap = HeightMap.generateHeightmap(positionData, self.selectedHeightmapMethod.get())