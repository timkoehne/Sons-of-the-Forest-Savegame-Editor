import tkinter as tk
from SavefileLoader import SavefileLoader
import json
from Misc import *
from TkImageViewer import CanvasImage
from HeightMap import HeightMap
import numbers


class TkTeleportTab(tk.Frame):
    
    def __init__(self, saveFileLoader: SavefileLoader):
        super().__init__()
        self.saveFileLoader = saveFileLoader
        
        self.rowconfigure(0, weight=1)  # make the CanvasImage widget expandable
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=6)
    
        leftFrame = tk.Frame(self)
        leftFrame.grid(row=0, column=0)
        self.playerSelectedVar = tk.BooleanVar()
        self.playerCheckbutton = tk.Checkbutton(leftFrame, text="Player", variable=self.playerSelectedVar, fg="red")
        self.playerCheckbutton.pack()
        self.kelvinSelectedVar = tk.BooleanVar()
        self.kelvinCheckbutton = tk.Checkbutton(leftFrame, text="Kelvin", variable=self.kelvinSelectedVar, fg="blue")
        self.kelvinCheckbutton.pack()
        self.virginiaSelectedVar = tk.BooleanVar()
        self.virginiaCheckbutton = tk.Checkbutton(leftFrame, text="Virginia", variable=self.virginiaSelectedVar, fg="green")
        self.virginiaCheckbutton.pack()
        
        self.heightLabelVar = tk.IntVar(self)
        self.heightLabelVar.set("estimated Height: 0")
        tk.Label(leftFrame, textvariable=self.heightLabelVar).pack()
    
        self.heightOffsetVar = tk.StringVar(self)
        tk.Label(leftFrame, text="Offset: ").pack()
        offsetEntry = tk.Entry(leftFrame, textvariable=self.heightOffsetVar)
        offsetEntry.pack(fill="x", expand=True)
        
        #  #TODO wann wird das ausgeführt????
        offsetEntry.bind("<KeyRelease>", self.onOffsetEntry)
        
        
        
        
        self.canvasMap = CanvasImage(self, "heightmap.png", self.onMapRightClick)
        self.canvasMap.grid(row=0, column=1)
        
        self.heightMap = HeightMap()
        
        self.setKnownPositions()
    
    def setKnownPositions(self):
        playerPos = self.getPlayerPos()
        self.setPlayerPos(playerPos)
        kelvinPos = self.saveFileLoader.getKelvinPosition()
        self.setKelvinPos(kelvinPos)
        virginiaPos = self.saveFileLoader.getVirginiaPosition()
        self.setVirginiaPos(virginiaPos)
                
    def setPlayerPos(self, ingamePos):
        print("Setting Player position to" , ingamePos)
        
        bboxMap = self.canvasMap.getImageBBox()
        imagePos = transformCoordinatesystemToImage(ingamePos, bboxMap)
        self.canvasMap.markPlayerPos(imagePos, ICONSIZE, color=self.playerCheckbutton["fg"])
        
        playerPosSetting = self.saveFileLoader.findPlayerSetting("player.position")
        SavefileLoader.setRelevantSettingsValue(playerPosSetting, ingamePos)
        
    def getPlayerPos(self):
        playerPosSetting = self.saveFileLoader.findPlayerSetting("player.position")
        return SavefileLoader.getRelevantSettingsValue(playerPosSetting)
    
    def setKelvinPos(self, ingamePos):
        print("Setting Kelvin position to" , ingamePos)
        
        bboxMap = self.canvasMap.getImageBBox()
        imagePos = transformCoordinatesystemToImage(ingamePos, bboxMap)
        self.canvasMap.markKelvinPos(imagePos, ICONSIZE, color=self.kelvinCheckbutton["fg"])
        
        posDict = self.createPositionDict(ingamePos)
        self.saveFileLoader.setKelvinPosition(posDict)

    def setVirginiaPos(self, ingamePos):
        print("Setting Virginia position to" , ingamePos)
        
        bboxMap = self.canvasMap.getImageBBox()
        imagePos = transformCoordinatesystemToImage(ingamePos, bboxMap)
        self.canvasMap.markVirginiaPos(imagePos, ICONSIZE, color=self.virginiaCheckbutton["fg"])
        
        posDict = self.createPositionDict(ingamePos)
        self.saveFileLoader.setVirginiaPosition(posDict)
        
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