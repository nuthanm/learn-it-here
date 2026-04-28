# 🐼 Learn It Here

**Learn It Here** is a multi-page Streamlit web app that helps developers know
their project stack before they start. Capture project requirements with a
targeted questionnaire, then dive into curated learning guides matched to your
exact tools and versions. Responses are stored in **Supabase (PostgreSQL)**
and can be exported as a **PDF report** with a single click.

<img width="959" height="409" alt="image" src="https://github.com/user-attachments/assets/18d96a2f-de04-4292-b5a3-febfac129aa8" />

---

## ✨ Features

| Feature | Detail |
|---|---|
| **Landing page** | Hero layout with animated 🐼 panda mascot and two CTAs |
| **8-question requirements form** | Covers version control, IDE, code push method, deployment, architecture, design patterns, ORM, and additional notes |
| **PDF export** | Multi-page-safe PDF with branded header & footer on every page |
| **Supabase storage** | Responses persisted in PostgreSQL via Supabase |
| **Learning hub** | 11 curated topic guides covering GIT (with sub-pages), Visual Studio IDE, VS Code, EF Core + Oracle, .NET, Unit Testing, LINQ, Blazor, C#, SQL Developer, and a Topic Suggestions tag cloud |
| **Suggest a topic** | Users can suggest new topics directly from the learning hub |
| **Animated panda mascot** | Kung Fu Panda–style Po with 5 cycling expressions (happy, excited, thinking, wink, determined) |
| **Responsive design** | Panda-themed palette (black / white / bamboo green), fully mobile-responsive |

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **UI / Frontend** | [Streamlit](https://streamlit.io) ≥ 1.36, < 2.0 |
| **Database** | [Supabase](https://supabase.com) (PostgreSQL) |
| **PDF Generation** | [fpdf2](https://py-fpdf2.readthedocs.io) ≥ 2.7.9 |
| **Deployment** | [Streamlit Community Cloud](https://share.streamlit.io) + Supabase |
| **Language** | Python 3.10+ |
| **Tooling** | `pytest` for tests, `ruff` for lint + format, `pre-commit` hooks |

---

## 🔗 URL Scheme

The app uses Streamlit's `st.navigation` API for path-based routing. Top-level
pages live at clean single-segment paths; the Learning Hub keeps section /
sub-section selection in the query string.

| Page | URL |
|---|---|
| Landing | `https://learnithere.streamlit.app/` |
| Project Requirements | `https://learnithere.streamlit.app/projectrequirements` |
| Default learning page (GIT) | `https://learnithere.streamlit.app/learning-hub` |
| Learning Hub section | `https://learnithere.streamlit.app/learning-hub?section=git` |
| Learning Hub sub-page | `https://learnithere.streamlit.app/learning-hub?section=git&sub=branching` |

> ⚠️ **Streamlit limitation:** `st.navigation` only supports a **single URL
> path segment per page**, and path segments cannot contain spaces. URLs like
> `/Learning Hub/GIT/Branching` (multiple segments and embedded spaces) are
> therefore not achievable on Streamlit Community Cloud. Section /
> sub-section selection is exposed through query parameters instead.

Legacy URLs from the previous query-string-only routing
(`?page=requirements`, `?page=learn&section=git&sub=branching`, `?go=home`)
are automatically redirected to the new path-based equivalents, so existing
shared links keep working.

---

## 🔗 URL Scheme

The app uses Streamlit's `st.navigation` API for path-based routing. Top-level pages live at clean single-segment paths; the Learning Hub keeps section / sub-section selection in the query string.

| Page | URL |
|---|---|
| Landing | `https://learnithere.streamlit.app/` |
| Project Requirements | `https://learnithere.streamlit.app/projectrequirements` |
| Default learning page (GIT) | `https://learnithere.streamlit.app/learning-hub` |
| Learning Hub section | `https://learnithere.streamlit.app/learning-hub?section=git` |
| Learning Hub sub-page | `https://learnithere.streamlit.app/learning-hub?section=git&sub=branching` |

> ⚠️ **Streamlit limitation:** `st.navigation` only supports a **single URL path segment per page**, and path segments cannot contain spaces. URLs like `/Learning Hub/GIT/Branching` (multiple segments and embedded spaces) are therefore not achievable on Streamlit Community Cloud. Section / sub-section selection is exposed through query parameters instead.

Legacy URLs from the previous query-string-only routing (`?page=requirements`, `?page=learn&section=git&sub=branching`, `?go=home`) are automatically redirected to the new path-based equivalents, so existing shared links keep working.

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

New topics can be suggested via the **"+ Suggest a topic"** button in the
sidebar inside the learning hub.

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

# 3. Install dependencies (editable install + dev tools)
make install
# or, without make:
pip install -e ".[dev]"

# 4. Configure secrets
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml and add your Supabase URL + key
```

### Configure Supabase Secrets

Edit `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "https://your-project-ref.supabase.co"
SUPABASE_KEY = "your-anon-public-key"
```

> ⚠️ **Never commit `secrets.toml`** — it is already in `.gitignore`.

### Run, test, lint

```bash
make run      # streamlit run app.py
make test     # pytest
make lint     # ruff check .
make fmt      # ruff format . && ruff check --fix .
make check    # lint + tests (the CI gate)
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

### Pre-commit hooks (recommended)

```bash
pre-commit install
```

After install, every `git commit` runs ruff + standard hygiene checks
automatically.

---

## 🗄 Database Setup (Supabase)

1. Create a new project at [supabase.com](https://supabase.com).
2. Open **SQL Editor** in your Supabase dashboard.
3. Run the contents of [`database/schema.sql`](database/schema.sql).
4. Copy your **Project URL** and **anon public key** from
   *Project Settings → API* into your secrets file.

Two tables will be created with Row Level Security enabled:

**`project_requirements`** — stores the 8-question form responses:
- **Anon** users can **INSERT** (submit responses via the app).
- **Authenticated** users can **SELECT** (view responses in the dashboard).

**`topic_suggestions`** — stores community topic requests:
- **Anon** users can **INSERT** (submit a suggestion) and **SELECT** (view the leaderboard).
- **Authenticated** users can **SELECT** (view all suggestions).

> ⚠️ If you see `"Could not find the table 'public.topic_suggestions' in the schema cache"`,
> it means the `topic_suggestions` table has not been created yet. Re-run
> [`database/schema.sql`](database/schema.sql) in the Supabase SQL Editor — the
> `CREATE TABLE IF NOT EXISTS` statements are safe to run again.

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

> **Without Supabase credentials** the app still works — responses are not
> saved to the database but the PDF download is always available.

---

## 📁 Project Structure

```
learn-it-here/
├── app.py                          # Entry point — page config + routing (~95 lines)
├── config.py                       # Constants, menu, routing helpers, session defaults
├── models.py                       # RequirementsRecord (TypedDict), SaveResult (dataclass)
├── pyproject.toml                  # Deps, ruff config, pytest config
├── Makefile                        # make run / test / lint / fmt / check
├── requirements.txt                # Pinned deps for Streamlit Cloud (subset of pyproject)
├── .pre-commit-config.yaml         # ruff + hygiene hooks
├── styles/
│   └── theme.css                   # All application CSS (panda palette, responsive layout)
├── components/
│   ├── css.py                      # inject_css() — reads theme.css and injects it via st.markdown
│   ├── content.py                  # section_title / paragraph / code_block / link_list primitives
│   ├── forms.py                    # select_with_other / multiselect_with_other widget helpers
│   ├── header.py                   # site_header_html() — slim brand + nav
│   ├── footer.py                   # footer_html / scroll_nav_html / copy_buttons_html
│   ├── panda.py                    # Animated panda HTML/SVG (landing, robot, sitting states)
│   └── dialogs.py                  # suggest_topic_dialog (@st.dialog)
├── pages/
│   ├── landing.py                  # page_landing()
│   ├── requirements.py             # page_requirements() — 8-question form + PDF export
│   └── learn/
│       ├── __init__.py             # page_learn() — sidebar nav + routing to topic modules
│       ├── git/
│       │   ├── __init__.py         # render_git()
│       │   ├── basics.py           # render() — sub-page
│       │   └── branching.py        # render() — sub-page
│       ├── visual_studio.py        # render_visual_studio()
│       ├── vscode.py               # render_vscode()
│       ├── efcore.py               # render_efcore()
│       ├── dotnet.py               # render_dotnet()
│       ├── unit_testing.py         # render_unit_testing()
│       ├── linq.py                 # render_linq()
│       ├── blazor.py               # render_blazor()
│       ├── blazor_webforms_comparison.py
│       ├── csharp.py               # render_csharp()
│       ├── sql_developer.py        # render_sql_developer()
│       └── topic_suggestions.py    # render_topic_suggestions()
├── services/
│   ├── supabase_client.py          # Cached client + save_requirements / save_topic / fetch_topics
│   └── pdf_service.py              # RequirementsPDF class + generate_pdf()
├── database/
│   └── schema.sql                  # Supabase PostgreSQL table schema
├── tests/
│   ├── conftest.py                 # Adds project root to sys.path
│   ├── test_models.py              # SaveResult / RequirementsRecord
│   ├── test_pdf.py                 # PDF generation, multi-page header/footer
│   ├── test_routing.py             # url_for + find_section + find_subsection
│   └── test_forms.py               # form-widget helper signatures
├── .streamlit/
│   ├── config.toml                 # Streamlit theme & server config
│   └── secrets.toml.example        # Credentials template (copy → secrets.toml)
└── README.md
```

### Architecture principles applied

| Principle | How it applies |
|---|---|
| **Separation of Concerns** | UI (`pages/`, `components/`), data (`services/`), domain (`models.py`), and config are fully decoupled |
| **Single Responsibility** | Each module has one job — `pdf_service.py` knows nothing about Supabase |
| **DRY** | CSS lives in one file; shared HTML helpers live in `components/`; the "select-or-Other" pattern is one helper, not five copies |
| **Open/Closed** | Adding a new learning section = one new file in `pages/learn/` + one entry in `LEARN_SECTIONS` |
| **Cached I/O** | `@st.cache_resource` for the Supabase client, `@st.cache_data(ttl=60)` for the topic-suggestions feed |

### Public API conventions

- Modules under `services/` expose **domain-named** functions (`save_requirements`, `save_topic`) and return a `SaveResult` dataclass — never a raw `(bool, str)` tuple.
- Helpers under `config.py` and `components/` use **public names** (`url_for`, `nav_to`, `site_header_html`). Older underscore-prefixed names (`_url_for`, `_nav_to`, `_site_header_html`, …) are kept as aliases for backwards compatibility but new code should use the public names.
- Anything injected via `st.markdown(..., unsafe_allow_html=True)` from a user-controlled source goes through `html.escape()` first.

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
