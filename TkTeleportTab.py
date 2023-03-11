import tkinter as tk
from SavefileLoader import SavefileLoader
import json
from Misc import *
from ImageViewer import CanvasImage

ICONSIZE = 50
MAPIMAGESIZE = 4096
imageToIngameScalingFactor = 0.9765


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
        
        
        tk.Label(leftFrame, text="Height:").pack()
        self.heightVar = tk.IntVar(self)
        tk.Entry(leftFrame, textvariable=self.heightVar).pack(fill="x", expand=True)
        
        self.mapCanvas = CanvasImage(self, "map.png", self.onMapRightClick)
        self.mapCanvas.grid(row=0, column=1)
        
        
        print("Loading initial entity positions")
        playerPos = self.getPlayerPos()
        self.setPlayerPos(playerPos)
        
        kelvinPos = self.saveFileLoader.getKelvinPosition()
        self.setKelvinPos(kelvinPos)
        
        virginiaPos = self.saveFileLoader.getVirginiaPosition()
        self.setVirginiaPos(virginiaPos)
        
        
    def setPlayerPos(self, ingamePos):
        print("Setting Player position to" , ingamePos)
        
        imagePos = self.transformCoordinatesystemToImage(ingamePos)
        self.mapCanvas.markPlayerPos(imagePos, ICONSIZE, color=self.playerCheckbutton["fg"])
        
        playerPosSetting = self.saveFileLoader.findPlayerSetting("player.position")
        SavefileLoader.setRelevantSettingsValue(playerPosSetting, ingamePos)
        
    def getPlayerPos(self):
        playerPosSetting = self.saveFileLoader.findPlayerSetting("player.position")
        return SavefileLoader.getRelevantSettingsValue(playerPosSetting)
    
    def setKelvinPos(self, ingamePos):
        print("Setting Kelvin position to" , ingamePos)
        
        imagePos = self.transformCoordinatesystemToImage(ingamePos)
        self.mapCanvas.markKelvinPos(imagePos, ICONSIZE, color=self.kelvinCheckbutton["fg"])
        
        posDict = self.createPositionDict(ingamePos)
        self.saveFileLoader.setKelvinPosition(posDict)

    def setVirginiaPos(self, ingamePos):
        print("Setting Virginia position to" , ingamePos)
        
        imagePos = self.transformCoordinatesystemToImage(ingamePos)
        self.mapCanvas.markVirginiaPos(imagePos, ICONSIZE, color=self.virginiaCheckbutton["fg"])
        
        posDict = self.createPositionDict(ingamePos)
        self.saveFileLoader.setVirginiaPosition(posDict)
        
    def onMapRightClick(self, imagePos):
        coordX, coordZ = self.transformCoordinatesystemToIngame(imagePos)
        # print("ingame coords", coordX, coordZ)
        # print("image coords", self.transformCoordinatesystemToImage(coordX, coordZ))
        
        newPos = (coordX, self.getHeight((coordX, coordZ)), coordZ)
        
        if self.playerSelectedVar.get():
            self.setPlayerPos(newPos)
        if self.kelvinSelectedVar.get():
            self.setKelvinPos(newPos)
        if self.virginiaSelectedVar.get():
            self.setVirginiaPos(newPos)
        
    def getHeight(self, ingamePos):
        return self.heightVar.get()
    
    def transformCoordinatesystemToIngame(self, mapPos):
        #image coordinate system is (0,0) in the top left and positive x,y to right and bottom
        #ingame coordinate system is (0,0) in the center of the map, north is z positive, east is x positive
        bboxMap = self.mapCanvas.getImageBBox()
        width = bboxMap[2] - bboxMap[0]
        height = bboxMap[3] - bboxMap[1]
        percentX = (mapPos[0] - bboxMap[0]) / width
        percentY = (mapPos[1] - bboxMap[1]) / height
        
        coordX = percentX - 0.5
        coordY = (percentY - 0.5) * -1
        
        coordX = coordX * imageToIngameScalingFactor * MAPIMAGESIZE
        coordY = coordY * imageToIngameScalingFactor * MAPIMAGESIZE
        
        return coordX, coordY
    
    def transformCoordinatesystemToImage(self, ingamePos):
        #image coordinate system is (0,0) in the top left and positive x,y to right and bottom
        #ingame coordinate system is (0,0) in the center of the map, north is z positive, east is x positive
        bboxMap = self.mapCanvas.getImageBBox()
        width = bboxMap[2] - bboxMap[0]
        height = bboxMap[3] - bboxMap[1]
        
        if len(ingamePos) == 2:
            xIngame = ingamePos[0]
            yIngame = ingamePos[1]
        elif len(ingamePos) == 3: 
            xIngame = ingamePos[0]
            yIngame = ingamePos[2]
        
        
        xIngame = xIngame / imageToIngameScalingFactor / MAPIMAGESIZE
        yIngame = yIngame / imageToIngameScalingFactor / MAPIMAGESIZE
        
        percentX = xIngame + 0.5
        percentY = -yIngame + 0.5
        
        xMap = (percentX * width) + bboxMap[0]
        yMap = (percentY * height) + bboxMap[1]
        
        return xMap, yMap
    
    def createPositionDict(self, ingamePos):
        return {
            "x": ingamePos[0],
            "y": ingamePos[1],
            "z": ingamePos[2]
        }        