from typing import TYPE_CHECKING

from .teams import Teams

if TYPE_CHECKING:
    from gtbot.core.bot import GTBot


def setup(bot: "GTBot"):
    bot.add_cog(Teams(bot))
