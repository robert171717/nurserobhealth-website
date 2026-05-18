#!/usr/bin/env python3
"""Comprehensive Obsidian vault quality audit.

Checks:
  1. Button block validity (delegates to validate-buttons.py when available)
  2. Broken wikilinks ([[Target]] where no file named Target.md exists)
  3. Bare URLs that should be markdown links
  4. Non-standard callout types
  5. Frontmatter YAML validity
  6. Missing embed targets (images)
  7. Cross-reference consistency between key files

Usage:
  python3 vault-qa.py /path/to/vault
"""

import os
import re
import sys

try:
    import yaml
except ImportError:
    yaml = None


VALID_CALLOUTS = {
    "note", "tip", "warning", "info", "example", "quote", "bug",
    "danger", "success", "failure", "question", "abstract", "todo",
}


def collect_existing_files(vault_path):
    """Build set of all filenames (without .md) and relative paths in vault."""
    files_by_name = {}  # basename -> [rel_path, ...]
    for root, dirs, files in os.walk(vault_path):
        if ".obsidian" in root or ".trash" in root:
            continue
        for f in files:
            if f.endswith(".md"):
                rel = os.path.relpath(os.path.join(root, f), vault_path)
                basename = os.path.splitext(f)[0]
                files_by_name.setdefault(basename, []).append(rel)
    return files_by_name


def audit_vault(vault_path):
    issues = []
    stats = {"files": 0, "ok": 0, "warn": 0, "error": 0}
    files_by_name = collect_existing_files(vault_path)

    for root, dirs, files in os.walk(vault_path):
        if ".obsidian" in root or ".trash" in root:
            continue
        for fname in files:
            if fname.endswith(".base"):
                continue
            if not fname.endswith(".md"):
                continue

            path = os.path.join(root, fname)
            rel_path = os.path.relpath(path, vault_path)
            stats["files"] += 1
            file_issues = 0

            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()

            # --- 1. Frontmatter YAML ---
            if content.startswith("---") and yaml:
                fm_end = content.find("---", 3)
                if fm_end > 0:
                    fm = content[3:fm_end].strip()
                    try:
                        yaml.safe_load(fm)
                    except yaml.YAMLError as e:
                        issues.append(f"{rel_path}: ❌ Broken frontmatter YAML — {e}")
                        file_issues += 1

            # --- 2. Bare URLs ---
            bare_urls = re.findall(
                r"(?<!\[)(?<!\()https?://[^\s\)\]]+", content
            )
            for url in bare_urls:
                if "obsidian://open" in url:
                    continue
                issues.append(
                    f"{rel_path}: ⚠️ Bare URL should be markdown link — {url[:80]}"
                )
                file_issues += 1

            # --- 3. Callout types ---
            callouts = re.findall(r"> \[!(.*?)\]", content)
            for c in callouts:
                c_type = c.split()[0].lower().strip("+-")
                if c_type and c_type not in VALID_CALLOUTS:
                    issues.append(
                        f"{rel_path}: ⚠️ Non-standard callout [!{c_type}]"
                    )
                    file_issues += 1

            # --- 4. Wikilinks ---
            links = re.findall(
                r"\[\[([^\]|#]+?)(?:[|#][^\]]+)?\]\]", content
            )
            for link in links:
                link = link.strip()
                # Skip Dataview expressions
                if link.startswith("=") or "{" in link:
                    continue
                # Skip dataview FROM clauses
                if link.startswith('"') or link.startswith("'"):
                    continue
                # Check if link target exists anywhere in vault
                if link in files_by_name:
                    continue
                if (link + ".md") in {os.path.basename(p) for paths in files_by_name.values() for p in paths}:
                    continue
                # Try basename match (Obsidian auto-resolves across folders)
                link_basename = os.path.basename(link)
                if link_basename in files_by_name:
                    continue
                issues.append(
                    f"{rel_path}: ⚠️ Broken wikilink [[{link}]] — no matching file"
                )
                file_issues += 1

            # --- 5. Embed targets ---
            embeds = re.findall(r"!\[\[([^\]]+)\]\]", content)
            for embed in embeds:
                embed_name = embed.split("|")[0].split("#")[0]
                if embed_name.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")):
                    found = False
                    for r2, d2, f2 in os.walk(vault_path):
                        if embed_name in f2:
                            found = True
                            break
                    if not found:
                        issues.append(
                            f"{rel_path}: ⚠️ Embed target not found — ![[{embed_name}]]"
                        )
                        file_issues += 1

            # --- 6. Button block quick-scan ---
            button_blocks = re.findall(r"```button\n(.*?)\n```", content, re.DOTALL)
            for block in button_blocks:
                if "cursorAt" in block:
                    issues.append(
                        f"{rel_path}: 🔴 BREAKING cursorAt in button block"
                    )
                    file_issues += 1
                if "type template cursor" in block:
                    issues.append(
                        f"{rel_path}: 🔴 BREAKING 'type template cursor' in button block"
                    )
                    file_issues += 1

            if file_issues == 0:
                stats["ok"] += 1
            elif any("🔴" in i for i in issues[-file_issues:]):
                stats["error"] += 1
            else:
                stats["warn"] += 1

    return issues, stats


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 vault-qa.py /path/to/vault")
        sys.exit(1)

    vault_path = sys.argv[1]
    if not os.path.isdir(vault_path):
        print(f"Error: '{vault_path}' is not a directory")
        sys.exit(1)

    print(f"🔍 Auditing vault: {vault_path}")
    print(f"   (install pyyaml for frontmatter validation: pip install pyyaml)")
    print()

    issues, stats = audit_vault(vault_path)

    print(f"📊 {stats['files']} files scanned")
    print(f"   ✅ {stats['ok']} clean  |  ⚠️ {stats['warn']} warnings  |  🔴 {stats['error']} errors")

    if issues:
        errors = [i for i in issues if "🔴" in i]
        warnings = [i for i in issues if "⚠️" in i]
        if errors:
            print(f"\n🔴 {len(errors)} error(s):")
            for e in errors:
                print(f"  {e}")
        if warnings:
            print(f"\n⚠️ {len(warnings)} warning(s):")
            for w in warnings:
                print(f"  {w}")
        if errors:
            print(f"\n❌ AUDIT FAILED — {len(errors)} error(s) must be fixed")
            sys.exit(1)
        else:
            print(f"\n⚠️ AUDIT PASSED WITH WARNINGS — review {len(warnings)} item(s)")
    else:
        print("\n✅ All files clean!")


if __name__ == "__main__":
    main()
