import json
import os
from tkinter import filedialog as tkfiledialog
from ItemIdLoader import ItemIdLoader
from InventoryLoader import InventoryLoader

jsonFiletypes = (
    ('json file', '*.json'),
    ('All files', '*.*')
)

class Setting():
    def __init__(self, name, options):
        self.name = name
        self.options = options

SETTINGS = {
    "Difficulty": Setting("Mode", ["Custom", "Hard", "Normal", "Peaceful"]),
    "CrashSite": Setting("CrashSite", ["tree", "ocean", "snow"]),
    "EnemySpawn": Setting("GameSetting.Vail.EnemySpawn", []),
    "EnemyHealth": Setting("GameSetting.Vail.EnemyHealth", ["High", "Normal", "Low"]),
    "EnemyDamage": Setting("GameSetting.Vail.EnemyDamage", ["High", "Normal", "Low"]),
    "EnemyArmour": Setting("GameSetting.Vail.EnemyArmour", ["High", "Normal", "Low"]),
    "EnemyAggression": Setting("GameSetting.Vail.EnemyAggression", ["High", "Normal", "Low"]),
    "AnimalSpawnRate": Setting("GameSetting.Vail.AnimalSpawnRate", ["High", "Normal", "Low"]),
    "StartingSeason": Setting("GameSetting.Environment.StartingSeason", ["Spring", "Summer", "Autumn", "Winter"]),
    "SeasonLength": Setting("GameSetting.Environment.SeasonLength", ["Realistic", "Normal", "Short"]),
    "DayLength": Setting( "GameSetting.Environment.DayLength", ["Long", "Realistic", "Normal", "Short"]),
    "PrecipitationFrequency": Setting("GameSetting.Environment.PrecipitationFrequency", ["High", "Default", "Low"]),
    "ConsumableEffects": Setting("GameSetting.Survival.ConsumableEffects", ["High", "Normal"]),
    "PlayerStatsDamage": Setting("GameSetting.Survival.PlayerStatsDamage", ["Hard", "Normal", "Off"])
}

GAMESTATEFILE =  "/GameStateSaveData.json"
GAMESETUPFILE =  "/GameSetupSaveData.json"
SAVEDATAFILE = "/SaveData.json"
INVENTORYFILE = "/PlayerInventorySaveData.json"
WEATHERFILE = "/WeatherSystemSaveData.json"


