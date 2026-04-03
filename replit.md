# Workspace

## Overview

pnpm workspace monorepo using TypeScript. Each package manages its own dependencies.

## Stack

- **Monorepo tool**: pnpm workspaces
- **Node.js version**: 24
- **Package manager**: pnpm
- **TypeScript version**: 5.9
- **API framework**: Express 5
- **Database**: PostgreSQL + Drizzle ORM
- **Validation**: Zod (`zod/v4`), `drizzle-zod`
- **API codegen**: Orval (from OpenAPI spec)
- **Build**: esbuild (CJS bundle)

## Structure

```text
artifacts-monorepo/
├── artifacts/              # Deployable applications
│   ├── api-server/         # Express API server
│   └── intro-video/        # AgentScrumMaster animated intro video (React + Framer Motion)
├── lib/                    # Shared libraries
│   ├── api-spec/           # OpenAPI spec + Orval codegen config
│   ├── api-client-react/   # Generated React Query hooks
│   ├── api-zod/            # Generated Zod schemas from OpenAPI
│   └── db/                 # Drizzle ORM schema + DB connection
├── scripts/                # Utility scripts (single workspace package)
│   └── src/                # Individual .ts scripts, run via `pnpm --filter @workspace/scripts run <script>`
├── pnpm-workspace.yaml     # pnpm workspace (artifacts/*, lib/*, lib/integrations/*, scripts)
├── tsconfig.base.json      # Shared TS options (composite, bundler resolution, es2022)
├── tsconfig.json           # Root TS project references
└── package.json            # Root package with hoisted devDeps
```

## TypeScript & Composite Projects

Every package extends `tsconfig.base.json` which sets `composite: true`. The root `tsconfig.json` lists all packages as project references. This means:

- **Always typecheck from the root** — run `pnpm run typecheck` (which runs `tsc --build --emitDeclarationOnly`). This builds the full dependency graph so that cross-package imports resolve correctly. Running `tsc` inside a single package will fail if its dependencies haven't been built yet.
- **`emitDeclarationOnly`** — we only emit `.d.ts` files during typecheck; actual JS bundling is handled by esbuild/tsx/vite...etc, not `tsc`.
- **Project references** — when package A depends on package B, A's `tsconfig.json` must list B in its `references` array. `tsc --build` uses this to determine build order and skip up-to-date packages.

## Root Scripts

- `pnpm run build` — runs `typecheck` first, then recursively runs `build` in all packages that define it
- `pnpm run typecheck` — runs `tsc --build --emitDeclarationOnly` using project references
- `pnpm run lint` — check code formatting with Prettier
- `pnpm run format` — auto-format code with Prettier
- `pnpm run docker:up` — start all Docker services (API + DB + Web)
- `pnpm run docker:down` — stop Docker services
- `pnpm run docker:logs` — tail Docker service logs
- `pnpm run setup` — full dev environment setup script
- `pnpm run healthcheck` — check health of all running services
- `pnpm run release <version>` — create a tagged release (triggers deploy pipeline)

## DevOps

### CI/CD (GitHub Actions)
- `.github/workflows/ci.yml` — runs on push/PR to main/develop: lint, typecheck, build, security audit, Docker build
- `.github/workflows/deploy.yml` — triggered by version tags (`v*`): builds and pushes Docker images to GHCR, deploys to staging/production
- `.github/workflows/pr-checks.yml` — PR quality gates: bundle size report, commit message check

### Docker
- `devops/docker/Dockerfile.api` — multi-stage build for API server (Node.js Alpine, non-root user, healthcheck)
- `devops/docker/Dockerfile.web` — multi-stage build for intro video (Nginx Alpine, gzip, SPA routing)
- `devops/docker/docker-compose.yml` — full stack: PostgreSQL 16, API server, intro video site
- `devops/docker/nginx.conf` — production Nginx config with caching, gzip, SPA fallback

### Scripts
- `devops/scripts/setup.sh` — automated dev environment bootstrap
- `devops/scripts/healthcheck.sh` — service health verification with retries
- `devops/scripts/release.sh` — semver tag creation and push

### Code Quality
- `.prettierrc` — Prettier config (semicolons, double quotes, 100 char width)
- `.prettierignore` — Prettier ignore rules
- `.github/PULL_REQUEST_TEMPLATE.md` — PR template with checklist
- `.github/CODEOWNERS` — automatic reviewer assignments
- `.env.example` — environment variable template

