import os
import sys
import time
import signal
import asyncio
import logging
import discord
import dislash
import argparse

from rich import print

from gtbot import __version__ as bot_version
from gtbot.loggers import init_logger
from gtbot.core.bot import GTBot
from gtbot.core.dev import Dev
from gtbot.core.commands import Core

log = logging.getLogger("gtbot")


def parse_cli_flags(arguments: str):
    parser = argparse.ArgumentParser(prog="GT bot", description="La guerre des Krampus et Lorax")
    parser.add_argument("--version", "-V", action="store_true", help="Affiche la version du bot")
    parser.add_argument("--debug", action="store_true", help="Active les logs de debug")
    parser.add_argument("--token", action="store", type=str, help="Le token du bot")
    parser.add_argument("--dev", action="store_true", help="Activer le mode développeur")
    args = parser.parse_args(arguments)
    return args


def print_welcome():
    print("[green]{0:-^50}[/green]".format(" Go Together bot "))
    print("[green]{0: ^50}[/green]".format(" Lorax/Krampus war "))
    print("[blue]{0:^50}[/blue]".format("Discord bot made by El Laggron"))
    print("")
    print(" [red]{0:<20}[/red] [yellow]{1:>10}[/yellow]".format("Bot version:", bot_version))
    print(
        " [red]{0:<20}[/red] [yellow]{1:>10}[/yellow]".format(
            "Discord.py version:", discord.__version__
        )
    )
    print("")


async def shutdown_handler(bot: GTBot, signal_type: str = None):
    if signal_type:
        log.info(f"Received {signal_type}, stopping the bot...")
    else:
        log.info("Shutting down the bot...")
    try:
        await bot.close()
    finally:
        pending = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        [task.cancel() for task in pending]
        await asyncio.gather(*pending, return_exceptions=True)


def main():
    bot = None
    cli_flags = parse_cli_flags(sys.argv[1:])
    if cli_flags.version:
        print(f"GT Discord bot - {bot_version}")
        sys.exit(0)

    print_welcome()
    time.sleep(1)

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        init_logger(cli_flags.debug)

        token = cli_flags.token or os.environ.get("GTBOT_TOKEN", None)
        if not token:
            log.error("Token non trouvé!")
            print("[yellow]Vous devez fournir un token avec le flag --token.[/yellow]")
            time.sleep(1)
            sys.exit(0)

        bot = GTBot(command_prefix="!?")
        bot.owner_id = 348415857728159745
        dislash.InteractionClient(bot, test_guilds=[176056427285184512])
        bot.add_cog(Core(bot))
        if cli_flags.dev:
            bot.add_cog(Dev())

        try:
            loop.add_signal_handler(
                signal.SIGTERM,
                lambda: asyncio.create_task(shutdown_handler(bot, signal.SIGTERM)),
                bot,
                "SIGTERM",
            )
        except NotImplementedError:
            # Not a UNIX environment (Windows)
            pass

        log.info("Initialized bot, connecting to Discord...")
        loop.create_task(bot.start(token))
        loop.run_forever()
    except KeyboardInterrupt:
        if bot is not None:
            loop.run_until_complete(shutdown_handler(bot, "Ctrl+C"))
    except SystemExit:
        if bot is not None:
            loop.run_until_complete(shutdown_handler(bot))
    except Exception:
        log.critical("Unhandled exception.", exc_info=True)
        if bot is not None:
            loop.run_until_complete(shutdown_handler(bot))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        asyncio.set_event_loop(None)
        loop.stop()
        loop.close()
        sys.exit(bot._shutdown)


if __name__ == "__main__":
    main()
