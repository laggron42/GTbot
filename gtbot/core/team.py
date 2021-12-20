import discord

from typing import List, Type, Union

from discord.errors import NotFound

from gtbot.core.errors import AlreadyPresent
from gtbot.core.player import Player
from gtbot.core.action import Action


class Team:
    """
    Represents a team in the war
    """

    name: str
    members: List[Player]
    actions: List[Type[Action]]

    def __init__(self, role: discord.Role, emoji: Union[str, discord.Emoji] = None):
        self.role = role
        self.emoji = emoji
        self.members = []
        self.actions = []

    def __str__(self):
        return self.name

    def __repr__(self):
        name = self.name
        role = self.role
        return f"<GTbot.Team {name=} {role=} size={len(role.members)}>"

    def __len__(self):
        return len(self.members)

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


class Lorax(Team):
    name = "Lorax"


class Krampus(Team):
    name = "Krampus"
