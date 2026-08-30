"""
database.py

All SQLite access for the Berry Broker lives here, and nowhere else.
No cog ever writes raw SQL directly — each cog calls a function from
this module. That keeps the schema and query logic in one auditable
place, and means the table design can change without touching command
code.

Schema
------
users
    One row per Discord member who has interacted with the bot.
    Berries are split into two pools on purpose:
      - wallet: spendable, tradeable, and the ONLY pool a raid can steal
                from. This is what's "on your person" as you walk the
                docks.
      - bank:   safe from raids entirely. Money you've deposited into
                the Broker's vault. Doesn't get gambled or raided away.
    This split is what makes !raid and the shop's shield item mean
    anything - without it, raiding would just be "steal from a single
    number", and there'd be no reason to ever move berries around.

items
    The shop catalog. Static reference data: what exists to buy, at
    what price, and what its effect_type is. This table rarely
    changes at runtime (it's seeded once); it's what !shop reads from.

inventory
    One row per item a user has purchased. This is what !inventory and
    !buy write to, and what !raid reads to check for an active shield.
    `active = 1` means unused/still in effect; `active = 0` means the
    item has already been consumed (a shield that blocked a raid, a
    cutlass that was used on a raid attempt). Splitting inventory from
    items means a user can own the same item more than once (e.g. two
    Reinforced Hulls), each tracked as its own row with its own
    active/spent state.
"""
import sqlite3
from datetime import datetime, timezone

from config import DB_PATH, STARTING_WALLET, STARTING_BANK

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id     INTEGER PRIMARY KEY,
    username    TEXT NOT NULL,
    wallet      INTEGER NOT NULL DEFAULT 0,
    bank        INTEGER NOT NULL DEFAULT 0,
    last_daily  TEXT,
    last_raid   TEXT
);

CREATE TABLE IF NOT EXISTS items (
    item_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    price       INTEGER NOT NULL,
    effect_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    item_id      INTEGER NOT NULL,
    active       INTEGER NOT NULL DEFAULT 1,
    acquired_at  TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (item_id) REFERENCES items (item_id)
);
"""

# Seeded once, if the items table is empty. (name, description, price, effect_type)
SHOP_CATALOG = [
    (
        "Reinforced Hull",
        "Blocks the next raid attempt against you, then breaks. Passive until triggered.",
        500,
        "shield",
    ),
    (
        "Cutlass",
        "Sharpens your next raid attempt, boosting your success chance. Consumed on use.",
        300,
        "raid_boost",
    ),
    (
        "Den Den Mushi",
        "A loyal snail companion. Pure flex - shows up in your inventory forever.",
        150,
        "cosmetic",
    ),
    (
        "Wanted Poster",
        "A poster of your own bounty, framed. Another flex item with no mechanical effect.",
        250,
        "cosmetic",
    ),
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    """Create tables if they don't exist yet, and seed the shop catalog."""
    conn = get_connection()
    try:
        conn.executescript(SCHEMA)
        conn.commit()

        existing = conn.execute("SELECT COUNT(*) AS c FROM items").fetchone()["c"]
        if existing == 0:
            conn.executemany(
                "INSERT INTO items (name, description, price, effect_type) "
                "VALUES (?, ?, ?, ?)",
                SHOP_CATALOG,
            )
            conn.commit()
    finally:
        conn.close()


def get_or_create_user(user_id: int, username: str) -> sqlite3.Row:
    """Fetch a user's row, creating a rookie entry with the starting
    stash if this is their first time interacting with the bot."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        if row is None:
            conn.execute(
                "INSERT INTO users (user_id, username, wallet, bank) "
                "VALUES (?, ?, ?, ?)",
                (user_id, username, STARTING_WALLET, STARTING_BANK),
            )
            conn.commit()
            row = conn.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            ).fetchone()
        else:
            # keep the stored username fresh in case they changed it
            if row["username"] != username:
                conn.execute(
                    "UPDATE users SET username = ? WHERE user_id = ?",
                    (username, user_id),
                )
                conn.commit()
        return row
    finally:
        conn.close()


def get_balance(user_id: int) -> tuple[int, int]:
    """Returns (wallet, bank) for a user. Assumes the user already exists."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT wallet, bank FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return (row["wallet"], row["bank"])
    finally:
        conn.close()


