"""
bot.py

The entry point. This file's only job is to wire things together:
configure intents, create the Bot, load each cog as an extension, set
up one shared error handler, and start the connection to Discord.

No command logic lives here - that's what cogs/economy.py, cogs/shop.py
and cogs/fun.py are for. Keeping this file thin means adding a new
command category later is just "write a new cog, add one load_extension
line" rather than editing a growing monolith.
"""
import asyncio

import discord
from discord.ext import commands

import config
import database as db

intents = discord.Intents.default()
intents.message_content = True  # required to read command text in prefix commands

bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f"\u2693 The Berry Broker is open for business as {bot.user} (id: {bot.user.id})")


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    """One shared handler for common mistakes, so every command doesn't
    need its own try/except for bad input."""
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            f"Missing something there, pirate. Usage: `{ctx.prefix}{ctx.command} {ctx.command.signature}`"
        )
        return
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("Couldn't find that pirate on this server.")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send("That doesn't look right \u2014 double check the person or amount you gave me.")
        return

    print(f"Unhandled error in command '{ctx.command}': {error!r}")
    await ctx.send("Something went wrong on the Broker's end. Try again in a moment.")


async def main():
    db.init_db()
    async with bot:
        await bot.load_extension("cogs.economy")
        await bot.load_extension("cogs.shop")
        await bot.load_extension("cogs.fun")
        await bot.start(config.DISCORD_TOKEN)


if __name__ == "__main__":
    if not config.DISCORD_TOKEN:
        raise SystemExit(
            "DISCORD_TOKEN is not set. Copy .env.example to .env and add your bot token."
        )
    asyncio.run(main())
