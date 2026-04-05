# 📋 Learn it here

A **professional, single-page Streamlit web app** that captures all key tech-stack
questions before a project kicks off. Responses are stored in **Supabase (PostgreSQL)**
and can be exported as a **PDF report** with a single click.

<img width="958" height="412" alt="image" src="https://github.com/user-attachments/assets/7bf54542-d385-45a5-99f5-52a64b917bc4" />

---

## ✨ Features

| Feature | Detail |
|---|---|
| **12-question form** | Covers version control, IDE, .NET/C#, EF Core, architecture, deployment, reporting, testing, logging, project management, unit testing, and code quality |
| **Animated robot mascot** | Welcome → Thinking → Bye states with smooth CSS animations |
| **PDF export** | Professional PDF generated on submission (no server needed) |
| **Supabase storage** | Responses persisted in PostgreSQL via Supabase |
| **Minimalistic design** | Clean blue-white palette, card layout, fully responsive |

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

## 📝 Questions Covered

| # | Topic | Reference |
|---|---|---|
| 1 | **Version Control** — GitHub / Azure DevOps / Bitbucket / GitLab | Git is used locally for all platforms |
| 2 | **IDE / Editor** — Visual Studio vs VS Code | Always use the latest version |
| 3 | **C# & .NET Version** — .NET 9 → C# 13, .NET 8 → C# 12 | [Language versioning](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-versioning) |
| 4 | **EF Core Version** | [What's new in EF Core](https://learn.microsoft.com/en-us/ef/core/what-is-new/) |
| 5 | **Application Architecture & Design Patterns** — Clean Arch, CQRS, DDD, MVC… | |
| 6 | **Deployment Process** — CI/CD pipeline, environments | |
| 7 | **Crystal Reports** — Required / Not required / Under consideration | |
| 8 | **Local Testing Feasibility** — Full / Partial / Deployment-only | |
| 9 | **Logging / Tracing Tools** — App Insights, Serilog, ELK, Splunk… | |
| 10 | **Project Management Tool** — Azure DevOps Boards / JIRA | |
| 11 | **Unit Testing Framework** — xUnit / NUnit / MSTest | |
| 12 | **Code Quality / Static Analysis** — SonarQube (mandatory / optional) | |

---

## 🚀 Local Development

### Prerequisites

- Python 3.10+
- A [Supabase](https://supabase.com) account (free tier works)

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/nuthanm/project-requirements.git
cd project-requirements

# 2. Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure secrets
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
copy .streamlit/secrets.toml.example .streamlit/secrets.toml # for windows
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
project-requirements/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── database/
│   └── schema.sql                  # Supabase PostgreSQL table schema
├── .streamlit/
│   ├── config.toml                 # Streamlit theme & server config
│   └── secrets.toml.example        # Credentials template (copy → secrets.toml)
└── README.md
```

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
