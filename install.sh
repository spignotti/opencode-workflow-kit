#!/usr/bin/env bash
set -euo pipefail

# Download and extract a pinned release of opencode-workflow-kit.
# Default target: ./opencode-workflow-kit/ (created, never overwritten).
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/spignotti/opencode-workflow-kit/v1.0.1/install.sh > install.sh
#   bash install.sh [TARGET]
#
# Requirements: curl, tar

TAG="v1.0.1"
REPO="spignotti/opencode-workflow-kit"
TARGET="${1:-$PWD/opencode-workflow-kit}"

die() { printf 'install.sh: %s\n' "$1" >&2; exit 1; }

# Dependency check
for cmd in curl tar; do
  command -v "$cmd" >/dev/null 2>&1 || die "required command not found: $cmd"
done

# Refuse an existing target
if [ -e "$TARGET" ]; then
  die "target already exists: $TARGET — remove it first or choose a different path"
fi

# Refuse if parent directory does not exist
PARENT="$(dirname "$TARGET")"
[ -d "$PARENT" ] || die "parent directory does not exist: $PARENT"

TMPDIR="${TMPDIR:-/tmp}/opencode-install-$$"
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT
mkdir -p "$TMPDIR"

URL="https://codeload.github.com/${REPO}/tar.gz/refs/tags/${TAG}"
printf 'Downloading %s ...\n' "$URL"
curl -fsSL -o "$TMPDIR/release.tar.gz" "$URL" || die "download failed"

# Extract into temp dir, capture the top-level directory name
tar -xzf "$TMPDIR/release.tar.gz" -C "$TMPDIR"
DIRNAME="$(find "$TMPDIR" -mindepth 1 -maxdepth 1 -type d | head -1)"
[ -d "$DIRNAME" ] || die "unexpected archive layout"

# Move into final location (atomic-ish: rename won't overwrite)
mv "$DIRNAME" "$TARGET" || die "failed to move extracted files to $TARGET"

printf 'Installed %s to %s\n' "$TAG" "$TARGET"