class SavefileLoader:
    def __init__(self, itemIdLoader: ItemIdLoader, saveFolderPath=None) -> None:
        self.inventoryLoader = InventoryLoader(itemIdLoader)
        self.load(saveFolderPath)

    def load(self, saveFolderPath=None):
        if saveFolderPath is None:
            saveFolderPath = selectFolder()
            
        gameStatePath = saveFolderPath + GAMESTATEFILE
        gameSavePath = saveFolderPath + SAVEDATAFILE
        gameSetupPath = saveFolderPath + GAMESETUPFILE
        weatherPath = saveFolderPath + WEATHERFILE
        self.readGamestateAndGamesave(gameStatePath, gameSavePath, gameSetupPath,weatherPath)
        self.inventoryLoader.loadInventory(saveFolderPath + INVENTORYFILE)
        self.saveTestdata()

    def save(self, saveFolderPath=None):
        if saveFolderPath is None:
            saveFolderPath = selectFolder()
        
        gameStatePath = saveFolderPath + GAMESTATEFILE
        gameSavePath = saveFolderPath + SAVEDATAFILE
        gameSetupPath = saveFolderPath + GAMESETUPFILE
        self.saveGamestateAndGamesave(gameStatePath, gameSavePath, gameSetupPath)
        self.inventoryLoader.saveInventory(saveFolderPath + INVENTORYFILE)

    def readGamestateAndGamesave(self, gameStatePath, gameSavePath, gameSetupPath, weatherPath):
        with open(gameStatePath, "r") as file:
            self.gameStateContent = json.loads(file.read())
            self.gamestate = json.loads(self.gameStateContent["Data"]["GameState"])

        with open(gameSavePath, "r") as file:
            self.gameSaveContent = json.loads(file.read())
            self.savedata = self.gameSaveContent["Data"]
            self.vailworldsim = json.loads(self.savedata["VailWorldSim"])
            self.actors = self.vailworldsim["Actors"]
            
        with open(gameSetupPath, "r") as file:
            self.gameSetupContent = json.loads(file.read())
            self.gameSetupData = self.gameSetupContent["Data"]
            self.gameSetup = json.loads(self.gameSetupData["GameSetup"])
            self.settings = self.gameSetup["_settings"]
            
        with open(weatherPath, "r") as file:
            self.weatherSystemSaveDataContent = json.loads(file.read())
            self.weatherData = self.weatherSystemSaveDataContent["Data"]
            self.weatherSystem = json.loads(self.weatherData["WeatherSystem"])
            

    def isKelvinAlive(self) -> bool:
        for actor in self.actors:
            if actor["TypeId"] == 9:
                kelvinActor = actor
                break
        
        if self.gamestate["IsRobbyDead"] == True or kelvinActor["State"] == 6 or kelvinActor["Stats"]["Health"] < 1:
            return False
        return True

    def isVirginiaAlive(self) -> bool:
        for actor in self.actors:
            if actor["TypeId"] == 10:
                virginiaActor = actor
                break
        
        if self.gamestate["IsVirginiaDead"] == True or virginiaActor["State"] == 6 or virginiaActor["Stats"]["Health"] < 1:
            return False
        return True

    def revive(self, kelvin=False, virginia=False):
        if kelvin:
            self.gamestate["IsRobbyDead"] = False
            for actor in self.actors:
                if actor["TypeId"] == 9:
                    actor["State"] = 2
                    actor["Stats"]["Health"] = 100
                    break
        if virginia:
            self.gamestate["IsVirginiaDead"] = False
            for actor in self.actors:
                if actor["TypeId"] == 10:
                    actor["State"] = 2
                    actor["Stats"]["Health"] = 100

    def kill(self, kelvin=False, virginia=False):
        if kelvin:
            self.gamestate["IsRobbyDead"] = True
            for actor in self.actors:
                if actor["TypeId"] == 9:
                    actor["State"] = 6
                    actor["Stats"]["Health"] = 0.0
                    break
        if virginia:
            self.gamestate["IsVirginiaDead"] = True
            for actor in self.actors:
                if actor["TypeId"] == 10:
                    actor["State"] = 6
                    actor["Stats"]["Health"] = 0.0

    def setCrashsite(self, crashsite):
        self.gamestate["CrashSite"] = crashsite

    def countNumActors(self):
        typeIds = {}
        for actor in self.actors:
            if not actor["TypeId"] in typeIds:
                typeIds[actor["TypeId"]] = 0
            typeIds[actor["TypeId"]] += 1

        typeIds = dict(sorted(typeIds.items()))
        for key, value in typeIds.items():
            print(f'{key} exists {value} times')

    def saveGamestateAndGamesave(self, gameStatePath, gameSavePath, gameSetupPath):
        with open(gameStatePath, "w") as file:
            self.gameStateContent["Data"]["GameState"] = json.dumps(self.gamestate)
            file.write(json.dumps(self.gameStateContent))

        with open(gameSavePath, "w") as file:
            self.vailworldsim["Actors"] = self.actors
            self.savedata["VailWorldSim"] = json.dumps(self.vailworldsim)
            self.gameSaveContent["Data"] = self.savedata
            file.write(json.dumps(self.gameSaveContent))
        
        self.saveTestdata()
       
    def _findSetting(self, s: str):
        for entry in self.settings:
            if entry["Name"] == s:
                return entry
        return None
    
    def _findSettingOrCreate(self, s: str):
        setting = self._findSetting(s)
        if setting is None:
            self.settings.append(createSettingsEntry(s))
            setting = self.settings[-1]
        return setting
            
    def getSetting(self, settingTitle: str) -> str:
        if settingTitle == "CrashSite":
            print(f'{settingTitle} has value {self.gamestate["CrashSite"]}')
            return self.gamestate["CrashSite"]
        else:
            setting = self._findSetting(SETTINGS[settingTitle].name)
            if setting is None:
                return ""
            print(f'{settingTitle} has value {setting["StringValue"]}')
            return setting['StringValue']
        
    def setSetting(self, settingTitle: str, value: str):
        if settingTitle == "Difficulty":
            self.gamestate["GameType"] = value
            setting = self._findSettingOrCreate(SETTINGS[settingTitle].name)
            print(f'{settingTitle} had value {setting["StringValue"]} changed to {value}')
            setting["StringValue"] = value
        elif settingTitle == "CrashSite":
            print(f'{settingTitle} had value {self.gamestate["CrashSite"]} changed to {value}')
            self.gamestate["CrashSite"] = value
        else:
            setting = self._findSettingOrCreate(SETTINGS[settingTitle].name)
            print(f'{settingTitle} had value {setting["StringValue"]} changed to {value}')
            setting["StringValue"] = value
            
    def saveTestdata(self):
        with open("actors.json", "w") as file:
            file.write(json.dumps(self.vailworldsim, indent=4))
            
        with open("gameState.json", "w") as file:
            file.write(json.dumps(self.gamestate, indent=4))
            
        with open("gameSetup.json", "w") as file:
            file.write(json.dumps(self.settings, indent=4))
            
        with open("weatherSystem.json", "w") as file:
            file.write(json.dumps(self.weatherSystem, indent=4))

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

def createSettingsEntry(name):
    return {        
        "Name": name,
        "SettingType": 3,
        "Version": 0,
        "BoolValue": False,
        "IntValue": 0,
        "FloatValue": 0.0,
        "StringValue": "",
        "Protected": False,
        "FloatArrayValue": [],
        "IsSet": False
    }
