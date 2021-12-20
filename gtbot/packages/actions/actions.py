import discord
import logging

from typing import Coroutine, List, Union, TYPE_CHECKING

from discord.ext import commands

from gtbot.core.action import Action
from gtbot.core.errors import NotAllowed, NotFound, SilentError
from gtbot.core.team import Lorax, Krampus

from .lorax import PlantTree, CreateForest, DoublePoints

if TYPE_CHECKING:
    from gtbot.core.player import Player
    from gtbot.core.bot import GTBot

LORAX_ACTIONS = [PlantTree, CreateForest, DoublePoints]
KRAMPUS_ACTIONS = []

log = logging.getLogger("gtbot.packages.actions")


class ActionList(commands.Cog):
    """
    The cog managing the player actions.
    """

    def __init__(self, bot: "GTBot"):
        self.bot = bot
        self.bot.lorax.actions = LORAX_ACTIONS
        self.bot.krampus.actions = KRAMPUS_ACTIONS

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

    async def run_action(self, player: "Player", action: type[Action], message: discord.Message):
        target = None
        if action.targeted:
            target = await self._get_target(message.mentions)
        action = action(self.bot, player, message, target)
        await self._run_action_hooks(action, action.pre_action_hook())
        await self._run_action_hooks(action, action.action())
        if action.trees > 0:
            await self.bot.trees.add_tree(action.trees, action.author)
        else:
            await self.bot.trees.remove_tree(-action.trees, action.author)
        await self._run_action_hooks(action, action.post_action_hook())

    @commands.Cog.listener("on_raw_reaction_add")
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.guild_id != self.bot.guild.id:
            return

        member = self.bot.guild.get_member(payload.user_id)
        try:
            player = self.bot.find_player(member)
        except NotFound as e:
            return

        if player.team is None:
            return
        if isinstance(player.team, Lorax):
            actions = self.bot.lorax.actions
        else:
            actions = self.bot.krampus.actions

        try:
            action = next(filter(lambda x: x.emoji == payload.emoji.name, actions))
        except StopIteration:
            return
        channel = self.bot.guild.get_channel(payload.channel_id)
        if channel is None:
            log.error(f"Channel {payload.channel_id} not found while processing action.")
            return
        try:
            message = await channel.fetch_message(payload.message_id)
        except discord.DiscordException as e:
            log.error(
                f"Cannot fetch message {payload.message_id} while processing action.",
                exc_info=True,
            )
            return
        try:
            await self.run_action(player, action, message)
        except NotAllowed:
            pass
        except:
            log.error(f"Failed running action {action}.", exc_info=True)


# try:
#     await action.message.add_reaction("\N{stop sign}")
# except discord.Forbidden:
#     pass
