# 🐼 Learn It Here

**Learn It Here** is a multi-page Streamlit web app that helps developers know their
project stack before they start. Capture project requirements with a targeted
questionnaire, then dive into curated learning guides matched to your exact tools and
versions. Responses are stored in **Supabase (PostgreSQL)** and can be exported as a
**PDF report** with a single click.

---

## ✨ Features

| Feature | Detail |
|---|---|
| **Landing page** | Hero layout with animated 🐼 panda mascot and two CTAs |
| **8-question requirements form** | Covers version control, IDE, code push method, deployment, architecture, design patterns, ORM, and additional notes |
| **PDF export** | Professional PDF generated on submission (no server needed) |
| **Supabase storage** | Responses persisted in PostgreSQL via Supabase |
| **Learning hub** | 9 curated topic guides: GIT, Visual Studio IDE, VS Code, EF Core + Oracle, .NET, Unit Testing, LINQ, Blazor, and C# |
| **Suggest a topic** | Users can suggest new topics directly from the learning hub |
| **Animated panda mascot** | Kung Fu Panda–style Po with 5 cycling expressions (happy, excited, thinking, wink, determined) |
| **Responsive design** | Panda-themed palette (black / white / bamboo green), fully mobile-responsive |

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **UI / Frontend** | [Streamlit](https://streamlit.io) |
| **Database** | [Supabase](https://supabase.com) (PostgreSQL) |
| **PDF Generation** | [fpdf2](https://py-fpdf2.readthedocs.io) |
| **Deployment** | [Streamlit Community Cloud](https://share.streamlit.io) + Supabase |
| **Language** | Python 3.10+ |

---

## 📝 Requirements Form — Questions Covered

| # | Topic |
|---|---|
| 1 | **Version Control** — GitHub / Azure DevOps / Bitbucket / GitLab |
| 2 | **IDE / Editor** — Visual Studio / VS Code / JetBrains Rider / Other |
| 3 | **Code Push Method** — Git CLI / IDE Git integration / GitHub Desktop / Other |
| 4 | **Deployment Approaches** — CI/CD pipelines, cloud targets, manual deploy (multi-select) |
| 5 | **Architecture Patterns** — Clean Architecture, CQRS, DDD, MVC, Microservices… (multi-select) |
| 6 | **Design Patterns** — Repository, Unit of Work, Factory, Singleton… (multi-select) |
| 7 | **ORM** — EF Core, Dapper, ADO.NET, SQLAlchemy, Prisma… |
| 8 | **Additional Requirements** — Any other tools, frameworks, or notes |

---

## 🎓 Learning Hub — Topics Available

| Topic | Highlights |
|---|---|
| **GIT** | Daily workflow, branching, rebasing, useful inspection commands |
| **Visual Studio IDE** | Shortcuts, extensions, debugging tips |
| **VS Code** | Settings, extensions, keyboard shortcuts |
| **EF Core + Oracle** | Fluent API, Oracle-specific configuration, migrations |
| **.NET** | Platform overview, LTS versions, tooling |
| **Unit Testing** | xUnit vs NUnit vs MSTest, mocking, best practices |
| **LINQ** | Deferred vs immediate execution, common operators, query syntax |
| **Blazor** | Blazor Server vs WebAssembly vs Web App, component model |
| **C#** | Language versions, value/reference types, generics, async/await, pattern matching |

New topics can be suggested via the **"Suggest a Topic"** button inside the learning hub.

---

## 🚀 Local Development

### Prerequisites

- Python 3.10+
- A [Supabase](https://supabase.com) account (free tier works)

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/nuthanm/learn-it-here.git
cd learn-it-here

# 2. Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure secrets
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
copy .streamlit/secrets.toml.example .streamlit/secrets.toml  # Windows
# Edit .streamlit/secrets.toml and add your Supabase URL + key
```

### Configure Supabase Secrets

Edit `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "https://your-project-ref.supabase.co"
SUPABASE_KEY = "your-anon-public-key"
```

> ⚠️ **Never commit `secrets.toml`** — it is already in `.gitignore`.

### Run the App

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🗄 Database Setup (Supabase)

1. Create a new project at [supabase.com](https://supabase.com).
2. Open **SQL Editor** in your Supabase dashboard.
3. Run the contents of [`database/schema.sql`](database/schema.sql).
4. Copy your **Project URL** and **anon public key** from
   *Project Settings → API* into your secrets file.

The table `project_requirements` will be created with Row Level Security enabled:
- **Anon** users can **INSERT** (submit responses via the app).
- **Authenticated** users can **SELECT** (view responses in the dashboard).

---

## ☁️ Deployment

### Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Select your repo, branch (`main`), and `app.py` as the main file.
4. Click **Advanced settings → Secrets** and paste:
   ```toml
   SUPABASE_URL = "https://your-project-ref.supabase.co"
   SUPABASE_KEY = "your-anon-public-key"
   ```
5. Click **Deploy**.

The app will be live at `https://your-app-name.streamlit.app`.

> **Without Supabase credentials** the app still works — responses are not saved
> to the database but the PDF download is always available.

---

## 📁 Project Structure

```
learn-it-here/
├── app.py                          # Entry point — page config + routing (~30 lines)
├── config.py                       # Constants (menu items, session-state defaults, nav helpers)
├── requirements.txt                # Python dependencies (streamlit, supabase, fpdf2)
├── styles/
│   └── theme.css                   # All application CSS (panda palette, responsive layout)
├── components/
│   ├── css.py                      # inject_css() — reads theme.css and injects it via st.markdown
│   ├── panda.py                    # Animated panda HTML helpers (landing, robot, sitting states)
│   ├── footer.py                   # Footer, scroll-nav, and copy-button HTML helpers
│   └── dialogs.py                  # Suggest-a-topic dialog (@st.dialog)
├── pages/
│   ├── landing.py                  # page_landing() — hero layout with panda mascot
│   ├── requirements.py             # page_requirements() — 8-question form + PDF export
│   └── learn/
│       ├── __init__.py             # page_learn() — sidebar nav + routing to section modules
│       ├── git.py                  # render_git()
│       ├── visual_studio.py        # render_visual_studio()
│       ├── vscode.py               # render_vscode()
│       ├── efcore.py               # render_efcore()
│       ├── dotnet.py               # render_dotnet()
│       ├── unit_testing.py         # render_unit_testing()
│       ├── linq.py                 # render_linq()
│       ├── blazor.py               # render_blazor()
│       ├── csharp.py               # render_csharp()
│       └── topic_suggestions.py    # render_topic_suggestions()
├── services/
│   ├── supabase_client.py          # Supabase helpers (save responses, topic suggestions, fetch)
│   └── pdf_service.py              # PDF generation (generate_pdf, _safe)
├── database/
│   └── schema.sql                  # Supabase PostgreSQL table schema
├── .streamlit/
│   ├── config.toml                 # Streamlit theme & server config
│   └── secrets.toml.example        # Credentials template (copy → secrets.toml)
└── README.md
```

### Architecture principles applied

| Principle | How it applies |
|---|---|
| **Separation of Concerns** | UI (`pages/`, `components/`), data (`services/`), and config are fully decoupled |
| **Single Responsibility** | Each module has one job — `pdf_service.py` knows nothing about Supabase |
| **DRY** | CSS lives in one file; shared HTML helpers live in `components/`; Supabase credentials fetched in one place |
| **Open/Closed** | Adding a new learning section = one new file in `pages/learn/` + one entry in `config.py` |

---

## 🔗 Reference Links

| Topic | Link |
|---|---|
| C# Language Versioning | https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-versioning |
| EF Core — What's New | https://learn.microsoft.com/en-us/ef/core/what-is-new/ |
| Streamlit Docs | https://docs.streamlit.io |
| Supabase Docs | https://supabase.com/docs |
| fpdf2 Docs | https://py-fpdf2.readthedocs.io |

---

## 📜 License

This project is open-source. Feel free to adapt it for your team's needs.
