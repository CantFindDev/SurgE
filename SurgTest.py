from enum import Enum
import discord
import random
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from typing import Optional
import typing
import math
import json
import urllib.parse
import time

 # SurgE Growtopia surgery simulator discord bot
 # Copyright (C) 2024 CantFind
 #
 # This program is free software: you can redistribute it and/or modify
 # it under the terms of the GNU Affero General Public License as published
 # by the Free Software Foundation, either version 3 of the License, or
 # (at your option) any later version.
 #
 #  This program is distributed in the hope that it will be useful,
 #  but WITHOUT ANY WARRANTY; without even the implied warranty of
 #  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #  GNU Affero General Public License for more details.
 #
 # You should have received a copy of the GNU Affero General Public License
 # along with this program.  If not, see <https://www.gnu.org/licenses/>.

class Patient:
    def __init__(self, SkillLevel: int = 100, malady: Optional[str] = None, specialcondition: Optional[str] = None,TrainEMode: Optional[bool] = False):
        self.SleepLevel = 0
        self.SpongeCount = 0
        self.ScalpCount = 0
        self.StitCount = 0
        self.AntibioticCount = 0
        self.AntisepticCount = 0
        self.UltraSoundCount = 0
        self.LabKitCount = 0
        self.AnestCount = 0
        self.DefibCount = 0
        self.SplintCount = 0
        self.PinCount = 0
        self.ClampCount = 0
        self.TransfusionCount = 0
        self.SkillFailCount = 0

        self.Pulse = 40
        self.Site = 0  
        self.SiteDirtyness = 0
        self.BrokenBoneCount = 0
        self.ShatteredBoneCount = 0
        self.Incisions = 0
        self.BleedingLevel = 0
        self.IncisionsNeeded = 0
        self.HeartDamage = 0
        self.Temp = 98.6
        self.Fever = 0.0
        self.IsPatientFixed = False
        self.IsFixable = False
        self.IsUltrasoundUsed = False
        self.IsLabKitUsed = False
        self.LabWorked = False
        self.IsSurgeryEnded = False
        self.Antibs = False
        self.SkillLevel = SkillLevel
        self.TrainE = TrainEMode
        self.TrainEText = ""
        self.ToolText = "Patient is prepped for surgery."
        self.HeartText = ""
        self.diagnostic = ""
        self.DirtynessText = ""
        self.PatientText = ""
        self.PulseText = ""
        self.TempText = ""
        self.BoneText = ""
        self.IncisionText = ""
        self.ScanText = TextManager.ErrorText("The patient has not been diagnosed.")
        self.EndText = ""
        self.PatientStatus = PatientStatus.GetPatientState(PatientState.Awake)
        self.BleedingText = ""
        self.FeverText = ""
        self.SpecialCondition = None
        self.IsBrainWorms = False
        self.CurrentDisease = None
        self.BoneStatus = ""
        self.SpecialConditionText = ""
        self.SpecialConditionVisibility = False

        self.ScalpSensivity = 1
        self.AntibSensivity = 3
        self.DirtSensitivity = 0
        self.AnestSensitivity = 10
        self.BleedSensitivity = 1

        self.StartTime = 0

        if malady: self.SetSpesificDisease(malady)  
        else: self.SetRandomDisease()  
        if specialcondition: self.SetSpesificSpecialCondition(specialcondition)
        else: self.SetRandomSpecialCondition() 



    def SetRandomDisease(self):
        disease = random.choice(Maladies.Maladies)
        self.ApplyDisease(disease)

    def SetSpesificDisease(self, MaladyName: str):
        for disease in Maladies.Maladies:
            if disease['diagnostic'].lower() == MaladyName.lower():
                self.ApplyDisease(disease)
                break

    def SetSpesificSpecialCondition(self, ConditionName: str):
        for cond in SpecialConditions.Conditions:
            if cond['condition_name'].lower() == ConditionName.lower():
                self.ApplyCondition(cond)
                break
                
    def SetRandomSpecialCondition(self):
        Random = math.floor(random.random()* 10)
        for cond in SpecialConditions.Conditions:
            if Random < cond['condition_chance']:
                self.ApplyCondition(cond)

    def ApplyCondition(self,cond):
        self.SpecialCondition = cond["condition_name"]
        self.SpecialConditionVisibility = cond["condition_visibility"]
        self.SpecialConditionText = cond["condition_text"]
        self.ApplySpecialConditionValues()

    def ApplyDisease(self, disease):
        self.CurrentDisease = disease
        self.diagnostic = disease["diagnostic"]
        self.BleedingLevel = disease.get("bleeding", 0)
        self.BrokenBoneCount = disease.get("broken", 0)
        self.ShatteredBoneCount = disease.get("shattered", 0)
        self.IncisionsNeeded = disease.get("incisions_needed", 0)
        self.Temp = disease.get("temperature", 98.6)
        self.Fever = disease.get("fever", 0.0)
        self.SiteDirtyness = disease.get("dirt", 0)
        self.IsPatientFixed = disease.get("patient_fixed", False)
        self.IsUltrasoundUsed = disease.get("ultrasound_used",False)
        self.Pulse = disease.get("pulse", 40)

    def ApplySpecialConditionValues(self):
        match self.SpecialCondition:
            case "Tough Skin":
                self.IncisionsNeeded += 1
            case "Antibiotic-Resistant Infection":
                self.AntibSensivity /= 2
            case "Filthy":
                self.DirtSensitivity = 10
            case "Hyperactive":
                self.AnestSensitivity /= 2
            case "Hemophiliac":
                self.BleedSensitivity = 2

    def GetAllToolsUsed(self) -> str:
            tooltext = ""
            if self.SpongeCount > 0:
                 tooltext +=  ToolIcon.SurgicalSponge.value + " Sponges: "  + str(self.SpongeCount) + "\n"
            if self.ScalpCount > 0:
                 tooltext += ToolIcon.SurgicalScalpel.value +  " Scalpels: " + str(self.ScalpCount) + "\n"
            if self.StitCount > 0:
                 tooltext += ToolIcon.SurgicalStitches.value +  " Stitches: " + str(self.StitCount) + "\n"
            if self.AntibioticCount > 0:
                 tooltext += ToolIcon.SurgicalAntibiotics.value + " Antibiotics: " + str(self.AntibioticCount) + "\n"
            if self.AntisepticCount > 0:
                 tooltext += ToolIcon.SurgicalAntiseptic.value +  " Antiseptics: " + str(self.AntisepticCount) + "\n"
            if self.UltraSoundCount > 0:
                tooltext += ToolIcon.SurgicalUltrasound.value +  " Ultrasounds: " + str(self.UltraSoundCount) + "\n"
            if self.LabKitCount > 0:
                tooltext += ToolIcon.SurgicalLabKit.value + " Lab Kits: "  + str(self.LabKitCount) + "\n"
            if self.AnestCount > 0:
                tooltext+= ToolIcon.SurgicalAnesthetic.value + " Anesthetics: "  + str(self.AnestCount) + "\n"
            if self.DefibCount > 0:
                tooltext += ToolIcon.SurgicalDefib.value + " Defibrillators: "  + str(self.DefibCount) + "\n"
            if self.SplintCount > 0:
                tooltext += ToolIcon.SurgicalSplint.value + " Splints: "  + str(self.SplintCount) + "\n"
            if self.PinCount > 0:
                tooltext += ToolIcon.SurgicalPins.value + " Pins: " + str(self.PinCount) + "\n"
            if self.ClampCount > 0:
                tooltext += ToolIcon.SurgicalClamp.value +  " Clamps: " + str(self.ClampCount) + "\n"
            if self.TransfusionCount > 0:
                tooltext += ToolIcon.SurgicalTransfusion.value + " Transfusions: " + str(self.TransfusionCount) + "\n"
            return tooltext
    

    def UseTool(self, toolType: Enum) -> bool:
        success = random.random() * 100 > (self.Site - 30 - self.SkillLevel / 4)
        skillfail_occurred = not success
        match toolType:
            case ToolType.SurgicalAntiseptic:
                self.AntisepticCount += 1
                if success:
                    self.Site = min(self.Site + 20,20)
                    self.ToolText = "You disinfected the operating site."
                else:
                    self.SkillFailCount += 1
                    self.ToolText = f"{TextManager.ErrorText("[Skill Fail]: ")}" + "You spilled antiseptic on your shoes. They are very clean now."

            case ToolType.SurgicalDefib:
                self.DefibCount += 1
                if success:
                    self.ToolText = "You shocked the patient back to life!"       
                    self.HeartDamage = 0
                else:
                    self.SkillFailCount += 1
                    self.SiteDirtyness += 1
                    self.ToolText = f"{TextManager.ErrorText("[Skill Fail]: ")}" + "You electrocuted yourself!"    
    
            case ToolType.SurgicalSponge:
                self.SpongeCount += 1
                if success: 
                    if self.SiteDirtyness == 0:
                        self.ToolText = f"{TextManager.WarningText("Everything was already clean, you wasted a sponge!")}"
                    else:                      
                        self.SiteDirtyness = 0
                        self.ToolText = "You mopped up the operation site."
                else:
                    self.SkillFailCount += 1
                    self.ToolText = f"{TextManager.ErrorText("[Skill Fail]: ")}" + "You somehow managed to eat the sponge."
    
            case ToolType.SurgicalScalpel:
                self.ScalpCount += 1
                if self.PatientStatus == PatientStatus.GetPatientState(PatientState.Awake):
                    self.EndText = "You cut the patient while they were awake!"
                    self.IsSurgeryEnded = True
                elif self.Incisions > self.IncisionsNeeded:
                    self.ToolText = TextManager.ErrorText("You stabbed the patient in a vital organ!")
                    self.BleedingLevel += self.BleedSensitivity
                elif self.PatientStatus == PatientStatus.GetPatientState(PatientState.Unconscious) and self.Incisions >= 0:
                    self.Incisions += self.ScalpSensivity
                    if self.Incisions < self.IncisionsNeeded:
                        if success:
                            self.ToolText = "You've made a neat incision."  
                        else: 
                            self.SkillFailCount += 1
                            self.BleedingLevel += self.BleedSensitivity
                            self.ToolText = f"{TextManager.ErrorText("[Skill Fail]: ")}" + "This will leave a nasty scar, but you managed to cut the right place."
                else: self.ScalpCount -= 1

            case ToolType.SurgicalStitches:
                self.StitCount += 1
                if success:
                    if self.Incisions > 0:
                        self.ToolText = "You stitched up an incision."
                    elif self.BleedingLevel > 0:
                        self.ToolText = "You stitched up a bleeding wound."
                    else:
                        self.ToolText = "You tried to stitch your patient\'s mouth shut!" 
    
                    if self.Incisions > 0:
                        self.Incisions -= 1
                    if self.BleedingLevel > 0:
                        self.BleedingLevel -= 1
                else:
                    self.SkillFailCount += 1
                    self.ToolText = f"{TextManager.ErrorText("[Skill Fail]: ")}" + "You somehow tied yourself up in stitches!"
    
            case ToolType.SurgicalUltrasound:
                self.UltraSoundCount += 1
                if success:
                    self.IsUltrasoundUsed = True
                    self.SpecialConditionVisibility = True
                    self.ScanText = self.CurrentDisease["scan_text"]
                    self.ToolText = f"You scanned the patient with ultrasound, discovering they are suffering from {self.CurrentDisease["scan_text"]} {("You Found" + self.BoneStatus) if self.BoneStatus != "" else ""}"
                else:
                    self.SkillFailCount += 1
                    self.ToolText =  f"{TextManager.ErrorText("[Skill Fail]: ")}" + "You scanned the nurse with your ultrasound!"
    
            case ToolType.SurgicalLabKit:
                self.LabKitCount += 1
                if success:
                    self.IsLabKitUsed = True
                    self.LabWorked = True
                    self.ToolText = "You performed lab work on the patient, and have antibiotics at the ready."
                else:
                    self.SkillFailCount += 1
                    self.ToolText = f"{TextManager.ErrorText("[Skill Fail]: ")}" + "You contaminated the sample."

            case ToolType.SurgicalAntibiotics:
                self.AntibioticCount += 1
                if success:
                    if self.Temp > 98.6:
                        self.Fever -= self.AntibSensivity
                        self.ToolText = 'You used antibiotics to reduce the patient\'s infection.'
                    if self.Fever > -3:
                        self.Antibs = True
                else:
                    self.SkillFailCount += 1
                    self.Fever += 1
                    self.ToolText = f"{TextManager.ErrorText("[Skill Fail]: ")}" + 'This is the wrong medication! The bacteria like it.'
    
            case ToolType.SurgicalSplint:
                self.SplintCount += 1
                if success:
                    self.BrokenBoneCount -= 1
                    self.ToolText = "You splinted a broken bone."
                else:
                    self.SkillFailCount += 1
                    self.BleedingLevel += self.BleedSensitivity
                    self.ToolText = f"{TextManager.ErrorText("[Skill Fail]: ")}" + "You somehow cut the patient."
    
            case ToolType.SurgicalPins:
                self.PinCount += 1
                if success:
                    self.ShatteredBoneCount -= 1
                    self.BrokenBoneCount += 1
                    self.ToolText = "You pinned a shattered bone together. Don\'t forget to splint it!"
                else:
                    self.SkillFailCount += 1
                    self.BleedingLevel += self.BleedSensitivity
                    self.ToolText = f"{TextManager.ErrorText("[Skill Fail]: ")}" + "You jabbed the pin through the artery!"
    
            case ToolType.SurgicalAnesthetic:
                self.AnestCount += 1
                if success:
                    if self.PatientStatus == PatientStatus.GetPatientState(PatientState.Unconscious) or self.PatientStatus == PatientStatus.GetPatientState(PatientState.NearComa):
                        if self.TrainE and self.PatientStatus == PatientStatus.GetPatientState(PatientState.Unconscious):
                            self.PatientStatus = PatientStatus.GetPatientState(PatientState.NearComa)
                            self.ToolText = "The patient falls into a deep sleep."
                        else:
                            self.EndText = "You put your patient to sleep. Permanently!"
                            self.IsSurgeryEnded = True
                    else:
                        self.PatientStatus = PatientStatus.GetPatientState(PatientState.Unconscious)
                        self.SleepLevel = self.AnestSensitivity
                        self.ToolText = "The patient is now asleep."
                else:
                    self.SkillFailCount += 1
                    self.SiteDirtyness += 1
                    self.ToolText = f"{TextManager.ErrorText("[Skill Fail]: ")}" + "You end up inhaling all the anesthetic yourself. You feel woozy."

            case ToolType.SurgicalTransfusion:
                self.TransfusionCount += 1
                if success:
                    self.Pulse = min(self.Pulse + 15,40)
                    self.ToolText = "You transfused several pints of blood into your patient."
                else:
                    self.SkillFailCount += 1
                    self.SiteDirtyness += 1
                    self.ToolText = f"{TextManager.ErrorText("[Skill Fail]: ")}" + "You spilled blood everywhere!"

            case ToolType.SurgicalClamp:
                self.ClampCount += 1
                if success:
                    self.BleedingLevel -= 1
                    self.ToolText = "You clamped up some blood vessels"
                else:
                    self.SkillFailCount += 1
                    self.ToolText = f"{TextManager.ErrorText("[Skill Fail]: ")}" + "The clamp fell out of your hand, oh well."     
                      
            case ToolType.FixIt:
                if success and self.IsFixable and not self.IsPatientFixed:
                    self.ToolText = "You fixed the issue!"
                    self.IsPatientFixed = True
                    self.IsFixable = False #It should not be fixable after being fixed...
                else:
                    self.SkillFailCount += 1
                    self.ToolText = f"{TextManager.ErrorText("[Skill Fail]: ")}" + "You screwed it up! Try again."
                
        self.UpdatePatientValues(toolType)
        self.UpdatePatientUI()
        return skillfail_occurred
    
    def UpdatePatientUI(self):
        if self.IsFixable: self.ScanText = self.CurrentDisease.get("fix_text",self.CurrentDisease["scan_text"])
        elif self.IsPatientFixed: self.ScanText = self.CurrentDisease.get("post_fix_text",self.CurrentDisease["scan_text"])

        if self.SiteDirtyness >= 10: self.DirtynessText = TextManager.ErrorText("You can't see what you are doing!")
        elif self.SiteDirtyness >= 4: self.DirtynessText = TextManager.WarningText("It is becoming hard to see your work.")
        else: self.DirtynessText = ""

        if self.BleedingLevel > 0:
            text = "Patient is "
            if self.BleedingLevel >= 4: text += f"loosing blood {TextManager.ErrorText("very quickly!")}"
            elif self.BleedingLevel == 1: text += f"losing blood {TextManager.SoftText("slowly.")}"
            else: text += f"{TextManager.WarningText("losing blood!")}"
            self.BleedingText = text + "\n"
        else:
           self.BleedingText = ""

        if self.Pulse < 11: self.PulseText = TextManager.ErrorText("Extremely Weak")
        elif self.Pulse < 21: self.PulseText = TextManager.WarningText("Weak")
        elif self.Pulse < 31: self.PulseText = TextManager.SoftText("Steady")
        else: self.PulseText = TextManager.PositiveText("Strong")

        if self.Fever > 0 and self.Temp > 100:
            text = "Patient\'s fever is "
            if self.Fever < 0.5: text += TextManager.SoftText(" slowly rising!")
            elif self.Fever > 2: text += TextManager.ErrorText(" climbing fast!")
            else: text += TextManager.WarningText(" climbing!")
            self.FeverText = text + "\n"
        else: self.FeverText = ""

        if self.Site < -3: self.SiteText = TextManager.ErrorText("Unsanitary")
        elif self.Site < -1: self.SiteText = TextManager.WarningText("Unclean")
        elif self.Site < 1: self.SiteText = TextManager.SoftText("Not sanitized")
        else: self.SiteText = TextManager.PositiveText("Clean")

        if self.Temp < 100: self.TempText = TextManager.PositiveText(self.Temp) 
        elif self.Temp < 104: self.TempText = TextManager.SoftText(self.Temp)
        elif self.Temp < 106: self.TempText = TextManager.WarningText(self.Temp) 
        else: self.TempText = TextManager.ErrorText(self.Temp)

        broken = str(self.BrokenBoneCount)
        shatter = str(self.ShatteredBoneCount)
        if (self.BrokenBoneCount > 0 or self.ShatteredBoneCount > 0) and self.IsUltrasoundUsed == True:
            txt = "Bones: "
            if self.BrokenBoneCount > 0: txt += TextManager.ErrorText(broken + " broken") if self.BrokenBoneCount > 1 else TextManager.WarningText(broken + " broken ")
            if self.ShatteredBoneCount > 0: txt +=TextManager.ErrorText("," + shatter + " shattered") if self.ShatteredBoneCount > 1 else TextManager.WarningText(shatter + " shattered")
            self.BoneText = txt
        else: self.BoneText = ""
        
        if self.Incisions == self.IncisionsNeeded: self.IncisionText = TextManager.PositiveText(self.Incisions)
        else: self.IncisionText = self.Incisions

        if self.HeartDamage > 0: self.PatientStatus = PatientStatus.GetPatientState(PatientState.HeartStopped)
        elif self.SleepLevel == 0: self.PatientStatus = PatientStatus.GetPatientState(PatientState.Awake)
        elif self.SleepLevel < 3 and self.SleepLevel > 0: self.PatientStatus = PatientStatus.GetPatientState(PatientState.ComingTo)
        else: self.PatientStatus = PatientStatus.GetPatientState(PatientState.Unconscious)
        
        if self.HeartDamage > 0:
            self.HeartText = TextManager.ErrorText("Patient\'s heart has stopped!")
        else:
            self.HeartText = ""
        
        #Train-E
        if self.TrainE:
            self.TrainEText = ""
            #Heart Stopped
            if self.HeartDamage > 0: 
                self.TrainEText += TextManager.ErrorText("Heart Stopped") + f" - You need to {TextManager.WarningText("Revive")} your patient with a {TextManager.PurpieText("Defiblirator")}!"
                return
            #Awake
            if self.SleepLevel == 0 and self.Incisions > 0: self.TrainEText += TextManager.ErrorText("Awake") + f" - Your patient is {TextManager.WarningText("Awake")}. Use {TextManager.PurpieText("Anesthetic")} to put them to sleep until you have closed the wound.\n"
            #Stitch
            if self.Incisions > 0 and self.IsPatientFixed: self.TrainEText += TextManager.PositiveText("Stitch it Up!") + f" - The issue is fixed! It's time to close it up with {TextManager.PurpieText("Stitches")}.\n"
            #FixIt
            if self.IsFixable: self.TrainEText += TextManager.PositiveText("Fix It!") + f" - You have found the issue and can now {TextManager.PurpieText("Fix It")}.\n"
            #Cleanless
            if self.Site < 1: self.TrainEText += TextManager.PositiveText("Clean the Area") + f" - Clean the area with {TextManager.PurpieText("Antiseptic")}.\n"
            #PrepPatient
            if self.SleepLevel == 0 and self.IsUltrasoundUsed and self.IncisionsNeeded > 0: self.TrainEText += TextManager.PositiveText("Prep Patient") + f" - Apply {TextManager.PurpieText("Anesthetic")} to put the patient to sleep.\n"
            #Incision
            if not self.IsFixable and not self.IsPatientFixed and self.SleepLevel > 0 and self.IsUltrasoundUsed: self.TrainEText += TextManager.PositiveText("Make an Incision!") + f" - Use {TextManager.PurpieText("Scalpel")} to make an incision.\n"
            #Visibility
            if self.SiteDirtyness >= 4: self.TrainEText += TextManager.WarningText("Poor Visibility") + f" - Apply a {TextManager.PurpieText("Sponge")}. Poor visibility increases the chance of a {TextManager.WarningText("Skill Failure")}.\n"
            #Diagnosis
            if not self.IsUltrasoundUsed or (not self.IsLabKitUsed and not self.IsUltrasoundUsed): self.TrainEText += TextManager.WarningText("Diagnosis") + f" - You can use the {TextManager.PurpieText("Ultrasound")} {f"or {TextManager.PurpieText("Lab Kit")}" if not self.IsLabKitUsed else ""} to diagnose the illness\n"
            #Losing Blood
            if self.BleedingLevel > 0: self.TrainEText += TextManager.WarningText("Losing Blood") if self.BleedingLevel < 4 else (TextManager.ErrorText("Losing Blood very quickly")) + f" - Apply {f"{TextManager.PurpieText("Clamps")} to reduce {TextManager.WarningText("Bleeding")} during surgery." if self.Incisions > 0 else f"{TextManager.PurpieText("Stitches")} to reduce {TextManager.WarningText("Bleeding")}."}\n"
            #Shattered Bone
            if self.ShatteredBoneCount > 0 and self.IsUltrasoundUsed: self.TrainEText += TextManager.WarningText("Shattered Bone") + f" - Apply {TextManager.PurpieText("Pins")}.You must put the patient to sleep with {TextManager.PurpieText("Anesthetic")} and {f"make an insicion with a {"" if self.IsFixable or self.IsPatientFixed else TextManager.PurpieText("Scalpel")} before you can apply pins."}\n"
            #Broken Bone
            if self.BrokenBoneCount > 0 and self.IsUltrasoundUsed: self.TrainEText += TextManager.WarningText("Broken Bone") + f" - Apply a {TextManager.PurpieText("Splint")}.\n"
            #Fever
            if self.Fever > 0: self.TrainEText += (TextManager.WarningText("Fever") if self.Fever < 0.5 else TextManager.ErrorText("High Fever")) + f" - {"Apply" if self.IsLabKitUsed else f"Diagnose the {TextManager.WarningText("Infection")} With a {TextManager.PurpieText("Lab Kit")} then apply"} {TextManager.PurpieText("Antibiotics")} to bring down {TextManager.WarningText("Temp")}\n"
            #Antibiotics 
            if self.Temp > 98.8 and self.Fever > 0 and self.IsLabKitUsed: self.TrainEText += TextManager.PositiveText("Antibiotics") + f" - Apply {TextManager.PurpieText("Antibiotics")} to prevent any infection. If all else fails, give antibiotics.\n"
            #Pulse
            if self.Pulse < 11: self.TrainEText += TextManager.ErrorText("Extremely Weak Pulse") + f" - You can increase the {TextManager.WarningText("Pulse")} with a {TextManager.PurpieText("Blood Transfusion")}."
            #Coming To
            if self.SleepLevel < 3 and self.SleepLevel > 0 and self.Incisions > 0: self.TrainEText += TextManager.WarningText("Coming To") + f" - Your patient is about to wake up but you still have some {TextManager.WarningText("Incisions")}. Use {TextManager.PurpieText("Anesthetic")} to keep them unconscious until you have closed to wound.\n"
    
    def UpdatePatientValues(self, toolType : Enum):

        if self.Incisions >= self.IncisionsNeeded and not self.IsPatientFixed:
            if  self.IsUltrasoundUsed:
                self.IsFixable = True
                self.Incisions = self.IncisionsNeeded
            else:
                self.IsFixable = False
            

        self.SiteDirtyness += self.BleedingLevel + self.Incisions

        #Pulse
        self.Pulse -= self.BleedingLevel + min(self.Incisions, 1)

        if self.Pulse < 1 and self.EndText == "":
            self.EndText = "The patient bled out!"
            self.IsSurgeryEnded = True
        
        #Fever
        if self.Fever < 0:
            if self.Fever > -0.06:
                self.Fever = 0
            elif self.Antibs:
                self.Fever = (self.Fever - self.AntibSensivity) / 2
        elif ((self.Site <= 2) and (self.BleedingLevel > 0) or (self.Site <= 4) and (self.Incisions > 0)):
            self.Fever += 0.06
        self.Temp += self.Fever
        self.Temp = round(self.Temp * 100,2) / 100
        
        if self.Temp < 98.6:
            self.Temp = 98.6 
        self.Antibs = False   
        # Managing status, heart stopping
        if (((self.SleepLevel > 0) and (random.random() > 0.9 and toolType != ToolType.SurgicalDefib)) or (self.HeartDamage > 0)):
             self.HeartDamage +=1
        else:
            self.SleepLevel = max(self.SleepLevel - 1, 0)

        if self.HeartDamage == 3:
            self.IsSurgeryEnded = True
            self.EndText="You failed to resucicate your patient in time!"

        if self.Incisions > 0 and self.PatientStatus == PatientStatus.GetPatientState(PatientState.Awake):
            self.BleedingLevel += self.BleedSensitivity
            self.PatientText = TextManager.ErrorText("The patient screams and flails!")
        else: self.PatientText = ""
        
        self.Site -= math.floor(self.SiteDirtyness / 3) + self.DirtSensitivity
        if self.Site < -25:
            self.Site = -25

        if  self.Temp >= 111:
            self.EndText = "Your patient succumbed to infection!"
            self.IsSurgeryEnded = True

        if  self.IsPatientFixed and self.BleedingLevel == 0 and self.Incisions == 0 and self.Temp < 101 and self.ShatteredBoneCount == 0 and self.BrokenBoneCount == 0 and self.HeartDamage == 0 and self.EndText == "":
            self.EndText = "The surgery was a success!\n"
            self.IsSurgeryEnded = True

    def SetCurrentPatientEmbed(self, embed : discord.Embed) -> str:
        if self.IsSurgeryEnded:
            embed.title = f"{"Train-E" if self.TrainE else "Surg-E"} | Time Elapsed: {round(time.time() - self.StartTime)} Seconds"
            embed.description = f"## {self.EndText}\n\n"
            embed.description += TextManager.AddFeild(value=f"**Malady:**\n{self.CurrentDisease["diagnostic"]}\n", inline=False)
            if self.SpecialConditionText != "" and self.SpecialConditionVisibility: embed.description += TextManager.AddFeild(value=f"**Special Condition:**\n{self.SpecialCondition}\n", inline=False)
            if self.SkillFailCount > 0: embed.description += TextManager.AddFeild(value=f"**Skill Fails:**\n{self.SkillFailCount}\n", inline=False)
            embed.description += TextManager.AddFeild(value=f"**Skill Level:**\n{self.SkillLevel}\n", inline=False)
            embed.description += TextManager.AddFeild(value=f"**Tools Used:**\n{self.GetAllToolsUsed()}", inline=False)
            item = Drops.GetDrop()
            if self.EndText == "The surgery was a success!\n":
                embed.description += TextManager.AddFeild(value=f"**{item["ItemName"]}**",inline=False)
                embed.set_image(url=Drops.GetItemImageByName(item["ItemName"]))
        else:
            embed.title = f"Surgery Simulator| Skill Level: {self.SkillLevel}\n\n" 
            embed.description = ""
            embed.description += TextManager.ansistart + "\n"
            embed.description += f"{TextManager.WarningText(self.SpecialConditionText)+"\n" if self.SpecialCondition != "None" and self.SpecialConditionVisibility else "\n"}" + f"{TextManager.BoldText(self.ScanText)}\n"
            embed.description += TextManager.AddFeild(value=f"Pulse: {self.PulseText}", inline=True)
            embed.description += TextManager.AddFeild(value=f"Status: {self.PatientStatus}", inline=True)
            embed.description += TextManager.AddFeild(value=f"Temp: {self.TempText}", inline=True)
            embed.description += TextManager.AddFeild(value=f"Operation site: {self.SiteText}", inline=True)
            if self.DirtynessText != "":embed.description +=  TextManager.AddFeild(value=f"{self.DirtynessText}", inline=False)
            embed.description += TextManager.AddFeild( value=f"Incisions: {self.IncisionText}", inline=True)
            if self.BoneText != "": embed.description += TextManager.AddFeild(value=f"{self.BoneText}", inline=True)
            if self.PatientText != "": embed.description += TextManager.AddFeild(value=f"{self.PatientText}", inline=False)
            if self.BleedingText != "": embed.description += TextManager.AddFeild(value=f"{self.BleedingText}", inline=False)
            if self.FeverText != "": embed.description += TextManager.AddFeild(value=f"{self.FeverText}", inline=False)
            if self.ToolText != "": embed.description += TextManager.AddFeild(value=f"{TextManager.SoftText(self.ToolText)}", inline=False)
            if self.HeartText != "": embed.description += TextManager.AddFeild(value=f"{self.HeartText}", inline=False)
            if self.TrainE == True: embed.description += TextManager.AddFeild(value=f"Bot Tips:\n{self.TrainEText}", inline=False)
            embed.description += "\n" + TextManager.ansiend
            
