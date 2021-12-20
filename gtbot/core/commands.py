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

    @commands.group()
    @commands.is_owner()
    async def extensions(self, inter: SlashInteraction):
        pass

    @extensions.command(name="load")
    async def extensions_load(self, ctx: commands.Context, extension: str):
        await self.bot.load_extension(extension)
        await ctx.send("Extension chargée.")

    @extensions.command(name="reload")
    async def extensions_reload(self, ctx: commands.Context, extension: str):
        await self.bot.reload_extension(extension)
        await ctx.send("Extension rechargée.")

    @extensions.command(name="unload")
    async def extensions_unload(self, ctx: commands.Context, extension: str):
        await self.bot.unload_extension(extension)
        await ctx.send("Extension déchargée.")
