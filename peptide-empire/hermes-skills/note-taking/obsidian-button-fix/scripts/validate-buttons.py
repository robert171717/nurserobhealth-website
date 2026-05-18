#!/usr/bin/env python3
"""Validate all button blocks in an Obsidian vault.

Scans every .md file for ```button fenced blocks and checks:
  1. Required params present (name, type, action)
  2. No BREAKING invalid params (cursorAt, type template cursor)
  3. Template references exist for template-type buttons
  4. Folder references exist for template-type buttons
  5. Link targets exist for link-type buttons

Usage:
  python3 validate-buttons.py /path/to/vault
  python3 validate-buttons.py .            # current directory as vault
"""

import os
import re
import sys


def norm_sym(s):
    return s.lstrip("$").strip().upper()


def find_button_blocks(content):
    """Extract all ```button blocks and their line numbers."""
    blocks = []
    for m in re.finditer(r"```button\n(.*?)\n```", content, re.DOTALL):
        blocks.append((m.start(), m.group(1)))
    return blocks


def parse_params(block):
    """Extract key=value and key value params from a button block."""
    params = {}
    for line in block.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        # key=value style
        eq_match = re.match(r"(\w+)\s*=\s*(.+)", line)
        if eq_match:
            params[eq_match.group(1)] = eq_match.group(2).strip()
            continue
        # key value style (space-separated)
        space_match = re.match(r"(\w+)\s+(.+)", line)
        if space_match:
            params[space_match.group(1)] = space_match.group(2).strip()
    return params


def validate_vault(vault_path):
    issues = []
    stats = {"files": 0, "buttons": 0, "ok": 0, "broken": 0}

    for root, dirs, files in os.walk(vault_path):
        # Skip obsidian internals
        if ".obsidian" in root or ".trash" in root:
            continue
        for fname in files:
            if not fname.endswith(".md"):
                continue

            path = os.path.join(root, fname)
            rel_path = os.path.relpath(path, vault_path)
            stats["files"] += 1

            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()

            for offset, block in find_button_blocks(content):
                stats["buttons"] += 1
                params = parse_params(block)
                name = params.get("name", "UNNAMED")
                btype = params.get("type", "")

                # Check 1: required params
                if "name" not in params:
                    issues.append(f"{rel_path}: MISSING 'name' in button")
                if "type" not in params:
                    issues.append(f"{rel_path}: MISSING 'type' in button '{name}'")
                    stats["broken"] += 1
                    continue
                if "action" not in params:
                    issues.append(
                        f"{rel_path}: MISSING 'action' in button '{name}'"
                    )
                    stats["broken"] += 1
                    continue

                # Check 2: BREAKING invalid params
                broken = False
                if "cursorAt" in block:
                    issues.append(
                        f"{rel_path}: 🔴 BREAKING 'cursorAt' param in button '{name}' — "
                        f"corrupts YAML-like parser, button won't render"
                    )
                    broken = True
                if "type template cursor" in block:
                    issues.append(
                        f"{rel_path}: 🔴 BREAKING 'type template cursor' in button '{name}' — "
                        f"not a valid type, button won't render"
                    )
                    broken = True

                if broken:
                    stats["broken"] += 1
                    continue

                # Check 3: template-type buttons — validate template and folder
                if btype.startswith("template") or btype.startswith("templater"):
                    action = params.get("action", "")
                    folder = params.get("folder")

                    # Validate template exists
                    tmpl_path = os.path.join(vault_path, "Templates", action + ".md")
                    if not os.path.exists(tmpl_path):
                        issues.append(
                            f"{rel_path}: MISSING template '{action}.md' for button '{name}'"
                        )
                        broken = True

                    # Validate folder exists
                    if folder:
                        folder_path = os.path.join(vault_path, folder)
                        if not os.path.isdir(folder_path):
                            issues.append(
                                f"{rel_path}: MISSING folder '{folder}' for button '{name}'"
                            )
                            broken = True

                # Check 4: link-type buttons — validate targets
                if btype == "link":
                    action = params.get("action", "")
                    # Skip obsidian:// URIs (can't easily validate)
                    if action.startswith("obsidian://"):
                        pass
                    elif action.endswith(".md"):
                        link_path = os.path.join(vault_path, action)
                        if not os.path.exists(link_path):
                            issues.append(
                                f"{rel_path}: MISSING link target '{action}' for button '{name}'"
                            )
                            broken = True
                    else:
                        # Try with .md extension
                        link_path = os.path.join(vault_path, action + ".md")
                        if not os.path.exists(link_path):
                            issues.append(
                                f"{rel_path}: POSSIBLY MISSING link target '{action}' "
                                f"for button '{name}' (no .md found)"
                            )

                if broken:
                    stats["broken"] += 1
                else:
                    stats["ok"] += 1

    return issues, stats


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate-buttons.py /path/to/vault")
        sys.exit(1)

    vault_path = sys.argv[1]
    if not os.path.isdir(vault_path):
        print(f"Error: '{vault_path}' is not a directory")
        sys.exit(1)

    print(f"🔍 Scanning vault: {vault_path}")
    issues, stats = validate_vault(vault_path)

    print(f"\n📊 Scanned {stats['files']} files, {stats['buttons']} buttons")
    print(f"   ✅ {stats['ok']} OK  |  🔴 {stats['broken']} broken")

    if issues:
        print(f"\n🔴 {len(issues)} issue(s) found:\n")
        for i in issues:
            print(f"  {i}")
        print(f"\n❌ VALIDATION FAILED — {len(issues)} issue(s)")
        sys.exit(1)
    else:
        print("\n✅ All buttons valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
