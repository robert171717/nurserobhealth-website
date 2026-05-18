---
name: gguf-model-download
description: Reliable methods for downloading large GGUF model files (~15-25 GB) from HuggingFace in WSL2 native mode. Addresses common failures at 92-93% with curl/wget.
version: 1.0.0
author: Robert
license: MIT
dependencies: []
metadata:
  hermes:
    tags: [GGUF, Model Download, HuggingFace, WSL2, Large Files, aria2c, wget, curl]

---

# GGUF Model Download in WSL2 Native

**Reliable methods for downloading large GGUF files (~15-25 GB) from HuggingFace in WSL2 native mode.**

## Problem: HuggingFace Download Failures

HuggingFace `resolve/main` URLs **consistently fail at 92-93%** completion due to server-side issues. This affects ALL download tools (curl, wget, aria2c) at the same byte range.

**Confirmed Failure Pattern:**
- Q4_K_M (18.6 GB expected): Stalls at 17.28 GB (92.9%) = 18,556,686,752 bytes
- Q4_0 (17.5 GB expected): Stalls at 16.19 GB (92.5%)
- Multiple tools fail at IDENTICAL byte ranges
- Server-side truncation or connection issues at specific byte offsets

**Symptoms:**
- Download stalls at 92-93% regardless of tool used
- Resume attempts fail to progress beyond stall point
- File has invalid GGUF header (e.g., `b'vers'` instead of `b'GGUF'`)
- Model cannot be loaded - corrupted/truncated

## Recommended Solutions (in order)

### 1. Free Download Manager (GUI) - **BEST** ⭐

Most reliable for large files in WSL2/Windows hybrid environments.

**Instructions:**
1. Open Free Download Manager in Windows
2. Add URL:
   ```
   https://huggingface.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF/resolve/main/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf
   ```
3. Save to: `C:/Users/Robert/Desktop/Models/`
4. Start download (FDM handles chunking and resume automatically)

**Advantages:**
- Automatic chunking and parallel downloads (8-16 connections)
- Reliable resume on failure
- No sudo required
- Works through WSL2 Windows mount

### 2. aria2c (CLI) - **REQUIRES SUDO**

Multi-connection download tool, excellent for large files.

**Install (requires sudo):**
```bash
sudo apt install aria2
# OR
sudo snap install aria2 --classic
```

**Use:**
```bash
aria2c -x 16 -s 16 -k 1M \
  -d /mnt/c/Users/Robert/Desktop/Models/ \
  -o Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf \
  "https://huggingface.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF/resolve/main/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf"
```

**Advantages:**
- 16 parallel connections (fastest CLI option)
- Excellent resume capability
- Checksum verification

### 3. wget - **UNRELIABLE FOR >15GB**

Built-in but frequently fails at 92-93%.

```bash
wget -c -O model.gguf --timeout=30 --tries=5 URL
```

**Only use if:** File is small (<10 GB) or as fallback.

### 4. curl - **UNRELIABLE FOR >15GB**

Same issues as wget.

```bash
curl -L -C - -o model.gguf URL
```

## Verification

After download, verify GGUF format:

```python
with open('model.gguf', 'rb') as f:
    header = f.read(4)
    assert header == b'GGUF', f"Invalid GGUF: {header}"
```

Check file size matches expected:
- Q4_K_M: ~18-20 GB for 30B model
- Q4_0: ~17-19 GB for 30B model

## Troubleshooting

**Stuck at 92.9%?**
1. HuggingFace server issue - switch to FDM GUI
2. Delete partial file and restart fresh
3. Try different quantization (Q4_0 is ~1GB smaller)

**Network issues?**
- Change VPN exit node
- Try different mirror (modelscope.cn, etc.)

**File is valid but truncated?**
- Model won't load properly - missing final layers
- Must re-download completely

## Notes

- In WSL2 native mode, `sudo` requires password (not available to agents)
- Windows GUI tools (FDM, IDM) work better than CLI for large files
- Download to Windows mount (`/mnt/c/`) for better reliability
- HuggingFace `resolve/main` endpoint has known reliability issues
- Consider using `huggingface-cli` if available (better resume)

## Example: Full Download Workflow

```bash
# 1. Check if file exists
ls -lh /mnt/c/Users/Robert/Desktop/Models/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf

# 2. If incomplete, delete it
rm /mnt/c/Users/Robert/Desktop/Models/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf

# 3. Use FDM GUI or aria2c (recommended)
# 4. Monitor progress
watch -n 60 'ls -lh /mnt/c/Users/Robert/Desktop/Models/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf'

# 5. Verify on completion
python3 -c "
with open('/mnt/c/Users/Robert/Desktop/Models/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf', 'rb') as f:
    assert f.read(4) == b'GGUF', 'Invalid file'
print('✅ GGUF verified')
"
```