class PatientState(Enum):
    HeartStopped = 0
    Awake = 1
    ComingTo = 2
    Unconscious = 3
    NearComa = 4

class PatientStatus:
    @staticmethod
    def GetPatientState(patientState : Enum) -> str:
        match patientState.value:
            case 0:
                return f"{TextManager.ErrorText("Heart Stopped!")}"
            case 1:
                return f"{TextManager.ErrorText("Awake")}"
            case 2:
                return f"{TextManager.WarningText("Coming To")}"
            case 3:
                return f"{TextManager.PositiveText("Unconscious")}"
            case 4:
                return f"{TextManager.ErrorText("Near Coma")}" #Traine-E Exclusive
class FileManager:
    @staticmethod
    def WriteToJson(FilePath:str,ListToRead:list):
        with open(FilePath, "w+") as file:
            json.dump(ListToRead, file, indent=4)

    @staticmethod
    def ReadFromJson(FilePath:str):
        with open(FilePath, "r+") as file:
            return json.load(file)

class SpecialConditions:

    Conditions = FileManager.ReadFromJson("SpecialConditions.json")

    @staticmethod
    def GetAllSpecialConditions():
        return [cond["condition_name"] for cond in SpecialConditions.Conditions]
    
class Maladies:

    Maladies = FileManager.ReadFromJson("Maladies.json")

    @staticmethod
    def GetAllMaladieNames():
        return [disease["diagnostic"] for disease in Maladies.Maladies]

