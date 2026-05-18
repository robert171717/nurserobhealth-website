---
name: file-edit-pattern
description: Safe pattern for editing existing files - always read first, verify changes, never assume file content
version: 1.0
author: NurseRobHealth
tags: [files, editing, safety, verification]
---

# File Edit Pattern
## Never Assume File Content - Always Read First

> **Critical lesson learned: Python's `.replace()` silently fails if text not found**

---

## 🚨 THE MISTAKE TO AVOID

❌ **WRONG:** Assume file content → Apply `.replace()` → Print "success" → Assume it worked

**Why this fails:**
- `.replace()` returns original string if pattern not found (no error!)
- File write succeeds even if content unchanged
- No way to know if edit actually happened

✅ **RIGHT:** Read file → Show user actual content → Apply exact match → Verify change persisted

---

## ✅ SAFE FILE EDIT PATTERN (6 STEPS)

### Step 1: READ THE FILE FIRST
```python
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print("Current content:")
print(content[:500])  # Show first 500 chars
```

### Step 2: VERIFY TEXT EXISTS
```python
if "text to replace" in content:
    print("✅ Found text to replace")
else:
    print("❌ Text NOT found - need to check exact content")
    print("Showing actual content...")
```

### Step 3: SHOW USER WHAT'S THERE
```python
print("\n📄 Current file content:")
print("-" * 70)
print(content[:1000])  # Show relevant section
```

### Step 4: APPLY CHANGE WITH EXACT MATCH
```python
# Use exact strings from file, not assumptions
old_text = "exact text from file"  # Copied from Step 1
new_text = "replacement text"

content = content.replace(old_text, new_text)
```

### Step 5: WRITE AND VERIFY
```python
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# IMMEDIATELY verify
with open(filepath, 'r', encoding='utf-8') as f:
    new_content = f.read()

if "expected new text" in new_content:
    print("✅ Change verified!")
else:
    print("❌ Change did NOT persist - investigate")
```

### Step 6: SHOW USER RESULT
```python
print("\n📄 Updated file content:")
print("-" * 70)
print(new_content[:1000])
```

---

## 📋 CHECKLIST FOR EVERY FILE EDIT

Before running any file edit code:

- [ ] Did I read the file first?
- [ ] Did I show the user the actual content?
- [ ] Did I verify the text to replace actually exists?
- [ ] Am I using exact string matches (not assumptions)?
- [ ] Did I verify the change persisted after write?
- [ ] Did I show the user the result?

**If any answer is NO → STOP and do that step first.**

---

## 🚫 NEVER DO THIS

```python
# ❌ DANGEROUS - Assumes file content
content = old_content.replace("assumed text", "new text")
with open(filepath, 'w') as f:
    f.write(content)
print("✅ Done!")  # Lie - might not have worked!
```

## ✅ ALWAYS DO THIS

```python
# ✅ SAFE - Reads first, verifies
with open(filepath, 'r') as f:
    content = f.read()

print("Current content:", content[:500])  # Show user

if "exact text" in content:
    content = content.replace("exact text", "new text")
    with open(filepath, 'w') as f:
        f.write(content)
    
    # Verify
    with open(filepath, 'r') as f:
        new_content = f.read()
    
    if "new text" in new_content:
        print("✅ Verified!")
    else:
        print("❌ Failed!")
else:
    print("⚠️ Text not found - checking actual content...")
```

---

## 🎯 WHY THIS MATTERS

| Risk | Consequence | Prevention |
|------|-------------|------------|
| Silent `.replace()` failure | File unchanged, user thinks it worked | Read first, verify after |
| Assumed file content | Wrong strings, no match | Show actual content |
| No error handling | No feedback on failure | Check if text exists |
| No verification | Can't trust changes happened | Read back and check |

---

## 📝 REAL EXAMPLE (FROM ACTUAL MISTAKE)

### ❌ What I Did Wrong:
```python
# Assumed README had this:
old_text = """# 🧠 Second Brain Duo 2026
> The PARA-powered productivity vault"""

# But file actually had:
# """# 🧠 Second Brain Duo 2026
# > **Notion + Obsidian PARA Vault** | 90% Automated"""

readme = readme.replace(old_text, new_text)  # Silently failed!
with open('README.md', 'w') as f:
    f.write(readme)  # File unchanged!
print("✅ Done!")  # Lie - nothing changed!
```

### ✅ What I Should Have Done:
```python
# Step 1: Read
with open('README.md', 'r') as f:
    readme = f.read()

# Step 2: Show
print("Current README:")
print(readme[:500])

# Step 3: Find exact text
if "**Notion + Obsidian**" in readme:
    old_text = """# 🧠 Second Brain Duo 2026
> **Notion + Obsidian PARA Vault** | 90% Automated"""
    
    # Step 4: Replace with exact match
    readme = readme.replace(old_text, new_text)
    
    # Step 5: Write & verify
    with open('README.md', 'w') as f:
        f.write(readme)
    
    with open('README.md', 'r') as f:
        new_readme = f.read()
    
    # Step 6: Confirm
    if "Highly automated" in new_readme:
        print("✅ Change verified!")
    else:
        print("❌ Change failed!")
```

---

## 🏆 GOLD STANDARD

**Every file edit must follow this pattern:**

1. **READ** → Show user actual content
2. **CHECK** → Verify text exists before replacing
3. **EDIT** → Use exact string matches
4. **WRITE** → Save changes
5. **VERIFY** → Read back and confirm change persisted
6. **SHOW** → Display result to user

**If you skip any step, the edit might silently fail.**

---

## ⚠️ CRITICAL PITFALL: `read_file` truncation + `write_file` = destroyed files

**DO NOT use `read_file()` without explicit `limit` + `write_file()` together in `execute_code` scripts.**

`read_file()` returns at most **500 lines by default**. If the file is 689 lines, you only see 500 lines. If you then `write_file()` that truncated content back, you **permanently delete 189 lines from the file** — with no warning, no confirmation, and no undo.

### Symptoms of this bug:
- File shrinks (e.g., 894→505 lines, 689→502 lines)
- `</body>` and `</html>` tags gone from file bottom
- Scripts, forms, and exit popups disappear
- User sees broken pages with no JS functionality

### ❌ NEVER DO THIS:
```python
# BUG: read_file truncates at 500 lines, write_file overwrites with truncated content
content = read_file(path)['content']  # Only 500 lines!
# ... make changes ...
write_file(path, content)  # TRUNCATED — bottom of file is GONE
```

### ✅ ALWAYS DO ONE OF THESE:

**Option A — Use `patch` tool (PREFERRED):**
The `patch` tool modifies files in-place by string replacement. It never truncates. Always prefer `patch` over read_file+write_file for modifications to existing files.

**Option B — Pass explicit `limit` if you must read_file:**
```python
content = read_file(path, limit=2000)['content']  # Exceed expected file size
# Verify before writing:
lines = content.split('\n')
if not content.strip().endswith('</html>'):
    print(f'FATAL: file appears truncated, got {len(lines)} lines')
    return
write_file(path, content)
```

**Option C — Use terminal for size checks:**
```bash
# Verify file integrity before and after any read+write cycle
wc -l file.html
tail -3 file.html  # Must show </body></html>
```

### Real-world damage (May 2026):
- 8 HTML production files truncated by 100-400 lines each
- Mobile menus, exit popups, Formspree forms, and sessionStorage scripts lost
- User saw broken overlay on iPhone with non-functional buttons
- Full git restore required from earlier commit

---

*File Edit Pattern v1.1 | Updated May 2026 with read_file truncation pitfall*