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

import discord
from discord.ui import Button, View

from core.enums import ToolType, ToolIcon
from core.patient import Patient
from core.text import TextManager

# Tool layout definition: (icon, type, visibility_fn)
# Each entry's visibility function receives (patient, IsSiteClean) and returns bool.
_TOOL_LAYOUT = [
    (ToolIcon.SurgicalDefib,      ToolType.SurgicalDefib,      lambda p, c: c and p.HeartDamage > 0),
    (ToolIcon.SurgicalSponge,     ToolType.SurgicalSponge,     lambda p, c: True),
    (ToolIcon.SurgicalAnesthetic, ToolType.SurgicalAnesthetic, lambda p, c: c),
    (ToolIcon.SurgicalStitches,   ToolType.SurgicalStitches,   lambda p, c: c),
    (ToolIcon.SurgicalScalpel,    ToolType.SurgicalScalpel,    lambda p, c: c),
    (ToolIcon.SurgicalUltrasound, ToolType.SurgicalUltrasound, lambda p, c: not p.IsUltrasoundUsed and c),
    (ToolIcon.SurgicalAntiseptic, ToolType.SurgicalAntiseptic, lambda p, c: c),
    (ToolIcon.FixIt,              ToolType.FixIt,              lambda p, c: (p.IsFixable and (not p.IsPatientFixed or p.IsBrainWorms or p.IncisionsNeeded == p.Incisions)) and c),
    (ToolIcon.SurgicalLabKit,     ToolType.SurgicalLabKit,     lambda p, c: not p.IsLabKitUsed and c),
    (ToolIcon.SurgicalAntibiotics,ToolType.SurgicalAntibiotics,lambda p, c: p.LabWorked and c),
    (ToolIcon.SurgicalTransfusion,ToolType.SurgicalTransfusion,lambda p, c: c),
    (ToolIcon.SurgicalSplint,     ToolType.SurgicalSplint,     lambda p, c: c),
    (ToolIcon.SurgicalPins,       ToolType.SurgicalPins,       lambda p, c: c and p.Incisions > 0),
    (ToolIcon.SurgicalClamp,      ToolType.SurgicalClamp,      lambda p, c: c and p.Incisions > 0),
    (ToolIcon.SurgicalLoveMallet, ToolType.SurgicalLoveMallet, lambda p, c: False),  # Valentines Only
]


class SurgeryView(View):
    def __init__(self, surgery, author):
        super().__init__(timeout=1800)
        self.author = author
        self.surgery = surgery
        self.patient: Patient = surgery.patient
        self.GenerateToolButtons()

    async def interaction_check(self, inter: discord.Interaction) -> bool:
        if inter.user != self.author:
            await inter.response.send_message(content="Let the doctor do their job!", ephemeral=True)
            return False
        return True

    def GenerateToolButtons(self):
        """Build the tool button grid based on current patient state."""
        IsSiteClean = self.patient.SiteDirtyness < 10

        for toolIcon, toolType, visibility_fn in _TOOL_LAYOUT:
            is_visible = visibility_fn(self.patient, IsSiteClean)
            if is_visible:
                self._AddActiveToolButton(toolIcon, toolType)
            else:
                self._AddDisabledButton()

        self._AddGiveUpButton()

    def _AddActiveToolButton(self, toolIcon: ToolIcon, toolType: ToolType):
        button = Button(emoji=toolIcon.value, style=discord.ButtonStyle.secondary)
        callback = self._MakeToolCallback(toolType)
        if callback is not None:
            button.callback = callback
            self.add_item(button)

    def _AddDisabledButton(self):
        button = Button(emoji=ToolIcon.EmptySurgeryTray.value, style=discord.ButtonStyle.secondary, disabled=True)
        self.add_item(button)

    def _AddGiveUpButton(self):
        button = Button(label="Give Up", style=discord.ButtonStyle.danger)
        button.callback = self._OnGiveUp
        self.add_item(button)

    async def _OnGiveUp(self, interaction: discord.Interaction):
        self.clear_items()
        embed = discord.Embed(
            title="Surgery Aborted",
            description=f"[Dr.{interaction.user.display_name}](https://github.com/CantFindDev/SurgE) was not ready for this surgery and gave up!",
            color=discord.Color.red()
        )
        self.patient.IsSurgeryEnded = True
        await interaction.response.edit_message(embed=embed, view=self)

    def _MakeToolCallback(self, toolType):
        async def callback(interaction: discord.Interaction):
            skillfail_occurred = self.patient.UseTool(toolType)
            embed_color = self._DetermineEmbedColor(skillfail_occurred)

            if self.patient.IsSurgeryEnded:
                self.clear_items()

            embed = discord.Embed(title="", description="", color=embed_color)

            self.clear_items()
            if not self.patient.IsSurgeryEnded:
                self.GenerateToolButtons()

            self.patient.SetCurrentPatientEmbed(embed)
            embed.set_footer(text="Surg system is being developed by CantFind")
            await interaction.response.edit_message(embed=embed, view=self)

        return callback

    def _DetermineEmbedColor(self, skillfail_occurred: bool) -> discord.Color:
        if self.patient.IsSurgeryEnded:
            return discord.Color.green() if "success" in self.patient.EndText.lower() else discord.Color.red()
        return discord.Color.red() if skillfail_occurred else discord.Color.blue()
