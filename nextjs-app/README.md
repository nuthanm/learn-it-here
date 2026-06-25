# Learn It Here — Next.js App

Migrated from Streamlit + Supabase → **Next.js 14 (App Router) + Neon DB**.

## Tech stack

| Concern | Choice |
|---|---|
| Framework | Next.js 14 (App Router, TypeScript) |
| Styling | Tailwind CSS + CSS custom properties |
| Database | Neon (serverless PostgreSQL) |
| DB driver | `@neondatabase/serverless` |
| PDF | jsPDF 4.x (server-side, `POST /api/pdf`) |
| Hosting | Vercel (recommended) |

## Project structure

```
nextjs-app/
├── app/
│   ├── api/
│   │   ├── pdf/route.ts           # POST → generate PDF bytes
│   │   ├── requirements/route.ts  # POST → insert project_requirements row
│   │   └── topics/route.ts        # GET / POST → topic_suggestions
│   ├── learning-hub/
│   │   ├── page.tsx               # Server wrapper (Suspense boundary)
│   │   └── LearningHubClient.tsx  # Client — sidebar + content router
│   ├── projectrequirements/
│   │   ├── page.tsx               # Server wrapper
│   │   └── RequirementsForm.tsx   # Client form component
│   ├── layout.tsx                 # Root layout (header + footer)
│   └── page.tsx                   # Landing page (/)
├── components/
│   ├── CodeBlock.tsx              # Syntax-highlighted code block with copy button
│   ├── ContentTable.tsx           # Styled table for learning content
│   ├── SiteHeader.tsx             # Responsive nav header
│   ├── SiteFooter.tsx             # Footer
│   └── TopicSuggestions.tsx       # Tag cloud + inline suggestion form
├── content/                       # Per-topic TSX components (learning content)
│   ├── git/index.tsx              # Git Basics + Branching
│   ├── unit-testing/index.tsx     # TDD, Unit Test, Integration Test
│   ├── blazor/index.tsx           # Blazor + subsections
│   ├── sql-developer/index.tsx    # SQL Developer + query comparison
│   ├── VisualStudio.tsx
│   ├── VSCode.tsx
│   ├── EFCoreOracle.tsx
│   ├── DotNet.tsx
│   ├── Linq.tsx
│   └── CSharp.tsx
├── db/
│   └── schema.sql                 # Neon DB schema (run once)
├── lib/
│   ├── db.ts                      # Neon connection helper
│   ├── learn-sections.ts          # LEARN_SECTIONS config (mirrors config.py)
│   ├── steps.ts                   # Questionnaire STEPS config
│   └── types.ts                   # Shared TypeScript types
├── scripts/
│   └── migrate-supabase-to-neon.ts  # One-time data migration
└── .env.local.example             # Required environment variables
```

## Getting started

### 1. Clone and install

```bash
cd nextjs-app
npm install
```

### 2. Configure environment

```bash
cp .env.local.example .env.local
# Edit .env.local and set DATABASE_URL to your Neon connection string
```

### 3. Provision the Neon database

Run `db/schema.sql` in the [Neon SQL Editor](https://console.neon.tech):

```sql
-- paste contents of db/schema.sql
```

### 4. Run locally

```bash
npm run dev
# → http://localhost:3000
```

## URL scheme (identical to Streamlit version)

| Path | Page |
|---|---|
| `/` | Landing |
| `/projectrequirements` | Requirements questionnaire |
| `/learning-hub?section=git` | Learning Hub — GIT overview |
| `/learning-hub?section=git&sub=basics` | Learning Hub — GIT Basics |

Legacy `?page=…` / `?go=home` links are redirected automatically via `next.config.mjs`.

## Data migration (Supabase → Neon)

See `scripts/migrate-supabase-to-neon.ts` for a step-by-step idempotent migration script.

```bash
SUPABASE_DB_URL="postgresql://postgres:<pw>@db.<ref>.supabase.co:5432/postgres" \
NEON_DATABASE_URL="..." \
  npx ts-node scripts/migrate-supabase-to-neon.ts
```

## Deployment (Vercel)

1. Push this repo to GitHub
2. Import the `nextjs-app` directory into Vercel
3. Set `DATABASE_URL` in Vercel → Project Settings → Environment Variables
4. Deploy — Vercel auto-detects Next.js and configures Edge + Serverless Functions

## Zero-downtime cutover

1. Keep the Streamlit app live until the Next.js deployment is validated
2. Run the migration script to sync historical data
3. Switch DNS / redirect the domain to the Vercel deployment
4. Monitor for 24-48 h, then decommission the Streamlit app