def adjust_wallet(user_id: int, delta: int) -> int:
    """Adds delta (can be negative) to a user's wallet. Returns new balance."""
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE users SET wallet = wallet + ? WHERE user_id = ?",
            (delta, user_id),
        )
        conn.commit()
        row = conn.execute(
            "SELECT wallet FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return row["wallet"]
    finally:
        conn.close()


def adjust_bank(user_id: int, delta: int) -> int:
    """Adds delta (can be negative) to a user's bank. Returns new balance."""
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE users SET bank = bank + ? WHERE user_id = ?",
            (delta, user_id),
        )
        conn.commit()
        row = conn.execute(
            "SELECT bank FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return row["bank"]
    finally:
        conn.close()


def get_last_daily(user_id: int) -> str | None:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT last_daily FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return row["last_daily"]
    finally:
        conn.close()


def set_last_daily(user_id: int) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE users SET last_daily = ? WHERE user_id = ?",
            (_now(), user_id),
        )
        conn.commit()
    finally:
        conn.close()


def get_last_raid(user_id: int) -> str | None:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT last_raid FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return row["last_raid"]
    finally:
        conn.close()


def set_last_raid(user_id: int) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE users SET last_raid = ? WHERE user_id = ?",
            (_now(), user_id),
        )
        conn.commit()
    finally:
        conn.close()


def get_shop_items() -> list[sqlite3.Row]:
    conn = get_connection()
    try:
        return conn.execute(
            "SELECT * FROM items ORDER BY price ASC"
        ).fetchall()
    finally:
        conn.close()


def get_item_by_name(name: str) -> sqlite3.Row | None:
    conn = get_connection()
    try:
        return conn.execute(
            "SELECT * FROM items WHERE LOWER(name) = LOWER(?)", (name,)
        ).fetchone()
    finally:
        conn.close()


def add_inventory_item(user_id: int, item_id: int) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO inventory (user_id, item_id, active, acquired_at) "
            "VALUES (?, ?, 1, ?)",
            (user_id, item_id, _now()),
        )
        conn.commit()
    finally:
        conn.close()


def get_inventory(user_id: int) -> list[sqlite3.Row]:
    """Returns each owned item joined with its name/description/effect,
    including whether it's still active or already spent."""
    conn = get_connection()
    try:
        return conn.execute(
            """
            SELECT inv.inventory_id, inv.active, inv.acquired_at,
                   it.name, it.description, it.effect_type
            FROM inventory inv
            JOIN items it ON it.item_id = inv.item_id
            WHERE inv.user_id = ?
            ORDER BY inv.acquired_at DESC
            """,
            (user_id,),
        ).fetchall()
    finally:
        conn.close()


def get_active_item_by_effect(user_id: int, effect_type: str) -> sqlite3.Row | None:
    """Finds the oldest still-active inventory row for a user matching a
    given effect_type (e.g. 'shield' or 'raid_boost'). Used by !raid to
    check for a defensive shield or an offensive boost."""
    conn = get_connection()
    try:
        return conn.execute(
            """
            SELECT inv.inventory_id, it.name, it.effect_type
            FROM inventory inv
            JOIN items it ON it.item_id = inv.item_id
            WHERE inv.user_id = ? AND inv.active = 1 AND it.effect_type = ?
            ORDER BY inv.acquired_at ASC
            LIMIT 1
            """,
            (user_id, effect_type),
        ).fetchone()
    finally:
        conn.close()


def mark_inventory_spent(inventory_id: int) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE inventory SET active = 0 WHERE inventory_id = ?",
            (inventory_id,),
        )
        conn.commit()
    finally:
        conn.close()


def get_top_users(limit: int = 5) -> list[sqlite3.Row]:
    """Top pirates by total net worth (wallet + bank combined)."""
    conn = get_connection()
    try:
        return conn.execute(
            """
            SELECT user_id, username, wallet, bank, (wallet + bank) AS total
            FROM users
            ORDER BY total DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    finally:
        conn.close()
