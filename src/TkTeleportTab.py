import tkinter as tk
from SavefileLoader import SavefileLoader
import json
from Misc import *
from TkImageViewer import CanvasImage
from HeightMap import HeightMap
from TkNPCTab import TkNPCTab


class TkTeleportTab(tk.Frame):
    
    def __init__(self, saveFileLoader: SavefileLoader, npcTab, playerTab):
        super().__init__()
        self.saveFileLoader = saveFileLoader
        self.npcTab = npcTab
        self.playerTab = playerTab
        
        self.rowconfigure(0, weight=1)  # make the CanvasImage widget expandable
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=6)
    
        leftFrame = tk.Frame(self)
        leftFrame.grid(row=0, column=0, sticky="nesw", padx=5, pady=5)
        
        leftTopFrame = tk.Frame(leftFrame)
        leftTopFrame.pack()
        leftBottomFrame = tk.Frame(leftFrame)
        leftBottomFrame.pack(fill="y", expand=True)
        
        self.playerSelectedVar = tk.BooleanVar()
        self.playerCheckbutton = tk.Checkbutton(leftTopFrame, text="Player", variable=self.playerSelectedVar, fg="red")
        self.playerCheckbutton.pack(side="top")
        self.kelvinSelectedVar = tk.BooleanVar()
        self.kelvinCheckbutton = tk.Checkbutton(leftTopFrame, text="Kelvin", variable=self.kelvinSelectedVar, fg="blue")
        self.kelvinCheckbutton.pack(side="top")
        self.virginiaSelectedVar = tk.BooleanVar()
        self.virginiaCheckbutton = tk.Checkbutton(leftTopFrame, text="Virginia", variable=self.virginiaSelectedVar, fg="green")
        self.virginiaCheckbutton.pack(side="top")
    
        offsetFrame = tk.Frame(leftBottomFrame)
        offsetFrame.pack(side="bottom")
        self.heightOffsetVar = tk.StringVar(self)
        tk.Label(offsetFrame, text="Offset: ").pack(side="left")
        offsetEntry = tk.Entry(offsetFrame, textvariable=self.heightOffsetVar, width=8)
        offsetEntry.pack(side="left")
        offsetEntry.bind("<KeyRelease>", self.onOffsetEntry)
        
        self.heightLabelVar = tk.IntVar(self)
        self.heightLabelVar.set("estimated Height: 0")
        tk.Label(leftBottomFrame, textvariable=self.heightLabelVar, width=20).pack(side="bottom")
    
        self.initializePointsOfInterest(leftBottomFrame)
    
        self.canvasMap = CanvasImage(self, "../res/map.png", self.onMapRightClick)
        self.canvasMap.grid(row=0, column=1)
        
        self.heightMap = HeightMap()
        
        self.setKnownPositions()
    
    def initializePointsOfInterest(self, frame):
        with open("../res/pointsOfInterest.json", "r") as file:
            self.pointsOfInterestJson = json.loads(file.read())
            
            
        for category in self.pointsOfInterestJson:
            poiCategoryVar = tk.BooleanVar()
            poiCategoryCheckbox = tk.Checkbutton(frame, text=f"Show {category['Name']}", fg=category["Color"],
                                    variable=poiCategoryVar, command=lambda poiVar=poiCategoryVar, category=category['Name']: 
                                    self.showPointsOfInterest(poiVar, category))
            poiCategoryCheckbox.pack(side="bottom")
     
    def getPointsOfInterestAndColor(self, filter: str):
        positions = []
        color = "pink"
        for poi in self.pointsOfInterestJson:
            if filter in poi["Name"]:
                color = poi["Color"]
                for pos in poi["Positions"]:
                    positions.append([pos[0], pos[1], pos[2]])
        return positions, color
    
    def showPointsOfInterest(self, checkboxVar: tk.BooleanVar, filter: str):
        self.canvasMap.togglePointsOfInterest(filter)
        if checkboxVar.get():
            bboxMap = self.canvasMap.getImageBBox()
            positionData, color = self.getPointsOfInterestAndColor(filter)
            for position in positionData:
                imagePos = transformCoordinatesystemToImage(position, bboxMap)
                self.canvasMap.addPointOfInterest(filter, imagePos, ICONSIZE, color=color)
    
    def setKnownPositions(self):
        playerPos = self.getPlayerPos()
        self.setPlayerPos(playerPos)
        kelvinPos = self.npcTab.getPosition("Kelvin")
        self.setKelvinPos(kelvinPos)
        virginiaPos = self.npcTab.getPosition("Virginia")
        self.setVirginiaPos(virginiaPos)
                
    def setPlayerPos(self, ingamePos):
        print("Setting Player position to" , ingamePos)
        
        bboxMap = self.canvasMap.getImageBBox()
        imagePos = transformCoordinatesystemToImage(ingamePos, bboxMap)
        self.canvasMap.markPlayerPos(imagePos, ICONSIZE, color=self.playerCheckbutton["fg"])
        
        playerPosSetting = self.playerTab.findPlayerSetting("player.position")
        SavefileLoader.setRelevantSettingsValue(playerPosSetting, ingamePos)
        
    def getPlayerPos(self):
        playerPosSetting = self.playerTab.findPlayerSetting("player.position")
        pos = SavefileLoader.getRelevantSettingsValue(playerPosSetting)
        return [pos[0], pos[1], pos[2]]
    
    def setKelvinPos(self, ingamePos):
        print("Setting Kelvin position to" , ingamePos)
        
        bboxMap = self.canvasMap.getImageBBox()
        imagePos = transformCoordinatesystemToImage(ingamePos, bboxMap)
        self.canvasMap.markKelvinPos(imagePos, ICONSIZE, color=self.kelvinCheckbutton["fg"])
        
        posDict = self.createPositionDict(ingamePos)
        self.npcTab.setPosition("Kelvin", posDict)

    def setVirginiaPos(self, ingamePos):
        print("Setting Virginia position to" , ingamePos)
        
        bboxMap = self.canvasMap.getImageBBox()
        imagePos = transformCoordinatesystemToImage(ingamePos, bboxMap)
        self.canvasMap.markVirginiaPos(imagePos, ICONSIZE, color=self.virginiaCheckbutton["fg"])
        
        posDict = self.createPositionDict(ingamePos)
        self.npcTab.setPosition("Virginia", posDict)
        
    def onOffsetEntry(self, event):
        
        offset = 0
        try:
            offset = int(self.heightOffsetVar.get())
        except ValueError:
            pass
        
        if self.playerSelectedVar.get():
            pos = self.getPlayerPos()
            height = round(self.getHeight((pos[0], pos[2])), 2)
            pos[1] = height + offset
            self.setPlayerPos(pos)
        if self.kelvinSelectedVar.get():
            pos = self.saveFileLoader.getKelvinPosition()
            height = round(self.getHeight((pos[0], pos[2])), 2)
            pos[1] = height + offset
            self.setKelvinPos(pos)
        if self.virginiaSelectedVar.get():
            pos = self.saveFileLoader.getVirginiaPosition()
            height = round(self.getHeight((pos[0], pos[2])), 2)
            pos[1] = height + offset
            self.setVirginiaPos(pos)
        
    def onMapRightClick(self, imagePos):
        bboxMap = self.canvasMap.getImageBBox()
        coordX, coordZ = transformCoordinatesystemToIngame(imagePos, bboxMap)
        # print("ingame coords", coordX, coordZ)
        # print("image coords", self.transformCoordinatesystemToImage(coordX, coordZ), bboxMap)

        height = round(self.getHeight((coordX, coordZ)), 2)
        self.heightLabelVar.set(f"estimated Height: {height}")
        
        
        try:
            offset = int(self.heightOffsetVar.get())
            height += offset
        except ValueError:
            pass
        newPos = (coordX, height, coordZ)
        
        if self.playerSelectedVar.get():
            self.setPlayerPos(newPos)
        if self.kelvinSelectedVar.get():
            self.setKelvinPos(newPos)
        if self.virginiaSelectedVar.get():
            self.setVirginiaPos(newPos)
        
    def getHeight(self, ingamePos) -> float:
        return self.heightMap.getHeight(ingamePos)
     
    def createPositionDict(self, ingamePos):
        return {
            "x": ingamePos[0],
            "y": ingamePos[1],
            "z": ingamePos[2]
        }