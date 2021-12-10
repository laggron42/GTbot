from discord.ui import Select
from discord.components import SelectOption
from discord.interactions import Interaction

from typing import List

from gtbot.core.team import Team


class TeamViewer(SelectOption):
    def __init__(self, team: Team):
        super().__init__(
            label=team.name,
            emoji=team.emoji,
        )


class TeamMenuSelector(Select):
    def __init__(self, teams: List[Team]):
        self.teams = teams
        options = []
        for team in self.teams:
            options.append(TeamViewer(team))
        super().__init__(
            placeholder="Cliquez pour afficher les détails d'une équipe",
            options=options,
        )

    async def callback(self, interaction: Interaction):
        print(interaction)
