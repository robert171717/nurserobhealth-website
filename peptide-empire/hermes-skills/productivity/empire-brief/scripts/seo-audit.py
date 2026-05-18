#!/usr/bin/env python3
"""
Comprehensive SEO audit for nurserobhealth.com.
Run: python3 /tmp/seo-audit.py
Requires: curl (already installed)

Checks: title, meta, headings, structured data, keywords, links, social cards, page size.
"""

import re, subprocess, sys

def fetch(url):
    result = subprocess.run(['curl', '-sL', url], capture_output=True, text=True, timeout=15)
    if result.returncode != 0:
        print(f"ERROR fetching {url}: {result.stderr}")
        sys.exit(1)
    return result.stdout

def head_check(url):
    result = subprocess.run(['curl', '-sI', url], capture_output=True, text=True, timeout=10)
    return result.stdout

html = fetch('https://nurserobhealth.com')

print("=" * 60)
print("NURSEROBHEALTH.COM — SEO AUDIT")
print("=" * 60)

# 1. TITLE
title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
title = title_match.group(1).strip() if title_match else "MISSING"
print(f'\nTITLE: "{title}" ({len(title)} chars)')

# 2. META DESCRIPTION
desc_match = re.search(r'<meta name="description" content="(.*?)"', html, re.IGNORECASE)
desc = desc_match.group(1) if desc_match else "MISSING"
print(f'DESCRIPTION: "{desc}" ({len(desc)} chars)')

# 3. HEADINGS
print('\n--- HEADINGS ---')
for level in range(1, 7):
    matches = re.findall(rf'<h{level}[^>]*>(.*?)</h{level}>', html, re.DOTALL)
    for m in matches:
        clean = re.sub(r'<[^>]+>', '', m).strip()
        if clean:
            print(f'  H{level}: "{clean[:120]}"')

# 4. STRUCTURED DATA
has_jsonld = bool(re.search(r'application/ld\+json', html))
has_microdata = bool(re.search(r'itemscope|itemprop|itemtype', html))
print(f'\nSTRUCTURED DATA: JSON-LD={"YES" if has_jsonld else "NO"} | Microdata={"YES" if has_microdata else "NO"}')

# 5. META TAGS
print('\n--- OPENGRAPH/TWITTER ---')
for tag in re.findall(r'<meta[^>]+>', html):
    name = re.search(r'(?:name|property)="([^"]+)"', tag)
    content = re.search(r'content="([^"]+)"', tag)
    if name and content:
        print(f'  {name.group(1)}: {content.group(1)[:80]}')

# 6. CANONICAL
canonical = re.search(r'<link rel="canonical" href="([^"]+)"', html)
print(f'\nCANONICAL: {canonical.group(1) if canonical else "MISSING"}')

# 7. KEYWORD DENSITY
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text).lower()
keywords = ['peptide', 'bpc-157', 'tb-500', 'wolverine', 'healing', 'research',
            'clinical', 'nurse', 'rn', 'consult', 'guide', 'dosing', 'injection',
            'muscle', 'recovery', 'regeneration', 'protocol']
print('\n--- KEYWORD COUNTS ---')
for kw in keywords:
    count = len(re.findall(r'\b' + re.escape(kw) + r'\b', text))
    if count > 0:
        print(f'  "{kw}": {count}x')

# 8. LINKS
links = re.findall(r'<a[^>]*href="([^"]*)"', html)
internal = [l for l in links if 'nurserobhealth' in l]
external = [l for l in links if 'http' in l and 'nurserobhealth' not in l]
print(f'\nLINKS: {len(links)} total | {len(internal)} internal | {len(external)} external')

# 9. PAGE SIZE
print(f'PAGE SIZE: {len(html)} bytes ({len(html)/1024:.1f} KB)')

# 10. ROBOTS.TXT + SITEMAP
robots = head_check('https://nurserobhealth.com/robots.txt')
sitemap = head_check('https://nurserobhealth.com/sitemap.xml')
print(f'ROBOTS.TXT: {"200" if "200" in robots.splitlines()[0] else "MISSING"}')
print(f'SITEMAP.XML: {"200" if "200" in sitemap.splitlines()[0] else "MISSING"}')

# 11. MISSING KEYWORDS (high-value search terms)
high_value = ['peptide therapy', 'peptide stack', 'semaglutide', 'tirzepatide',
              'ghk-cu', 'ipamorelin', 'cjc-1295', 'anti-aging peptides',
              'bodybuilding peptides', 'peptide injection guide']
print('\n--- MISSING HIGH-VALUE KEYWORDS ---')
for kw in high_value:
    if kw.lower() not in text:
        print(f'  MISSING: "{kw}"')

print('\n' + '=' * 60)
print('AUDIT COMPLETE')
