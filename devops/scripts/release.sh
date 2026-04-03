#!/usr/bin/env bash
set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: ./devops/scripts/release.sh <version>"
  echo "  Example: ./devops/scripts/release.sh 1.0.0"
  echo "  Example: ./devops/scripts/release.sh 1.1.0-rc.1  (release candidate)"
  exit 1
fi

VERSION="$1"
TAG="v$VERSION"

if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$ ]]; then
  echo "[ERROR] Invalid version format: $VERSION"
  echo "  Use semver: MAJOR.MINOR.PATCH or MAJOR.MINOR.PATCH-prerelease"
  exit 1
fi

if git rev-parse "$TAG" >/dev/null 2>&1; then
  echo "[ERROR] Tag $TAG already exists"
  exit 1
fi

echo "=== Creating Release $TAG ==="

echo "[1/3] Running checks..."
pnpm run typecheck
pnpm run build

echo "[2/3] Creating tag..."
git tag -a "$TAG" -m "Release $TAG"

echo "[3/3] Pushing tag..."
git push origin "$TAG"

echo ""
echo "=== Release $TAG created ==="
echo "The deploy pipeline will now build and push Docker images."
echo "Monitor the pipeline at: https://github.com/$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/actions"
