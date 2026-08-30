"""
config.py

All the tunable numbers for the Berry Broker's economy live here in one
place, instead of scattered as magic numbers through the command files.
This makes balancing the economy (or reusing the bot for a different
server) a one-file change.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- Discord ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = "!"

# --- Database ---
DB_PATH = "berry_broker.db"

# --- Starting stash for a brand new rookie ---
STARTING_WALLET = 500
STARTING_BANK = 0

# --- !setsail (daily claim) ---
DAILY_MIN = 100
DAILY_MAX = 400
DAILY_COOLDOWN_HOURS = 24

# --- !raid ---
RAID_COOLDOWN_MINUTES = 30
RAID_BASE_SUCCESS_CHANCE = 0.45     # 45% base chance, before item bonuses
RAID_CUTLASS_BONUS = 0.20           # +20% chance if raider has an active Cutlass
RAID_STEAL_MIN_PCT = 0.10           # steal between 10%...
RAID_STEAL_MAX_PCT = 0.25           # ...and 25% of the target's wallet
RAID_FAIL_PENALTY_PCT = 0.10        # on failure, raider pays 10% of their
                                     # own wallet to the target as compensation

# --- One Piece API (for !logpose) ---
ONE_PIECE_API_BASE = "https://api.api-onepiece.com/v2"
ONE_PIECE_API_TIMEOUT_SECONDS = 8
