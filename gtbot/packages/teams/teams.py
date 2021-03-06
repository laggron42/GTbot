from enum import Enum
from typing import TYPE_CHECKING

from discord.ext import commands
# from discord.ui.view import View
from dislash.application_commands.slash_core import slash_command
from dislash.interactions.app_command_interaction import SlashInteraction
from dislash.interactions.application_command import OptionParam

from gtbot.core.errors import NotFound
from gtbot.core.team import Team

# from .team_viewer import TeamMenuSelector

if TYPE_CHECKING:
    from gtbot.core.bot import GTBot


class TeamSelector(Enum):
    Lorax = "lorax"
    Krampus = "krampus"


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
        if len(TeamSelector) != 2:
            await inter.reply(
                ":warning: Le bot n'est pas proprement initialisé "
                "et les équipes ne sont pas disponibles."
            )
            return
        team: Team = getattr(self.bot, team)
        try:
            player = self.bot.find_player(inter.author)
        except NotFound:
            player = self.bot.add_player(inter.author)
            await team.add_player(player)
            await inter.reply(
                "Vous êtes désormais inscrit à l'événement "
                f"et avez rejoint l'équipe des {team.name}!"
            )
        else:
            await player.clear_team()
            await team.add_player(player)
            await inter.reply("Vous avez désormais changé d'équipe.")

    @teams.sub_command(name="leave", description="Quittez votre équipe actuelle")
    async def teams_leave(
        self,
        inter: SlashInteraction,
    ):
        try:
            player = self.bot.find_player(inter.author)
        except NotFound:
            await inter.reply("Vous n'êtes pas inscrit à l'événement.")
        else:
            if player.team is None:
                await inter.reply("Vous n'avez pas de team actuellement.")
            else:
                await player.clear_team()
                await inter.reply("Vous avez quitté votre équipe.")

    @teams.sub_command(name="list", description="Liste les différentes équipes")
    async def teams_list(self, inter: SlashInteraction):
        # view = View()
        # view.add_item(TeamMenuSelector(self.bot.teams))
        message = "__**Liste des équipes**__\n\n"
        for team in [self.bot.lorax, self.bot.krampus]:
            message += f"**{team.name}**: {len(team)} membres\n"
        await inter.reply(message)
