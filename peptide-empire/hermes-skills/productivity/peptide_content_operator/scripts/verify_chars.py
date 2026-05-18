#!/usr/bin/env python3
"""Verify character counts for all tweets in a Nurse Rob content file.

Handles two post types (v2.5+, 2 posts/day):
  - Post 1 (Thread): Tweets separated by blank lines within code block.
  - Post 2 (Rotating): Poll, Short Form, Hot Take, Myth-Buster, or Q&A.

Backward-compatible with old 3-post files (Post 2 + Post 3).

Usage:
  python3 scripts/verify_chars.py /path/to/YYYY-MM-DD_posts.md
"""

import re
import sys

X_TWEET_LIMIT = 280
X_POLL_OPTION_LIMIT = 25


def verify_post1_thread(block: str) -> list[str]:
    """Verify thread tweets. Returns list of issues."""
    issues = []
    tweets = [t.strip() for t in block.strip().split('\n\n') if t.strip()]
    for j, tweet in enumerate(tweets):
        chars = len(tweet)
        if chars > X_TWEET_LIMIT:
            issues.append(
                f"  Tweet {j+1}: {chars} chars ⚠️ OVER {X_TWEET_LIMIT}! "
                f"(excess: {chars - X_TWEET_LIMIT})"
            )
        else:
            print(f"  Tweet {j+1}: {chars} chars ✓")

    # RN credential check on opener
    if tweets and 'RN' not in tweets[0] and 'nurse' not in tweets[0].lower():
        issues.append("  ⚠️ Thread opener missing RN credential!")
    return issues


def detect_post2_format(block: str) -> str:
    """Detect whether Post 2 is a poll, short-form, or other format."""
    lower = block.lower()
    if re.search(r'^[A-D]\) ', block, re.MULTILINE):
        return 'poll'
    if 'not medical advice' in lower and '\n\n' not in block.strip():
        return 'short_form'
    return 'general'


def verify_post2_poll(block: str) -> list[str]:
    """Verify poll post. Returns list of issues."""
    issues = []
    parts = block.strip().split('\n\n')

    body = parts[0].strip()
    options_text = parts[1].strip() if len(parts) > 1 else ""
    disclaimer = parts[2].strip() if len(parts) > 2 else ""

    # Combined tweet text
    combined = body
    if disclaimer:
        combined += '\n' + disclaimer
    chars = len(combined)
    if chars > X_TWEET_LIMIT:
        issues.append(
            f"  Tweet text: {chars} chars ⚠️ OVER {X_TWEET_LIMIT}! "
            f"(excess: {chars - X_TWEET_LIMIT})"
        )
    else:
        print(f"  Tweet text: {chars} chars ✓")

    # Poll options (25-char limit each)
    if options_text:
        options = options_text.split('\n')
        for opt in options:
            opt_text = opt.split(') ', 1)[1] if ') ' in opt else opt
            opt_len = len(opt_text)
            if opt_len > X_POLL_OPTION_LIMIT:
                issues.append(
                    f'  {opt.split(")")[0]}): "{opt_text}" = {opt_len} chars '
                    f'⚠️ OVER {X_POLL_OPTION_LIMIT}!'
                )
            else:
                print(f'  {opt.split(")")[0]}): "{opt_text}" = {opt_len} chars ✓')

    # Disclaimer check
    if 'not medical advice' not in block.lower():
        issues.append("  ⚠️ Post 2 missing disclaimer!")
    return issues


def verify_post2_short(block: str) -> list[str]:
    """Verify short-form post. Returns list of issues."""
    issues = []
    tweet = block.strip()
    chars = len(tweet)
    if chars > X_TWEET_LIMIT:
        issues.append(
            f"  Tweet: {chars} chars ⚠️ OVER {X_TWEET_LIMIT}! "
            f"(excess: {chars - X_TWEET_LIMIT})"
        )
    else:
        print(f"  Tweet: {chars} chars ✓")

    # RN credential check
    first_sentence = tweet.split('.')[0] if '.' in tweet else tweet[:80]
    if not ('RN' in first_sentence or 'nurse' in first_sentence.lower()):
        issues.append("  ⚠️ RN credential not in first sentence!")

    # Disclaimer check
    if 'not medical advice' not in tweet.lower():
        issues.append("  ⚠️ Post 2 missing disclaimer!")
    return issues


def verify_post2(block: str) -> list[str]:
    """Route Post 2 to correct verifier based on detected format."""
    fmt = detect_post2_format(block)
    if fmt == 'poll':
        return verify_post2_poll(block)
    elif fmt == 'short_form' or fmt == 'general':
        return verify_post2_short(block)
    return []


def main(filepath: str):
    with open(filepath) as f:
        content = f.read()

    blocks = re.findall(r'```\n(.*?)```', content, re.DOTALL)
    if len(blocks) not in (2, 3):
        print(f"⚠️ Expected 2 or 3 posts, found {len(blocks)} code blocks")
        sys.exit(1)

    all_issues = []

    print("=== Post 1 (Thread) ===")
    all_issues.extend(verify_post1_thread(blocks[0]))

    print("\n=== Post 2 (Rotating Format) ===")
    all_issues.extend(verify_post2(blocks[1]))

    if len(blocks) == 3:
        # Legacy 3-post file — Post 3 is always short form
        print("\n=== Post 3 (Legacy Short Form) ===")
        all_issues.extend(verify_post2_short(blocks[2]))

    # Summary
    print(f"\n{'='*50}")
    if all_issues:
        print("❌ ISSUES FOUND — FIX BEFORE SAVING:")
        for issue in all_issues:
            print(issue)
        sys.exit(1)
    else:
        print("✅ ALL CHECKS PASSED — CONTENT READY")
        sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} /path/to/YYYY-MM-DD_posts.md")
        sys.exit(1)
    main(sys.argv[1])
