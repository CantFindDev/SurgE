from enum import Enum
import discord
import random
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from typing import Optional
import typing
import math

class Patient:
    def __init__(self, SkillLevel: int = 100, malady: Optional[str] = None, specialcondition: Optional[str] = None):
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
        self.ToolText = "Patient is prepped for surgery."
        self.diagnostic = ""
        self.PatientText = ""
        self.PulseText = ""
        self.TempText = ""
        self.BoneText = ""
        self.IncisionText = ""
        self.ScanText = "The patient has not been diagnosed."
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
        for cond in SpecialConditions.conditions:
            if cond['condition_name'].lower() == ConditionName.lower():
                self.ApplyCondition(cond)
                break
                
    def SetRandomSpecialCondition(self):
        cond = random.choice(SpecialConditions.conditions)
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
        self.treatment_steps = disease["steps"]

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


    def UseTool(self, toolType: Enum) -> bool:
        success = random.random() * 100 > (30 - self.SkillLevel / 4)
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
                    self.ToolText = "You stabbed the patient in a vital organ!"
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
                    if self.Incisions == self.IncisionsNeeded and not self.IsPatientFixed:
                        self.IsFixable = True
                    else:
                        self.IsFixable = False
            case ToolType.SurgicalStitches:
                self.StitCount += 1
                if success:
                    if self.Incisions > 0:
                        self.ToolText = "You stitched up an incision."
                    elif self.BleedingLevel > 0:
                        self.ToolText = "You stitched up a bleeding wound."
                    else:
                        self.ToolText = "You tried to stitch your patient's mouth shut!" 
    
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
                    if self.PatientStatus == PatientStatus.GetPatientState(PatientState.Unconscious):
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
        if self.SiteDirtyness >= 10: self.ToolText = TextManager.ErrorText("You can't see what you are doing!")

        if self.BleedingLevel > 0:
            text = "Patient is "
            if self.BleedingLevel >= 4: text += f"loosing blood {TextManager.ErrorText("fast!")}"
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

        if self.Temp == 98.6: self.TempText = TextManager.PositiveText(self.Temp) 
        elif self.Temp > 98.8: self.TempText = TextManager.SoftText(self.Temp)
        elif self.Temp > 104: self.TempText = TextManager.WarningText(self.Temp) 
        elif self.Temp > 106: self.TempText = TextManager.ErrorText(self.Temp) 
        else: self.TempText = ""

        broken = str(self.BrokenBoneCount)
        shatter = str(self.ShatteredBoneCount)
        if (self.BrokenBoneCount > 0 or self.ShatteredBoneCount > 0) and self.IsUltrasoundUsed == True:
            txt = "Bones: "
            if self.BrokenBoneCount > 0: txt += broken + " broken "
            if self.ShatteredBoneCount > 0: txt += shatter + " shattered "
            self.BoneText = txt
        else: self.BoneText = ""
        
        if self.IsFixable: self.IncisionText = TextManager.PositiveText(self.Incisions)
        else: self.IncisionText = self.Incisions

        if self.HeartDamage > 0: self.PatientStatus = PatientStatus.GetPatientState(PatientState.HeartStopped)
        elif self.SleepLevel == 0: self.PatientStatus = PatientStatus.GetPatientState(PatientState.Awake)
        elif self.SleepLevel < 3: self.PatientStatus = PatientStatus.GetPatientState(PatientState.ComingTo)
        else: self.PatientStatus = PatientStatus.GetPatientState(PatientState.Unconscious)

    def UpdatePatientValues(self, toolType : Enum):
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
                self.Fever = (self.Fever - 3) / 2
        elif ((self.Site <= 2) and (self.BleedingLevel > 0) or (self.Site <= 4) and (self.Incisions > 0)):
            self.Fever += 0.06
        self.Temp += round(self.Fever)
        self.Temp = round(self.Temp * 100 / 100)
        if self.Temp < 98.6:
            self.Temp = 98.6 
        self.Antibs = False   
        # Managing status, heart stopping
        if (((self.SleepLevel > 0) and (random.random() > 0.8 and toolType != ToolType.SurgicalDefib)) or (self.HeartDamage > 0)):
             self.HeartDamage +=1
        else:
            self.SleepLevel = max(self.SleepLevel - 1, 0)

        if self.HeartDamage == 3:
            self.IsSurgeryEnded = True
            self.EndText="You failed to resucicate your patient in time!"

        if self.Incisions > 0 and self.PatientStatus == PatientStatus.GetPatientState(PatientState.Awake):
            self.BleedingLevel += self.BleedSensitivity
            self.PatientText = TextManager.ErrorText("The patient screams and flails!")
        
        self.Site -= math.floor(self.SiteDirtyness / 3) + self.DirtSensitivity
        if self.Site < -25:
            self.Site = -25

        if  self.Temp >= 111:
            self.EndText = "Your patient succumbed to infection!"
            self.IsSurgeryEnded = True

        if  self.IsPatientFixed and self.BleedingLevel == 0 and self.Incisions == 0 and self.Temp < 101 and self.ShatteredBoneCount == 0 and self.BrokenBoneCount == 0 and self.HeartDamage == 0 and self.EndText == "":
            self.EndText = "The surgery was a success!\n"
            self.IsSurgeryEnded = True

    def GetCurrentStatus(self) -> str:
        if self.IsSurgeryEnded:
            usedtext = ""
            usedtext += f"### Malady:{TextManager.AddSpace(6)}Special Condition:"
            if self.SpecialCondition != "" and self.SpecialConditionVisibility:
                usedtext += f"\n{self.CurrentDisease["diagnostic"]}{TextManager.AddSpace(5)} {self.SpecialCondition}"
            if (self.SkillFailCount > 0):
                usedtext += f"\n\n### Skill Fails: {self.SkillFailCount}"
            usedtext += "\n### Tools Used:\n"
            if self.SpongeCount > 0:
                 usedtext +=  ToolIcon.SurgicalSponge.value + " Sponges: "  + str(self.SpongeCount) + "\n"
            if self.ScalpCount > 0:
                 usedtext += ToolIcon.SurgicalScalpel.value +  " Scalpels: " + str(self.ScalpCount) + "\n"
            if self.StitCount > 0:
                 usedtext += ToolIcon.SurgicalStitches.value +  " Stitches: " + str(self.StitCount) + "\n"
            if self.AntibioticCount > 0:
                 usedtext += ToolIcon.SurgicalAntibiotics.value + " Antibiotics: " + str(self.AntibioticCount) + "\n"
            if self.AntisepticCount > 0:
                 usedtext += ToolIcon.SurgicalAntiseptic.value +  " Antiseptics: " + str(self.AntisepticCount) + "\n"
            if self.UltraSoundCount > 0:
                usedtext += ToolIcon.SurgicalUltrasound.value +  " Ultrasounds: " + str(self.UltraSoundCount) + "\n"
            if self.LabKitCount > 0:
                usedtext += ToolIcon.SurgicalLabKit.value + " Lab Kits: "  + str(self.LabKitCount) + "\n"
            if self.AnestCount > 0:
                usedtext += ToolIcon.SurgicalAnesthetic.value + " Anesthetics: "  + str(self.AnestCount) + "\n"
            if self.DefibCount > 0:
                usedtext += ToolIcon.SurgicalDefib.value + " Defibrillators: "  + str(self.DefibCount) + "\n"
            if self.SplintCount > 0:
                usedtext += ToolIcon.SurgicalSplint.value + " Splints: "  + str(self.SplintCount) + "\n"
            if self.PinCount > 0:
                usedtext += ToolIcon.SurgicalPins.value + " Pins: " + str(self.PinCount) + "\n"
            if self.ClampCount > 0:
                usedtext += ToolIcon.SurgicalClamp.value +  " Clamps: " + str(self.ClampCount) + "\n"
            if self.TransfusionCount > 0:
                usedtext += ToolIcon.SurgicalTransfusion.value + " Transfusions: " + str(self.TransfusionCount) + "\n"
            return f"### [{self.EndText}](https://discord.gg/d9puKpHWjn)\n" + usedtext 

        spacecount = 8
        return (("```ansi\n" if TextManager.ColoredUI else "") + f"{(TextManager.WarningText(self.SpecialConditionText)+"\n" if self.SpecialCondition != "" and self.SpecialConditionVisibility else "")}"
                f"{TextManager.BoldText(self.ScanText)}\n\n"
                f"Pulse: {self.PulseText}{TextManager.AddSpace(SpaceCount=spacecount)}Status: {self.PatientStatus} \n"
                f"Temp: {self.TempText}{TextManager.AddSpace(SpaceCount=spacecount +2)}Operation site: {self.SiteText}\n"
                f"Incisions: {self.IncisionText}{TextManager.AddSpace(SpaceCount=spacecount)}{self.BoneText}\n"
                f"{self.PatientText}"
                f"{self.BleedingText}"
                f"{self.FeverText}"
                f"\n{TextManager.SoftText(self.ToolText)}" + ("```" if TextManager.ColoredUI else ""))

