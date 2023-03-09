import json
from ItemIdLoader import ItemIdLoader
from InventoryLoader import InventoryLoader
from Misc import *

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
            self.gameSetupSettings = self.gameSetup["_settings"]
            
        with open(weatherPath, "r") as file:
            self.weatherSystemSaveDataContent = json.loads(file.read())
            self.weatherData = self.weatherSystemSaveDataContent["Data"]
            self.weatherSystem = json.loads(self.weatherData["WeatherSystem"])
        
        self.inventoryLoader.loadInventory(saveFolderPath + INVENTORYFILE)
        self.saveTestdata()

    def save(self, saveFolderPath=None):
        if saveFolderPath is None:
            saveFolderPath = selectFolder()
        
        gameStatePath = saveFolderPath + GAMESTATEFILE
        gameSavePath = saveFolderPath + SAVEDATAFILE
        gameSetupPath = saveFolderPath + GAMESETUPFILE
        weatherPath = saveFolderPath + WEATHERFILE
        
        with open(gameStatePath, "w") as file:
            self.gameStateContent["Data"]["GameState"] = json.dumps(self.gamestate)
            file.write(json.dumps(self.gameStateContent))

        with open(gameSavePath, "w") as file:
            self.vailworldsim["Actors"] = self.actors
            self.savedata["VailWorldSim"] = json.dumps(self.vailworldsim)
            self.gameSaveContent["Data"] = self.savedata
            file.write(json.dumps(self.gameSaveContent))
            
        with open(gameSetupPath, "w") as file:
            self.gameSetup["_settings"] = self.gameSetupSettings
            self.gameSetupData["GameSetup"] = json.dumps(self.gameSetup)
            self.gameSetupContent["Data"] = self.gameSetupData
            file.write(json.dumps(self.gameSetupContent))
            
        with open(weatherPath, "w") as file:
            self.weatherData["WeatherSystem"] = json.dumps(self.weatherSystem)
            self.weatherSystemSaveDataContent["Data"] = self.weatherData
            file.write(json.dumps(self.weatherSystemSaveDataContent))
        
        self.saveTestdata()
        
        self.inventoryLoader.saveInventory(saveFolderPath + INVENTORYFILE)

    def setDay(self, day):
        self.gamestate["GameDays"] = day

    def setTime(self, time):
        hour, minute = time.split(":")
        hour = int(hour)
        minute = int(minute)
        self.gamestate["GameHours"] = hour
        self.gamestate["GameMinutes"] = minute
    
    def getTime(self) -> str:
        hour = self.gamestate["GameHours"]
        minute = self.gamestate["GameMinutes"]
        return str(hour) + ":" + str(minute)
    
    def getDay(self) -> int:
        return self.gamestate["GameDays"]
    
    def entrySetTimeAndDayCallback(self, callback):
        day = self.gamestate["GameDays"]
        hour = self.gamestate["GameHours"]
        minute = self.gamestate["GameMinutes"]
        callback(day, hour, minute)

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

    def countNumActors(self):
        typeIds = {}
        for actor in self.actors:
            if not actor["TypeId"] in typeIds:
                typeIds[actor["TypeId"]] = 0
            typeIds[actor["TypeId"]] += 1

        typeIds = dict(sorted(typeIds.items()))
        for key, value in typeIds.items():
            print(f'{key} exists {value} times')
       
    def _findGameSetupSetting(self, s: str):
        for entry in self.gameSetupSettings:
            if entry["Name"] == s:
                return entry
        return None
    
    def _findGameSetupSettingOrCreate(self, s: str):
        setting = self._findGameSetupSetting(s)
        if setting is None:
            self.gameSetupSettings.append(createGameSetupSettingsEntry(s))
            setting = self.gameSetupSettings[-1]
        return setting
            
    def getSetting(self, settingTitle: str) -> str:
        
        settingsFile = SETTINGS[settingTitle].file
        if settingTitle == "KelvinAlive":
            status = self.isKelvinAlive()
            return "alive" if status else "dead"
        
        elif settingTitle == "VirginiaAlive":
            status = self.isKelvinAlive()
            return "alive" if status else "dead"
        
        elif settingTitle == "Difficulty":
            return self.gamestate["GameType"]
        
        elif settingsFile == "gameStateFile":
            return self.gamestate["CrashSite"]
        
        elif settingsFile == "gameSetupFile":
            setting = self._findGameSetupSetting(SETTINGS[settingTitle].name)
            if setting is None:
                return SETTINGS[settingTitle].default
            return setting['StringValue']
        
        elif settingsFile == "weatherSystem":
            setting = SETTINGS[settingTitle].name
            if settingTitle == "CurrentSeason":
                seasonKeys = list(SEASONS.keys())
                return seasonKeys[self.weatherSystem[setting]]
            if settingTitle == "IsRaining":
                return str(self.weatherSystem[setting])
        return SETTINGS[settingTitle].default
        
    def setSeason(self, value):
        setting = SETTINGS["CurrentSeason"].name
        
        # the game calculates the season from these
        currentDay = self.gamestate["GameDays"]
        seasonLengthText = self.getSetting("SeasonLength")
        offset = seasonStart(value, seasonLengthText) - (currentDay)
        self.weatherSystem["_startingDayOffset"] = offset
    
        #  this is not actually used by the game to set the season
        value = SEASONS[value]
        self.weatherSystem[setting] = value
        
    def setRaining(self, settingTitle, value):
        setting = SETTINGS[settingTitle].name
        
        #_wetness values could also play a role here but this is good enough for now
        self.weatherSystem["_currentRainType"] = 2 #rain intensity
        if value == "True":
            newValue = True
        else:
            newValue = False
        self.weatherSystem[setting] = newValue
    
    def setKelvinStatus(self, value):
        if value == "alive": 
            self.gamestate["IsRobbyDead"] = False
            for actor in self.actors:
                if actor["TypeId"] == 9:
                    actor["State"] = 2
                    actor["Stats"]["Health"] = 100
                    break
            print("Kelvin was revived")
        else: 
            self.gamestate["IsRobbyDead"] = True
            for actor in self.actors:
                if actor["TypeId"] == 9:
                    actor["State"] = 6
                    actor["Stats"]["Health"] = 0.0
                    break
            print("Kelvin was killed")
        
    def setVirginiaStatus(self, value):
        if value == "alive": 
            self.gamestate["IsVirginiaDead"] = False
            for actor in self.actors:
                if actor["TypeId"] == 10:
                    actor["State"] = 2
                    actor["Stats"]["Health"] = 100
                    break
            print("Virginia was revived")
        else: 
            self.gamestate["IsVirginiaDead"] = True
            for actor in self.actors:
                if actor["TypeId"] == 10:
                    actor["State"] = 6
                    actor["Stats"]["Health"] = 0.0
            print("Virginia was killed")
        
    def setSetting(self, settingTitle: str, value: str):
        print(f"Setting {settingTitle} to {value}")
        
        settingsFile = SETTINGS[settingTitle].file
        
        if settingTitle == "KelvinAlive":
            self.setKelvinStatus(value)
        
        elif settingTitle == "VirginiaAlive":
            self.setVirginiaStatus(value)
        
        elif settingTitle == "Difficulty":
            self.gamestate["GameType"] = value
            setting = self._findGameSetupSettingOrCreate(SETTINGS[settingTitle].name)
            setting["StringValue"] = value
            
        elif settingsFile == "gameStateFile":
            self.gamestate["CrashSite"] = value
            
        elif settingsFile == "gameSetupFile":
            setting = self._findGameSetupSettingOrCreate(SETTINGS[settingTitle].name)
            setting["StringValue"] = value
            
        elif settingsFile == "weatherSystem":
            if settingTitle == "CurrentSeason":
                self.setSeason(value)
                
            elif settingTitle == "IsRaining":
                self.setRaining(settingTitle, value)
            
    def saveTestdata(self):
        with open("actors.json", "w") as file:
            file.write(json.dumps(self.vailworldsim, indent=4))
            
        with open("gameState.json", "w") as file:
            file.write(json.dumps(self.gamestate, indent=4))
            
        with open("gameSetup.json", "w") as file:
            file.write(json.dumps(self.gameSetupSettings, indent=4))
            
        with open("weatherSystem.json", "w") as file:
            file.write(json.dumps(self.weatherSystem, indent=4))