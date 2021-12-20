import discord
import asyncio
import logging
import sys

from importlib.machinery import ModuleSpec
from importlib.util import find_spec
from dislash.application_commands.slash_client import SlashClient
from rich import print
from typing import List

from discord.ext import commands
from dislash import SlashInteraction
from dislash.application_commands.errors import ApplicationCommandError

from gtbot.core.team import Team, Lorax, Krampus
from gtbot.core.trees import TreeManager
from gtbot.core.player import Player
from gtbot.core.errors import NotFound

log = logging.getLogger("gtbot.core.bot")

PACKAGES = ["teams", "actions"]
GUILD_ID = 176056427285184512
TEAMS = {
    Lorax: {
        "role_id": 912266638890508289,
    },
    Krampus: {
        "role_id": 912266644519268403,
    },
}


class GTBot(commands.Bot):
    """
    Go Together! bot
    """

    slash: SlashClient

    def __init__(self, command_prefix, **options):
        intents = discord.Intents(guilds=True, members=True, messages=True, reactions=True)
        super().__init__(command_prefix, intents=intents, **options)
        self._shutdown = 0

        self.guild: discord.Guild
        self.players: List[Player] = []
        self.lorax: Lorax
        self.krampus: Krampus
        self.trees = TreeManager(150)

    def init_teams(self):
        for team, data in TEAMS.items():
            role = self.guild.get_role(data["role_id"])
            if not role:
                log.warning(
                    f"Failed to load team {team}, "
                    f"role with ID {data['role_id']} could not be found!"
                )
                continue
            try:
                setattr(self, team.__name__.lower(), team(role))
            except Exception:
                log.warning(f"Failed to initialize team {team}.", exc_info=True)

    def find_player(self, member: discord.Member):
        try:
            return next(filter(lambda x: x.member.id == member.id, self.players))
        except StopIteration:
            raise NotFound("Member not registered as a player.")

    def add_player(self, member: discord.Member):
        player = Player(member)
        self.players.append(player)
        return player

    async def load_extension(self, spec: ModuleSpec):
        name = spec.name.split(".")[-1]
        if name in self.extensions:
            raise RuntimeError(f"Package {spec.name.split('.')[-1]} is already loaded.")

        lib = spec.loader.load_module()
        if not hasattr(lib, "setup"):
            del lib
            raise discord.ClientException(f"extension {name} does not have a setup function")

        try:
            if asyncio.iscoroutinefunction(lib.setup):
                await lib.setup(self)
            else:
                lib.setup(self)
        except Exception:
            self._remove_module_references(lib.__name__)
            self._call_module_finalizers(lib, name)
            raise

    async def on_shard_ready(self, shard_id: int):
        log.debug(f"Connected to shard #{shard_id}")

    async def on_ready(self):
        log.info(f"Successfully logged in as {self.user} ({self.user.id})!")
        self.guild = self.get_guild(GUILD_ID)
        if not self.guild:
            log.critical(
                f"Guild with ID {GUILD_ID} cannot be found within the bot! Shutting down..."
            )
            await self.close()
            self._shutdown = 1
            sys.exit(self._shutdown)
        log.info(f'The bot is set to run on guild "{self.guild.name}" with ID {self.guild.id}')
        try:
            self.init_teams()
        except Exception:
            log.error(
                "Failed to initialize teams! "
                "You may want to shutdown the bot now to prevent unexpected behaviours.",
                exc_info=True,
            )
        else:
            log.info(f"Loaded teams.")
        log.info("Loading packages...")
        loaded_packages = []
        for package in PACKAGES:
            try:
                await self.load_extension(find_spec("gtbot.packages." + package))
            except Exception:
                log.error(f"Failed to load package {package}", exc_info=True)
            else:
                loaded_packages.append(package)
        if loaded_packages:
            log.info(f"Packages loaded: {', '.join(loaded_packages)}")
        else:
            log.info("No package loaded.")
        print("\n    [bold][red]GTbot[/red] [green]is now operational![/green][/bold]\n")

    async def on_slash_command_error(
        self, inter: SlashInteraction, error: ApplicationCommandError
    ):
        log.error(f"Error in slash command {inter.slash_command.name}", exc_info=error)
        await inter.reply("An error occured.")

    async def on_command_error(
        self, context: commands.Context, exception: commands.errors.CommandError
    ):
        if isinstance(exception, commands.CommandNotFound):
            return
        log.error(f"Error in text command {context.command.name}", exc_info=exception)