class Drops:

    Items = FileManager.ReadFromJson("Items.json")

    @staticmethod
    def GetItemImageByName(Filename : str):
      url = "https://raw.githubusercontent.com/CantFindDev/SurgE/Release/Images/Items/"
      url += urllib.parse.quote(Filename, safe='') + ".png?raw=true"
      return url
    @staticmethod
    def GetSpesificItem(ItemName : str):
        for Item in Drops.Items:
            if Item['ItemName'].lower() == ItemName.lower():
                return Item
            
    @staticmethod
    def GetDrop():
        Random = math.floor(random.random()* 1000)
        for Item in Drops.Items:
            if Random < Item['ItemChance']:
                return Item


class ToolType(Enum):
    SurgicalAntibiotics = "SurgicalAntibiotics"
    SurgicalAntiseptic = "SurgicalAntiseptic"
    SurgicalAnesthetic = "SurgicalAnesthetic"
    SurgicalClamp = "SurgicalClamp" 
    SurgicalDefib = "SurgicalDefib"
    SurgicalPins = "SurgicalPins"
    SurgicalLoveMallet = "SurgicalLoveMallet"
    SurgicalSponge = "SurgicalSponge"
    SurgicalScalpel = "SurgicalScalpel"
    SurgicalStitches = "SurgicalStitches"
    SurgicalSplint = "SurgicalSplint"
    SurgicalUltrasound = "SurgicalUltrasound"
    SurgicalTransfusion = "SurgicalTransfusion"
    SurgicalLabKit = "SurgicalLabKit"
    FixIt = "FixIt"
    