class PatientState(Enum):
    HeartStopped = 0
    Awake = 1
    ComingTo = 2
    Unconscious = 3

class PatientStatus:
    @staticmethod
    def GetPatientState(patientState : Enum) -> str:
        match patientState.value:
            case 0:
                return f"{TextManager.ErrorText("Heart Stopped")}"
            case 1:
                return f"{TextManager.ErrorText("Awake")}"
            case 2:
                return f"{TextManager.WarningText("Coming To")}"
            case 3:
                return f"{TextManager.PositiveText("Unconscious")}"
class SpecialConditions:
    conditions = [
        {"condition_name": "None", "condition_text": "","condition_visibility": False},
        {"condition_name": "Tough Skin", "condition_text": "The patient exhibits very tough skin. Possibly a superhero.","condition_visibility": True},
        {"condition_name": "Antibiotic-Resistant Infection", "condition_text": "The patient has an antibiotic-resistant infection.","condition_visibility": False},
        {"condition_name": "Filthy", "condition_text": "The patient is absolutely filthy.","condition_visibility": True},
        {"condition_name": "Hyperactive", "condition_text": "The patient is hyperactive.","condition_visibility": True},
        {"condition_name": "Hemophiliac", "condition_text": "The patient is a hemophiliac.","condition_visibility": False}
        ]
    @staticmethod
    def GetAllSpecialConditions():
        return [cond["condition_name"] for cond in SpecialConditions.conditions]
