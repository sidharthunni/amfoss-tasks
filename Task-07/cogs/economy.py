"""
cogs/economy.py

The core money commands: checking your bounty, claiming daily berries,
trading with other pirates, moving berries between wallet and bank, and
raiding a rival's stash.

Every command here follows the same shape: make sure the user(s) exist
in the database, read what's needed, validate, then write. All actual
persistence goes through the `database` module - this file never touches
SQL directly.
"""
import random
from datetime import datetime, timezone, timedelta

import discord
from discord.ext import commands

import config
import database as db


class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="bounty")
    async def bounty(self, ctx: commands.Context, member: discord.Member = None):
        """Check your (or another pirate's) current Berry bounty."""
        target = member or ctx.author
        db.get_or_create_user(target.id, str(target))
        wallet, bank = db.get_balance(target.id)

        embed = discord.Embed(
            title=f"{target.display_name}'s Bounty",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Wallet", value=f"{wallet} berries", inline=True)
        embed.add_field(name="Bank", value=f"{bank} berries", inline=True)
        embed.add_field(name="Total", value=f"{wallet + bank} berries", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="setsail")
    async def setsail(self, ctx: commands.Context):
        """Claim your daily Berries, like raiding a merchant ship at dawn."""
        user_id = ctx.author.id
        db.get_or_create_user(user_id, str(ctx.author))

        last = db.get_last_daily(user_id)
        now = datetime.now(timezone.utc)
        cooldown = timedelta(hours=config.DAILY_COOLDOWN_HOURS)

        if last:
            elapsed = now - datetime.fromisoformat(last)
            if elapsed < cooldown:
                remaining = cooldown - elapsed
                hours, rem = divmod(int(remaining.total_seconds()), 3600)
                minutes = rem // 60
                await ctx.send(
                    f"\u2693 {ctx.author.mention}, your crew already set sail today. "
                    f"Next voyage in {hours}h {minutes}m."
                )
                return

        amount = random.randint(config.DAILY_MIN, config.DAILY_MAX)
        db.adjust_wallet(user_id, amount)
        db.set_last_daily(user_id)
        await ctx.send(
            f"\U0001F3F4\u200D\u2620\uFE0F {ctx.author.mention} raided a merchant ship at dawn "
            f"and earned **{amount}** berries!"
        )

    @commands.command(name="trade")
    async def trade(self, ctx: commands.Context, member: discord.Member, amount: int):
        """Transfer Berries from your wallet to another pirate's wallet."""
        if member.id == ctx.author.id:
            await ctx.send("You can't trade berries with yourself.")
            return
        if member.bot:
            await ctx.send("You can't trade berries with a bot.")
            return
        if amount <= 0:
            await ctx.send("You need to trade a positive amount of berries.")
            return

        db.get_or_create_user(ctx.author.id, str(ctx.author))
        db.get_or_create_user(member.id, str(member))

        wallet, _ = db.get_balance(ctx.author.id)
        if wallet < amount:
            await ctx.send(
                f"You only have {wallet} berries in your wallet - not enough to trade {amount}."
            )
            return

        db.adjust_wallet(ctx.author.id, -amount)
        db.adjust_wallet(member.id, amount)
        await ctx.send(
            f"\U0001F4B0 {ctx.author.mention} traded **{amount}** berries to {member.mention}."
        )

    @commands.command(name="deposit")
    async def deposit(self, ctx: commands.Context, amount: int):
        """Move Berries from your wallet into the safety of the bank (raid-proof)."""
        user_id = ctx.author.id
        db.get_or_create_user(user_id, str(ctx.author))

        if amount <= 0:
            await ctx.send("Deposit amount must be positive.")
            return

        wallet, _ = db.get_balance(user_id)
        if wallet < amount:
            await ctx.send(f"You only have {wallet} berries in your wallet.")
            return

        db.adjust_wallet(user_id, -amount)
        db.adjust_bank(user_id, amount)
        await ctx.send(
            f"\U0001F3E6 {ctx.author.mention} stashed **{amount}** berries safely in the bank."
        )

    @commands.command(name="withdraw")
    async def withdraw(self, ctx: commands.Context, amount: int):
        """Move Berries from the bank back into your (raidable) wallet."""
        user_id = ctx.author.id
        db.get_or_create_user(user_id, str(ctx.author))

        if amount <= 0:
            await ctx.send("Withdraw amount must be positive.")
            return

        _, bank = db.get_balance(user_id)
        if bank < amount:
            await ctx.send(f"You only have {bank} berries in the bank.")
            return

        db.adjust_bank(user_id, -amount)
        db.adjust_wallet(user_id, amount)
        await ctx.send(
            f"\U0001F4B8 {ctx.author.mention} withdrew **{amount}** berries back to their wallet."
        )

    @commands.command(name="raid")
    async def raid(self, ctx: commands.Context, member: discord.Member):
        """Attempt to raid a rival's wallet. Chance-based, with a cooldown."""
        attacker_id = ctx.author.id
        target_id = member.id

        if target_id == attacker_id:
            await ctx.send("You can't raid your own crew.")
            return
        if member.bot:
            await ctx.send("You can't raid a bot's stash.")
            return

        db.get_or_create_user(attacker_id, str(ctx.author))
        db.get_or_create_user(target_id, str(member))

        last = db.get_last_raid(attacker_id)
        now = datetime.now(timezone.utc)
        cooldown = timedelta(minutes=config.RAID_COOLDOWN_MINUTES)

        if last:
            elapsed = now - datetime.fromisoformat(last)
            if elapsed < cooldown:
                remaining = cooldown - elapsed
                minutes = int(remaining.total_seconds() // 60) + 1
                await ctx.send(
                    f"\U0001F553 Your crew is still recovering. Try raiding again in "
                    f"{minutes} minute(s)."
                )
                return

        target_wallet, _ = db.get_balance(target_id)
        if target_wallet <= 0:
            db.set_last_raid(attacker_id)
            await ctx.send(f"{member.display_name}'s wallet is empty - nothing to raid.")
            return

        # A Reinforced Hull on the target auto-blocks the raid and is consumed.
        shield = db.get_active_item_by_effect(target_id, "shield")
        if shield:
            db.mark_inventory_spent(shield["inventory_id"])
            db.set_last_raid(attacker_id)
            await ctx.send(
                f"\U0001F6E1\uFE0F {member.mention}'s Reinforced Hull held strong! "
                f"The raid was repelled and their shield is now spent."
            )
            return

        # A Cutlass on the attacker boosts their success chance, then is consumed.
        success_chance = config.RAID_BASE_SUCCESS_CHANCE
        cutlass = db.get_active_item_by_effect(attacker_id, "raid_boost")
        if cutlass:
            success_chance += config.RAID_CUTLASS_BONUS
            db.mark_inventory_spent(cutlass["inventory_id"])

        db.set_last_raid(attacker_id)

        if random.random() < success_chance:
            pct = random.uniform(config.RAID_STEAL_MIN_PCT, config.RAID_STEAL_MAX_PCT)
            stolen = max(1, int(target_wallet * pct))
            db.adjust_wallet(target_id, -stolen)
            db.adjust_wallet(attacker_id, stolen)
            await ctx.send(
                f"\u2694\uFE0F {ctx.author.mention} raided {member.mention}'s stash and "
                f"made off with **{stolen}** berries!"
            )
        else:
            attacker_wallet, _ = db.get_balance(attacker_id)
            penalty = min(attacker_wallet, max(1, int(attacker_wallet * config.RAID_FAIL_PENALTY_PCT)))
            if penalty > 0:
                db.adjust_wallet(attacker_id, -penalty)
                db.adjust_wallet(target_id, penalty)
            await ctx.send(
                f"\U0001F6A8 {ctx.author.mention}'s raid on {member.mention} was caught! "
                f"They paid **{penalty}** berries in compensation."
            )

    @commands.command(name="worstgeneration")
    async def worstgeneration(self, ctx: commands.Context):
        """Show the top 5 richest pirates (wallet + bank combined)."""
        top = db.get_top_users(limit=5)
        if not top:
            await ctx.send("No pirates have made a name for themselves yet.")
            return

        medals = ["\U0001F947", "\U0001F948", "\U0001F949", "4\uFE0F\u20E3", "5\uFE0F\u20E3"]
        lines = [
            f"{medals[i]} **{row['username']}** - {row['total']} berries"
            for i, row in enumerate(top)
        ]

        embed = discord.Embed(
            title="\U0001F3F4\u200D\u2620\uFE0F Worst Generation \u2014 Richest Pirates",
            description="\n".join(lines),
            color=discord.Color.dark_gold(),
        )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
