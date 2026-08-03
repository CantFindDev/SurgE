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

from enum import Enum


class PatientState(Enum):
    HeartStopped = 0
    Awake = 1
    ComingTo = 2
    Unconscious = 3
    NearComa = 4


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
