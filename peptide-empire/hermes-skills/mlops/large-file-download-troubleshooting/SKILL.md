---
description: Troubleshoot large ML model downloads that stall or fail repeatedly
tags:
  - downloads
  - troubleshooting
  - ml-models
  - wsl2
name: large-file-download-troubleshooting
---

# Large File Download Troubleshooting for ML Models

## Overview
Guide for reliably downloading large ML model files (>10 GB) in WSL2/Ubuntu environments, especially when downloads stall or fail repeatedly.

## Common Issue: Downloads Stalling at Same Point

**Symptom:** Download consistently fails at the same percentage (e.g., 92.9%, 17.28 GB of 18.6 GB)

**Diagnosis:** This is typically a **server-side truncation issue**, not a client problem. Multiple download tools failing at the exact same byte position confirms this.

### Troubleshooting Steps

#### 1. Try Multiple Download Tools
Test in this order (most to least reliable):

```bash
# Method 1: wget with resume (most reliable for WSL2)
wget -c -O model.gguf \
  --timeout=60 \
  --waitretry=5 \
  --tries=20 \
  --no-check-certificate \
  "URL"

# Method 2: aria2c with multi-connection (requires installation)
aria2c -x 16 -s 16 -k 1M \
  --continue=true \
  --auto-file-renaming=false \
  -d /path/to/models/ \
  -o model.gguf \
  "URL"

# Method 3: curl with resume
curl -L -C - -o model.gguf "URL"
```

#### 2. Install aria2c (if needed)

```bash
# Via apt (requires sudo)
sudo apt-get update && sudo apt-get install -y aria2

# Via snap (requires sudo)
sudo snap install aria2 --classic
```

#### 3. Try Different URL Endpoints

HuggingFace provides multiple endpoints - try them in order:

```bash
# Most reliable: resolve endpoint
https://huggingface.co/user/repo/resolve/main/file.gguf

# Alternative: raw endpoint
https://huggingface.co/user/repo/raw/main/file.gguf
```

#### 4. Verify File Integrity

Check if partial download is valid GGUF:

```python
import os

model_path = "path/to/model.gguf"

if os.path.exists(model_path):
    size_gb = os.path.getsize(model_path) / (1024**3)
    print(f"File size: {size_gb:.2f} GB")
    
    with open(model_path, 'rb') as f:
        header = f.read(4)
        if header == b'GGUF':
            print("✅ Valid GGUF header")
        else:
            print("❌ Invalid/corrupted file")
```

#### 5. If Download Stalls Repeatedly

If all tools fail at the same point:

**Option A: Test Partial File**
- Valid GGUF header + >90% complete may still work
- Some truncated weights may cause issues, but model could be usable

**Option B: Try Different Quantization**
- Q4_0 is smaller (~15-20% less) than Q4_K_M
- Similar performance, may download successfully

**Option C: Use GUI Download Manager**
- Free Download Manager, IDM, or similar
- Better retry logic for stalled connections

## Monitoring Progress

```python
import os
import time

model_path = "path/to/file.gguf"
expected_gb = 18.6

for i in range(20):
    time.sleep(120)
    
    if os.path.exists(model_path):
        size_gb = os.path.getsize(model_path) / (1024**3)
        progress = (size_gb / expected_gb) * 100
        print(f"Update {i+1}: {size_gb:.2f} GB ({progress:.1f}%)")
        
        if size_gb >= expected_gb * 0.98:
            print("✅ Complete!")
            break
```

## Pitfalls

1. **sudo required for system packages** - aria2c installation via apt/snap needs sudo
2. **WSL2 network issues** - Sometimes need to restart WSL or switch VPN exit
3. **File path confusion** - In WSL2, Windows path is `/mnt/c/Users/...`
4. **Server-side truncation** - If all tools fail at same byte position, it's the server, not your network

## Recommendation

For files >15 GB that keep stalling:
1. First try wget with resume (built-in, no installation)
2. If that fails at same point, try different quantization (smaller file)
3. Test partial file if >90% complete with valid header
4. Use GUI download manager as last resort
