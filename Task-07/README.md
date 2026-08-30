# Task 07: Dank Memer-style Discord Bot — The Berry Broker 🏴‍☠️

A Discord bot that runs a fake in-server pirate economy: every server
member is a nameless rookie pirate who earns, trades, gambles, and
raids Berries off each other, climbing the Worst Generation leaderboard.

## File Structure

```
Task-07/
├── bot.py              # Entry point: wires everything together, starts the bot
├── config.py           # All tunable constants (odds, cooldowns, prices, token)
├── database.py         # The ONLY file that touches SQLite — schema + all queries
├── cogs/
│   ├── economy.py      # !bounty !setsail !trade !deposit !withdraw !raid !worstgeneration
│   ├── shop.py         # !shop !buy !inventory
│   └── fun.py          # !logpose (live One Piece API)
├── requirements.txt
├── .env.example
└── .gitignore
```

### Why organized this way

- **`bot.py` stays thin.** Its only job is intents, loading cogs, and one
  shared error handler. It never contains command logic, so adding a new
  command category later means writing a new cog and adding one
  `load_extension` line — not editing a growing single file.
- **`database.py` is the only file that writes SQL.** Every cog calls a
  named function (`adjust_wallet`, `get_active_item_by_effect`, etc.)
  instead of running its own queries. This means the schema can change
  in one place without hunting through three cogs for scattered SQL,
  and it's the natural place to look when debugging any data bug.
- **`config.py` separates numbers from logic.** Raid odds, daily claim
  ranges, and cooldowns are all constants in one file, so balancing the
  economy (or reusing this bot for a different server's taste) doesn't
  require touching command code at all.
- **Cogs are split by *feature domain*, not by command count.** `economy.py`
  owns anything that moves Berries between users or the bank.
  `shop.py` owns the item catalog and ownership. `fun.py` is isolated
  specifically because it's the only file that talks to the network
  (the One Piece API) instead of the database — if that API ever
  changes or goes down, the blast radius is contained to one file that
  doesn't touch money at all.

## Database Schema

Three tables, deliberately:

```
users
  user_id     INTEGER PRIMARY KEY   -- Discord user ID
  username    TEXT
  wallet      INTEGER               -- spendable AND raidable
  bank        INTEGER               -- safe from raids entirely
  last_daily  TEXT                  -- ISO timestamp, for the !setsail cooldown
  last_raid   TEXT                  -- ISO timestamp, for the !raid cooldown

items
  item_id     INTEGER PRIMARY KEY
  name        TEXT UNIQUE
  description TEXT
  price       INTEGER
  effect_type TEXT                  -- 'shield' | 'raid_boost' | 'cosmetic'

inventory
  inventory_id INTEGER PRIMARY KEY
  user_id      INTEGER  -> users.user_id
  item_id      INTEGER  -> items.item_id
  active       INTEGER               -- 1 = still in effect, 0 = already used
  acquired_at  TEXT
```

**Why the wallet/bank split matters:** without two pools, `!raid` would
just be "steal from a single number," and there'd be no reason for a
shield item, a bank, or strategy to exist at all. `wallet` is what's "on
your person" — tradeable, spendable, and the *only* thing a raid can
ever touch. `bank` is berries you've deliberately stashed away (via
`!deposit`) that raids can never reach. `!withdraw` moves it back out
when you want to spend it.

**Why `items` and `inventory` are separate tables:** `items` is static
catalog data — it barely changes once seeded. `inventory` is one row
*per purchase*, which is what lets a player own the same item twice
(two Reinforced Hulls, say), each tracked independently as active or
spent. Folding these into one table would mean either duplicating the
item's name/price/description on every single purchase row, or losing
the ability to track per-copy active/spent state — this design avoids
both.

## Features

