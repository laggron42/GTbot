import discord
import logging

from datetime import timedelta
from typing import Coroutine, List, Optional, Union

from discord.ext import commands

from gtbot.core.bot import GTBot
from gtbot.core.errors import NotAllowed, NotFound, SilentError
from gtbot.core.player import Player

log = logging.getLogger("gtbot.packages.actions")


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

    def __init__(self, bot: GTBot, player: Player, message: discord.Message, target: Optional[Player]):
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


class ActionList(commands.Cog):
    """
    The cog managing the player actions.
    """

    def __init__(self, bot: GTBot):
        self.bot = bot

    async def _get_target(self, mentions: List[Union[discord.User, discord.Member]]):
        try:
            target = mentions[0]
        except IndexError:
            # action requires a member to be mentioned but none was found
            raise NotAllowed("No member mentioned")
        try:
            return self.bot.find_player(target)
        except NotFound as e:
            raise NotAllowed("Mentioned member is not a registered player") from e

    async def _run_action_hooks(self, action: Action, method: Coroutine):
        try:
            await method
        except NotAllowed:
            raise
        except Exception as e:
            log.error(
                f"Error when running {action.__class__.__name__}.{method.__name__}.\n"
                f"Author: {action.player} ; Channel: {action.channel} ; Target: {action.taget}",
                exc_info=True,
            )
            raise SilentError from e

    async def run_action(self, action: type[Action], message: discord.Message):
        try:
            player = self.bot.find_player(message.author)
        except NotFound as e:
            raise NotAllowed("Only player can perform actions") from e
        target = None
        if action.targeted:
            target = await self._get_target(message.mentions)
        action = action(self.bot, player, message, target)
        await self._run_action_hooks(action, action.pre_action_hook())
        await self._run_action_hooks(action, action.action())
        if action.trees > 0:
            self.bot.trees.add_tree(action.trees, action.author)
        else:
            self.bot.trees.remove_tree(-action.trees, action.author)
        await self._run_action_hooks(action, action.post_action_hook())


# try:
#     await action.message.add_reaction("\N{stop sign}")
# except discord.Forbidden:
#     pass