class ToolIcon(Enum):
    SurgicalAntibiotics = "<:SurgicalAntibiotics:1275847290787074049>"
    SurgicalAntiseptic = "<:SurgicalAntiseptic:1275847308088578213>"
    SurgicalAnesthetic = "<:SurgicalAnesthetic:1275847279189823498>"
    SurgicalClamp = "<:SurgicalClamp:1275847320503848970>" 
    SurgicalDefib = "<:SurgicalDefibrillator:1275847332545695948>"
    SurgicalPins = "<:SurgicalPins:1275259504535142502>"
    SurgicalLoveMallet = "<:SurgicalLoveMallet:1275847358940446852>"
    SurgicalSponge = "<:SurgicalSponge:1275847403404132413>"
    SurgicalScalpel = "<:SurgicalScalpel:1275847384475238440>"
    SurgicalStitches = "<:SurgicalStitches:1275847413910864024>"
    SurgicalSplint = "<:SurgicalSplint:1275847394650751139>"
    SurgicalUltrasound = "<:SurgicalUltrasound:1275847435477975143>"
    SurgicalTransfusion = "<:SurgicalTransfusion:1275847423897505872>"
    SurgicalLabKit = "<:SurgicalLabKit:1275847345669672980>"
    FixIt = "<:FixIt:1275847264698503231>"
    EmptySurgeryTray = "<:EmptySurgeryTray:1275847243341238384>"