| Command | What it does |
|---|---|
| `!bounty [@user]` | Shows wallet, bank, and total Berries |
| `!setsail` | Claims daily Berries (100–400, 24h cooldown) |
| `!trade @user <amt>` | Wallet-to-wallet transfer between pirates |
| `!deposit <amt>` | Wallet → bank (protects it from raids) |
| `!withdraw <amt>` | Bank → wallet |
| `!raid @user` | Chance-based wallet theft, with cooldown, shields, and boosts |
| `!shop` | Lists items for sale |
| `!buy <item>` | Purchases an item, deducts Berries, records ownership |
| `!inventory [@user]` | Shows owned items and whether they're active or spent |
| `!worstgeneration` | Top 5 richest pirates (wallet + bank) |
| `!logpose` | Random character or Devil Fruit intel from a live One Piece API |

`!deposit` / `!withdraw` weren't in the original feature list, but I
added them deliberately — without some way to move Berries into the
bank, the wallet/bank split the task calls for would have no purpose at
all. This felt like the smallest, most natural addition to make that
schema decision actually mean something in play.

## Raid Mechanics

- 30-minute cooldown per raider
- 45% base success chance
- If the target owns an active **Reinforced Hull**, the raid is
  auto-blocked and the shield is consumed
- If the raider owns an active **Cutlass**, their success chance gets
  +20% (consumed on the attempt, win or lose)
- On success: steals 10–25% of the target's *wallet* (never the bank)
- On failure: the raider pays 10% of their own wallet to the target, as
  a caught-in-the-act penalty

## Setup & Run

```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env and paste your bot token in place of your_bot_token_here
python3 bot.py
```

The SQLite database file (`berry_broker.db`) is created automatically
on first run, tables and shop catalog included.

### Important — I could not run/test this bot directly

The sandbox this was built in has no Discord bot token and (unusually)
couldn't reach `pypi.org` for the `discord.py` package specifically, so
I was unable to actually launch the bot and click through the commands
live. What I *did* verify:
- Every Python file passes `python3 -m py_compile` with no syntax errors
- The entire `database.py` module — user creation, wallet/bank
  adjustments, the shop catalog seeding, buying an item, checking for
  and consuming an active shield, and the leaderboard query — tested
  standalone with real SQLite calls (no Discord dependency needed for
  that layer) and produced correct results
- The One Piece API endpoints used by `!logpose`
  (`api.api-onepiece.com/v2/characters/en` and `/fruits/en`) were
  fetched directly and confirmed to return real JSON in the shape the
  code expects

What's untested is the Discord-facing glue itself (intents, cog
loading, command parsing, embeds actually rendering). Please run it
against a real bot token and test each command yourself before treating
this as done — if something errors out, paste me the traceback and
I'll fix it.

## Concepts Learned

- **Cogs (discord.py's extension system)**: splitting commands into
  separate classes/files that get loaded into the bot at startup,
  instead of one giant file of `@bot.command()` decorators.
- **Designing a schema around what a mechanic needs, not just what a
  command asks for**: the task only lists commands, but implementing
  `!raid` meaningfully required deciding *what* a raid can and can't
  touch — which is what led to the wallet/bank split and the
  active/spent inventory flag.
- **SQLite foreign keys and joins**: `inventory` joining to `items` to
  answer "what does this owned item actually do" without duplicating
  item data per purchase.
- **Cooldown patterns**: storing a last-action ISO timestamp per user
  and comparing elapsed time against a `timedelta`, used identically
  for both `!setsail` and `!raid`.
- **Async HTTP inside a Discord bot**: using `aiohttp.ClientSession`
  inside a command so a live network call doesn't block the bot's
  event loop the way a synchronous `requests.get()` would.
- **Zero-sum economy design**: making `!raid`'s failure penalty go *to*
  the target (not just vanish) keeps the total Berries in the economy
  roughly conserved, which matters for a small server economy staying
  balanced over time.

## Resources Used

- [discord.py official documentation](https://discordpy.readthedocs.io/) —
  Cogs, `commands.Bot`, intents, embeds
- [Python `sqlite3` official docs](https://docs.python.org/3/library/sqlite3.html)
- [aiohttp documentation](https://docs.aiohttp.org/) — async HTTP client usage
- [One Piece API documentation](https://documentation.api-onepiece.com/en) —
  used for `!logpose` (base URL `https://api.api-onepiece.com/v2`)
- [python-dotenv documentation](https://pypi.org/project/python-dotenv/) —
  loading the bot token from a `.env` file instead of hardcoding it
