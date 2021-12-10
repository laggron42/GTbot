import discord
import asyncio
import logging

from importlib.machinery import ModuleSpec
from importlib.util import find_spec

from discord.ext import commands
from dislash import SlashInteraction
from dislash.application_commands.errors import ApplicationCommandError

log = logging.getLogger("gtbot.core.bot")

PACKAGES = []


class GTBot(commands.Bot):
    """
    Go Together! bot
    """
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
