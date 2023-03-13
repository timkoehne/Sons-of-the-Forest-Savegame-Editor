import os
from tkinter import filedialog as tkfiledialog
import json


ICONSIZE = 50
MAPIMAGESIZE = 4096
imageToIngameScalingFactor = 0.9765

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
    "EnemySpawn": Setting("gameSetupFile", "GameSetting.Vail.EnemySpawn", ["Enabled", "Disabled"], "Enabled"),
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

def createGameSetupSettingsEntry(name, settingType: int):
    #settingstype defines which is the relavant value for this setting, 0=bool, 1=int, ...
    return {        
        "Name": name,
        "SettingType": settingType,
        "Version": 0,
        "BoolValue": False,
        "IntValue": 0,
        "FloatValue": 0.0,
        "StringValue": "",
        "Protected": False,
        "FloatArrayValue": [],
        "IsSet": False
    }
    
def transformCoordinatesystemToIngame(mapPos, bboxMap):
    #image coordinate system is (0,0) in the top left and positive x,y to right and bottom
    #ingame coordinate system is (0,0) in the center of the map, north is z positive, east is x positive
    width = bboxMap[2] - bboxMap[0]
    height = bboxMap[3] - bboxMap[1]
    percentX = (mapPos[0] - bboxMap[0]) / width
    percentY = (mapPos[1] - bboxMap[1]) / height
    
    coordX = percentX - 0.5
    coordY = (percentY - 0.5) * -1
    
    coordX = coordX * imageToIngameScalingFactor * MAPIMAGESIZE
    coordY = coordY * imageToIngameScalingFactor * MAPIMAGESIZE
    
    return coordX, coordY
    
def transformCoordinatesystemToImage(ingamePos, bboxMap):
    #image coordinate system is (0,0) in the top left and positive x,y to right and bottom
    #ingame coordinate system is (0,0) in the center of the map, north is z positive, east is x positive
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

def countNumActors(actors):
    typeIds = {}
    for actor in actors:
        if not actor["TypeId"] in typeIds:
            typeIds[actor["TypeId"]] = 0
        typeIds[actor["TypeId"]] += 1

    typeIds = dict(sorted(typeIds.items()))
    for key, value in typeIds.items():
        print(f'{key} exists {value} times') 

def saveTestdata(actors, gamestate, gameSetupSettings, weatherSystem, playerState):
    with open("../test/actors.json", "w") as file:
        file.write(json.dumps(actors, indent=4))
        
    with open("../test/gameState.json", "w") as file:
        file.write(json.dumps(gamestate, indent=4))
        
    with open("../test/gameSetup.json", "w") as file:
        file.write(json.dumps(gameSetupSettings, indent=4))
        
    with open("../test/weatherSystem.json", "w") as file:
        file.write(json.dumps(weatherSystem, indent=4))
        
    with open("../test/playerState.json", "w") as file:
        file.write(json.dumps(playerState, indent=4))