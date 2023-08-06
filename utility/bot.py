import nextcord
from nextcord.ext.commands import Bot

import datetime
import logging
import os
import time
from typing import Optional
import aiohttp
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s"
)

class Vortex(Bot):

    def __init__(self) -> None:
        super().__init__(
            command_prefix="v!",
            case_insensitive=True,
            intents=nextcord.Intents.all(),
            strip_after_prefix=True,
            owner_id=455971566199767040,
        )

        # Internal Stuff
        self.aiohttp_session: Optional[aiohttp.ClientSession] = None
        self.token: Optional[str] = os.getenv("BOT_TOKEN")
        self.start_time = time.time()

        # Versions
        # self.major_version, self.minor_version, self.patch_version = os.getenv(
        #    "BOT_VERSION"
        # ).split(".")

        self.MAIN_COLOUR = nextcord.Colour.from_rgb(0, 208, 255)
        self.ERROR_COLOUR = nextcord.Colour.from_rgb(255, 75, 75)
        self.SUCCESS_COLOUR = nextcord.Colour.from_rgb(75, 255, 75)
        self.transparent = "<:transparent:911319446918955089>"
    
    def get_uptime(self) -> datetime.timedelta:
        delta = int(time.time() - self.start_time)
        uptime = datetime.timedelta(seconds=delta)
        return uptime

    def load_dir(self, directory: str) -> None:
        files = [
            file[:-3] for file in os.listdir(directory) if not file.startswith("__")
        ]
        for file in files:
            ext = f"{directory}.{file}"
            self.load_extension(ext)
            logging.info(f"{ext} loaded successfully")

    def load_cogs(self) -> None:
        self.load_dir("cogs")
        # self.load_extension("jishaku")
        logging.info("loading extensions finished")

    def load_tasks(self) -> None:
        # self.load_dir("tasks")
        logging.info("loading tasks finished")

    async def register_aiohttp_session(self) -> None:
        self.aiohttp_session = aiohttp.ClientSession()

    def run_bot(self) -> None:
        logging.info("starting up...")
        self.loop.create_task(self.register_aiohttp_session())
        self.load_cogs()
        self.load_tasks()
        super().run(self.token)

    # Events
    async def on_ready(self) -> None:
        logging.info(f"ready as {self.user} / {self.user.id}")