class Maladies:
    Maladies = [
        {"diagnostic": "Broken Arm", "scan_text": "Patient broke his arm.","patient_fixed": True, "bleeding": 1, "broken": 1, "incisions_needed": 1, "steps": ["Use Surgical Splint", "Use Surgical Stitches to reduce bleeding"]},
        {"diagnostic": "Broken Leg", "scan_text": "Patient broke his leg.","patient_fixed": True,  "bleeding": 1, "broken": 1, "shattered": 1, "incisions_needed": random.randint(1, 2), "steps": ["Use Surgical Splint", "Use Surgical Anesthetic", "Use Surgical Scalpel", "Use Surgical Pins", "Close incisions with Surgical Stitches"]},
        {"diagnostic": "Bird Flu", "scan_text": "Patient is showing signs of the bird flu.","patient_fixed": True, "flu": True, "temperature": round(random.uniform(102.0, 105.0)), "fever": 3.0, "dirt": 3, "steps": ["Use Surgical Lab Kit", "Use Surgical Antibiotics until fever stabilizes"]},
        {"diagnostic": "Turtle Flu", "scan_text": "Patient is showing signs of the turtle flu.","patient_fixed": True, "flu": True, "temperature": round(random.uniform(101.0, 104.0)), "fever": 3.0, "dirt": 3, "steps": ["Use Surgical Lab Kit", "Use Surgical Antibiotics until fever stabilizes"]},
        #ADD MONKEY FLU
        {"diagnostic": "Nose Job", "scan_text": "Patient is showing signs of the turtle flu.", "incisions_needed": 1, "steps": ["Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Stitches"]},
        {"diagnostic": "Lung Tumor", "scan_text": "a lung tumor!", "incisions_needed": 1, "steps": ["Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Stitches"]},
        {"diagnostic": "Heart Attack", "scan_text": "a heart attack!", "incisions_needed": 2, "steps": ["Use Surgical Antibiotics (optional)", "Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Stitches"]},
        {"diagnostic": "Brain Tumor", "scan_text": "a brain tumor!", "incisions_needed": 5, "steps": ["Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Stitches"]},
        {"diagnostic": "Appendicitis", "scan_text": "appendicitis!", "incisions_needed": 3, "steps": ["Use Surgical Antibiotics", "Use Surgical Antiseptic", "Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Stitches"]},
        {"diagnostic": "Liver Infection", "scan_text": "liver infection!", "incisions_needed": 2, "steps": ["Use Surgical Antibiotics", "Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Stitches"]},
        {"diagnostic": "Kidney Failure", "scan_text": "kidney failure!", "incisions_needed": 2, "steps": ["Use Surgical Antibiotics", "Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Stitches"]},
        {"diagnostic": "Broken Heart", "scan_text": "a broken heart!", "incisions_needed": 3, "steps": ["Use Surgical Lab Kit", "Use Surgical Antibiotics", "Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Pins", "Use Surgical Stitches", "Use Surgical Splint"]},
        {"diagnostic": "Swallowed a World Lock", "scan_text": "swallowed a world lock!", "incisions_needed": 2, "steps": ["Use Surgical Antibiotics", "Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Stitches"]},
        {"diagnostic": "Serious Head Injury", "scan_text": "a serious head injury!", "incisions_needed": 1, "steps": ["Use Surgical Stitches", "Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Stitches"]},
        {"diagnostic": "Serious Trauma", "scan_text": "serious trauma with a punctured lung!", "incisions_needed": 2, "steps": ["Use Surgical Stitches", "Use Surgical Splint", "Use Surgical Antiseptic", "Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Pins", "Close incisions with Surgical Stitches"]},
        {"diagnostic": "Massive Trauma", "scan_text": "massive trauma!", "incisions_needed": 3, "steps": ["Use Surgical Stitches", "Use Surgical Transfusion", "Use Surgical Ultrasound", "Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Pins", "Close incisions with Surgical Stitches", "Use Surgical Splint"]},
        {"diagnostic": "Torn Punching Muscle", "scan_text": "a torn punching muscle!", "incisions_needed": 1, "steps": ["Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Stitches"]},
        {"diagnostic": "Gem Cuts", "scan_text": "gem cuts!", "incisions_needed": 2, "steps": ["Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Stitches"]},
        {"diagnostic": "Grumbleteeth", "scan_text": "grumbleteeth!", "incisions_needed": 2, "steps": ["Use Surgical Antibiotics", "Use Surgical Ultrasound", "Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Pins", "Close incisions with Surgical Stitches", "Use Surgical Splint"]},
        {"diagnostic": "Chicken Feet", "scan_text": "chicken feet!", "incisions_needed": 2, "steps": ["Use Surgical Lab Kit", "Use Surgical Antibiotics", "Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Pins", "Use Surgical Splint", "Use Surgical Stitches"]},
        {"diagnostic": "Chaos Infection", "scan_text": "chaos infection!", "incisions_needed": 3, "steps": ["Use Surgical Sponge", "Use Surgical Lab Kit", "Use Surgical Antibiotics", "Use Surgical Splint", "Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Stitches"]},
        {"diagnostic": "Lupus", "scan_text": "lupus!", "incisions_needed": 5, "steps": ["Use Surgical Lab Kit", "Use Surgical Antibiotics", "Use Surgical Stitches", "Use Surgical Anesthetic", "Use Surgical Scalpel", "Use Surgical Clamp", "Use Surgical Stitches"]},
        {"diagnostic": "Brainworms", "scan_text": "brainworms!", "incisions_needed": 1, "steps": ["Use Surgical Lab Kit", "Use Surgical Antibiotics", "Use Surgical Stitches", "Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Pins", "Use Surgical Splint", "Use Surgical Stitches", "Use Surgical Transfusion"]},
        {"diagnostic": "Moldy Guts", "scan_text": "moldy guts!", "incisions_needed": 2, "steps": ["Use Surgical Lab Kit", "Use Surgical Antibiotics", "Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Pins", "Use Surgical Stitches", "Use Surgical Splint", "Use Surgical Sponge"]},
        {"diagnostic": "Ecto-Bones", "scan_text": "ecto-bones!", "incisions_needed": 1, "steps": ["Use Surgical Anesthetic", "Use Surgical Splint", "Use Surgical Scalpel", "Fix it", "Use Surgical Pins", "Close incisions with Surgical Stitches", "Use Surgical Splint"]},
        {"diagnostic": "Fatty-Liver", "scan_text": "fatty-liver!", "incisions_needed": 3, "steps": ["Use Surgical Lab Kit", "Use Surgical Antibiotics", "Use Surgical Sponge", "Use Surgical Antiseptic", "Use Surgical Anesthetic", "Use Surgical Scalpel", "Fix it", "Use Surgical Stitches"]}
        ]
    @staticmethod
    def GetAllMaladieNames():
        return [disease["diagnostic"] for disease in Maladies.Maladies]
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
            (ToolIcon.SurgicalUltrasound.value,ToolType.SurgicalUltrasound, not self.patient.IsUltrasoundUsed and IsSiteClean),
            (ToolIcon.SurgicalLabKit.value,ToolType.SurgicalLabKit, not self.patient.IsLabKitUsed and IsSiteClean),
            (ToolIcon.SurgicalAntiseptic.value,ToolType.SurgicalAntiseptic, IsSiteClean),
            (ToolIcon.SurgicalAnesthetic.value,ToolType.SurgicalAnesthetic, IsSiteClean),
            (ToolIcon.SurgicalTransfusion.value,ToolType.SurgicalTransfusion, IsSiteClean),
            (ToolIcon.SurgicalSplint.value, ToolType.SurgicalSplint, IsSiteClean),
            (ToolIcon.SurgicalPins.value, ToolType.SurgicalPins, IsSiteClean and self.patient.Incisions > 0),
            (ToolIcon.SurgicalLoveMallet.value, ToolType.SurgicalLoveMallet, False), #Valentines Only
            (ToolIcon.SurgicalDefib.value, ToolType.SurgicalDefib, IsSiteClean and self.patient.HeartDamage > 0),
            (ToolIcon.SurgicalClamp.value, ToolType.SurgicalClamp, IsSiteClean and self.patient.Incisions > 0),
            (ToolIcon.FixIt.value,ToolType.FixIt, (self.patient.IsFixable and (not self.patient.IsPatientFixed or self.patient.IsBrainWorms or self.patient.IncisionsNeeded == self.patient.Incisions)) and IsSiteClean)
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
            title=f"Surgery Simulator| Skill Level: {self.patient.SkillLevel}",
            description="You gave up on the surgery.",
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
                title=f"Surgery Simulator | Skill Level: {self.patient.SkillLevel}",
                description=self.patient.GetCurrentStatus(),
                color=embed_color
            )
            file = discord.File("./Images/SurgE.png", filename="SurgE.png")
            self.clear_items()
            if not self.patient.IsSurgeryEnded:
                self.GenerateToolButtons()

            # file = discord.File("./Images/SurgE.png", filename="SurgE.png")
            # embed.set_thumbnail(url="attachment://SurgE.png")
            embed.set_footer(text="Surg system is being developed by CantFind")
            await interaction.response.edit_message(embed=embed, view=self)

        return callback
    