class SurgeryView(View): 
    def __init__(self, surgery, author):
        super().__init__(timeout=1800)
        self.author = author
        self.surgery = surgery
        self.patient : Patient = surgery.patient
        self.GenerateToolButtons()

    async def interaction_check(self, inter: discord.Interaction) -> bool:
     if inter.user != self.author:
        await inter.response.send_message(content="Let the doctor do their job!", ephemeral=True)
        return False
     return True

    def GenerateToolButtons(self):
        IsSiteClean = self.patient.SiteDirtyness < 10
        tools = [
            (ToolIcon.SurgicalSponge.value,ToolType.SurgicalSponge, True),
            (ToolIcon.SurgicalScalpel.value,ToolType.SurgicalScalpel, IsSiteClean),
            (ToolIcon.SurgicalStitches.value,ToolType.SurgicalStitches, IsSiteClean),
            (ToolIcon.SurgicalAntibiotics.value,ToolType.SurgicalAntibiotics, self.patient.LabWorked and IsSiteClean),
            (ToolIcon.SurgicalAntiseptic.value,ToolType.SurgicalAntiseptic, IsSiteClean),
            (ToolIcon.FixIt.value,ToolType.FixIt, (self.patient.IsFixable and (not self.patient.IsPatientFixed or self.patient.IsBrainWorms or self.patient.IncisionsNeeded == self.patient.Incisions)) and IsSiteClean),
            (ToolIcon.SurgicalUltrasound.value,ToolType.SurgicalUltrasound, not self.patient.IsUltrasoundUsed and IsSiteClean),
            (ToolIcon.SurgicalLabKit.value,ToolType.SurgicalLabKit, not self.patient.IsLabKitUsed and IsSiteClean),
            (ToolIcon.SurgicalAnesthetic.value,ToolType.SurgicalAnesthetic, IsSiteClean),
            (ToolIcon.SurgicalDefib.value, ToolType.SurgicalDefib, IsSiteClean and self.patient.HeartDamage > 0),
            (ToolIcon.SurgicalSplint.value, ToolType.SurgicalSplint, IsSiteClean),
            (ToolIcon.SurgicalPins.value, ToolType.SurgicalPins, IsSiteClean and self.patient.Incisions > 0),
            (ToolIcon.SurgicalClamp.value, ToolType.SurgicalClamp, IsSiteClean and self.patient.Incisions > 0),
            (ToolIcon.SurgicalTransfusion.value,ToolType.SurgicalTransfusion, IsSiteClean),
            (ToolIcon.SurgicalLoveMallet.value, ToolType.SurgicalLoveMallet, False) #Valentines Only
        ]

        for toolIcon ,toolType, toolVisibility  in tools:
            if toolVisibility:
                button = Button(emoji=toolIcon, style=discord.ButtonStyle.secondary)
                ToolCallBack = self.ToolCallback(toolType)
                if ToolCallBack is None:
                    continue
                button.callback = ToolCallBack
                self.add_item(button)
            else:
                button = Button(emoji=ToolIcon.EmptySurgeryTray.value, style=discord.ButtonStyle.secondary,disabled=True)
                self.add_item(button)

        giveupbutton = Button(label="Give Up", style=discord.ButtonStyle.danger)
        giveupbutton.callback = self.GiveUpOnSurgery
        self.add_item(giveupbutton)

    async def GiveUpOnSurgery(self, interaction: discord.Interaction):
        self.clear_items()
        embed = discord.Embed(
            title= "Surgery Aborted",
            description=f"You have chosen to abandon the surgery. Remember, doctors need courage and precision—today just wasn't your day. Maybe next time you'll become the hero of the operating room! Until then, thanks for trying, [Dr.{interaction.user.display_name}](https://github.com/CantFindDev/SurgE). Brave efforts are also part of the journey!",
            color=discord.Color.red()
        )
        self.patient.IsSurgeryEnded = True
        await interaction.response.edit_message(embed=embed, view=self)
    
    def ToolCallback(self, toolType):
        async def callback(interaction: discord.Interaction):

            skillfail_occurred = self.patient.UseTool(toolType)
            embed_color = discord.Color.red() if skillfail_occurred else discord.Color.blue()

            if self.patient.IsSurgeryEnded:
                embed_color = discord.Color.green() if "success" in self.patient.EndText.lower() else discord.Color.red()
                self.clear_items()

            embed = discord.Embed(
                title= "",
                description="",
                color=embed_color
            )
            
            self.clear_items()
            if not self.patient.IsSurgeryEnded:
                self.GenerateToolButtons()
            self.patient.SetCurrentPatientEmbed(embed)
            embed.set_footer(text="Surg system is being developed by CantFind")
            await interaction.response.edit_message(embed=embed, view=self)

        return callback
    
