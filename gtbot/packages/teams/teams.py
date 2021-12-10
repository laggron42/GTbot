from enum import Enum
from typing import TYPE_CHECKING

from discord.ext import commands
from dislash.application_commands.slash_core import slash_command
from dislash.interactions.app_command_interaction import SlashInteraction
from dislash.interactions.application_command import OptionParam

from gtbot.core.errors import NotFound

if TYPE_CHECKING:
    from gtbot.core.bot import GTBot


class TeamSelector(str, Enum):
    Lorax = 1
    Krampus = 2


class Teams(commands.Cog):
    """
    Handles the different teams. Currently hard-coded teams.
    """

    def __init__(self, bot: "GTBot"):
        self.bot = bot

    @slash_command(description="Gestions des équipes")
    async def teams(self, inter: SlashInteraction):
        pass

    @teams.sub_command(name="join", description="Rejoignez la team de votre choix")
    async def teams_join(
        self,
        inter: SlashInteraction,
        team: TeamSelector = OptionParam(description="Votre nouvelle team"),
    ):
        try:
            player = self.bot.find_player(inter.author)
        except NotFound:
            player = self.bot.add_player(inter.author)
            await inter.reply(
                "Vous êtes désormais inscrit à l'événement et avez rejoint l'équipe des {}!"
            )
        else:
            # edit player team
            await inter.reply("Vous avez désormais changé d'équipe.")