## Packages

### `artifacts/api-server` (`@workspace/api-server`)

Express 5 API server. Routes live in `src/routes/` and use `@workspace/api-zod` for request and response validation and `@workspace/db` for persistence.

- Entry: `src/index.ts` — reads `PORT`, starts Express
- App setup: `src/app.ts` — mounts CORS, JSON/urlencoded parsing, routes at `/api`
- Routes: `src/routes/index.ts` mounts sub-routers; `src/routes/health.ts` exposes `GET /health` (full path: `/api/health`)
- Depends on: `@workspace/db`, `@workspace/api-zod`
- `pnpm --filter @workspace/api-server run dev` — run the dev server
- `pnpm --filter @workspace/api-server run build` — production esbuild bundle (`dist/index.cjs`)
- Build bundles an allowlist of deps (express, cors, pg, drizzle-orm, zod, etc.) and externalizes the rest

### `lib/db` (`@workspace/db`)

Database layer using Drizzle ORM with PostgreSQL. Exports a Drizzle client instance and schema models.

- `src/index.ts` — creates a `Pool` + Drizzle instance, exports schema
- `src/schema/index.ts` — barrel re-export of all models
- `src/schema/<modelname>.ts` — table definitions with `drizzle-zod` insert schemas (no models definitions exist right now)
- `drizzle.config.ts` — Drizzle Kit config (requires `DATABASE_URL`, automatically provided by Replit)
- Exports: `.` (pool, db, schema), `./schema` (schema only)

Production migrations are handled by Replit when publishing. In development, we just use `pnpm --filter @workspace/db run push`, and we fallback to `pnpm --filter @workspace/db run push-force`.

### `lib/api-spec` (`@workspace/api-spec`)

Owns the OpenAPI 3.1 spec (`openapi.yaml`) and the Orval config (`orval.config.ts`). Running codegen produces output into two sibling packages:

1. `lib/api-client-react/src/generated/` — React Query hooks + fetch client
2. `lib/api-zod/src/generated/` — Zod schemas

Run codegen: `pnpm --filter @workspace/api-spec run codegen`

### `lib/api-zod` (`@workspace/api-zod`)

Generated Zod schemas from the OpenAPI spec (e.g. `HealthCheckResponse`). Used by `api-server` for response validation.

### `lib/api-client-react` (`@workspace/api-client-react`)

Generated React Query hooks and fetch client from the OpenAPI spec (e.g. `useHealthCheck`, `healthCheck`).

### `scripts` (`@workspace/scripts`)

Utility scripts package. Each script is a `.ts` file in `src/` with a corresponding npm script in `package.json`. Run scripts via `pnpm --filter @workspace/scripts run <script>`. Scripts can import any workspace package (e.g., `@workspace/db`) by adding it as a dependency in `scripts/package.json`.

## Agentic Scrum Master (Python Backend)

Standalone Python 3.11 FastAPI backend at `agentic-scrum-master/`. Implements an AI-powered Scrum facilitation agent.

### Structure

```text
agentic-scrum-master/
├── agents/              # Agent implementations (base, standup, blocker, summary)
├── api/routes/          # FastAPI route handlers
├── core/                # Config, logging, exceptions
├── models/              # Domain entities (StandupUpdate, DailySummary)
├── schemas/             # Pydantic request/response schemas
├── services/            # Business logic (StandupService)
├── utils/               # Dependency injection helpers
├── tests/               # pytest test suite (agents, services, API)
├── main.py              # Entry point
└── requirements.txt     # Python dependencies
```

### Running

```bash
cd agentic-scrum-master
pip install -r requirements.txt
python main.py              # Starts on http://0.0.0.0:8000
python -m pytest tests/ -v  # Run test suite
```

### API Endpoints

- `GET  /api/healthz` — Health check
- `POST /api/standups` — Submit standup update (auto-detects blockers)
- `GET  /api/standups` — List updates by team/date
- `GET  /api/standups/{id}` — Get specific update
- `POST /api/standups/summary` — Generate daily summary
- `GET  /api/standups/summary/{team_id}` — Get cached summary

### Architecture

- **StandupAgent** → orchestrates update processing, delegates to BlockerAgent
- **BlockerAgent** → keyword + pattern-based blocker detection from text
- **SummaryAgent** → aggregates team updates into daily summaries
- **StandupService** → service layer managing agent pipelines + in-memory storage
- In-memory storage (Phase 1); persistent DB planned for future phase
