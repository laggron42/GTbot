import discord


class Team:
    """
    Represents a team in the war
    """

    def __init__(self, name: str, role: discord.Role):
        self.name = name
        self.role = role

    def __str__(self):
        return self.name

    def __repr__(self):
        name = self.name
        role = self.role
        return f"<GTbot.Team {name=} {role=} size={len(role.members)}>"
