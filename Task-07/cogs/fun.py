"""
cogs/fun.py

The non-economy, flavor command: !logpose, which pulls live data from
the public One Piece API (https://api.api-onepiece.com/v2) - a random
character's bounty/crew, or a random Devil Fruit's power.

This is the one file in the bot that talks to the network instead of
the database, which is exactly why it's split out into its own cog:
economy.py and shop.py never need to know that logpose exists, and if
the One Piece API ever changes or goes down, the blast radius is
contained to this one file.
"""
import random

import aiohttp
import discord
from discord.ext import commands

import config


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="logpose")
    async def logpose(self, ctx: commands.Context):
        """Spin the Log Pose for a random bit of Grand Line intel."""
        async with ctx.typing():
            embed = await self._fetch_random_intel()

        if embed is None:
            await ctx.send(
                "\U0001F9ED The Log Pose spins wildly... the Grand Line's currents are "
                "too strong right now. Try again in a moment."
            )
            return

        await ctx.send(embed=embed)

    async def _fetch_random_intel(self) -> discord.Embed | None:
        """Picks either a random character or a random Devil Fruit from the
        live One Piece API and formats it as a Discord embed. Returns None
        on any network/parsing failure so the caller can show a friendly
        in-character error instead of crashing."""
        category = random.choice(["character", "fruit"])
        endpoint = "characters" if category == "character" else "fruits"
        url = f"{config.ONE_PIECE_API_BASE}/{endpoint}/en"

        try:
            timeout = aiohttp.ClientTimeout(total=config.ONE_PIECE_API_TIMEOUT_SECONDS)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return None
                    data = await response.json()
        except Exception:
            return None

        if not data:
            return None

        if category == "character":
            return self._build_character_embed(data)
        return self._build_fruit_embed(data)

    @staticmethod
    def _build_character_embed(characters: list) -> discord.Embed:
        # prefer characters that actually have a bounty on file, for a
        # more interesting pull, but fall back to the full list if none do
        with_bounty = [c for c in characters if c.get("bounty")]
        char = random.choice(with_bounty or characters)

        embed = discord.Embed(
            title=f"\U0001F9ED Log Pose Intel: {char.get('name', 'Unknown Pirate')}",
            color=discord.Color.teal(),
        )
        if char.get("bounty"):
            embed.add_field(name="Bounty", value=f"{char['bounty']} berries", inline=True)
        if char.get("job"):
            embed.add_field(name="Role", value=char["job"], inline=True)

        crew = char.get("crew")
        if crew and crew.get("name"):
            embed.add_field(name="Crew", value=crew["name"], inline=True)

        fruit = char.get("fruit")
        if fruit and fruit.get("name"):
            embed.add_field(name="Devil Fruit", value=fruit["name"], inline=False)

        return embed

    @staticmethod
    def _build_fruit_embed(fruits: list) -> discord.Embed:
        with_description = [f for f in fruits if f.get("description")]
        fruit = random.choice(with_description or fruits)

        embed = discord.Embed(
            title=f"\U0001F9ED Log Pose Intel: {fruit.get('name', 'Unknown Devil Fruit')}",
            color=discord.Color.dark_teal(),
        )
        if fruit.get("type"):
            embed.add_field(name="Type", value=fruit["type"], inline=True)
        if fruit.get("roman_name"):
            embed.add_field(name="Japanese Name", value=fruit["roman_name"], inline=True)

        description = fruit.get("description") or "No further intel available."
        if len(description) > 500:
            description = description[:497] + "..."
        embed.add_field(name="Power", value=description, inline=False)

        return embed


async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))
