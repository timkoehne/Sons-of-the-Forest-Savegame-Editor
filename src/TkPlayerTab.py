import tkinter as tk
from tkinter import ttk
from SavefileLoader import SavefileLoader
from TkNPCTab import NPC, Stat
import json
        
class Player(NPC):
    def __init__(self):
        self.stats = []
        self.stats.append(Stat("CurrentHealth", 0, 100))
        self.stats.append(Stat("Fullness", 0, 100))
        self.stats.append(Stat("Hydration", 0, 100))
        self.stats.append(Stat("Rest", 0, 100))
        self.stats.append(Stat("Stamina", 0, 100))
        self.armourSlots = [0, 1, 4, 5, 6, 7, 8, 9, 10, 11]

    def setStat(self, name, value):
        print(f"set {name} to {int(value)}")
        for stat in self.stats:
            if stat.name == name:
                if value == "min":
                    value = stat.minValue
                elif value == "max":
                    value = stat.maxValue

                stat.value.set(int(value))

    def getStat(self, name) -> Stat:
        for stat in self.stats:
            if stat.name == name:
                return stat

class TkPlayerTab(tk.Frame):

    def __init__(self, saveFileLoader: SavefileLoader):
        super().__init__()
        self.saveFileLoader = saveFileLoader
        
        with open("../res/armour.json", "r") as file:
            self.possibleArmourItems = json.loads(file.read())
        
        self.initializePlayerStats()
        self.initializeArmour()

    def initializeArmour(self):
        armourFrame = tk.Frame(self)
        armourFrame.pack(side="left", expand=True, fill="both")
        
        tk.Label(armourFrame, text="Armour").pack(padx=5, pady=5)
        
        self.selectedArmourVars = {}
        possibleArmourNames = [item["Name"] for item in self.possibleArmourItems]
        for armourSlot in self.playerNpc.armourSlots:
            var = tk.StringVar(armourFrame)
            var.set(self.getArmourNameFromSlot(armourSlot))
            box = ttk.Combobox(armourFrame, textvariable=var, values=possibleArmourNames, state="readonly")
            box.bind("<<ComboboxSelected>>", lambda event=None, slot=armourSlot: self.onArmourSelected(slot))
            box.pack(padx=5, pady=5)
            self.selectedArmourVars[armourSlot] = var

    def initializePlayerStats(self):
        statsFrame = tk.Frame(self, highlightthickness=2,
                              highlightbackground="lightblue")
        statsFrame.pack(side="left", expand=True, fill="both")
        statsFrame.grid_rowconfigure(0, minsize=30)
        statsFrame.grid_columnconfigure(0, weight=0)
        statsFrame.grid_columnconfigure(1, weight=1)

        statsFrame.grid_rowconfigure(1, minsize=30)
        statsFrame.grid_rowconfigure(2, minsize=30)
        statsFrame.grid_rowconfigure(3, minsize=30)

        self.playerNpc = Player()
        tk.Label(statsFrame, text="Stats", anchor="center", bg="lightblue").grid(
            row=0, column=0, columnspan=2, sticky="new")

        tk.Label(statsFrame, text="Position", anchor="w").grid(
            row=1, column=0, sticky="nesw")
        self.playerPositionVar = tk.StringVar(self)

        self.strengthVar = tk.StringVar(self)
        tk.Label(statsFrame, text="StrengthLevel", anchor="w").grid(
            row=2, column=0, sticky="nesw")
        strengthEntry = tk.Entry(statsFrame, textvariable=self.strengthVar)
        strengthEntry.bind("<KeyRelease>", lambda event=None, name="StrengthLevel",
                           var=self.strengthVar: self.onEntryChange(name, var))
        strengthEntry.grid(row=2, column=1, sticky="w")

        self.maxHealthVar = tk.StringVar(self)
        tk.Label(statsFrame, text="Max Health", anchor="w").grid(
            row=3, column=0, sticky="nesw")
        maxHealthEntry = tk.Entry(statsFrame, textvariable=self.maxHealthVar)
        maxHealthEntry.bind("<KeyRelease>", lambda event=None, name="MaxHealth",
                            var=self.maxHealthVar: self.onEntryChange(name, var))
        maxHealthEntry.grid(row=3, column=1, sticky="w")

        tk.Label(statsFrame, textvariable=self.playerPositionVar,
                 anchor="w").grid(row=1, column=1, sticky="nesw")

        self.scales = []
        for index, stat in enumerate(self.playerNpc.stats):
            tk.Label(statsFrame, text=stat.name, anchor="w").grid(
                row=index+4, column=0, sticky="nesw")

            scale = tk.Scale(statsFrame, from_=stat.minValue, to=stat.maxValue,
                             variable=stat.value, orient="horizontal", resolution=1,
                             command=lambda event=None, statIndex=index, statValue=stat.value:
                             self.onStatChange(statIndex, statValue.get()))
            self.scales.append((stat.name, scale))
            scale.grid(row=index+4, column=1, sticky="nesw")

        self.readStats()

    def onArmourSelected(self, armourSlot):
        selectedArmourName = self.selectedArmourVars[armourSlot].get()
        print(f"selected {selectedArmourName} on index {armourSlot}")
        
        for item in self.possibleArmourItems:
            if selectedArmourName == item["Name"]:
                
                if item["Name"] == "None":
                    print("delete")
                    self.deleteArmorPiece(armourSlot)
                else:
                    self.setArmourInSlot(armourSlot, item["ItemId"], item["Armourpoints"])
                
    def setArmourInSlot(self, slot: int, itemId: int, armourPoints: int):
        for entry in self.saveFileLoader.armourPieces:
            if entry["Slot"] == slot:
                    entry["ItemId"] = itemId
                    entry["RemainingArmourpoints"] = armourPoints
                    print(f"putting {itemId} into armour slot {slot} with {armourPoints} armourpoints")
                    return
        
        #slot not in file yet
        entry = {"ItemId": itemId, "Slot": slot, "RemainingArmourpoints": armourPoints}
        self.saveFileLoader.armourPieces.append(entry)

    def getArmourNameFromSlot(self, slot) -> str:
        for entry in self.saveFileLoader.armourPieces:
            if entry["Slot"] == slot:
                return self.getArmourNameFromItemId(entry["ItemId"])
        return "None"

    def getArmourNameFromItemId(self, itemId):
        for entry in self.possibleArmourItems:
            if entry["ItemId"] == itemId:
                return entry["Name"]

    def deleteArmorPiece(self, slot):
        foundIndex = -1
        for index, entry in enumerate(self.saveFileLoader.armourPieces):
            if entry["Slot"] == slot:
                foundIndex = index
                
        if foundIndex != -1:
            del self.saveFileLoader.armourPieces[foundIndex]

    def onEntryChange(self, name, entryVar):
        value = 0
        try:
            value = int(entryVar.get())
            # print(f"Setting {name} to {value}")
            setting = self.findPlayerSetting(name)
            SavefileLoader.setRelevantSettingsValue(setting, value)

            if name == "MaxHealth":
                setting = self.findPlayerSetting("MaxHealth")
                maxHealth = SavefileLoader.getRelevantSettingsValue(setting)
                self.maxHealthVar.set(int(maxHealth))
                self.findScale("CurrentHealth").configure(to=maxHealth)

        except ValueError:
            pass

    def readStats(self):
        self.playerPosSetting = self.findPlayerSetting("player.position")
        playerPos = SavefileLoader.getRelevantSettingsValue(
            self.playerPosSetting)
        self.playerPositionVar.set(
            f"x: {int(playerPos[0])}, y: {int(playerPos[1])}, z: {int(playerPos[2])}")

        setting = self.findPlayerSetting("StrengthLevel")
        self.strengthVar.set(SavefileLoader.getRelevantSettingsValue(setting))

        setting = self.findPlayerSetting("MaxHealth")
        maxHealth = int(SavefileLoader.getRelevantSettingsValue(setting))
        self.maxHealthVar.set(maxHealth)
        self.findScale("CurrentHealth").configure(to=maxHealth)

        for stat in self.playerNpc.stats:
            setting = self.findPlayerSetting(stat.name)
            self.playerNpc.setStat(
                stat.name, SavefileLoader.getRelevantSettingsValue(setting))

    def findScale(self, name) -> tk.Scale:
        for scaleName, scale in self.scales:
            if scaleName == name:
                return scale

    def findPlayerSetting(self, name):
        for setting in self.saveFileLoader.playerState:
            if setting["Name"] == name:
                return setting

    def onStatChange(self, statIndex, statValue):
        statName = self.playerNpc.stats[statIndex].name
        print(f"Setting {statName} to {statValue}")

        setting = self.findPlayerSetting(statName)
        SavefileLoader.setRelevantSettingsValue(setting, statValue)

        if statName == "CurrentHealth":
            setting = self.findPlayerSetting("TargetHealth")
            SavefileLoader.setRelevantSettingsValue(setting, statValue)
