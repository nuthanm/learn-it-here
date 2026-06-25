# 🐼 Learn It Here

**Learn It Here** helps developers know their project stack before they start. Capture project requirements with a targeted questionnaire, then dive into curated learning guides matched to your exact tools and versions. Responses are stored in **Neon (PostgreSQL)** and can be exported as a **PDF report** with a single click.

<img width="959" height="369" alt="image" src="https://github.com/user-attachments/assets/9225a4df-6bbb-4436-9dc9-aa04ef92aeed" />

---

## ✨ Features

| Feature | Detail |
|---|---|
| **Landing page** | Hero layout with animated 🐼 panda mascot and two CTAs |
| **8-question requirements form** | Covers version control, IDE, code push method, deployment, architecture, design patterns, ORM, and additional notes |
| **PDF export** | Multi-page-safe PDF with branded header & footer on every page |
| **Neon DB storage** | Responses persisted in serverless PostgreSQL via Neon |
| **Learning hub** | 11 curated topic guides covering GIT (with sub-pages), Visual Studio IDE, VS Code, EF Core + Oracle, .NET, Unit Testing, LINQ, Blazor, C#, SQL Developer, and a Topic Suggestions tag cloud |
| **Suggest a topic** | Users can suggest new topics directly from the learning hub |
| **Animated panda mascot** | Kung Fu Panda–style Po with 5 cycling expressions (happy, excited, thinking, wink, determined) |
| **Responsive design** | Panda-themed palette (black / white / bamboo green), fully mobile-responsive |

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **UI / Frontend** | [Next.js 14](https://nextjs.org) (App Router) + Tailwind CSS |
| **Database** | [Neon](https://neon.tech) (serverless PostgreSQL) |
| **PDF Generation** | jsPDF via Next.js API route |
| **Deployment** | [Vercel](https://vercel.com) |
| **Language** | TypeScript |

---

## 📝 Requirements Form — Questions Covered

| # | Topic |
|---|---|
| 1 | **Version Control** — Git / SVN / TFS / Mercurial / Perforce |
| 2 | **IDE / Editor** — Visual Studio / VS Code / Rider / IntelliJ / others |
| 3 | **Code Push Method** — Git CLI / GitHub Desktop / IDE Git / others |
| 4 | **Deployment Approaches** — CI/CD pipelines, cloud targets, manual deploy (multi-select) |
| 5 | **Architecture Patterns** — Clean Architecture, CQRS, DDD, MVC, Microservices… (multi-select) |
| 6 | **Design Patterns** — Repository, Unit of Work, Factory, Singleton… (multi-select) |
| 7 | **ORM** — EF Core, Dapper, ADO.NET, SQLAlchemy, Prisma… |
| 8 | **Additional Requirements** — Any other tools, frameworks, or notes |

Every "Other" option reveals a free-text input automatically.

---

## 🎓 Learning Hub — Topics Available

| Topic | Highlights |
|---|---|
| **GIT** | Daily workflow, with `Basics` and `Branching` sub-pages |
| **Visual Studio IDE** | Shortcuts, extensions, debugging tips |
| **VS Code** | Settings, extensions, keyboard shortcuts |
| **EF Core + Oracle** | Fluent API, Oracle-specific configuration, migrations |
| **.NET** | Platform overview, LTS versions, tooling |
| **Unit Testing** | xUnit vs NUnit vs MSTest, mocking, best practices |
| **LINQ** | Deferred vs immediate execution, common operators, query syntax |
| **Blazor** | Blazor Server vs WebAssembly vs Web App, component model |
| **C#** | Language versions, value/reference types, generics, async/await, pattern matching |
| **SQL Developer** | Day-to-day SQL workflow tips |
| **Topic Suggestions** | Live tag cloud of community-requested topics |

New topics can be suggested via the **"+ Suggest a topic"** button in the sidebar inside the learning hub.

---

## 🚀 Local Development

### Prerequisites

- Node.js 18+
- A [Neon](https://neon.tech) account (free tier works)

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/nuthanm/learn-it-here.git
cd learn-it-here/nextjs-app

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.local.example .env.local
# Edit .env.local → set DATABASE_URL to your Neon connection string

# 4. Start the dev server
npm run dev
# → http://localhost:3000
```

### Run, build, lint

```bash
npm run dev      # start development server
npm run build    # production build
npm run lint     # ESLint
```

---

## 🗄 Database Setup (Neon)

1. Create a new project at [neon.tech](https://neon.tech).
2. Copy your **connection string** from the Neon dashboard.
3. Set `DATABASE_URL` in your `.env.local` file.
4. Run the schema migrations (see [`nextjs-app/README.md`](./nextjs-app/README.md) for details).

---

## ☁️ Deployment

### Vercel

1. Push this repo to GitHub.
2. Import the project at [vercel.com](https://vercel.com/new).
3. Set the **Root Directory** to `nextjs-app`.
4. Add the `DATABASE_URL` environment variable.
5. Click **Deploy**.

---

## 📁 Project Structure

```
learn-it-here/
└── nextjs-app/          # Next.js 14 App Router application
    ├── app/             # App router pages and API routes
    ├── components/      # React components
    ├── lib/             # Utilities and DB helpers
    ├── public/          # Static assets
    └── README.md        # Full Next.js documentation
```

See [`nextjs-app/README.md`](./nextjs-app/README.md) for the full Next.js documentation.

---

## 🔗 Reference Links

| Topic | Link |
|---|---|
| C# Language Versioning | https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-versioning |
| EF Core — What's New | https://learn.microsoft.com/en-us/ef/core/what-is-new/ |
| Next.js Docs | https://nextjs.org/docs |
| Neon Docs | https://neon.tech/docs |

---

## 📜 License

This project is open-source. Feel free to adapt it for your team's needs.
