import logging
from datetime import time

import nextcord
from nextcord.ext import commands, tasks

from utility.bot import Vortex


class TemplateTask(commands.Cog):
    def __init__(self, bot: Vortex):
        self.bot: Vortex = bot
        self.template_task.start()

    def cog_unload(self) -> None:
        self.template_task.cancel()

    @tasks.loop(time=time(hour=10, minute=00))
    async def template_task(self):
        ...

    @template_task.before_loop
    async def before_task(self) -> None:
        await self.bot.wait_until_ready()
        logging.info(f"{self.__class__.__name__} started")


def setup(bot: Vortex):
    bot.add_cog(TemplateTask(bot))