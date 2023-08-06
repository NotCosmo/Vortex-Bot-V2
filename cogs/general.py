from utility.bot import Vortex
from utility.bot import Vortex
from utility.constants import BotConstants
from nextcord import slash_command, Interaction, SlashOption, Embed, Member, Spotify, Colour
from nextcord.ext.commands import Cog, Context, command, guild_only
from datetime import datetime
from logging import info
from time import time
from platform import python_version
from psutil import Process, virtual_memory
from nextcord import __version__ as nc_ver

import humanize
import xmltodict


class General(Cog, description="General commands of the bot."):

    def __init__(self, bot: Vortex) -> None:
        self.bot: Vortex = bot

    @command(name="ping", aliases=["latency"], description="Display bot latency in ms")
    async def ping(self, ctx: Context):

        embed = Embed(
            title=":ping_pong: Pong!",
            description=f"Bot Latency: {round(self.bot.latency * 1000, 2)}",
            colour=self.bot.MAIN_COLOUR,
        )
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @command(name="userinfo", aliases=["ui", "memberinfo", "mi"], description="Shows a bunch of information about a user.")
    async def userinfo(self, ctx: Context, member: Member | None = None):

        member = member or ctx.author
        joined_days_ago = (datetime.today().replace(tzinfo=member.joined_at.tzinfo) - member.joined_at).days
        created_days_ago = (datetime.today().replace(tzinfo=member.joined_at.tzinfo) - member.created_at).days
        booster = (
            member.premium_since.strftime("%H:%M:%S, %d.%m.%Y")
            if member.premium_since
            else "No active boosts."
        )

        embed = Embed(title=f"{member}", colour=self.bot.MAIN_COLOUR)
        embed.set_thumbnail(url=member.avatar.with_size(4096).url)
        user = await self.bot.fetch_user(member.id)
        if user.banner:
            embed.set_image(user.banner.with_size(4096).url)

        embed.add_field(name=":hammer: Joined Discord", value=f"<t:{int(member.created_at.timestamp())}:R>\n{created_days_ago} days ago", inline=True)
        embed.add_field(name=":busts_in_silhouette: Joined Server", value=f"<t:{int(member.joined_at.timestamp())}:R>\n{joined_days_ago} days ago", inline=True)
        embed.add_field(name=self.bot.transparent, value=self.bot.transparent, inline=True)
        embed.add_field(name=":rocket: Boosts", value=f"{booster}", inline=True)
        embed.add_field(name=":robot: Bot", value=member.bot, inline=True)
        embed.add_field(name="Top Role", value=member.top_role, inline=True)
        embed.add_field(
            name=f"Roles [{len(member.roles) - 1}]",
            value=" ".join([role.mention for role in member.roles[1:]]),
            inline=False,
        )
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.with_size(4096).url)
        await ctx.send(embed=embed)

    @command(
        name="stats",
        aliases=["about", "info"],
        brief="Shows a bunch of stuff about the bot.",
    )
    async def stats(self, ctx: Context) -> None:
        stats_embed = Embed(
            title=f"Bot stats | Commands: {len(self.bot.commands)}",
            color=self.bot.MAIN_COLOUR,
        )
        stats_embed.set_thumbnail(url=self.bot.user.display_avatar.with_size(4096).url)
        proc = Process()
        with proc.oneshot():
            mem_total = virtual_memory().total / (1024**2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)

        fields = [
            (
                "Bot version",
                f"v0.0.1",
                #f"v{self.bot.major_version}.{self.bot.minor_version}.{self.bot.patch_version}",
                True,
            ),
            ("Python version", python_version(), True),
            ("Nextcord version", nc_ver, True),
            ("Uptime", self.bot.get_uptime(), True),
            (
                "Memory usage",
                f"{mem_usage:,.3f} MiB / {mem_total:,.3f} MiB ({mem_of_total:.3f}%)",
                True,
            ),
            (
                "Popularity",
                f"{len(self.bot.users):,} users in {len(self.bot.guilds):,} servers",
                True,
            ),
            ("Developed by", f"<@{self.bot.owner_id}>", False),
        ]

        for name, value, inline in fields:
            stats_embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=stats_embed)

def setup(bot: Vortex) -> None:
    bot.add_cog(General(bot))