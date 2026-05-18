#!/usr/bin/env python3
"""Generate a Nurse Rob branded image via xAI Imagine API.

Reads XAI_API_KEY from ~/.hermes/.env. Downloads and saves the image.
Works independently of the Hermes image_generate tool — no plugin needed.

Usage:
    python3 generate_image.py \\
      --prompt "Semaglutide: Beyond the Hype — evidence-based GLP-1 education" \\
      --aspect landscape \\
      --output "/path/to/output.jpg"

Cost: ~$0.02/image (grok-imagine-image), ~$0.05-0.07 (grok-imagine-image-quality).
"""

import argparse
import os
import sys
import requests


def load_api_key():
    env_path = os.path.expanduser("~/.hermes/.env")
    if not os.path.exists(env_path):
        sys.exit("ERROR: ~/.hermes/.env not found")
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("XAI_API_KEY="):
                return line.split("=", 1)[1].strip()
    sys.exit("ERROR: XAI_API_KEY not found in ~/.hermes/.env")


def build_prompt(topic_text, aspect="landscape"):
    """Build a complete image prompt from the topic, using Nurse Rob brand template."""
    
    brand_block = (
        "Medical education social media graphic. "
        "Background: deep navy #0A1F3F with subtle molecular pattern overlay. "
        "A glass-morphism card in the center with teal #00C4B4 border glow. "
        "Professional medical education aesthetic — clean, modern, trustworthy. "
        "Photorealistic medical graphic style, not cartoon, not illustration. "
        "NO text rendering errors, NO garbled letters."
    )
    
    return f"{brand_block} Content: {topic_text}"


def generate(api_key, prompt, model="grok-imagine-image", n=1):
    """Call xAI Imagine API and return (image_url, cost_ticks)."""
    resp = requests.post(
        "https://api.x.ai/v1/images/generations",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": model, "prompt": prompt, "n": n},
        timeout=120,
    )
    
    if resp.status_code != 200:
        sys.exit(f"ERROR: xAI API returned {resp.status_code}: {resp.text}")
    
    data = resp.json()
    url = data["data"][0]["url"]
    cost_ticks = data.get("usage", {}).get("cost_in_usd_ticks", 0)
    return url, cost_ticks


def download(url, output_path):
    """Download image from URL and save to output_path."""
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(resp.content)
    return len(resp.content)


def main():
    parser = argparse.ArgumentParser(description="Generate Nurse Rob branded image via xAI")
    parser.add_argument("--prompt", required=True, help="Topic/hook text for the image")
    parser.add_argument("--aspect", default="landscape", choices=["landscape", "square", "portrait"])
    parser.add_argument("--output", required=True, help="Output file path (.jpg)")
    parser.add_argument("--model", default="grok-imagine-image",
                        choices=["grok-imagine-image", "grok-imagine-image-quality"])
    args = parser.parse_args()
    
    api_key = load_api_key()
    full_prompt = build_prompt(args.prompt, args.aspect)
    
    print(f"Generating image...")
    print(f"  Topic: {args.prompt[:80]}...")
    print(f"  Model: {args.model}")
    
    url, cost_ticks = generate(api_key, full_prompt, args.model)
    cost_usd = cost_ticks / 10_000_000_000  # xAI ticks to USD
    
    size = download(url, args.output)
    
    print(f"  Saved: {args.output} ({size:,} bytes)")
    print(f"  Cost:  ${cost_usd:.4f}")
    print(f"OUTPUT:{args.output}")


if __name__ == "__main__":
    main()
