#!/usr/bin/env bash
#
# rm_dirs.sh
#
set -e  # Exit immediately if a command exits with a non-zero status

TARGET_DIR="$1"

rm -rf "$TARGET_DIR"