#!/usr/bin/env python3
"""Self-contained Discord scan for lead_sniper — reads token from config.yaml.

No env var needed. Eliminates the agent token-hallucination risk of manually
copying the token from config.yaml into a terminal command.

Usage:
    /home/robert/.hermes/hermes-agent/venv/bin/python /tmp/discord_scan_selfcontained.py
"""
import json, sys, yaml
from datetime import datetime, timezone, timedelta

# --- Read token from config.yaml (no manual copy-paste needed) ---
with open('/home/robert/.hermes/config.yaml') as f:
    config = yaml.safe_load(f)
TOKEN = config['discord']['token']  # May 2026: verified at line ~335 under `discord:` key

CHANNEL_ID = 1484946244768895056
SCAN_HOURS_BACK = 6

PEPTIDE_KEYWORDS = [
    "peptide", "bpc-157", "bpc157", "tb-500", "tb500", "nad+", "nad",
    "semaglutide", "tirzepatide", "cjc", "ipamorelin", "ghk-cu", "ghkcu",
    "wolverine stack", "dose", "dosage", "inject", "injection",
    "heal", "healing", "recovery", "injury", "biohack", "biohacking",
    "longevity", "anti-aging", "muscle", "weight loss", "fat loss",
    "hgh", "growth hormone", "source", "where to buy", "vendor",
    "side effect", "compound", "compounding", "research chem",
    "stack", "cycle", "pinning", "subq", "subcutaneous",
]

SCAN_SINCE = datetime.now(timezone.utc) - timedelta(hours=SCAN_HOURS_BACK)


def match_peptide(text: str) -> list[str]:
    text_lower = text.lower()
    return [kw for kw in PEPTIDE_KEYWORDS if kw in text_lower]


import discord


class Scanner(discord.Client):
    async def on_ready(self):
        print(json.dumps({"status": "connected", "user": str(self.user)}), file=sys.stderr)
        channel = self.get_channel(CHANNEL_ID)
        if not channel:
            print(json.dumps({"error": f"Channel {CHANNEL_ID} not found"}), file=sys.stderr)
            await self.close()
            return
        print(json.dumps({"info": f"Scanning #{channel.name} in {channel.guild.name}"}), file=sys.stderr)
        results = []
        total = 0
        skipped = 0
        try:
            async for msg in channel.history(after=SCAN_SINCE, limit=200):
                total += 1
                # Skip bot's own messages (cron notifications flood keywords like "recovery", "heal")
                if msg.author.id == self.user.id:
                    skipped += 1
                    continue
                matches = match_peptide(msg.content)
                if matches:
                    is_mention = any(
                        n in msg.content.lower()
                        for n in ("nurse rob", "realsolanameme")
                    )
                    results.append({
                        "author": str(msg.author),
                        "author_id": msg.author.id,
                        "content": msg.content[:500],
                        "timestamp": msg.created_at.isoformat(),
                        "matches": matches[:5],
                        "is_mention": is_mention,
                        "msg_id": msg.id,
                    })
        except Exception as e:
            print(json.dumps({"error": str(e)}), file=sys.stderr)
        print(json.dumps({"scanned": total, "skipped_self": skipped, "matches": len(results)}), file=sys.stderr)
        print(json.dumps(results, indent=2))
        await self.close()


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    client = Scanner(intents=intents)
    client.run(TOKEN)
