import json
from ItemIdLoader import ItemIdLoader
from InventoryLoader import InventoryLoader
from Misc import *

GAMESTATEFILE =  "/GameStateSaveData.json"
GAMESETUPFILE =  "/GameSetupSaveData.json"
SAVEDATAFILE = "/SaveData.json"
INVENTORYFILE = "/PlayerInventorySaveData.json"
WEATHERFILE = "/WeatherSystemSaveData.json"
PLAYERFILE = "/PlayerStateSaveData.json"


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
        playerPath = saveFolderPath + PLAYERFILE
        
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
            
            
        with open(playerPath, "r") as file:
            self.playerStateSaveDataContent = json.loads(file.read())
            self.playerStateSaveData = self.playerStateSaveDataContent["Data"]
            self.playerStateWrapper = json.loads(self.playerStateSaveData["PlayerState"])
            self.playerState = self.playerStateWrapper["_entries"]
        
        self.inventoryLoader.loadInventory(saveFolderPath + INVENTORYFILE)
        saveTestdata(self.actors, self.gamestate, 
                     self.gameSetupSettings, self.weatherSystem, self.playerState)

    def save(self, saveFolderPath=None):
        if saveFolderPath is None:
            saveFolderPath = selectFolder()
        
        gameStatePath = saveFolderPath + GAMESTATEFILE
        gameSavePath = saveFolderPath + SAVEDATAFILE
        gameSetupPath = saveFolderPath + GAMESETUPFILE
        weatherPath = saveFolderPath + WEATHERFILE
        playerPath = saveFolderPath + PLAYERFILE
        
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
            
        with open(playerPath, "w") as file:
            self.playerStateWrapper["_entries"] = self.playerState
            self.playerStateSaveData["PlayerState"] = json.dumps(self.playerStateWrapper)
            self.playerStateSaveDataContent["Data"] = self.playerStateSaveData
            file.write(json.dumps(self.playerStateSaveDataContent))
            
        saveTestdata(self.actors, self.gamestate, self.gameSetupSettings, self.weatherSystem, self.playerState)
        
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

    def findPlayerSetting(self, name):
        for setting in self.playerState:
            if setting["Name"] == name:
                return setting
       
    def findGameSetupSetting(self, settingTitle: str):
        for entry in self.gameSetupSettings:
            if entry["Name"] == SETTINGS[settingTitle].name:
                return entry
        return None
    
    def findGameSetupSettingOrCreate(self, settingTitle: str):
        setting = self.findGameSetupSetting(settingTitle)
        if setting is None:
            
            if settingTitle == "EnemySpawn":
                settingType = 0
            else:
                settingType = 3
            
            self.gameSetupSettings.append(createGameSetupSettingsEntry(SETTINGS[settingTitle].name, settingType))
            setting = self.gameSetupSettings[-1]
        return setting
            
    def getSetting(self, settingTitle: str) -> str:
        
        settingsFile = SETTINGS[settingTitle].file
        if settingTitle == "KelvinAlive":
            status = self.isKelvinAlive()
            return "alive" if status else "dead"
        
        elif settingTitle == "VirginiaAlive":
            status = self.isVirginiaAlive()
            return "alive" if status else "dead"
        
        elif settingTitle == "Difficulty":
            return self.gamestate["GameType"]
        
        elif settingsFile == "gameStateFile":
            return self.gamestate["CrashSite"]
        
        elif settingsFile == "gameSetupFile":
            setting = self.findGameSetupSetting(settingTitle)
            if setting is None:
                return SETTINGS[settingTitle].default
            
            relevantValue = self.getRelevantSettingsValue(setting)
            
            if settingTitle == "EnemySpawn":
                return "Enabled" if relevantValue else "Disabled"
            else:
                return relevantValue
        
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

    def setKelvinPosition(self, posDict):
        for actor in self.actors:
            if actor["TypeId"] == 9:
                actor["Position"] = posDict
                break
            
    def getKelvinPosition(self):
        for actor in self.actors:
            if actor["TypeId"] == 9:
                return [actor["Position"]["x"], actor["Position"]["y"], actor["Position"]["z"]]
            
    def getVirginiaPosition(self):
        for actor in self.actors:
            if actor["TypeId"] == 10:
                return [actor["Position"]["x"], actor["Position"]["y"], actor["Position"]["z"]]
        
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

    def setVirginiaPosition(self, posDict):
        for actor in self.actors:
            if actor["TypeId"] == 10:
                actor["Position"] = posDict
                break
        
    def setSetting(self, settingTitle: str, value: str):
        print(f"Setting {settingTitle} to {value}")
        
        settingsFile = SETTINGS[settingTitle].file
        
        if settingTitle == "KelvinAlive":
            self.setKelvinStatus(value)
        
        elif settingTitle == "VirginiaAlive":
            self.setVirginiaStatus(value)
        
        elif settingTitle == "Difficulty":
            self.gamestate["GameType"] = value
            setting = self.findGameSetupSettingOrCreate(settingTitle)
            setting["StringValue"] = value
            
        elif settingsFile == "gameStateFile":
            self.gamestate["CrashSite"] = value
            
        elif settingsFile == "gameSetupFile":
            setting = self.findGameSetupSettingOrCreate(settingTitle)
        
            if settingTitle == "EnemySpawn":
                value = True if value == "Enabled" else False
            
            self.setRelevantSettingsValue(setting, value)
            
        elif settingsFile == "weatherSystem":
            if settingTitle == "CurrentSeason":
                self.setSeason(value)
                
            elif settingTitle == "IsRaining":
                self.setRaining(settingTitle, value)
   
    def getPositiondataForActorId(self, typeids):
        positionData = []
        for actor in self.actors:
            if actor["TypeId"] in typeids:
                posDict = actor["Position"]
                positionData.append([posDict["x"], posDict["y"], posDict["z"]])
        return positionData
    
    def getRelevantSettingsValue(setting):
        if setting["SettingType"] == 0:
            return bool(setting["BoolValue"])
        elif setting["SettingType"] == 1:
            return int(setting["IntValue"])
        elif setting["SettingType"] == 2:
            return float(setting["FloatValue"])
        elif setting["SettingType"] == 3:
            return str(setting["StringValue"])
        elif setting["SettingType"] == 4:
            return setting["FloatArrayValue"]
        
    def setRelevantSettingsValue(setting, value):
        if setting["SettingType"] == 0:
            setting["BoolValue"] = bool(value)
        elif setting["SettingType"] == 1:
            setting["IntValue"] = int(value)
        elif setting["SettingType"] == 2:
            setting["FloatValue"] = float(value)
        elif setting["SettingType"] == 3:
            setting["StringValue"] = str(value)
        elif setting["SettingType"] == 4:
            setting["FloatArrayValue"] = value