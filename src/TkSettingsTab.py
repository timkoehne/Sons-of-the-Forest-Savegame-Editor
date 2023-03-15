import tkinter as tk
from tkinter import ttk
from TkInventoryTab import TkInventoryTab
import HeightMap as HeightMap
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
        
        saveKnownItemsButton = tk.Button(heightmapFrame, text="Save Actor Ids", command=self.saveActorIds)
        saveKnownItemsButton.grid(row=2, column=0, columnspan=2, ipadx=5, ipady=5, padx=5, pady=5)
        
    def saveActorIds(self):
        posDict = []
        
        with open("../res/knownActorPositions.json", "r") as file:
            posDict = json.loads(file.read())
        
        positionData = self.savefileLoader.getPositiondataForActorId(HeightMap.ACTORSFORHEIGHTMAP)
        for pos in positionData:
            posDict.append(
                {
                    "FloatArrayValue": [
                        pos[0],
                        pos[1],
                        pos[2]
                    ]
                }
            )
        
        with open("../res/knownActorPositions.json", "w") as file:
            file.write(json.dumps(posDict, indent=4))
        
        
    def toggleHeightmapActors(self):
        
        #test
        #countNumActors(self.saveFileLoader.actors)
        
        if self.showPositions.get():
            bboxMap = self.tkTeleportTab.canvasMap.getImageBBox()
            positionData = self.getPositionData()
            for position in positionData:
                imagePos = transformCoordinatesystemToImage(position, bboxMap)
                self.tkTeleportTab.canvasMap.markPos(imagePos, ICONSIZE, color="yellow")
        else:
            self.tkTeleportTab.canvasMap.deleteOtherMarks()
        
    def generateHeightmap(self):
        
        positionData = self.getPositionData()
        HeightMap.generateHeightmap(positionData, self.selectedHeightmapMethod.get())
        self.tkTeleportTab.heightMap = HeightMap()
        
    def getPositionData(self):
        positionData = []
        # positionData = self.savefileLoader.getPositiondataForActorId(HeightMap.ACTORSFORHEIGHTMAP)
        numActorPositions = len(positionData)
                
        knownHeights = ""
        with open("../res/knownActorPositions.json") as file:
            knownHeights = json.loads(file.read())
        
        for entry in knownHeights:
            try:
                positionData.append(entry["FloatArrayValue"])
            except KeyError:
                pass
        print(f"There are {numActorPositions} positions from actors")
        print(f"There are {len(positionData) - numActorPositions} manually added positions")
        print(f"For a total of {len(positionData)} positions")
        return positionData