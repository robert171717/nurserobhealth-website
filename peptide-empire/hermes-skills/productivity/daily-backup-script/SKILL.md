---
name: daily-backup-script
description: Automated backup solution for creating timestamped compressed archives of directories with configurable exclusions.
tags: [backup, automation, tar, compression]
---

# Daily Backup Script

Automated backup solution for creating timestamped compressed archives of directories with configurable exclusions.

## Overview

Creates tar.gz backups of specified directories (default: `~/Documents`) to a backup location (default: `~/backups`), excluding common development folders like `node_modules` and `.git`.

## Prerequisites

- Python 3.6+
- Standard library only (no external dependencies)

## Quick Start

```bash
# Run the backup script
python ~/projects/daily-automation/backup.py
```

## Features

- **Timestamped backups**: Each backup includes date and time in filename (`documents_backup_YYYY-MM-DD_HHMMSS.tar.gz`)
- **Smart exclusions**: Automatically excludes `node_modules` and `.git` directories
- **Size reporting**: Shows backup size in MB
- **Recent backups list**: Displays last 5 backups with sizes

## Configuration

Edit these variables in `backup.py`:

```python
documents_dir = os.path.expanduser("~/Documents")  # Source directory
backups_dir = os.path.expanduser("~/backups")      # Backup destination
```

To exclude additional directories, modify the exclusion list:

```python
if any(excluded in str(item).split(os.sep) for excluded in ['node_modules', '.git', 'venv', '__pycache__']):
    continue
```

## Usage Examples

### Backup a different directory

```bash
python3 -c "
from backup import create_backup
create_backup('/path/to/source', '/path/to/backups')
"
```

### List all backups

```bash
ls -lh ~/backups/documents_backup_*.tar.gz
```

### Restore from backup

```bash
# Extract to a specific location
tar -xzf ~/backups/documents_backup_2026-03-22_065833.tar.gz -C /tmp/restore-location
```

## File Structure

```
~/projects/daily-automation/
└── backup.py          # Main backup script

~/backups/
├── documents_backup_2026-03-22_065823.tar.gz
└── documents_backup_2026-03-22_065833.tar.gz
```

## Output Format

```
==================================================
DAILY BACKUP SCRIPT
==================================================
Creating backup: documents_backup_2026-03-22_065833.tar.gz
Source: /root/Documents
Destination: /root/backups/documents_backup_2026-03-22_065833.tar.gz
✓ Backup created successfully!
  File: /root/backups/documents_backup_2026-03-22_065833.tar.gz
  Size: 1.23 MB

✓ Backup completed successfully!

Recent backups:
  - documents_backup_2026-03-22_065833.tar.gz (1.23 MB)
  - documents_backup_2026-03-22_065823.tar.gz (0.98 MB)
```

## Troubleshooting

### "Source directory does not exist"
Ensure the source directory exists: `mkdir -p ~/Documents`

### Permission errors
Run with appropriate permissions or adjust backup location to a writable directory

### Large backups taking too long
Add more exclusions for large directories like `venv`, `.cache`, or build outputs
