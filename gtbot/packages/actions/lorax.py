import asyncio
from datetime import date, timedelta
from gtbot.core.errors import NotAllowed

from .actions import Action


class PlantTree(Action):
    emoji = "\N{deciduous tree}"
    cooldown = 10
    targeted = False
    trees = 1


class CreateForest(Action):
    emoji = "\N{evergreen tree}"
    cooldown = 600
    targeted = False
    trees = 0

    async def pre_action_hook(self):
        category = self.channel.category
        for channel in category.text_channels:
            if channel.name == "forest":
                await self.message.reply(
                    f"Il y a déjà un salon {channel.mention} dans la catégorie !",
                    mention_author=False,
                )
                raise NotAllowed

    async def action(self):
        async def create_and_destroy():
            channel = await self.channel.category.create_text_channel("forest")
            await asyncio.sleep(300)
            await channel.delete()

        self.bot.loop.create_task(create_and_destroy())


class DoublePoints(Action):
    emoji = "\N{christmas tree}"
    cooldown = 10
    targeted = False
    trees = 1

    async def pre_action_hook(self):
        if date.today().replace(year=0) != date(year=0, month=12, day=25):
            self.trees = 2
