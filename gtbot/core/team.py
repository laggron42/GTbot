import discord

from typing import List

from discord.errors import NotFound

from gtbot.core.errors import AlreadyPresent
from gtbot.core.player import Player


class Team:
    """
    Represents a team in the war
    """

    def __init__(self, name: str, role: discord.Role):
        self.name = name
        self.role = role
        self.members: List[Player] = []

    def __str__(self):
        return self.name

    def __repr__(self):
        name = self.name
        role = self.role
        return f"<GTbot.Team {name=} {role=} size={len(role.members)}>"

    async def add_player(self, player: Player):
        if player in self.members:
            raise AlreadyPresent("Player is already in the specified team.")
        await player.member.add_roles(self.role)
        player.team = self
        self.members.append(player)

    async def remove_player(self, player: Player):
        if player not in self.members:
            raise NotFound("The given player is not in this team.")
        await player.member.remove_roles(self.role)
        self.members.remove(player)
        player.team = None
