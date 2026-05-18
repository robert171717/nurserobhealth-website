#!/usr/bin/env python3
"""Scan Discord channel for peptide-related messages within a time window.
Used by lead_sniper cron job. Requires discord.py in the Hermes venv.
Usage: /home/robert/.hermes/hermes-agent/venv/bin/python discord_scan.py
       Or set DISCORD_TOKEN env var, CHANNEL_ID, SCAN_HOURS_BACK
"""
import os
import json
import sys
from datetime import datetime, timezone, timedelta

# --- CONFIG ---
TOKEN = os.environ.get("DISCORD_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "1484946244768895056"))
SCAN_HOURS_BACK = int(os.environ.get("SCAN_HOURS_BACK", "6"))

PEPTIDE_KEYWORDS = [
    "peptide", "bpc-157", "bpc157", "tb-500", "tb500", "nad+", "nad",
    "semaglutide", "tirzepatide", "cjc", "ipamorelin", "ghk-cu", "ghkcu",
    "wolverine stack", "dose", "dosage", "inject", "injection",
    "heal", "healing", "recovery", "injury", "biohack", "biohacking",
    "longevity", "anti-aging", "muscle", "weight loss", "fat loss",
    "hgh", "growth hormone", "source", "where to buy", "vendor",
    "side effect", "compound", "compounding", "research chem",
    "stack", "cycle", "pinning", "subq", "subcutaneous"
]

SCAN_SINCE = datetime.now(timezone.utc) - timedelta(hours=SCAN_HOURS_BACK)

def match_peptide(text: str) -> list[str]:
    """Return list of matching keywords found in text."""
    text_lower = text.lower()
    return [kw for kw in PEPTIDE_KEYWORDS if kw in text_lower]


import discord

class Scanner(discord.Client):
    async def on_ready(self):
        print(f"Connected as {self.user}", file=sys.stderr)
        channel = self.get_channel(CHANNEL_ID)
        if not channel:
            print(f"ERROR: Channel {CHANNEL_ID} not found", file=sys.stderr)
            await self.close()
            return

        print(f"Scanning #{channel.name} in {channel.guild.name} "
              f"(since {SCAN_SINCE.isoformat()})", file=sys.stderr)

        results = []
        total_scanned = 0
        bot_user_id = self.user.id  # Exclude bot's own messages from scan
        skipped_self = 0
        try:
            async for message in channel.history(after=SCAN_SINCE, limit=200):
                total_scanned += 1
                if message.author.id == bot_user_id:
                    skipped_self += 1
                    continue  # Don't self-match on keywords in own cron job posts
                matches = match_peptide(message.content)
                if matches:
                    is_mention = any(
                        name in message.content.lower()
                        for name in ("nurse rob", "realsolanameme")
                    )
                    results.append({
                        "author": str(message.author),
                        "author_id": message.author.id,
                        "content": message.content[:500],
                        "timestamp": message.created_at.isoformat(),
                        "matches": matches[:5],
                        "is_mention": is_mention,
                        "message_id": message.id,
                    })
        except Exception as e:
            print(f"Error reading history: {e}", file=sys.stderr)

        print(f"Scanned {total_scanned} messages ({skipped_self} bot self-messages filtered), {len(results)} matches", file=sys.stderr)
        print(json.dumps(results, indent=2))
        await self.close()


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    client = Scanner(intents=intents)
    client.run(TOKEN)
