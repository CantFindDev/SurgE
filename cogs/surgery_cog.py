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

import typing
from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands

from core.patient import Patient
from core.surgery import Surgery
from core.enums import PatientState
from core.data_loaders import Maladies, SpecialConditions, Modifiers
from core.text import TextManager, PatientStatus
from ui.surgery_view import SurgeryView


class SurgeryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    async def AutoCompleteMalady(self, interaction: discord.Interaction,
    current: str) -> typing.List[app_commands.Choice[str]]:
     match = []
     for disease in Maladies.GetAllMaladieNames():
        if current.lower() in disease.lower():
            match.append(app_commands.Choice(name=disease, value=disease))
        if len(match) >= 25:
           break
     return match

    async def AutoCompleteModifier(self, interaction: discord.Interaction,
    current: str) -> typing.List[app_commands.Choice[str]]:
     match = []
     for modifiers in Modifiers.GetAllModifiersByNames():
            if current.lower() in modifiers.lower():
                match.append(app_commands.Choice(name=modifiers, value=modifiers))
            if len(match) >= 25:
                break
     return match

    async def AutoCompleteCondition(self, interaction: discord.Interaction,
    current: str) -> typing.List[app_commands.Choice[str]]:
     CondMatch = []
     for condition in SpecialConditions.GetAllSpecialConditions():
        if current.lower() in condition.lower():
            CondMatch.append(app_commands.Choice(name=condition, value=condition))
        if len(CondMatch) >= 25:
           break
     return CondMatch

    LastExecutionByUser = {}

    @app_commands.command(name="repeat", description="Repeat the last surgery.")
    async def repeat(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if interaction.user.id not in self.LastExecutionByUser:
            return await interaction.followup.send(
                embed=discord.Embed(
                    title="No Past Surgeries Found",
                    description="You have not started a surgery yet.",
                    color=discord.Color.red()
                ),
                ephemeral=True  # Make it ephemeral to the user
            )

        # Retrieve the stored surgery arguments
        surgery_data = self.LastExecutionByUser[interaction.user.id]

        # Call the helper function to perform the surgery
        await self.start_surgery(
            interaction,
            modifier=surgery_data.get('modifier'),
            malady=surgery_data.get('malady'),
            special_condition=surgery_data.get('special_condition'),
            skill_level=surgery_data.get('skill_level'),
            colored_ui=surgery_data.get('colored_ui'),
            hidden_embed=surgery_data.get('hidden_embed'),
            traine_mode=surgery_data.get('traine_mode')
        )

    @app_commands.command(
        name="surg",
        description="Start a surgery simulation."
    )
    @app_commands.describe(
        modifier="Select a modifier that can improve your surgery",
        malady="Select a specific malady to surg",
        special_condition="Select a special condition",
        skill_level="Set the skill level (default is 100)",
        colored_ui="Make the UI colored (Might not work on mobile)",
        hidden_embed="Hide the surgery UI from other people",
        traine_mode="I'm not Train-E but I can try to act like it :)"
    )
    @app_commands.autocomplete(
        malady=AutoCompleteMalady,
        special_condition=AutoCompleteCondition,
        modifier=AutoCompleteModifier
    )
    async def surg(self, interaction: discord.Interaction, modifier: Optional[str] = None, malady: Optional[str] = None,
                   special_condition: Optional[str] = None, skill_level: Optional[int] = 100,
                   colored_ui: Optional[bool] = False, hidden_embed: Optional[bool] = False,
                   traine_mode: Optional[bool] = False):

        # Defer the response, using ephemeral=hidden_embed to control visibility
        await interaction.response.defer(ephemeral=hidden_embed)

        # Store the surgery data for repeat use
        self.LastExecutionByUser[interaction.user.id] = {
            'modifier': modifier,
            'malady': malady,
            'special_condition': special_condition,
            'skill_level': skill_level,
            'colored_ui': colored_ui,
            'hidden_embed': hidden_embed,
            'traine_mode': traine_mode
        }

        # Call the helper function to perform the surgery
        await self.start_surgery(
            interaction,
            modifier=modifier,
            malady=malady,
            special_condition=special_condition,
            skill_level=skill_level,
            colored_ui=colored_ui,
            hidden_embed=hidden_embed,
            traine_mode=traine_mode
        )

    async def start_surgery(self, interaction: discord.Interaction, modifier: Optional[str], malady: Optional[str],
                            special_condition: Optional[str], skill_level: Optional[int],
                            colored_ui: Optional[bool], hidden_embed: Optional[bool],
                            traine_mode: Optional[bool]):

        # Ensure skill level is within bounds
        skill_level = max(0, min(100, skill_level))

        # Check for invalid maladies
        if malady and malady not in Maladies.GetAllMaladieNames():
            return await interaction.followup.send(
                embed=discord.Embed(
                    title="Invalid Malady!",
                    description="**Please choose from the following:**\n" + "\n".join(Maladies.GetAllMaladieNames()),
                    color=discord.Color.red()
                ),
                ephemeral=hidden_embed  # Ephemeral flag based on user's choice
            )

        # Check for invalid special conditions
        if special_condition and special_condition not in SpecialConditions.GetAllSpecialConditions():
            return await interaction.followup.send(
                embed=discord.Embed(
                    title="Invalid Condition!",
                    description="**Please choose from the following:**\n" + "\n".join(SpecialConditions.GetAllSpecialConditions()),
                    color=discord.Color.red()
                ),
                ephemeral=hidden_embed  # Ephemeral flag based on user's choice
            )

        # Create the patient and surgery
        patient = Patient(
            SkillLevel=skill_level,
            malady=malady,
            specialcondition=special_condition,
            modifier=modifier,
            TrainEMode=traine_mode
        )
        surgery = Surgery(patient=patient, user=interaction.user)

        view = SurgeryView(surgery, interaction.user)
        TextManager.setTextManager(colored_ui)
        patient.PatientStatus = PatientStatus.GetPatientState(PatientState.Awake)
        if not patient.ScanText:
            patient.ScanText = TextManager.ErrorText("The patient has not been diagnosed.")

        # Create an embed for the surgery
        embed = discord.Embed(
            title="Surgery",
            description="",
            color=discord.Color.blue()
        )
        patient.UpdatePatientUITexts()
        patient.SetCurrentPatientEmbed(embed)
        embed.set_footer(text="Surg system is being developed by CantFind")

        # Send the surgery UI, with ephemeral flag based on hidden_embed
        message = await interaction.followup.send(embed=embed, view=view, ephemeral=hidden_embed)

        await patient.timer(2)

        if patient.IsSurgeryEnded:
            return

        # If surgery is abandoned, clear the items and notify
        view.clear_items()
        embed = discord.Embed(
            title="Surgery Abandoned",
            description=f"[Dr.{interaction.user.display_name}](https://github.com/CantFindDev/SurgE) has left the room and abandoned the patient. Leaving them to their death!",
            color=discord.Color.red()
        )

        await message.edit(embed=embed, view=view)
        patient.IsSurgeryEnded = True


# Setup the cog
async def setup(bot):
    await bot.add_cog(SurgeryCog(bot))
