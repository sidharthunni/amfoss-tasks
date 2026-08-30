"""
cogs/shop.py

Everything related to the shop catalog and what a pirate owns:
browsing what's for sale, buying it, and checking your inventory.
"""
import discord
from discord.ext import commands

import database as db


class Shop(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="shop")
    async def shop(self, ctx: commands.Context):
        """Browse items available for purchase."""
        items = db.get_shop_items()

        embed = discord.Embed(
            title="\U0001F3EA The Berry Broker's Shop",
            description=f"Buy with `{ctx.prefix}buy <item name>`",
            color=discord.Color.blue(),
        )
        for item in items:
            embed.add_field(
                name=f"{item['name']} \u2014 {item['price']} berries",
                value=item["description"],
                inline=False,
            )
        await ctx.send(embed=embed)

    @commands.command(name="buy")
    async def buy(self, ctx: commands.Context, *, item_name: str):
        """Spend Berries to buy an item from the shop."""
        user_id = ctx.author.id
        db.get_or_create_user(user_id, str(ctx.author))

        item = db.get_item_by_name(item_name)
        if item is None:
            await ctx.send(
                f"No item called '{item_name}' in the shop. Check `{ctx.prefix}shop` for the list."
            )
            return

        wallet, _ = db.get_balance(user_id)
        if wallet < item["price"]:
            await ctx.send(
                f"You need {item['price']} berries for {item['name']}, "
                f"but your wallet only has {wallet}."
            )
            return

        db.adjust_wallet(user_id, -item["price"])
        db.add_inventory_item(user_id, item["item_id"])
        await ctx.send(
            f"\U0001F6D2 {ctx.author.mention} bought a **{item['name']}** for {item['price']} berries!"
        )

    @commands.command(name="inventory")
    async def inventory(self, ctx: commands.Context, member: discord.Member = None):
        """View items you (or another pirate) currently own, active or spent."""
        target = member or ctx.author
        db.get_or_create_user(target.id, str(target))

        items = db.get_inventory(target.id)
        if not items:
            await ctx.send(
                f"{target.display_name} doesn't own any items yet. Check `{ctx.prefix}shop` to browse!"
            )
            return

        lines = []
        for row in items:
            status = "\U0001F7E2 Active" if row["active"] else "\u26AB Spent"
            lines.append(f"**{row['name']}** \u2014 {status}")

        embed = discord.Embed(
            title=f"{target.display_name}'s Inventory",
            description="\n".join(lines),
            color=discord.Color.purple(),
        )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Shop(bot))
