import tkinter as tk
from tkinter import ttk
from SavefileLoader import SavefileLoader
import json
from TkVerticalScrolledFrame import TkVerticalScrolledFrame

class Stat():
    def __init__(self, name, minValue: int, maxValue: int):
        self.name = name
        self.minValue = minValue
        self.maxValue = maxValue
        self.value = tk.IntVar()

class NPC():
    def __init__(self, name):
        self.name = name
        self.stats = []
        self.stats.append(Stat("Health", 0, 100))
        self.stats.append(Stat("Anger", 0, 100))
        self.stats.append(Stat("Fear", 0, 100))
        self.stats.append(Stat("Fullness", 0, 100))
        self.stats.append(Stat("Hydration", 0, 100))
        self.stats.append(Stat("Energy", 0, 100))
        self.stats.append(Stat("Affection", 0, 100))
        self.stats.append(Stat("Sentiment Influence", 0, 100))
        
    def setStat(self, name, value):
        for stat in self.stats:
            if stat.name == name:
                if value == "min":
                    value = stat.minValue
                elif value == "max":
                    value = stat.maxValue
                
                stat.value.set(int(value))
                
    def getStat(self, name):
        for stat in self.stats:
            if stat.name == name:
                return stat

class Kelvin(NPC):
    def __init__(self):
        super().__init__("Kelvin")
        
class Virginia(NPC):
    def __init__(self):
        super().__init__("Virginia")
        for stat in self.stats:
            if stat.name == "Health":
                stat.maxValue = 120
                break