class TextManager:
    ColoredUI = False

    @staticmethod
    def ErrorText(text: str):
        txt = ""
        if (TextManager.ColoredUI): txt = f"\x1B[2;31m{text}\x1B[0m\x1B[2;31m\x1B[0m" 
        else: txt = f"**[{text}](https://discord.gg/d9puKpHWjn)**"
        return txt
    @staticmethod
    def WarningText(text : str):
        txt = ""
        if (TextManager.ColoredUI): txt = f"\x1B[2;31m\x1B[2;32m\x1B[2;33m{text}\x1B[0m\x1B[2;32m\x1B[0m\x1B[2;31m\x1B[0m\x1B[2;31m\x1B[0m"
        else: txt = f"*[{text}](https://discord.gg/d9puKpHWjn)*"
        return txt
    @staticmethod
    def PositiveText(text : str):
        txt = ""
        if (TextManager.ColoredUI): txt = f"\x1B[2;31m\x1B[2;32m{text}\x1B[0m\x1B[2;31m\x1B[0m\x1B[2;31m\x1B[0m"
        else: txt = f"{text}"
        return txt
    @staticmethod
    def SoftText(text : str):
        txt = ""
        if (TextManager.ColoredUI): txt = f"\x1B[2;34m{text}\x1B[0m"
        else: txt = f"_{text}_"
        return txt
    @staticmethod
    def BoldText(text :str):
        txt = ""
        if (TextManager.ColoredUI): txt = f"\x1B[1;2m{text}\x1B[0m\x1B[1;2m\x1B[0m"
        else: txt = f"### {text}"
        return txt
    @staticmethod
    def AddSpace(SpaceCount : int) -> str:
        txt = ""
        for number in range(SpaceCount):
            txt += "\u1CBC"
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
    
    @app_commands.command(name="surgery", description="Start a surgery simulation.")
    @app_commands.describe(coloredui="Make the ui colored (Might not work on mobile)",hidden="Hide the surgery UI from other people", malady="Select a specific malady to surg", specialcondition="Select a special condition", skilllevel="Set the skill level (default is 100)")
    @app_commands.autocomplete(malady=AutoCompleteMalady,specialcondition=AutoCompleteCondition)
    async def surgery(self ,interaction: discord.Interaction,coloredui: Optional[bool] = True, hidden: Optional[bool] = False, malady: Optional[str] = None, specialcondition: Optional[str] = None, skilllevel: Optional[int] = 100):
        await interaction.response.defer(ephemeral=hidden)

        if malady is not None and malady not in Maladies.GetAllMaladieNames():
            return await interaction.followup.send(
                embed=discord.Embed( title="Invalid malady!",description="**Please choose from the following:**\n" + "\n".join(Maladies.GetAllMaladieNames()), color=discord.Color.red())
            )

        if specialcondition is not None and specialcondition not in SpecialConditions.GetAllSpecialConditions():
            return await interaction.followup.send(
                embed=discord.Embed( title="Invalid Condition!",description="**Please choose from the following:**\n" + "\n".join(SpecialConditions.GetAllSpecialConditions()), color=discord.Color.red())
            )
            
        patient = Patient(SkillLevel=100 if skilllevel > 100 else 0 if skilllevel < 0 else skilllevel, malady=malady, specialcondition=specialcondition)
        surgery = Surgery(patient=patient, user=interaction.user)
        view = SurgeryView(surgery,interaction.user)
        TextManager.ColoredUI = coloredui
        patient.UpdatePatientUI()
        embed = discord.Embed(
            title=f"Surgery Simulator| Skill Level: {patient.SkillLevel}",
            description=patient.GetCurrentStatus(),
            color=discord.Color.blue()
        )
        embed.set_footer(text="Surg system is being developed by CantFind")
        await interaction.followup.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(SurgeryCog(bot))
    