class TextManager:
    ansistart = ""
    ansiend = ""
    ColoredUI = False
    FeildCount = 0
    @staticmethod
    def setTextManager(ColoredUI : bool):
        TextManager.ColoredUI = ColoredUI
        TextManager.ansistart = "```ansi\n" if ColoredUI else ""
        TextManager.ansiend = "```" if ColoredUI else ""
        TextManager.FeildCount = 0
    @staticmethod
    def ErrorText(text: str):
        txt = ""
        if (TextManager.ColoredUI): txt = f"\x1B[2;31m{text}\x1B[0m\x1B[2;31m\x1B[0m" 
        else: txt = f"**[{text}](https://github.com/CantFindDev/SurgE)**"
        return txt
    @staticmethod
    def WarningText(text : str):
        txt = ""
        if (TextManager.ColoredUI): txt = f"\x1B[2;31m\x1B[2;32m\x1B[2;33m{text}\x1B[0m\x1B[2;32m\x1B[0m\x1B[2;31m\x1B[0m\x1B[2;31m\x1B[0m"
        else: txt = f"**_{text}_**"
        return txt
    @staticmethod
    def PositiveText(text : str):
        txt = ""
        if (TextManager.ColoredUI): txt = f"\x1B[2;31m\x1B[2;32m{text}\x1B[0m\x1B[2;31m\x1B[0m\x1B[2;31m\x1B[0m"
        else: txt = f"*[{text}](https://github.com/CantFindDev/SurgE)*"
        return txt
    @staticmethod
    def SoftText(text : str):
        txt = ""
        if (TextManager.ColoredUI): txt = f"\x1B[2;34m{text}\x1B[0m"
        else: txt = f"_{text}_"
        return txt   
    @staticmethod
    def PurpieText(text : str):
        txt = ""
        if (TextManager.ColoredUI): txt = f"\x1B[2;35m\x1B[2;35m{text}\x1B[0m\x1B[2;35m\x1B[0m"
        else: txt = f"[{text}](https://github.com/CantFindDev/SurgE)"
        return txt
    @staticmethod
    def BoldText(text :str):
        txt = ""
        if (TextManager.ColoredUI): txt = f"\x1B[1;2m{text}\x1B[0m\x1B[1;2m\x1B[0m"
        else: txt = f"**{text}**"
        return txt
    @staticmethod
    def AddFeild(value : str, inline : bool = False) -> str:
        txt = ""
        if inline:
            if TextManager.FeildCount == 0:
                txt = "\n"
            txt += value
            if TextManager.FeildCount == 1:
                TextManager.FeildCount = 0
            else:
                txt += TextManager.AddSpace(2)
                TextManager.FeildCount +=1
        else:
            if TextManager.FeildCount > 0:
                txt += "\n"
                TextManager.FeildCount = 0
            txt += "\n" + value
        return txt
    @staticmethod
    def AddSpace(SpaceCount : int) -> str:
        txt = ""
        for number in range(SpaceCount):
            txt += " ‍"
        return txt
