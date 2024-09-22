from discord.ext.commands import Cog, group

from bot.bot import Ordis
from bot.context import Context


class Market(Cog):
    def __init__(self, bot: Ordis) -> None:
        self.bot = bot

    @group()
    async def market(self, ctx: Context) -> None:
        await ctx.check_subcommands()


async def setup(bot: Ordis) -> None:
    await bot.add_cog(Market(bot))
