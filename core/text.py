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

from core.enums import PatientState

# Mapping of ANSI color codes used for Discord's ansi code blocks.
_ANSI_RESET   = "\x1B[0m"
_ANSI_RED     = "\x1B[2;31m"
_ANSI_GREEN   = "\x1B[2;32m"
_ANSI_YELLOW  = "\x1B[2;33m"
_ANSI_BLUE    = "\x1B[2;34m"
_ANSI_PURPLE  = "\x1B[2;35m"
_ANSI_BOLD    = "\x1B[1;2m"

# GitHub project link used for markdown-styled colored text.
_PROJECT_URL = "https://github.com/CantFindDev/SurgE"


class TextManager:
    """Handles text formatting for both ANSI (colored) and Markdown (fallback) modes."""

    ansistart = ""
    ansiend = ""
    ColoredUI = False
    FeildCount = 0

    @staticmethod
    def setTextManager(Colored_UI: bool):
        TextManager.ColoredUI = Colored_UI
        TextManager.ansistart = "```ansi\n" if Colored_UI else ""
        TextManager.ansiend = "```" if Colored_UI else ""
        TextManager.FeildCount = 0

    @staticmethod
    def ErrorText(text: str) -> str:
        if TextManager.ColoredUI:
            return f"{_ANSI_RED}{text}{_ANSI_RESET}{_ANSI_RED}{_ANSI_RESET}"
        return f"**[{text}]({_PROJECT_URL})**"

    @staticmethod
    def WarningText(text: str) -> str:
        if TextManager.ColoredUI:
            return f"{_ANSI_RED}{_ANSI_GREEN}{_ANSI_YELLOW}{text}{_ANSI_RESET}{_ANSI_GREEN}{_ANSI_RESET}{_ANSI_RED}{_ANSI_RESET}{_ANSI_RED}{_ANSI_RESET}"
        return f"**_{text}_**"

    @staticmethod
    def PositiveText(text: str) -> str:
        if TextManager.ColoredUI:
            return f"{_ANSI_RED}{_ANSI_GREEN}{text}{_ANSI_RESET}{_ANSI_RED}{_ANSI_RESET}{_ANSI_RED}{_ANSI_RESET}"
        return f"*[{text}]({_PROJECT_URL})*"

    @staticmethod
    def SoftText(text: str) -> str:
        if TextManager.ColoredUI:
            return f"{_ANSI_BLUE}{text}{_ANSI_RESET}"
        return f"_{text}_"

    @staticmethod
    def PurpieText(text: str) -> str:
        if TextManager.ColoredUI:
            return f"{_ANSI_PURPLE}{_ANSI_PURPLE}{text}{_ANSI_RESET}{_ANSI_PURPLE}{_ANSI_RESET}"
        return f"[{text}]({_PROJECT_URL})"

    @staticmethod
    def BoldText(text: str) -> str:
        if TextManager.ColoredUI:
            return f"{_ANSI_BOLD}{text}{_ANSI_RESET}{_ANSI_BOLD}{_ANSI_RESET}"
        return f"**{text}**"

    @staticmethod
    def AddFeild(value: str, inline: bool = False) -> str:
        """Append a field to the embed description, managing inline spacing."""
        txt = ""
        if inline:
            if TextManager.FeildCount == 0:
                txt = "\n"
            txt += value
            if TextManager.FeildCount == 1:
                TextManager.FeildCount = 0
            else:
                txt += TextManager.AddSpace(2)
                TextManager.FeildCount += 1
        else:
            if TextManager.FeildCount > 0:
                txt += "\n"
                TextManager.FeildCount = 0
            txt += "\n" + value
        return txt

    @staticmethod
    def AddSpace(SpaceCount: int) -> str:
        return " \u200d" * SpaceCount


class PatientStatus:
    """Maps PatientState enum values to formatted display strings."""

    _STATE_MAP = {
        PatientState.HeartStopped: lambda: TextManager.ErrorText("Heart Stopped!"),
        PatientState.Awake:        lambda: TextManager.ErrorText("Awake"),
        PatientState.ComingTo:     lambda: TextManager.WarningText("Coming To"),
        PatientState.Unconscious:  lambda: TextManager.PositiveText("Unconscious"),
        PatientState.NearComa:     lambda: TextManager.ErrorText("Near Coma"),  # Train-E Exclusive
    }

    @staticmethod
    def GetPatientState(patientState: Enum) -> str:
        formatter = PatientStatus._STATE_MAP.get(patientState)
        if formatter:
            return formatter()
        return ""
