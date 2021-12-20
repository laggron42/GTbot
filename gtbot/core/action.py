import discord

from datetime import timedelta
from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from gtbot.core.bot import GTBot
    from gtbot.core.player import Player


class Action:
    """
    Represents a single action.

    When creating an action, inherit from this class and implement the following values:

    Attributes
    ----------
    emoji: Union[str, discord.Emoji]
        The emoji representing the action.
    cooldown: Union[int, timedelta]
        If the action was successful, set the following cooldown on the user
        (seconds or timedelta object).
    targeted: bool
        Set to `True` if the user has to specify a member with his action.
    trees: int
        The number (positive or negative) of trees to edit once the action is over.
    """

    def __init__(
        self, bot: "GTBot", player: "Player", message: discord.Message, target: Optional["Player"]
    ):
        self.bot = bot
        self.player = self.author = player
        self.message = message
        self.channel = message.channel
        self.taget = target

    emoji: Union[str, discord.Emoji]
    cooldown: Union[int, timedelta]
    targeted: bool
    trees: int

    async def pre_action_hook(self):
        """
        This function is called before performing an action.
        You must put any kind of verification here (cooldown excluded).

        If you must cancel the action, raise `~gtbot.core.errors.NotAllowed`.
        """
        pass

    async def action(self):
        """
        The function called when a member is running the specified action.

        This passed the cooldown and other checks.

        If nothing special has to be done or is already specified by the `trees` attribute,
        leave this empty.
        """
        pass

    async def post_action_hook(self):
        """
        The action was successful.
        You may put any kind of post processing here (cooldown excluded).
        """
        pass
