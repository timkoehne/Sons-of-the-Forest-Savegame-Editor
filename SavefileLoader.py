import json
import os
from tkinter import filedialog as tkfiledialog
from ItemIdLoader import ItemIdLoader
from InventoryLoader import InventoryLoader

jsonFiletypes = (
    ('json file', '*.json'),
    ('All files', '*.*')
)

GAMESTATEFILE =  "/GameStateSaveData.json"
SAVEDATAFILE = "/SaveData.json"
INVENTORYFILE = "/PlayerInventorySaveData.json"


class SavefileLoader:
    def __init__(self, itemIdLoader: ItemIdLoader, saveFolderPath=None) -> None:
        self.inventoryLoader = InventoryLoader(itemIdLoader)
        self.load(saveFolderPath)

    def load(self, saveFolderPath=None):
        if saveFolderPath is None:
            saveFolderPath = selectFolder()
            
        gameStatePath = saveFolderPath + GAMESTATEFILE
        gameSavePath = saveFolderPath + SAVEDATAFILE
        self.readGamestateAndGamesave(gameStatePath, gameSavePath)
        self.inventoryLoader.loadInventory(saveFolderPath + INVENTORYFILE)
        self.saveTestdata()

    def save(self, saveFolderPath=None):
        if saveFolderPath is None:
            saveFolderPath = selectFolder()
        
        gameStatePath = saveFolderPath + GAMESTATEFILE
        gameSavePath = saveFolderPath + SAVEDATAFILE
        self.saveGamestateAndGamesave(gameStatePath, gameSavePath)
        self.inventoryLoader.saveInventory(saveFolderPath + INVENTORYFILE)

    def readGamestateAndGamesave(self, gameStatePath, gameSavePath):
        with open(gameStatePath, "r") as file:
            self.gameStateContent = json.loads(file.read())
            self.gamestate = json.loads(self.gameStateContent["Data"]["GameState"])

        with open(gameSavePath, "r") as file:
            self.gameSaveContent = json.loads(file.read())
            self.savedata = self.gameSaveContent["Data"]
            self.vailworldsim = json.loads(self.savedata["VailWorldSim"])
            self.actors = self.vailworldsim["Actors"]

    def revive(self, kelvin=False, virginia=False):
        self.readGamestateAndGamesave()
        if kelvin:
            self.gamestate["IsRobbyDead"] = False
            for actor in self.actors:
                if actor["TypeId"] == 9:
                    actor["State"] = 2
                    actor["Health"] = 100
                    break
        if virginia:
            self.gamestate["IsVirginiaDead"] = False
            for actor in self.actors:
                if actor["TypeId"] == 10:
                    actor["State"] = 2
                    actor["Health"] = 100
        self.saveGamestateAndGamesave()

    def kill(self, kelvin=False, virginia=False):
        self.readGamestateAndGamesave()
        if kelvin:
            self.gamestate["IsRobbyDead"] = True
            for actor in self.actors:
                if actor["TypeId"] == 9:
                    actor["State"] = 6
                    actor["Health"] = 0.0
                    break
        if virginia:
            self.gamestate["IsVirginiaDead"] = True
            for actor in self.actors:
                if actor["TypeId"] == 10:
                    actor["State"] = 6
                    actor["Health"] = 0.0
        self.saveGamestateAndGamesave()

    def countNumActors(self):
        self.readGamestateAndGamesave()
        typeIds = {}
        for actor in self.actors:
            if not actor["TypeId"] in typeIds:
                typeIds[actor["TypeId"]] = 0
            typeIds[actor["TypeId"]] += 1

        typeIds = dict(sorted(typeIds.items()))
        for key, value in typeIds.items():
            print(f'{key} exists {value} times')

    def saveGamestateAndGamesave(self, gameStatePath, gameSavePath):
        with open(gameStatePath, "w") as file:
            self.gameStateContent["Data"]["GameState"] = json.dumps(self.gamestate)
            file.write(json.dumps(self.gameStateContent))

        with open(gameSavePath, "w") as file:
            self.vailworldsim["Actors"] = self.actors
            self.savedata["VailWorldSim"] = json.dumps(self.vailworldsim)
            self.gameSaveContent["Data"] = self.savedata
            file.write(json.dumps(self.gameSaveContent))

    def saveTestdata(self):
        with open("actors.json", "w") as file:
            file.write(json.dumps(self.vailworldsim, indent=4))
            
        with open("gameState.json", "w") as file:
            file.write(json.dumps(self.gamestate, indent=4))

def selectFolder():
        numberedFolder = os.listdir(f"C:/Users/{os.getlogin()}/AppData/LocalLow/Endnight/SonsOfTheForest/Saves/.")[0]
        saveFolderPath = tkfiledialog.askdirectory(title="Select Save File", 
                                initialdir=f"C:/Users/{os.getlogin()}/AppData/LocalLow/Endnight/SonsOfTheForest/Saves/{numberedFolder}/")
        
        files = os.listdir(saveFolderPath)
        filePaths = map(lambda name: os.path.join(saveFolderPath, name), os.listdir(saveFolderPath))
        subfolders = []
        for file in filePaths:
            if os.path.isdir(file):
                subfolders.append(file)
                
        if len(subfolders) > 0:
            saveFolderPath = subfolders[0]
        return saveFolderPath