class TkNPCTab(tk.Frame):
    def __init__(self, savefileLoader: SavefileLoader):
        super().__init__()
        self.savefileLoader = savefileLoader
        
        containerExterior = TkVerticalScrolledFrame(self)
        container = containerExterior.interior
        containerExterior.pack(expand=True, fill="both")
    
        self.initializeKelvin(container)
        self.initializeVirginia(container)
        
    def initializeKelvin(self, container):
        kelvinFrame = tk.Frame(container, highlightthickness=2, highlightbackground="lightblue")
        kelvinFrame.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        kelvinFrame.grid_rowconfigure(0, minsize=30)
        kelvinFrame.grid_columnconfigure(0, weight=0)
        kelvinFrame.grid_columnconfigure(1, weight=1)
        
        self.kelvin = Kelvin()
                
        for actor in self.savefileLoader.actors:
            if actor["TypeId"] == 9:
                self.kelvinActor = actor
                break
        
        tk.Label(kelvinFrame, text=self.kelvin.name, anchor="center", bg="lightblue").grid(row=0, column=0, columnspan=2, sticky="new")
        tk.Label(kelvinFrame, text="Status", anchor="w").grid(row=1, column=0, sticky="nesw")
        self.kelvinStatusVar = tk.StringVar(self)
        tk.Button(kelvinFrame, textvariable=self.kelvinStatusVar, anchor="w", 
                  command=lambda event=None, npcName="Kelvin": self.onButton(npcName)).grid(row=1, column=1, sticky="nsw")
        tk.Label(kelvinFrame, text="Position", anchor="w").grid(row=2, column=0, sticky="nesw")
        self.kelvinPositionVar = tk.StringVar(self)
        tk.Label(kelvinFrame, textvariable=self.kelvinPositionVar, anchor="w").grid(row=2, column=1, sticky="nesw")
        
        #scales
        for index, stat in enumerate(self.kelvin.stats):
            tk.Label(kelvinFrame, text=stat.name, anchor="w").grid(row=index+3, column=0, sticky="nesw")
            
            scale = tk.Scale(kelvinFrame, from_=stat.minValue, to=stat.maxValue, 
                             variable=stat.value, orient="horizontal", resolution=1,
                             command=lambda event=None, npcName="Kelvin", statIndex=index, statValue=stat.value: 
                                 self.onStatChange(npcName, statIndex, statValue.get()))
            scale.grid(row=index+3, column=1, sticky="nesw")
        self.readStats("Kelvin")
        
        #clothing
        tk.Label(kelvinFrame, text="Clothing", anchor="w").grid(row=index+3+len(self.kelvin.stats), column=0, sticky="nesw")
        with open("../res/kelvinClothing.json", "r") as file:
            self.possibleKelvinClothingItems = json.loads(file.read())
            
        possibleKelvinClothingNames = [item["Name"] for item in self.possibleKelvinClothingItems]
        self.kelvinClothingVar = tk.StringVar(kelvinFrame)
        self.kelvinClothingVar.set(self.getClothingNameFromId("Kelvin", self.kelvinActor["OutfitId"]))
        box = ttk.Combobox(kelvinFrame, textvariable=self.kelvinClothingVar, 
                           values=possibleKelvinClothingNames, state="readonly")
        box.bind("<<ComboboxSelected>>", lambda event=None, npcName="Kelvin": self.onClothingSelected(npcName))
        box.grid(row=index+3+len(self.kelvin.stats), column=1, sticky="w", padx=10, pady=10)

    def initializeVirginia(self, container):
        virginiaFrame = tk.Frame(container, highlightthickness=2, highlightbackground="lightblue")
        virginiaFrame.pack(side="left", expand=True, fill="x", padx=10, pady=10)
        virginiaFrame.grid_rowconfigure(0, minsize=30)
        virginiaFrame.grid_columnconfigure(0, weight=0)
        virginiaFrame.grid_columnconfigure(1, weight=1)
        
        self.virginia = Virginia()
        
        for actor in self.savefileLoader.actors:
            if actor["TypeId"] == 10:
                self.virginiaActor = actor
                break
        if not hasattr(self, "virginiaActor"):
            self.createVirginia()
        
        tk.Label(virginiaFrame, text=self.virginia.name, anchor="center", bg="lightblue").grid(row=0, column=0, columnspan=2, sticky="new")
        tk.Label(virginiaFrame, text="Status", anchor="w").grid(row=1, column=0, sticky="nesw")
        self.virginiaStatusVar = tk.StringVar(self)
        tk.Button(virginiaFrame, textvariable=self.virginiaStatusVar, anchor="w",
                  command=lambda event=None, npcName="Virginia": self.onButton(npcName)).grid(row=1, column=1, sticky="nsw")
        tk.Label(virginiaFrame, text="Position", anchor="w").grid(row=2, column=0, sticky="nesw")
        self.virginiaPositionVar = tk.StringVar(self)
        tk.Label(virginiaFrame, textvariable=self.virginiaPositionVar, anchor="w").grid(row=2, column=1, sticky="nesw")
        
        #scales
        for index, stat in enumerate(self.virginia.stats):
            tk.Label(virginiaFrame, text=stat.name, anchor="w").grid(row=index+3, column=0, sticky="nesw")
            
            scale = tk.Scale(virginiaFrame, from_=stat.minValue, to=stat.maxValue, 
                             variable=stat.value, orient="horizontal", resolution=1,
                             command=lambda event=None, npcName="Virginia", statIndex=index, statValue=stat.value: 
                                 self.onStatChange(npcName, statIndex, statValue.get()))
            scale.grid(row=index+3, column=1, sticky="nesw")
        self.readStats("Virginia")
        
        #clothing
        tk.Label(virginiaFrame, text="Clothing", anchor="w").grid(row=index+3+len(self.virginia.stats), column=0, sticky="nesw")
        with open("../res/virginiaClothing.json", "r") as file:
            self.possibleVirginiaClothingItems = json.loads(file.read())
            
        possibleVirginiaClothingNames = [item["Name"] for item in self.possibleVirginiaClothingItems]
        self.virginiaClothingVar = tk.StringVar(virginiaFrame)
        self.virginiaClothingVar.set(self.getClothingNameFromId("Virginia", self.virginiaActor["OutfitId"]))
        box = ttk.Combobox(virginiaFrame, textvariable=self.virginiaClothingVar, 
                           values=possibleVirginiaClothingNames, state="readonly")
        box.bind("<<ComboboxSelected>>", lambda event=None, npcName="Virginia": self.onClothingSelected(npcName))
        box.grid(row=index+3+len(self.virginia.stats), column=1, sticky="w", padx=10, pady=10)
        
    def findClothingByName(self, npcName, clothingName):
        possibleClothingItems = self._findPossibleClothing(npcName)
        for item in possibleClothingItems:
            if item["Name"] == clothingName:
                return item

    def onClothingSelected(self, npcName):
        clothingVar = self._findClothingVar(npcName)
        clothingItem = self.findClothingByName(npcName, clothingVar.get())
        print(f"{clothingItem['Name']} selected for {npcName}")
        
        npc = self._findActor(npcName)
        npc["OutfitId"] = clothingItem["ItemId"]
    
    def getClothingNameFromId(self, npcName, itemId):
        possibleClothingItems = self._findPossibleClothing(npcName)
        for item in possibleClothingItems:
            if itemId == item["ItemId"]:
                return item["Name"]
    
    def onButton(self, npcName):
        print(npcName)
        if self.isAlive(npcName):
            self.setStatus(npcName, "dead")
            print(f"{npcName} was killed")
            self._findNpc(npcName).setStat("Health", "min")
        else:
            self.setStatus(npcName, "alive")
            self._findNpc(npcName).setStat("Health", "max")
            print(f"{npcName} was revived")
        self.statusVarRefresh(npcName)

    def positionRefresh(self, npcName):
        posVar = self._findPositionVar(npcName)
        pos = self.getPosition(npcName)
        posVar.set(f"x: {int(pos[0])}, y: {int(pos[1])}, z: {int(pos[2])}")
        
    def statusVarRefresh(self, npcName):
        statusVar = self._findStatusVar(npcName)
        statusVar.set("Alive" if self.isAlive(npcName) else "Dead")
        
    def onStatChange(self, npcName, statIndex: int, value):
        npc = self._findNpc(npcName)
        actor = self._findActor(npcName)
        
        statName = npc.stats[statIndex].name
        
        if "Influence" in statName:
            influenceName = str(npc.stats[statIndex].name).removesuffix(" Influence")
            self.setInfluenceTowards(npcName, influenceName, value)
        else:
            #regular actors stats
            stats = actor["Stats"]
            stats[statName] = float(value)
            
            if statName == "Health":
                self.setStatus(npcName, "alive" if value > 0 else "Dead")
                self.statusVarRefresh(npcName)
            
        print(f"Setting {npcName} {statName} to {value}")
        
    def readStats(self, npcName=None):
        
        if npcName == None:
            self.readStats("Kelvin")
            self.readStats("Virginia")
            return
        
        npc = self._findNpc(npcName)
        actor = self._findActor(npcName)
        
        self.statusVarRefresh(npcName)
        self.positionRefresh(npcName)
        
        stats = actor["Stats"]
        for name, value in stats.items():
            npc.setStat(name, value)
            
        for stat in self._findNpc(npcName).stats:
            if "Influence" in stat.name:
                influenceName = str(stat.name).removesuffix(" Influence")
                influenceValue = self.getInfluenceTowards(npcName, influenceName)
                npc.setStat(stat.name, influenceValue)
        
    def getPosition(self, npcName):
        actor = self._findActor(npcName)
        
        return [actor["Position"]["x"], actor["Position"]["y"], actor["Position"]["z"]]

    def setStatus(self, npcName, value):
        actor = self._findActor(npcName)
        gamestateName = self._findGamestateName(npcName)
        statusVar = self._findStatusVar(npcName)
    
        if value == "alive": 
            self.savefileLoader.gamestate[gamestateName] = False
            actor["State"] = 2
            actor["Stats"]["Health"] = 100
            statusVar.set("Alive")
        else: 
            self.savefileLoader.gamestate[gamestateName] = True
            actor["State"] = 6
            actor["Stats"]["Health"] = 0.0
            statusVar.set("Dead")

    def setPosition(self, npcName, posDict):
        self._findActor(npcName)["Position"] = posDict
        self.positionRefresh(npcName)
    
    def isAlive(self, npcName) -> bool:
        gamestateName = self._findGamestateName(npcName)
        actor = self._findActor(npcName)
    
        #self.savefileLoader.gamestate[gamestateName] == True or 
        if actor["State"] == 6 or actor["Stats"]["Health"] < 1:
            return False
        return True
    
    def createVirginia(self):
        with open("../res/virginia.json") as file:
            self.virginiaActor = json.loads(file.read())
            self.savefileLoader.actors.append(self.virginiaActor)
            
        uniqueId = self._findUniqueId("Virginia")
        with open("../res/influenceMemory.json") as file:
            influenceMemory = json.loads(file.read())
            influenceMemory["UniqueId"] = uniqueId
            self.savefileLoader.influenceMemory.append(influenceMemory)

    def getInfluenceTowards(self, npcName, influenceName, towards="Player"):
        uniqueId = self._findUniqueId(npcName)
        for source in self.savefileLoader.influenceMemory:
            if source["UniqueId"] == uniqueId:
                for target in source["Influences"]:
                    if target["TypeId"] == towards:
                        return target[influenceName]

    def setInfluenceTowards(self, npcName, influenceName, value, towards="Player"):
        uniqueId = self._findUniqueId(npcName)
        for source in self.savefileLoader.influenceMemory:
            if source["UniqueId"] == uniqueId:
                for target in source["Influences"]:
                    if target["TypeId"] == towards:
                        target[influenceName] = value

    def _findActor(self, npcName):
        if npcName == "Kelvin":
            return self.kelvinActor
        elif npcName == "Virginia":
            return self.virginiaActor
    
    def _findGamestateName(self, npcName):
        if npcName == "Kelvin":
            return "IsRobbyDead"
        elif npcName == "Virginia":
            return "IsVirginiaDead"
        
    def _findNpc(self, npcName):
        if npcName == "Kelvin":
            return self.kelvin
        elif npcName == "Virginia":
            return self.virginia
        
    def _findStatusVar(self, npcName):
        if npcName == "Kelvin":
            return self.kelvinStatusVar
        elif npcName == "Virginia":
            return self.virginiaStatusVar
        
    def _findPositionVar(self, npcName):
        if npcName == "Kelvin":
            return self.kelvinPositionVar
        elif npcName == "Virginia":
            return self.virginiaPositionVar
        
    def _findPossibleClothing(self, npcName):
        if npcName == "Kelvin":
            return self.possibleKelvinClothingItems
        elif npcName == "Virginia":
            return self.possibleVirginiaClothingItems
        
    def _findClothingVar(self, npcName):
        if npcName == "Kelvin":
            return self.kelvinClothingVar
        elif npcName == "Virginia":
            return self.virginiaClothingVar
        
    def _findUniqueId(self, npcName):
        if npcName == "Kelvin":
            return self.kelvinActor["UniqueId"]
        elif npcName == "Virginia":
            return self.virginiaActor["UniqueId"]