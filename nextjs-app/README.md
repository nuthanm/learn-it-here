# Learn It Here — Next.js App

> **Migrated from Streamlit + Supabase → Next.js 14 (App Router) + Neon DB**

A minimalist, fully-responsive web app that helps developers know their project stack before they start. Answer 8 targeted questions, download a branded PDF brief, and jump into curated learning guides matched to your exact tools and versions.

---

## ✨ What it does

| Feature | Detail |
|---|---|
| **Hero landing page** | Animated 🐼 panda, bold headline, CTAs, stat strip, topic preview grid |
| **Requirements questionnaire** | 8 questions across 4 sections — version control, IDE, deployment, architecture, patterns, ORM, and notes |
| **PDF export** | Server-side jsPDF — download a branded brief instantly after submission |
| **Neon DB persistence** | Responses saved to PostgreSQL via `@neondatabase/serverless` |
| **Learning hub** | 11 curated topic guides with sidebar navigation, sub-topic tabs and breadcrumbs |
| **Topic suggestions** | Community tag-cloud — suggest and vote on new topics |
| **Progress tracking** | Live answer-count progress bar on the questionnaire |
| **Mobile-responsive** | Sticky header, mobile topic picker in learning hub, fluid layouts |

---

## 🛠 Tech Stack

| Concern | Choice |
|---|---|
| **Framework** | Next.js 14 (App Router, TypeScript) |
| **Styling** | Tailwind CSS + CSS custom properties (design tokens) |
| **Database** | [Neon](https://neon.tech) (serverless PostgreSQL) |
| **DB driver** | `@neondatabase/serverless` |
| **PDF** | jsPDF 4.x (`POST /api/pdf`) |
| **Hosting** | Vercel (recommended) |
| **Language** | TypeScript 5 |

---

## 🗂 Project Structure

```
nextjs-app/
├── app/
│   ├── globals.css                    # Design tokens, animations, utility classes
│   ├── layout.tsx                     # Root layout — sticky header + footer
│   ├── page.tsx                       # Landing page — hero, how-it-works, topics grid, CTA banner
│   ├── api/
│   │   ├── pdf/route.ts               # POST → generate PDF bytes (jsPDF)
│   │   ├── requirements/route.ts      # POST → insert project_requirements row
│   │   └── topics/route.ts            # GET / POST → topic_suggestions
│   ├── learning-hub/
│   │   ├── page.tsx                   # Server wrapper with Suspense boundary
│   │   └── LearningHubClient.tsx      # Sidebar + sub-topic tabs + content router
│   └── projectrequirements/
│       ├── page.tsx                   # Page header with section pills
│       └── RequirementsForm.tsx       # Multi-section form with live progress bar
├── components/
│   ├── CodeBlock.tsx                  # Dark code block with copy button
│   ├── ContentTable.tsx               # Styled table for learning content
│   ├── SiteHeader.tsx                 # Sticky nav with mobile hamburger
│   ├── SiteFooter.tsx                 # Footer with links and tech attribution
│   └── TopicSuggestions.tsx          # Tag cloud + inline suggestion form
├── content/                           # Per-topic TSX learning content components
│   ├── git/index.tsx                  # Git overview, Basics, Branching
│   ├── unit-testing/index.tsx         # TDD, Unit Test, Integration Test
│   ├── blazor/index.tsx               # Blazor + Web Forms, Fluent UI, CQRS, Oracle
│   ├── sql-developer/index.tsx        # SQL Developer + cross-DB query comparison
│   ├── VisualStudio.tsx
│   ├── VSCode.tsx
│   ├── EFCoreOracle.tsx
│   ├── DotNet.tsx
│   ├── Linq.tsx
│   └── CSharp.tsx
├── db/
│   └── schema.sql                     # Neon DB schema (run once to provision)
├── lib/
│   ├── db.ts                          # Neon connection helper
│   ├── learn-sections.ts              # LEARN_SECTIONS — topic/subsection registry
│   ├── steps.ts                       # STEPS — questionnaire definition
│   └── types.ts                       # Shared TypeScript interfaces
├── scripts/
│   └── migrate-supabase-to-neon.ts    # One-time data migration script
├── .env.local.example                 # Required environment variables
└── README.md
```

---

## 🔗 URL Scheme

| Path | Page |
|---|---|
| `/` | Landing page |
| `/projectrequirements` | Requirements questionnaire |
| `/learning-hub` | Learning hub — default section (GIT) |
| `/learning-hub?section=git` | GIT overview |
| `/learning-hub?section=git&sub=basics` | GIT — Basics sub-page |
| `/learning-hub?section=blazor&sub=cqrs` | Blazor — CQRS sub-page |
| `/learning-hub?section=topic-suggestions` | Community topic suggestions |

Legacy `?page=…` / `?go=home` links are redirected automatically via `next.config.mjs`.

---

## 🚀 Getting Started

### 1. Install

```bash
cd nextjs-app
npm install
```

### 2. Configure environment

```bash
cp .env.local.example .env.local
# Edit .env.local and set DATABASE_URL to your Neon connection string
```

### 3. Provision the database

Open the [Neon SQL Editor](https://console.neon.tech) and run `db/schema.sql`:

```sql
-- paste contents of db/schema.sql
```

### 4. Run locally

```bash
npm run dev
# → http://localhost:3000
```

### 5. Build for production

```bash
npm run build
npm start
```

---

## 🗄 Database (Neon)

Two tables are created by `db/schema.sql`:

**`project_requirements`** — stores questionnaire responses

**`topic_suggestions`** — stores community topic requests

> Without a `DATABASE_URL` the app still works — form submissions fail gracefully and the PDF download is always available.

---

## ☁️ Deployment (Vercel)

1. Push this repo to GitHub
2. Import the `nextjs-app` sub-directory (or the whole repo) into Vercel
3. Set `DATABASE_URL` in **Vercel → Project Settings → Environment Variables**
4. Deploy — Vercel auto-detects Next.js and configures Edge + Serverless Functions

---

## 🔄 Data Migration (Supabase → Neon)

```bash
SUPABASE_DB_URL="postgresql://postgres:<pw>@db.<ref>.supabase.co:5432/postgres" \
NEON_DATABASE_URL="postgresql://..." \
  npx ts-node scripts/migrate-supabase-to-neon.ts
```

---

## 📋 Requirements Questionnaire — Topics

| # | Question | Type |
|---|---|---|
| 1 | Version control (Git / SVN / TFS…) | Single-select |
| 2 | How do you push code? | Single-select |
| 3 | IDE or editor | Single-select |
| 4 | Deployment approaches | Multi-select |
| 5 | Architecture patterns | Multi-select |
| 6 | Design patterns | Multi-select |
| 7 | ORM framework | Single-select |
| 8 | Additional notes | Free text |

---

## 🎓 Learning Hub — Topics

| Icon | Topic | Sub-topics |
|---|---|---|
| 🌿 | **GIT** | Basics, Branching |
| 🔷 | **Visual Studio IDE** | — |
| 🟦 | **VS Code** | — |
| 🗄 | **EF Core + Oracle** | — |
| 🔵 | **.NET** | — |
| ✅ | **Unit Testing** | TDD, Unit Test, Integration Test |
| 🔗 | **LINQ** | — |
| ⚡ | **Blazor** | Web Forms vs Blazor, Fluent UI, Oracle EF Core Dapper, CQRS |
| 🎯 | **C#** | — |
| 🐘 | **SQL Developer** | SQL Server vs Oracle vs PostgreSQL |
| 💡 | **Topic Suggestions** | Community tag cloud |

---

## 📜 License

Open-source — free to adapt for your team's needs.

