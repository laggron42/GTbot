import discord

from typing import Optional


class Player:
    """
    Describes a player in the war
    """

    def __init__(self, member: discord.Member):
        self.member = member
        self.team = None

    def __repr__(self):
        member = self.member
        team = self.team
        return f"<GTbot.player {member=} {team=}>"
