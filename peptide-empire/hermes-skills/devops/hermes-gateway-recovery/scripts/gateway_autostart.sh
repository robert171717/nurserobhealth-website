#!/bin/bash
# Hermes Gateway auto-start — call from .bashrc
# WSL2 user systemd services don't survive Windows reboots, so we check and start on first shell

if systemctl --user is-active --quiet hermes-gateway 2>/dev/null; then
    exit 0  # already running, nothing to do
fi

systemctl --user start hermes-gateway 2>/dev/null
