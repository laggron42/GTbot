import discord

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gtbot.core.team import Team


class Player:
    """
    Describes a player in the war
    """

    def __init__(self, member: discord.Member):
        self.member = member
        self.team: "Team" = None

    def __repr__(self):
        member = self.member
        team = self.team
        return f"<GTbot.player {member=} {team=}>"

    async def clear_team(self):
        if self.team is not None:
            await self.team.remove_player(self)
