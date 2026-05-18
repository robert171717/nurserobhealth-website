---
name: local-llm-model-selection
description: Select optimal local LLM models for specific GPU hardware - benchmarks, VRAM requirements, and recommendations for consumer setups
version: 1.0
author: Robert (@RealSolanaMeme)
tags: [llm, local-inference, llama-cpp, gpu, benchmarks, model-selection]
---

# Optimal Local LLM Model Selection Guide

## Overview

Select the best open-source LLM models for your specific GPU hardware based on VRAM capacity, desired speed, and use case. This guide covers the state-of-the-art as of April 2026.

## Quick Recommendations by Hardware

### 24GB VRAM (RTX 3090/3090Ti/4090) - Most Common Consumer Setup 🎯

**BEST OVERALL: Qwen3-Coder-30B-A3B (MoE)**
- **Speed**: ~50-53 tok/s
- **VRAM**: ~17GB (Q4_K_M quantization)
- **Best for**: Coding, tool-calling, agent workflows, general use
- **Why**: MoE architecture loads only 3B active parameters per token, 30% faster than dense 27B models
- **Download**: `https://huggingface.co/ggml-org/Qwen3-30B-A3B-Instruct-2507-GGUF`

**ALTERNATIVES:**

| Model | Speed | VRAM | Best For | Notes |
|-------|-------|------|----------|-------|
| Qwen3.5-27B | ~40 tok/s | ~19GB | General use | Solid dense model, reliable |
| Qwen3.5-35B-A3B | ~35-45 tok/s | ~20GB | Reasoning tasks | Better reasoning, slightly slower |
| Llama-3.3-70B (Q3_K_S) | ~15-20 tok/s | ~24GB | Max quality | Heavily quantized, slowest |

### 12-16GB VRAM (RTX 3060/4060Ti/4070)

**BEST: Qwen3-Coder-30B-A3B (Q4_XS)**
- Fits in 12GB with room for context
- ~30-35 tok/s on 12GB cards
- Fallback: Llama-3.1-8B (Q8_0) for maximum speed

### 8-10GB VRAM (RTX 3050/4060)

**BEST: Llama-3.1-8B (Q6_K or Q8_0)**
- ~60-80 tok/s
- Minimal VRAM usage (~6-8GB)
- Leave room for long contexts

## Key Selection Criteria

### 1. **VRAM Requirements** (Rule of Thumb)

```
VRAM Needed = (Model Parameters × Quant Bits / 8) + Context Overhead

Q4_K_M (4-bit): ~0.7 GB per billion parameters
Q6_K (6-bit): ~1.0 GB per billion parameters
Q8_0 (8-bit): ~1.1 GB per billion parameters

Add 2-4GB for context window (depends on sequence length)
```

### 2. **Speed Expectations by GPU**

| GPU | Qwen3.5-27B | Qwen3-Coder-30B-A3B | Llama-3.1-8B |
|-----|-------------|---------------------|--------------|
| RTX 3090Ti | ~40 tok/s | ~50-53 tok/s | ~80-100 tok/s |
| RTX 4090 | ~55 tok/s | ~65-75 tok/s | ~120-140 tok/s |
| RTX 3060 (12GB) | ~20 tok/s | ~30-35 tok/s | ~50-60 tok/s |

### 3. **Use Case Optimization**

- **Agent/Tool Workflows**: Qwen3-Coder-30B-A3B (excellent tool-calling)
- **Reasoning/Complex Tasks**: Qwen3.5-35B-A3B (Reasoning variant)
- **General Chat/Assistance**: Qwen3.5-27B (balanced)
- **Maximum Quality**: Llama-3.3-70B Q3_K (if you have VRAM)
- **Fast Responses**: Llama-3.1-8B Q8_0 (instant)

## Research Methodology

To find current best models (repeat this quarterly):

### Step 1: Check Benchmarks
```bash
# Key sources for model comparisons:
- https://artificialanalysis.ai/models/open-source
- https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard
- https://pricepertoken.com/leaderboards
- r/LocalLLaMA on Reddit (search "best model [your VRAM]")
```