class Surgery:
    def __init__(self, patient, user):
        self.patient = patient
        self.user = user

class SurgeryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    async def AutoCompleteMalady(self,interaction: discord.Interaction, 
    current: str)  -> typing.List[app_commands.Choice[str]]:
     match = []
     for disease in Maladies.GetAllMaladieNames():
        if current.lower() in disease.lower():
            match.append(app_commands.Choice(name=disease, value=disease))
        if len(match) >= 25:
           break
     return match    

    async def AutoCompleteCondition(self,interaction: discord.Interaction, 
    current: str)  -> typing.List[app_commands.Choice[str]]:
     CondMatch = []
     for condition in SpecialConditions.GetAllSpecialConditions():
        if current.lower() in condition.lower():
            CondMatch.append(app_commands.Choice(name=condition, value=condition))
        if len(CondMatch) >= 25:
           break
     return CondMatch
    
    @app_commands.command(name="surg", description="Start a surgery simulation.")
    @app_commands.describe(colored_ui="Make the ui colored (Might not work on mobile)",hidden_embed="Hide the surgery UI from other people", traine_mode="I'm not Train-E but I can try to act like it :)", malady="Select a specific malady to surg", special_condition="Select a special condition", skill_level="Set the skill level (default is 100)")
    @app_commands.autocomplete(malady=AutoCompleteMalady,special_condition=AutoCompleteCondition)
    async def surg(self ,interaction: discord.Interaction,colored_ui: Optional[bool] = False, hidden_embed: Optional[bool] = False, traine_mode: Optional[bool] = False, malady: Optional[str] = None, special_condition: Optional[str] = None, skill_level: Optional[int] = 100):
        await interaction.response.defer(ephemeral=hidden_embed)

        if malady is not None and malady not in Maladies.GetAllMaladieNames():
            return await interaction.followup.send(
                embed=discord.Embed( title="Invalid malady!",description="**Please choose from the following:**\n" + "\n".join(Maladies.GetAllMaladieNames()), color=discord.Color.red())
            )

        if special_condition is not None and special_condition not in SpecialConditions.GetAllSpecialConditions():
            return await interaction.followup.send(
                embed=discord.Embed( title="Invalid Condition!",description="**Please choose from the following:**\n" + "\n".join(SpecialConditions.GetAllSpecialConditions()), color=discord.Color.red())
            )
        
        patient = Patient(SkillLevel=100 if skill_level > 100 else 0 if skill_level < 0 else skill_level, malady=malady, specialcondition=special_condition,TrainEMode=traine_mode)
        surgery = Surgery(patient=patient, user=interaction.user)
        view = SurgeryView(surgery,interaction.user)
        TextManager.setTextManager(colored_ui)
        embed = discord.Embed(
            title= "",
            description="",
            color=discord.Color.blue()
        ) 
        patient.UpdatePatientUI()
        patient.SetCurrentPatientEmbed(embed)
        embed.set_footer(text="Surg system is being developed by CantFind")
        await interaction.followup.send(embed=embed, view=view)
        patient.StartTime = time.time()

async def setup(bot):
    await bot.add_cog(SurgeryCog(bot))
    