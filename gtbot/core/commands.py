import time

from typing import TYPE_CHECKING
from discord.ext import commands

from dislash.application_commands.slash_core import slash_command
from dislash.interactions.app_command_interaction import SlashInteraction

if TYPE_CHECKING:
    from .bot import GTBot


class Core(commands.Cog):
    """
    Core commands of GT bot
    """

    def __init__(self, bot: "GTBot"):
        self.bot = bot

    @slash_command(description="Affiche le temps de réponse du bot.")
    async def ping(self, inter: SlashInteraction):
        t1 = time.time()
        msg = await inter.reply("Pong!")
        t2 = time.time()
        await msg.edit(content="Pong!\nDelay: `{t}ms`".format(t=round((t2 - t1) * 1000)))