### Step 2: Verify VRAM Compatibility
```bash
# Check GGUF file sizes on HuggingFace
# Q4_K_M files are ~16-18GB for 30B models
# Add 2-4GB buffer for KV cache

# Example: Qwen3-30B-A3B Q4_K_M
# Model: ~17.5 GB
# KV Cache (8K context): ~2 GB
# Total: ~19.5 GB (fits in 24GB VRAM)
```

### Step 3: Test Speed Locally
```bash
# Benchmark with llama.cpp
./llama-bench -m model.gguf -n 1024 -t 8

# Or use CTranslateR for detailed metrics
```

## Quantization Guide

### Quality vs Speed Tradeoffs

| Quant | Quality Loss | Speed | VRAM | Recommended For |
|-------|--------------|-------|------|-----------------|
| Q8_0 | None | Baseline | Max | When quality critical |
| Q6_K | Minimal | +10% | -15% | High-quality use |
| **Q4_K_M** | **~2%** | **+25%** | **-35%** | **Sweet spot** ⭐ |
| Q4_K_S | ~5% | +35% | -40% | VRAM constrained |
| Q3_K_S | ~10% | +50% | -50% | Emergency only |

**Rule**: Q4_K_M is the sweet spot for most use cases. Only go lower if VRAM-constrained.

## Installation Steps

### Download Model
```bash
# Using huggingface-cli
huggingface-cli download ggml-org/Qwen3-30B-A3B-Instruct-2507-GGUF \
  qwen3-30b-a3b-instruct-2507-q4_k_m.gguf \
  --local-dir ~/.cache/llama.cpp/models/

# Or download manually from HuggingFace
# https://huggingface.co/ggml-org/Qwen3-30B-A3B-Instruct-2507-GGUF
```

### Test with llama.cpp
```bash
./main -m ~/.cache/llama.cpp/models/qwen3-30b-a3b-instruct-2507-q4_k_m.gguf \
  -n 512 --color -p "Explain quantum computing in simple terms"
```

### Integrate with Hermes/Local Setup
```bash
# Update your llama.cpp server config
# Point to new model path
# Restart inference service
```

## Optimization Tips

### 1. **GPU Offloading**
```bash
# Use -ngl 999 to offload all layers to GPU
./main -m model.gguf -ngl 999

# If VRAM runs out, reduce to -ngl 80-90
```

### 2. **Context Management**
```bash
# Shorter context = more VRAM for model
# Use -c 4096 for 4K context instead of default 8K

# Or enable flash attention if supported
```

### 3. **Batch Processing**
```bash
# Increase -b for faster prompt processing
# Trade: uses more VRAM during initial prompt
```

## Troubleshooting

### Out of VRAM
```
Solution 1: Use lower quantization (Q4_K_S or Q3_K_S)
Solution 2: Reduce context window (-c 2048)
Solution 3: Reduce GPU layers (-ngl 80)
Solution 4: Switch to smaller model (7B or 8B)
```

### Slow Performance
```
Solution 1: Ensure all layers on GPU (-ngl 999)
Solution 2: Check GPU is not thermal throttling
Solution 3: Close other GPU-intensive apps
Solution 4: Update CUDA/cuDNN drivers
```

### Model Not Found
```
Solution: Verify GGUF file path and permissions
Check llama.cpp version supports the model architecture
```

## Current State (April 2026)

### Top Models by Category

| Category | Model | Parameters | Why |
|----------|-------|------------|-----|
| **Best Overall (24GB)** | Qwen3-Coder-30B-A3B | 30B MoE | Speed + quality balance |
| **Best Reasoning** | Qwen3.5-35B-A3B | 35B MoE | Strongest reasoning |
| **Best Dense** | Qwen3.5-27B | 27B | Reliable, no MoE quirks |
| **Best Small** | Llama-3.1-8B | 8B | Fast, efficient |
| **Best Large** | Llama-3.3-70B | 70B | Max quality (needs 24GB) |

### Emerging Models to Watch
- Mistral Small 3 (rumored, check availability)
- Gemma 3 variants (Google's latest)
- DeepSeek-R1 derivatives

## References

- **Benchmarks**: https://artificialanalysis.ai/
- **GGUF Models**: https://huggingface.co/ggml-org/
- **llama.cpp**: https://github.com/ggml-org/llama.cpp
- **Community**: r/LocalLLaMA on Reddit
- **Price/Speed**: https://pricepertoken.com/