---
name: video-repurposer
description: Takes one long Nurse Rob video and turns it into 8-12 short clips with captions, hooks, and CTAs — automated pipeline
version: 2.0
author: Nurse Rob
---

# Video Repurposer v2.0 🎥

**Purpose:** Automated video processing pipeline: takes one long-form video (5-20 min) → extracts key moments → generates 8-12 short clips (30-90 sec) with AI captions, hooks, and Nurse Rob branding.

## TRIGGER
- Manual: "repurpose this video" / "extract clips from [file]"
- On-demand: after Nurse Rob records new content

## PROFILE ROUTING
Use `creative-mode` (gpt-5.5-codex) for clip selection and caption writing.

## WORKFLOW

### Step 1: Accept Video Input
Video source can be:
- Local file: `~/NurseRob_PeptideEmpire/videos/raw/[filename].mp4`
- YouTube URL (use youtube-content skill for transcript)
- X/Twitter video URL

### Step 2: Extract Transcript
```bash
# If local video, use whisper for transcription
# If YouTube, use youtube-content skill to get transcript
```
Save transcript to: `~/NurseRob_PeptideEmpire/videos/transcripts/[filename].txt`

### Step 3: Identify Clip Moments
Analyze transcript and identify 8-12 clip-worthy moments:
- 🔥 **Hook moment:** Surprising fact or statement (first 15 sec)
- 📚 **Insight drop:** Key research finding or clinical insight
- ⚡ **Hot take:** Controversial or counter-intuitive point
- 😂 **Relatable moment:** Humor or personal story
- 🎯 **CTA moment:** Natural pitch or value offer
- ⚠️ **Warning moment:** Safety insight or caution

### Step 4: Generate Clip Specs
For each clip, specify:
```json
{
  "clip_number": 1,
  "start_time": "0:45",
  "end_time": "1:30",
  "duration": "0:45",
  "type": "hook",
  "title": "BPC-157: What the research ACTUALLY says",
  "caption_text": "As a nurse, I read the studies so you don't have to 🏥",
  "hook_overlay": "Most people get this WRONG 👇",
  "cta_text": "Follow @NurseRobHealth for more peptide education",
  "disclaimer": "⚠️ Educational content. Not medical advice.",
  "hashtags": "#peptides #biohacking #nurserob #bpc157",
  "platform": "reels_shorts_tiktok"
}
```

### Step 5: Generate Caption Files
For each clip, generate SRT caption file:
```
1
00:00:00,000 --> 00:00:03,000
Most people get BPC-157 completely wrong.

2
00:00:03,000 --> 00:00:07,000
As a nurse, I actually read the research.
```

### Professional Captions & Overlays (preferred: HyperFrames)

For broadcast-quality captions, lower-thirds, transitions, and branding overlays, use the **HyperFrames** skill instead of raw FFmpeg `subtitles=` / `drawtext=` filters. See `references/hyperframes-integration.md` for the full integration strategy and workflow.

If HyperFrames is not yet set up, fall back to Step 6's FFmpeg approach.

### Step 6: Generate Processing Commands (FFmpeg fallback)
Produce FFmpeg commands for automated clip extraction:
```bash
# Clip 1: BPC-157 hook (0:45 → 1:30)
ffmpeg -i input.mp4 -ss 0:45 -to 1:30 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -c:a aac clip_01_bpc157.mp4

# Burn captions into clip
ffmpeg -i clip_01_bpc157.mp4 -vf "subtitles=clip_01_bpc157.srt:force_style='FontSize=24,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BorderStyle=3,Outline=2'" \
  clip_01_bpc157_captioned.mp4
```

### Step 7: Add Nurse Rob Branding
- Intro bumper (3 sec): Nurse Rob logo + "Nurse Rob, RN"
- Outro bumper (3 sec): "Follow for more peptide education" + disclaimer
- Watermark: Small RN logo in corner throughout

### Step 8: Generate Post Copy
For each clip, write platform-optimized copy:

**TikTok/Reels:**
```
Most people get BPC-157 wrong 🧬

As a licensed RN, I read the research so you don't have to.

Here's what actually works 👇

⚠️ Educational content. Not medical advice.

#peptides #biohacking #nurserob #bpc157
```

**X/Twitter (clip + thread):**
```
🎥 BPC-157: What the research ACTUALLY says

I read 12 studies so you don't have to. Here's the 45-second breakdown:

[VIDEO CLIP]

Key takeaways:
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

Full peptide safety guide → link in bio

⚠️ Educational from Nurse Rob, RN
```

### Step 9: Save Output Package
Save to: `~/NurseRob_PeptideEmpire/videos/processed/[date]_[topic]/`
- Raw clips (8-12 .mp4 files)
- Captioned clips (8-12 .mp4 files)
- Caption files (8-12 .srt files)
- Post copy document (markdown)
- Thumbnail prompts for image-generator

### Step 10: Push to Content Scheduler
Call `content_scheduler`:
"Schedule video clips from `~/NurseRob_PeptideEmpire/videos/processed/[date]_[topic]/` — optimal times across next 2 weeks"

## CLIP TYPE DISTRIBUTION (Target)
| Type | Count | Purpose |
|------|-------|---------|
| Hook/Teaser | 2-3 | Viral potential, stop the scroll |
| Educational | 3-4 | Authority building, save-worthy |
| Hot Take | 1-2 | Engagement, comments |
| Personal/Story | 1 | Connection, trust |
| CTA/Offer | 1 | Monetization (soft) |
| Warning/Safety | 1 | RN credibility, "he actually cares" |

## PITFALLS
- Don't cut mid-sentence — always at natural pauses
- Captions must be accurate — review against audio
- Keep disclaimers visible or in first comment
- Don't over-edit — keep Nurse Rob's natural delivery
- Avoid clips that require missing context from full video

## QUALITY CHECKLIST
- [ ] All clips have accurate captions (.srt files)
- [ ] Each clip has platform-optimized post copy
- [ ] Disclaimers on every clip/post
- [ ] Nurse Rob branding present (intro/outro/watermark)
- [ ] Clip types balanced (not all hooks, not all education)
- [ ] FFmpeg commands generated and tested
- [ ] Thumbnail prompts provided
- [ ] Output saved to organized folder
