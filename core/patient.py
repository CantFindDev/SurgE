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

import asyncio
import math
import random
import time
from enum import Enum
from typing import Optional

from core.enums import PatientState, ToolType, ToolIcon
from core.data_loaders import Maladies, SpecialConditions, Modifiers, Drops
from core.text import TextManager, PatientStatus


class Patient:
    def __init__(self, SkillLevel: int = 100, malady: Optional[str] = None, specialcondition: Optional[str] = None, modifier: Optional[str] = None, TrainEMode: Optional[bool] = False):
        # Tool usage counters
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

        # Patient vitals
        self.Pulse = 40
        self.Temp = 98.6
        self.Fever = 0.0
        self.SleepLevel = 0
        self.HeartDamage = 0
        self.BleedingLevel = 0

        # Surgery site state
        self.SiteSanitation = 0
        self.SiteDirtyness = 0
        self.Incisions = 0
        self.IncisionsNeeded = 0
        self.BrokenBoneCount = 0
        self.ShatteredBoneCount = 0

        # Surgery progress flags
        self.IsPatientFixed = False
        self.IsFixable = False
        self.IsUltrasoundUsed = False
        self.IsLabKitUsed = False
        self.LabWorked = False
        self.IsSurgeryEnded = False
        self.Antibs = False
        self.IsBrainWorms = False

        # Configuration
        self.SkillLevel = SkillLevel
        self.TrainE = TrainEMode
        self.ModifierItem = None
        self.SpecialCondition = None
        self.SpecialConditionVisibility = False
        self.CurrentDisease = None

        # Sensitivity modifiers (adjusted by special conditions)
        self.ScalpSensivity = 1
        self.AntibSensivity = 3
        self.DirtSensitivity = 0
        self.AnestSensitivity = 10
        self.BleedSensitivity = 1

        # UI text fields
        self.ToolText = "Patient is prepped for surgery."
        self.TrainEText = ""
        self.HeartText = ""
        self.diagnostic = ""
        self.DirtynessText = ""
        self.PatientText = ""
        self.PulseText = ""
        self.TempText = ""
        self.BoneText = ""
        self.IncisionText = ""
        self.ScanText = ""
        self.EndText = ""
        self.PatientStatus = ""
        self.BleedingText = ""
        self.FeverText = ""
        self.BoneStatus = ""
        self.SpecialConditionText = ""
        self.NurseText = ""

        # Timer
        self.StartTime = 0
        self.TimerEnded = False

        # Initialize disease & condition
        if malady: self.SetSpesificDisease(malady)
        else: self.SetRandomDisease()
        if specialcondition: self.SetSpesificSpecialCondition(specialcondition)
        else: self.SetRandomSpecialCondition()
        self.ModifierItem = modifier

    def SetRandomDisease(self):
        disease = random.choice(Maladies.Maladies)
        self.ApplyDisease(disease)

    def SetSpesificDisease(self, MaladyName: str):
        for disease in Maladies.Maladies:
            if disease['diagnostic'].lower() == MaladyName.lower():
                self.ApplyDisease(disease)
                break

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
        self.IsUltrasoundUsed = disease.get("ultrasound_used", False)
        self.Pulse = disease.get("pulse", 40)

    def SetRandomSpecialCondition(self):
        Random = math.floor(random.random() * 10)
        for cond in SpecialConditions.Conditions:
            if Random < cond['condition_chance']:
                self.ApplyCondition(cond)
                break

    def SetSpesificSpecialCondition(self, ConditionName: str):
        for cond in SpecialConditions.Conditions:
            if cond['condition_name'].lower() == ConditionName.lower():
                self.ApplyCondition(cond)
                break

    def ApplyCondition(self, cond):
        self.SpecialCondition = cond["condition_name"]
        self.SpecialConditionVisibility = cond["condition_visibility"]
        self.SpecialConditionText = cond["condition_text"]
        self.ApplySpecialConditionValues()

    def ApplySpecialConditionValues(self):
        match self.SpecialCondition:
            case "Tough Skin":
                self.IncisionsNeeded += 1
            case "Antibiotic-Resistant Infection":
                self.AntibSensivity /= 2
            case "Hemophiliac":
                self.BleedSensitivity = 2
            case "Filthy":
                self.DirtSensitivity = 10
            case "Hyperactive":
                self.AnestSensitivity /= 2


    def GetAllToolsUsed(self) -> str:
        """Builds the item-used summary shown at the end of a surgery."""
        tool_entries = [
            (self.SpongeCount,      ToolIcon.SurgicalSponge,      "Sponges"),
            (self.ScalpCount,       ToolIcon.SurgicalScalpel,     "Scalpels"),
            (self.StitCount,        ToolIcon.SurgicalStitches,    "Stitches"),
            (self.AntibioticCount,  ToolIcon.SurgicalAntibiotics, "Antibiotics"),
            (self.AntisepticCount,  ToolIcon.SurgicalAntiseptic,  "Antiseptics"),
            (self.UltraSoundCount,  ToolIcon.SurgicalUltrasound,  "Ultrasounds"),
            (self.LabKitCount,      ToolIcon.SurgicalLabKit,      "Lab Kits"),
            (self.AnestCount,       ToolIcon.SurgicalAnesthetic,  "Anesthetics"),
            (self.DefibCount,       ToolIcon.SurgicalDefib,       "Defibrillators"),
            (self.SplintCount,      ToolIcon.SurgicalSplint,      "Splints"),
            (self.PinCount,         ToolIcon.SurgicalPins,        "Pins"),
            (self.ClampCount,       ToolIcon.SurgicalClamp,       "Clamps"),
            (self.TransfusionCount, ToolIcon.SurgicalTransfusion, "Transfusions"),
        ]

        lines = []
        for count, icon, label in tool_entries:
            if count > 0:
                lines.append(f"{icon.value} {label}: {count}")
        return "\n".join(lines) + ("\n" if lines else "")

    def UseTool(self, toolType: Enum) -> bool:
        """Apply a tool to the patient. Returns True if a skill-fail occurred."""

        SkillFailRate = self._CalculateSkillFailRate()
        NurseChance = self._RollNurseChance()
        success = random.random() * 100 > SkillFailRate
        skillfail_occurred = not success

        match toolType:
            case ToolType.SurgicalAntiseptic:
                self._ApplyAntiseptic(success, SkillFailRate, NurseChance)
            case ToolType.SurgicalDefib:
                self._ApplyDefib(success, SkillFailRate, NurseChance)
            case ToolType.SurgicalSponge:
                self._ApplySponge(success, SkillFailRate, NurseChance)
            case ToolType.SurgicalScalpel:
                self._ApplyScalpel(success, SkillFailRate, NurseChance)
            case ToolType.SurgicalStitches:
                self._ApplyStitches(success, SkillFailRate, NurseChance)
            case ToolType.SurgicalUltrasound:
                self._ApplyUltrasound(success, SkillFailRate, NurseChance)
            case ToolType.SurgicalLabKit:
                self._ApplyLabKit(success, SkillFailRate, NurseChance)
            case ToolType.SurgicalAntibiotics:
                self._ApplyAntibiotics(success, SkillFailRate, NurseChance)
            case ToolType.SurgicalSplint:
                self._ApplySplint(success, SkillFailRate, NurseChance)
            case ToolType.SurgicalPins:
                self._ApplyPins(success, SkillFailRate, NurseChance)
            case ToolType.SurgicalAnesthetic:
                self._ApplyAnesthetic(success, SkillFailRate, NurseChance)
            case ToolType.SurgicalTransfusion:
                self._ApplyTransfusion(success, SkillFailRate, NurseChance)
            case ToolType.SurgicalClamp:
                self._ApplyClamp(success, SkillFailRate, NurseChance)
            case ToolType.FixIt:
                self._ApplyFixIt(success, SkillFailRate)

        self.UpdatePatientValues(toolType)
        self.UpdatePatientUITexts()
        return skillfail_occurred

    def _CalculateSkillFailRate(self) -> int:
        """Compute the skill-fail percentage based on modifier and skill level."""
        if self.ModifierItem == "Stethoscope":
            return round((30 - self.SkillLevel / 4) / 2)
        elif self.ModifierItem is not None:
            return round(35 - self.SkillLevel / 3)
        else:
            return round(30 - self.SkillLevel / 4)

    def _RollNurseChance(self) -> bool:
        """Roll the Nano Nurse Bot save chance if the modifier is a Nursing type."""
        if Modifiers.GetModifierType(self.ModifierItem) == "Nursing":
            return Modifiers.GetNurseChance()
        return False

    def _HandleNurseText(self, NurseChance: bool, tool_name: str, counter_attr: str):
        """Shared pattern: either set nurse-save text or increment the tool counter."""
        if NurseChance:
            self.NurseText = (
                f"{TextManager.PositiveText('[Nano Nurse Bot]: ')}"
                + TextManager.SoftText("Nano nurse bot prevented you from losing one " + TextManager.PurpieText(tool_name))
            )
        else:
            setattr(self, counter_attr, getattr(self, counter_attr) + 1)
            self.NurseText = ""

    def _ApplyAntiseptic(self, success, SkillFailRate, NurseChance):
        self._HandleNurseText(NurseChance, "antiseptic", "AntisepticCount")
        if success:
            self.SiteSanitation = min(self.SiteSanitation + 20, 20)
            self.ToolText = "You disinfected the operating site."
        else:
            self.SkillFailCount += 1
            self.ToolText = f"{TextManager.ErrorText(f"[Skill Fail {SkillFailRate}%]: ")}" + TextManager.SoftText("You spilled antiseptic on your shoes. They are very clean now.")

    def _ApplyDefib(self, success, SkillFailRate, NurseChance):
        self._HandleNurseText(NurseChance, "defiblirator", "DefibCount")
        if success:
            self.ToolText = "You shocked the patient back to life!"
            self.HeartDamage = 0
        else:
            self.SkillFailCount += 1
            self.SiteDirtyness += 1
            self.ToolText = f"{TextManager.ErrorText(f"[Skill Fail {SkillFailRate}%]: ")}" + TextManager.SoftText("You electrocuted yourself!")

    def _ApplySponge(self, success, SkillFailRate, NurseChance):
        self._HandleNurseText(NurseChance, "sponge", "SpongeCount")
        if success:
            if self.SiteDirtyness == 0:
                self.ToolText = f"{TextManager.WarningText("Everything was already clean, you wasted a sponge!")}"
            else:
                self.SiteDirtyness = 0
                self.ToolText = "You mopped up the operation site."
        else:
            self.SkillFailCount += 1
            self.ToolText = f"{TextManager.ErrorText(f"[Skill Fail {SkillFailRate}%]: ")}" + TextManager.SoftText("You somehow managed to eat the sponge.")

    def _ApplyScalpel(self, success, SkillFailRate, NurseChance):
        self._HandleNurseText(NurseChance, "scalpel", "ScalpCount")
        if self.PatientStatus == PatientStatus.GetPatientState(PatientState.Awake):
            self.EndText = "You cut the patient while they were awake!"
            self.IsSurgeryEnded = True
        elif self.Incisions >= self.IncisionsNeeded:
            self.ToolText = TextManager.ErrorText("You stabbed the patient in a vital organ!")
            self.BleedingLevel += self.BleedSensitivity
        elif self.Incisions >= 0:
            self.Incisions += self.ScalpSensivity
            if self.Incisions < self.IncisionsNeeded:
                if success:
                    self.ToolText = "You've made a neat incision."
                else:
                    self.SkillFailCount += 1
                    self.BleedingLevel += self.BleedSensitivity
                    self.ToolText = f"{TextManager.ErrorText(f"[Skill Fail {SkillFailRate}%]: ")}" + TextManager.SoftText("This will leave a nasty scar, but you managed to cut the right place.")
        else:
            self.ScalpCount -= 1

    def _ApplyStitches(self, success, SkillFailRate, NurseChance):
        self._HandleNurseText(NurseChance, "stitch", "StitCount")
        if success:
            if self.Incisions > 0:
                self.ToolText = "You stitched up an incision."
                self.Incisions -= 1
            elif self.BleedingLevel > 0:
                self.ToolText = "You stitched up a bleeding wound."
                self.BleedingLevel -= 1
            else:
                self.ToolText = "You tried to stitch your patient\'s mouth shut!"
        else:
            self.SkillFailCount += 1
            self.ToolText = f"{TextManager.ErrorText(f"[Skill Fail {SkillFailRate}%]: ")}" + TextManager.SoftText("You somehow tied yourself up in stitches!")

    def _ApplyUltrasound(self, success, SkillFailRate, NurseChance):
        self._HandleNurseText(NurseChance, "ultrasound", "UltraSoundCount")
        if success:
            self.IsUltrasoundUsed = True
            self.SpecialConditionVisibility = True
            self.ToolText = f"You scanned the patient with ultrasound, discovering they are suffering from {self.CurrentDisease["scan_text"]} {"You Found" + self.BoneStatus if self.BoneStatus != "" else ""}"
        else:
            self.SkillFailCount += 1
            self.ToolText = f"{TextManager.ErrorText(f"[Skill Fail {SkillFailRate}%]: ")}" + TextManager.SoftText("You scanned the nurse with your ultrasound!")

    def _ApplyLabKit(self, success, SkillFailRate, NurseChance):
        self._HandleNurseText(NurseChance, "Lab Kit", "LabKitCount")
        if success:
            self.IsLabKitUsed = True
            self.LabWorked = True
            self.ToolText = "You performed lab work on the patient, and have antibiotics at the ready."
        else:
            self.SkillFailCount += 1
            self.ToolText = f"{TextManager.ErrorText(f"[Skill Fail {SkillFailRate}%]: ")}" + TextManager.SoftText("You contaminated the sample.")

    def _ApplyAntibiotics(self, success, SkillFailRate, NurseChance):
        self._HandleNurseText(NurseChance, "Antibiotics", "AntibioticCount")
        if success:
            if self.Temp > 98.6:
                self.Fever -= self.AntibSensivity
                self.ToolText = 'You used antibiotics to reduce the patient\'s infection.'
            if self.Fever > -3:
                self.Antibs = True
        else:
            self.SkillFailCount += 1
            self.Fever += 1
            self.ToolText = f"{TextManager.ErrorText(f"[Skill Fail {SkillFailRate}%]: ")}" + TextManager.SoftText("This is the wrong medication! The bacteria like it.")

    def _ApplySplint(self, success, SkillFailRate, NurseChance):
        self._HandleNurseText(NurseChance, "Splint", "SplintCount")
        if success:
            self.BrokenBoneCount -= 1
            self.ToolText = "You splinted a broken bone."
        else:
            self.SkillFailCount += 1
            self.BleedingLevel += self.BleedSensitivity
            self.ToolText = f"{TextManager.ErrorText(f"[Skill Fail {SkillFailRate}%]: ")}" + TextManager.SoftText("You somehow cut the patient.")

    def _ApplyPins(self, success, SkillFailRate, NurseChance):
        self._HandleNurseText(NurseChance, "Pins", "PinCount")
        if success:
            self.ShatteredBoneCount -= 1
            self.BrokenBoneCount += 1
            self.ToolText = "You pinned a shattered bone together. Don\'t forget to splint it!"
        else:
            self.SkillFailCount += 1
            self.BleedingLevel += self.BleedSensitivity
            self.ToolText = f"{TextManager.ErrorText(f"[Skill Fail {SkillFailRate}%]: ")}" + TextManager.SoftText("You jabbed the pin through the artery!")

    def _ApplyAnesthetic(self, success, SkillFailRate, NurseChance):
        self._HandleNurseText(NurseChance, "Anesthetic", "AnestCount")
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
            self.ToolText = f"{TextManager.ErrorText(f"[Skill Fail {SkillFailRate}%]: ")}" + TextManager.SoftText("You end up inhaling all the anesthetic yourself. You feel woozy.")

    def _ApplyTransfusion(self, success, SkillFailRate, NurseChance):
        self._HandleNurseText(NurseChance, "Transfusion", "TransfusionCount")
        if success:
            self.Pulse = min(self.Pulse + 15, 40)
            self.ToolText = "You transfused several pints of blood into your patient."
        else:
            self.SkillFailCount += 1
            self.SiteDirtyness += 1
            self.ToolText = f"{TextManager.ErrorText(f"[Skill Fail {SkillFailRate}%]: ")}" + TextManager.SoftText("You spilled blood everywhere!")

    def _ApplyClamp(self, success, SkillFailRate, NurseChance):
        self._HandleNurseText(NurseChance, "Clamp", "ClampCount")
        if success:
            self.BleedingLevel -= 1
            self.ToolText = "You clamped up some blood vessels"
        else:
            self.SkillFailCount += 1
            self.ToolText = f"{TextManager.ErrorText(f"[Skill Fail {SkillFailRate}%]: ")}" + TextManager.SoftText("The clamp fell out of your hand, oh well.")

    def _ApplyFixIt(self, success, SkillFailRate):
        if success and self.IsFixable and not self.IsPatientFixed:
            self.ToolText = "You fixed the issue!"
            self.IsPatientFixed = True
            self.IsFixable = False
        else:
            self.SkillFailCount += 1
            self.ToolText = f"{TextManager.ErrorText(f"[Skill Fail {SkillFailRate}%]: ")}" + TextManager.SoftText("You screwed it up! Try again.")

    def UpdatePatientValues(self, toolType: Enum):
        """Recalculate all patient state values after a tool action."""
        self._UpdateFixability()
        self._UpdateDirtyness()
        self._UpdatePulse()
        self._UpdateFever()
        self._UpdateHeartStatus(toolType)
        self._UpdateAwakeBleed()
        self._UpdateSanitation()
        self._CheckDeathByInfection()
        self._CheckSurgerySuccess()

    def _UpdateFixability(self):
        if self.Incisions >= self.IncisionsNeeded and not self.IsPatientFixed:
            if self.IsUltrasoundUsed:
                self.IsFixable = True
                self.Incisions = self.IncisionsNeeded
            # else:
            #     self.IsFixable = False
            # Removed because the actual growtopia does not have this system but In my opinion it is better to have it

    def _UpdateDirtyness(self):
        self.SiteDirtyness += self.BleedingLevel + self.Incisions

    def _UpdatePulse(self):
        self.Pulse -= self.BleedingLevel + min(self.Incisions, 1)
        if self.Pulse < 1 and self.EndText == "":
            self.EndText = "The patient bled out!"
            self.IsSurgeryEnded = True

    def _UpdateFever(self):
        if self.Fever > 4:
            self.Fever = 4

        if self.Fever < 0:
            if self.Fever > -0.06:
                self.Fever = 0
            elif self.Antibs:
                self.Fever = (self.Fever - self.AntibSensivity) / 2
        elif ((self.SiteSanitation <= 2) and (self.BleedingLevel > 0) or (self.SiteSanitation <= 4) and (self.Incisions > 0)):
            self.Fever += 0.06

        self.Temp += self.Fever
        self.Temp = round(self.Temp * 100, 2) / 100

        if self.Temp < 98.6:
            self.Temp = 98.6
        self.Antibs = False

    def _UpdateHeartStatus(self, toolType: Enum):
        if (((self.SleepLevel > 0) and (random.random() > 0.9 and toolType != ToolType.SurgicalDefib)) or (self.HeartDamage > 0)):
            self.HeartDamage += 1
        else:
            self.SleepLevel = max(self.SleepLevel - 1, 0)

        if self.HeartDamage == 3:
            self.IsSurgeryEnded = True
            self.EndText = "You failed to resucicate your patient in time!"

    def _UpdateAwakeBleed(self):
        if self.Incisions > 0 and self.PatientStatus == PatientStatus.GetPatientState(PatientState.Awake):
            self.BleedingLevel += self.BleedSensitivity
            self.PatientText = TextManager.ErrorText("The patient screams and flails!")
        else:
            self.PatientText = ""

    def _UpdateSanitation(self):
        self.SiteSanitation -= math.floor(self.SiteDirtyness / 3) + self.DirtSensitivity
        if self.SiteSanitation < -25:
            self.SiteSanitation = -25

    def _CheckDeathByInfection(self):
        if self.Temp >= 111:
            self.EndText = "Your patient succumbed to infection!"
            self.IsSurgeryEnded = True

    def _CheckSurgerySuccess(self):
        if (self.IsPatientFixed and self.BleedingLevel == 0 and self.Incisions == 0
                and self.Temp < 101 and self.ShatteredBoneCount == 0 and self.BrokenBoneCount == 0
                and self.HeartDamage == 0 and self.EndText == ""):
            self.EndText = "The surgery was a success!\n"
            self.IsSurgeryEnded = True

    def UpdatePatientUITexts(self):
        """Regenerate all UI text fields based on current patient state."""
        self._UpdateDiagnoseText()
        self._UpdateDirtynessText()
        self._UpdateBleedingText()
        self._UpdatePulseText()
        self._UpdateFeverText()
        self._UpdateSanitationText()
        self._UpdateTemperatureText()
        self._UpdateBoneText()
        self._UpdateIncisionText()
        self._UpdateConsciousnessText()
        self._UpdateHeartStopText()
        self._UpdateTrainEText()

    def _UpdateDiagnoseText(self):
        if self.IsUltrasoundUsed:
            if self.IsFixable:
                self.ScanText = self.CurrentDisease.get("fix_text", self.CurrentDisease["scan_text"])
            elif self.IsPatientFixed:
                self.ScanText = self.CurrentDisease.get("post_fix_text", self.CurrentDisease["scan_text"])
            else:
                self.ScanText = self.CurrentDisease["scan_text"]

    def _UpdateDirtynessText(self):
        if self.SiteDirtyness >= 10:
            self.DirtynessText = TextManager.ErrorText("You can't see what you are doing!")
        elif self.SiteDirtyness >= 4:
            self.DirtynessText = TextManager.WarningText("It is becoming hard to see your work.")
        else:
            self.DirtynessText = ""

    def _UpdateBleedingText(self):
        if self.BleedingLevel > 0:
            text = "Patient is "
            if self.BleedingLevel >= 4:
                text += f"loosing blood {TextManager.ErrorText("very quickly!")}"
            elif self.BleedingLevel == 1:
                text += f"losing blood {TextManager.SoftText("slowly.")}"
            else:
                text += f"{TextManager.WarningText("losing blood!")}"
            self.BleedingText = text + "\n"
        else:
            self.BleedingText = ""

    def _UpdatePulseText(self):
        if self.Pulse < 11:
            self.PulseText = TextManager.ErrorText("Extremely Weak")
        elif self.Pulse < 21:
            self.PulseText = TextManager.WarningText("Weak")
        elif self.Pulse < 31:
            self.PulseText = TextManager.SoftText("Steady")
        else:
            self.PulseText = TextManager.PositiveText("Strong")

    def _UpdateFeverText(self):
        if self.Fever > 0 and self.Temp > 100:
            text = "Patient\'s fever is "
            if self.Fever < 0.5:
                text += TextManager.SoftText(" slowly rising!")
            elif self.Fever > 2:
                text += TextManager.ErrorText(" climbing fast!")
            else:
                text += TextManager.WarningText(" climbing!")
            self.FeverText = text + "\n"
        else:
            self.FeverText = ""

    def _UpdateSanitationText(self):
        if self.SiteSanitation < -3:
            self.SiteText = TextManager.ErrorText("Unsanitary")
        elif self.SiteSanitation < -1:
            self.SiteText = TextManager.WarningText("Unclean")
        elif self.SiteSanitation < 1:
            self.SiteText = TextManager.SoftText("Not sanitized")
        else:
            self.SiteText = TextManager.PositiveText("Clean")

    def _UpdateTemperatureText(self):
        if self.Temp < 100:
            self.TempText = TextManager.PositiveText(self.Temp)
        elif self.Temp < 104:
            self.TempText = TextManager.SoftText(self.Temp)
        elif self.Temp < 106:
            self.TempText = TextManager.WarningText(self.Temp)
        else:
            self.TempText = TextManager.ErrorText(self.Temp)

    def _UpdateBoneText(self):
        broken = self.BrokenBoneCount
        shatter = self.ShatteredBoneCount
        if (broken > 0 or shatter > 0) and self.IsUltrasoundUsed == True:
            txt = "Bones: "
            if broken > 0:
                txt += TextManager.ErrorText(str(broken) + " broken") if broken > 1 else TextManager.WarningText(str(broken) + " broken ")
            if broken > 0 and shatter > 0:
                txt += ","
            if shatter > 0:
                txt += TextManager.ErrorText(str(shatter) + " shattered") if shatter > 1 else TextManager.WarningText(str(shatter) + " shattered")
            self.BoneText = txt
        else:
            self.BoneText = ""

    def _UpdateIncisionText(self):
        if self.Incisions == self.IncisionsNeeded:
            self.IncisionText = TextManager.PositiveText(self.Incisions)
        else:
            self.IncisionText = self.Incisions

    def _UpdateConsciousnessText(self):
        if self.HeartDamage > 0:
            self.PatientStatus = PatientStatus.GetPatientState(PatientState.HeartStopped)
        elif self.SleepLevel == 0:
            self.PatientStatus = PatientStatus.GetPatientState(PatientState.Awake)
        elif self.SleepLevel < 3 and self.SleepLevel > 0:
            self.PatientStatus = PatientStatus.GetPatientState(PatientState.ComingTo)
        else:
            self.PatientStatus = PatientStatus.GetPatientState(PatientState.Unconscious)

    def _UpdateHeartStopText(self):
        if self.HeartDamage > 0:
            self.HeartText = TextManager.ErrorText("Patient\'s heart has stopped!")
        else:
            self.HeartText = ""

    def _UpdateTrainEText(self):
        if not self.TrainE:
            return

        self.TrainEText = ""

        # Heart Stopped
        if self.HeartDamage > 0:
            self.TrainEText += TextManager.ErrorText("Heart Stopped") + f" - You need to {TextManager.WarningText("Revive")} your patient with a {TextManager.PurpieText("Defiblirator")}!"
            return

        # Awake with open wound
        if self.SleepLevel == 0 and self.Incisions > 0:
            self.TrainEText += TextManager.ErrorText("Awake") + f" - Your patient is {TextManager.WarningText("Awake")}. Use {TextManager.PurpieText("Anesthetic")} to put them to sleep until you have closed the wound.\n"

        # Stitch it up
        if self.Incisions > 0 and self.IsPatientFixed:
            self.TrainEText += TextManager.PositiveText("Stitch it Up!") + f" - The issue is fixed! It's time to close it up with {TextManager.PurpieText("Stitches")}.\n"

        # Fix It
        if self.IsFixable:
            self.TrainEText += TextManager.PositiveText("Fix It!") + f" - You have found the issue and can now {TextManager.PurpieText("Fix It")}.\n"

        # Clean the area
        if self.SiteSanitation < 1:
            self.TrainEText += TextManager.PositiveText("Clean the Area") + f" - Clean the area with {TextManager.PurpieText("Antiseptic")}.\n"

        # Prep Patient
        if self.SleepLevel == 0 and self.IsUltrasoundUsed and self.IncisionsNeeded > 0:
            self.TrainEText += TextManager.PositiveText("Prep Patient") + f" - Apply {TextManager.PurpieText("Anesthetic")} to put the patient to sleep.\n"

        # Make an Incision
        if not self.IsFixable and not self.IsPatientFixed and self.SleepLevel > 0 and self.IsUltrasoundUsed:
            self.TrainEText += TextManager.PositiveText("Make an Incision!") + f" - Use {TextManager.PurpieText("Scalpel")} to make an incision.\n"

        # Poor Visibility
        if self.SiteDirtyness >= 4:
            self.TrainEText += TextManager.WarningText("Poor Visibility") + f" - Apply a {TextManager.PurpieText("Sponge")}. Poor visibility increases the chance of a {TextManager.WarningText("Skill Failure")}.\n"

        # Diagnosis
        if not self.IsUltrasoundUsed or (not self.IsLabKitUsed and not self.IsUltrasoundUsed):
            self.TrainEText += TextManager.WarningText("Diagnosis") + f" - You can use the {TextManager.PurpieText("Ultrasound")} {f"or {TextManager.PurpieText("Lab Kit")}" if not self.IsLabKitUsed else ""} to diagnose the illness\n"

        # Losing Blood
        if self.BleedingLevel > 0:
            self.TrainEText += TextManager.WarningText("Losing Blood") if self.BleedingLevel < 4 else (TextManager.ErrorText("Losing Blood very quickly")) + f" - Apply {f"{TextManager.PurpieText("Clamps")} to reduce {TextManager.WarningText("Bleeding")} during surgery." if self.Incisions > 0 else f"{TextManager.PurpieText("Stitches")} to reduce {TextManager.WarningText("Bleeding")}."}\n"

        # Shattered Bone
        if self.ShatteredBoneCount > 0 and self.IsUltrasoundUsed:
            self.TrainEText += TextManager.WarningText("Shattered Bone") + f" - Apply {TextManager.PurpieText("Pins")}.You must put the patient to sleep with {TextManager.PurpieText("Anesthetic")} and {f"make an insicion with a {"" if self.IsFixable or self.IsPatientFixed else TextManager.PurpieText("Scalpel")} before you can apply pins."}\n"

        # Broken Bone
        if self.BrokenBoneCount > 0 and self.IsUltrasoundUsed:
            self.TrainEText += TextManager.WarningText("Broken Bone") + f" - Apply a {TextManager.PurpieText("Splint")}.\n"

        # Fever
        if self.Fever > 0:
            self.TrainEText += (TextManager.WarningText("Fever") if self.Fever < 0.5 else TextManager.ErrorText("High Fever")) + f" - {"Apply" if self.IsLabKitUsed else f"Diagnose the {TextManager.WarningText("Infection")} With a {TextManager.PurpieText("Lab Kit")} then apply"} {TextManager.PurpieText("Antibiotics")} to bring down {TextManager.WarningText("Temp")}\n"

        # Antibiotics
        if self.Temp > 98.8 and self.Fever > 0 and self.IsLabKitUsed:
            self.TrainEText += TextManager.PositiveText("Antibiotics") + f" - Apply {TextManager.PurpieText("Antibiotics")} to prevent any infection. If all else fails, give antibiotics.\n"

        # Pulse
        if self.Pulse < 11:
            self.TrainEText += TextManager.ErrorText("Extremely Weak Pulse") + f" - You can increase the {TextManager.WarningText("Pulse")} with a {TextManager.PurpieText("Blood Transfusion")}."

        # Coming To
        if self.SleepLevel < 3 and self.SleepLevel > 0 and self.Incisions > 0:
            self.TrainEText += TextManager.WarningText("Coming To") + f" - Your patient is about to wake up but you still have some {TextManager.WarningText("Incisions")}. Use {TextManager.PurpieText("Anesthetic")} to keep them unconscious until you have closed to wound.\n"

    def SetCurrentPatientEmbed(self, embed) -> str:
        """Populate a Discord embed with the current surgery state."""
        if self.IsSurgeryEnded:
            self._BuildEndedEmbed(embed)
        else:
            self._BuildActiveEmbed(embed)

    def _BuildEndedEmbed(self, embed):
        embed.title = f"{"Train-E" if self.TrainE else "Surg-E"}"
        embed.description = f"## {self.EndText}\n\n"
        embed.description += TextManager.AddFeild(value=f"**Time Elapsed:**\n" + f"{round(time.time() - self.StartTime)} Seconds\n", inline=False)
        embed.description += TextManager.AddFeild(value=f"**Malady:**\n{self.CurrentDisease["diagnostic"]}\n", inline=False)

        if self.SpecialConditionText != "" and self.SpecialConditionVisibility:
            embed.description += TextManager.AddFeild(value=f"**Special Condition:**\n{self.SpecialCondition}\n", inline=False)
        if self.SkillFailCount > 0:
            embed.description += TextManager.AddFeild(value=f"**Skill Fails:**\n{self.SkillFailCount}\n", inline=False)
        if self.ModifierItem is not None:
            embed.description += TextManager.AddFeild(value=f"**Modifier:**\n{self.ModifierItem}\n", inline=False)

        embed.description += TextManager.AddFeild(value=f"**Skill Level:**\n{self.SkillLevel}\n", inline=False)
        embed.description += TextManager.AddFeild(value=f"**Tools Used:**\n{self.GetAllToolsUsed()}", inline=False)

        # Drop reward on success
        item = Drops.GetDrop()
        if self.EndText == "The surgery was a success!\n":
            embed.description += TextManager.AddFeild(value="**Reward:**", inline=False)
            embed.description += TextManager.AddFeild(value=f"{item["ItemName"]}", inline=False)
            embed.set_image(url=Drops.GetItemImageByName(item["ItemName"]))

    def _BuildActiveEmbed(self, embed):
        embed.title = f"Surgery Simulator| Skill Level: {self.SkillLevel}\n\n"
        embed.description = ""
        embed.description += TextManager.ansistart + "\n"
        embed.description += f"{TextManager.WarningText(self.SpecialConditionText)+"\n" if self.SpecialCondition != "None" and self.SpecialConditionVisibility else ""}" + f"{TextManager.BoldText(self.ScanText)}\n"

        # Vital stats row
        embed.description += TextManager.AddFeild(value=f"Pulse: {self.PulseText}", inline=True)
        embed.description += TextManager.AddFeild(value=f"Status: {self.PatientStatus}", inline=True)
        embed.description += TextManager.AddFeild(value=f"Temp: {self.TempText}", inline=True)
        embed.description += TextManager.AddFeild(value=f"Operation site: {self.SiteText}", inline=True)

        # Conditional status lines
        if self.DirtynessText != "":
            embed.description += TextManager.AddFeild(value=f"{self.DirtynessText}", inline=False)
        embed.description += TextManager.AddFeild(value=f"Incisions: {self.IncisionText}", inline=True)
        if self.BoneText != "":
            embed.description += TextManager.AddFeild(value=self.BoneText, inline=True)
        if self.PatientText != "":
            embed.description += TextManager.AddFeild(value=self.PatientText, inline=False)
        if self.BleedingText != "":
            embed.description += TextManager.AddFeild(value=self.BleedingText, inline=False)
        if self.FeverText != "":
            embed.description += TextManager.AddFeild(value=self.FeverText, inline=False)
        if self.ToolText != "":
            embed.description += TextManager.AddFeild(value=self.ToolText, inline=False)
        if self.NurseText != "":
            embed.description += TextManager.AddFeild(value=self.NurseText, inline=False)
        if self.HeartText != "":
            embed.description += TextManager.AddFeild(value=self.HeartText, inline=False)
        if self.TrainE == True:
            embed.description += TextManager.AddFeild(value=f"Bot Tips:\n{self.TrainEText}", inline=False)

        embed.description += "\n" + TextManager.ansiend

    async def timer(self, minutes: Optional[int] = 2):
        self.StartTime = time.time()
        await asyncio.sleep(minutes * 60)
