from typing import TYPE_CHECKING

from .actions import ActionList

if TYPE_CHECKING:
    from gtbot.core.bot import GTBot


def setup(bot: "GTBot"):
    bot.add_cog(ActionList(bot))
