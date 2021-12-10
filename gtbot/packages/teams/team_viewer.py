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
        for i, team in enumerate(self.teams):
            tv = TeamViewer(team)
            tv.value = i
            options.append(tv)
        super().__init__(
            placeholder="Cliquez pour afficher les détails d'une équipe",
            options=options,
        )

    async def show_team_info(self):
        pass

    async def callback(self, interaction: Interaction):
        pass
