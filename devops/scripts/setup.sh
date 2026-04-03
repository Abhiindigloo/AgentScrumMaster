#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== AgentScrumMaster Dev Setup ==="
echo ""

if ! command -v pnpm &> /dev/null; then
  echo "[ERROR] pnpm is not installed. Install it with: npm install -g pnpm"
  exit 1
fi

if ! command -v node &> /dev/null; then
  echo "[ERROR] Node.js is not installed."
  exit 1
fi

NODE_MAJOR=$(node -v | cut -d. -f1 | tr -d 'v')
if [ "$NODE_MAJOR" -lt 20 ]; then
  echo "[WARN] Node.js 20+ recommended (found: $(node -v))"
fi

echo "[1/4] Installing dependencies..."
cd "$ROOT_DIR"
pnpm install

echo "[2/4] Setting up environment..."
if [ ! -f "$ROOT_DIR/.env" ]; then
  cp "$ROOT_DIR/.env.example" "$ROOT_DIR/.env"
  echo "  Created .env from .env.example"
else
  echo "  .env already exists, skipping"
fi

echo "[3/4] Verifying TypeScript..."
pnpm run typecheck && echo "  Typecheck passed" || echo "  [WARN] Typecheck had issues"

echo "[4/4] Building projects..."
pnpm run build && echo "  Build passed" || echo "  [WARN] Build had issues"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Available commands:"
echo "  pnpm run build         - Build all packages"
echo "  pnpm run typecheck     - Run TypeScript checks"
echo "  pnpm run lint          - Lint code"
echo "  pnpm run format        - Format code"
echo "  pnpm run docker:up     - Start Docker services"
echo "  pnpm run docker:down   - Stop Docker services"
echo ""
