import os
from tkinter import filedialog as tkfiledialog

jsonFiletypes = (
    ('json file', '*.json'),
    ('All files', '*.*')
)

class Setting():
    def __init__(self, file, name, options, default):
        self.file = file
        self.name = name
        self.options = options
        self.default = default

SEASONLENGTH = {
    "Short": 3,
    "Default": 5,
    "Long": 10,
    "Realistic": 91
}

SEASONS = {
    "Spring": 0,
    "Summer": 1,
    "Autumn": 2,
    "Winter": 3
}

SETTINGS = {
    "KelvinAlive": Setting("", "IsRobbyDead", ["alive", "dead"], "alive"),
    "VirginiaAlive": Setting("", "IsVirginiaDead", ["alive", "dead"], "alive"),
    "Difficulty": Setting("", "Mode", ["Custom", "Hard", "Normal", "Peaceful"], "Normal"),
    "CrashSite": Setting("gameStateFile", "CrashSite", ["tree", "ocean", "snow"], "ocean"),
    # "EnemySpawn": Setting("gameSetupFile", "GameSetting.Vail.EnemySpawn", [], ""),
    "EnemyHealth": Setting("gameSetupFile", "GameSetting.Vail.EnemyHealth", ["High", "Normal", "Low"], "Normal"),
    "EnemyDamage": Setting("gameSetupFile", "GameSetting.Vail.EnemyDamage", ["High", "Normal", "Low"], "Normal"),
    "EnemyArmour": Setting("gameSetupFile", "GameSetting.Vail.EnemyArmour", ["High", "Normal", "Low"], "Normal"),
    "EnemyAggression": Setting("gameSetupFile", "GameSetting.Vail.EnemyAggression", ["High", "Normal", "Low"], "Normal"),
    "AnimalSpawnRate": Setting("gameSetupFile", "GameSetting.Vail.AnimalSpawnRate", ["High", "Normal", "Low"], "Normal"),
    # "StartingSeason": Setting("gameSetupFile", "GameSetting.Environment.StartingSeason", ["Spring", "Summer", "Autumn", "Winter"], "Summer"),
    "SeasonLength": Setting("gameSetupFile", "GameSetting.Environment.SeasonLength", ["Realistic", "Long", "Default", "Short"], "Default"),
    "DayLength": Setting("gameSetupFile", "GameSetting.Environment.DayLength", ["Realistic", "Long", "Default", "Short"], "Default"),
    "PrecipitationFrequency": Setting("gameSetupFile", "GameSetting.Environment.PrecipitationFrequency", ["High", "Default", "Low"], "Default"),
    "ConsumableEffects": Setting("gameSetupFile", "GameSetting.Survival.ConsumableEffects", ["High", "Normal"], "Normal"),
    "PlayerStatsDamage": Setting("gameSetupFile", "GameSetting.Survival.PlayerStatsDamage", ["Hard", "Normal", "Off"], "Off"),
    "CurrentSeason": Setting("weatherSystem", "_currentSeason", ["Spring", "Summer", "Autumn", "Winter"], "Summer"),
    "IsRaining": Setting("weatherSystem", "_isRaining", [True, False], False)
}

def seasonStart(season: str, seasonLength: str) -> int:
    # print(f"In {seasonLength}, {season} starts at day {SEASONS[season] * SEASONLENGTH[seasonLength]}")
    return SEASONS[season] * SEASONLENGTH[seasonLength]

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

def createGameSetupSettingsEntry(name):
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
