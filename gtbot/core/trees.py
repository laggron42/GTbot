import asyncio

from gtbot.core.player import Player


class TreeManager:
    """
    Handles the leaderboard and counting of the trees.

    This is using a lock object to prevent asyncronous edit of the count.
    """

    def __init__(self, to_reach: int, count: int = 0):
        self.to_reach = to_reach
        self._count = count
        self.lock = asyncio.Lock()

    async def add_tree(self, count: int, player: Player = None):
        async with self.lock:
            self._count += count
            if player:
                player.score += count

    async def remove_tree(self, count: int, player: Player = None):
        async with self.lock:
            self._count -= count
            if player:
                player.score -= count

    async def count(self):
        async with self.lock:
            return self._count
