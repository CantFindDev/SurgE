# SurgE Growtopia surgery simulator discord bot
# Copyright (C) 2024 CantFind
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import math
import random
import pathlib
import urllib.parse

# Resolve data directory relative to the project root (parent of core/)
_DATA_DIR = pathlib.Path(__file__).parent.parent / "data"


class FileManager:
    @staticmethod
    def WriteToJson(FilePath: str, ListToRead: list):
        with open(FilePath, "w+") as file:
            json.dump(ListToRead, file, indent=4)

    @staticmethod
    def ReadFromJson(FilePath: str):
        with open(FilePath, "r+") as file:
            return json.load(file)


class SpecialConditions:

    Conditions = FileManager.ReadFromJson(_DATA_DIR / "special_conditions.json")

    @staticmethod
    def GetAllSpecialConditions():
        return [cond["condition_name"] for cond in SpecialConditions.Conditions]


class Maladies:

    Maladies = FileManager.ReadFromJson(_DATA_DIR / "maladies.json")

    @staticmethod
    def GetAllMaladieNames():
        return [disease["diagnostic"] for disease in Maladies.Maladies]


class Drops:

    Items = FileManager.ReadFromJson(_DATA_DIR / "items.json")

    @staticmethod
    def GetItemImageByName(Filename: str):
        url = "https://raw.githubusercontent.com/CantFindDev/SurgE/Release/Images/Items/"
        url += urllib.parse.quote(Filename, safe='') + ".png?raw=true"
        return url

    @staticmethod
    def GetSpesificItem(ItemName: str):
        for Item in Drops.Items:
            if Item['ItemName'].lower() == ItemName.lower():
                return Item

    @staticmethod
    def GetDrop():
        Random = math.floor(random.random() * 1000)
        for Item in Drops.Items:
            if Random < Item['ItemChance']:
                return Item


class Modifiers:

    Modif = FileManager.ReadFromJson(_DATA_DIR / "modifiers.json")

    @staticmethod
    def GetModifierByName(ModifName: str):
        if ModifName == None: return None
        for Modif in Modifiers.Modif:
            if Modif['ModifierName'].lower() == ModifName.lower():
                return Modif

    @staticmethod
    def GetModifierType(ModifName: str):
        if ModifName == None: return None
        return Modifiers.GetModifierByName(ModifName)["ModifierType"]

    @staticmethod
    def GetAllModifiersByNames():
        return [Modif["ModifierName"] for Modif in Modifiers.Modif]

    @staticmethod
    def GetNurseChance():
        Random = math.floor(random.random() * 100)
        if Random < 2:
            return True
        return False
