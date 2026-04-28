from components.content import (
    code_block,
    link_list,
    paragraph,
    section_intro,
    section_title,
    subsection,
)


def render_git():
    section_title("GIT", "Version control for collaborative software development.")
    section_intro(
        "Git is a distributed version control system that tracks changes in source code. "
        "It lets multiple developers collaborate simultaneously, maintains a complete history "
        "of every change, and supports powerful branching and merging workflows."
    )

    subsection("What is GIT?")
    paragraph(
        "Git lives on your machine. The cloud platforms like GitHub, Azure DevOps, Bitbucket, "
        "and GitLab are hosting services that store your Git repositories and add collaboration "
        "features like pull requests, pipelines, and boards."
    )

    subsection("Real-world example — Your first day on a team project")
    paragraph(
        "You just joined a company building an online shopping website. Five other developers are "
        "already working on it. Your task: add a Forgot Password feature. Without Git, you would copy "
        "the entire project folder, make changes, and then try to manually merge your changes back — "
        "a nightmare when five people do this at once. Git solves this entirely."
    )
    paragraph("Step 1 — Get the project onto your laptop:")
    code_block(
        "git clone https://github.com/mycompany/shopping-website.git\ncd shopping-website",
        language="bash"
    )
    paragraph("Now you have a full copy of the project. Everyone else is working on their own copies too.")
    paragraph("Step 2 — Create your own workspace (branch) so you don't disturb others:")
    code_block("git checkout -b feature/forgot-password", language="bash")
    paragraph("Think of a branch like a personal notebook. Your changes go here without touching the main codebase.")
    paragraph("Step 3 — Write your code. Then save your progress:")
    code_block('git add .\ngit commit -m "feat: add forgot password email flow"', language="bash")
    paragraph("A commit is like a save point in a video game — you can always go back to it.")
    paragraph("Step 4 — Share your work with the team:")
    code_block("git push origin feature/forgot-password", language="bash")
    paragraph(
        "Your branch is now on GitHub or Azure DevOps. You open a Pull Request and a teammate reviews it. "
        "After approval it gets merged into the main codebase — safely, with a full history of every change "
        "you made. If your code breaks something, Git lets the team roll back to the last good state in seconds. "
        "No files are ever lost."
    )

    subsection("Supported platforms")
    paragraph(
        "Git works the same way locally regardless of which platform hosts your remote repository. "
        "Each platform adds its own collaboration and CI/CD features on top."
    )
    link_list([
        "GitHub — Open-source leader, GitHub Actions CI/CD, GitHub Copilot",
        "Azure DevOps — Microsoft ecosystem, Boards, Pipelines, Repos",
        "Bitbucket — Atlassian ecosystem, integrates with JIRA natively",
        "GitLab — All-in-one DevOps platform, built-in CI/CD pipelines",
    ])

    subsection("Workflow")
    paragraph(
        "Clone or Pull → Create Branch → Write Code → Stage Changes → Commit → "
        "Push → Pull Request → Code Review → Merge."
    )

    subsection("Starting out")
    code_block(
        """# Clone the repository to your local machine
git clone https://github.com/your-org/your-repo.git

# Navigate into the project folder
cd your-repo

# Check current branch and status
git status
git branch""",
        language="bash"
    )

    subsection("Daily workflow")
    code_block(
        """# Always pull latest changes before starting work
git fetch origin
git pull origin main

# Create and switch to a new feature branch
git checkout -b feature/my-feature-name

# See what has changed
git status
git diff

# Stage your changes (all files, or a specific file)
git add .
git add src/MyFile.cs

# Commit with a clear message
git commit -m "feat: add user login endpoint"

# Push your branch to the remote
git push origin feature/my-feature-name""",
        language="bash"
    )

    subsection("Keeping your branch up to date")
    code_block(
        """# Option 1: Rebase on main (keeps history clean — preferred)
git fetch origin
git rebase origin/main

# Option 2: Merge main into your branch
git merge origin/main

# Undo staged changes (before commit)
git reset HEAD src/MyFile.cs

# Temporarily stash unfinished work and come back later
git stash
git stash pop""",
        language="bash"
    )

    subsection("Useful inspection commands")
    code_block(
        """# Last 10 commits on current branch
git log --oneline -10

# See changes between your branch and main
git diff main..HEAD

# Show all local and remote branches
git branch -a

# Delete a local branch after merging
git branch -d feature/my-feature-name""",
        language="bash"
    )

    subsection("Real-world example — Fixing a bug while someone else adds a feature")
    paragraph(
        "Your teammate Alice is adding a new payment page. At the same time, your manager calls "
        "and says the login button is broken in production — fix it NOW! You don't want to disturb "
        "Alice's half-finished payment work."
    )
    paragraph("1. Get the very latest code:")
    code_block("git fetch origin\ngit pull origin main", language="bash")
    paragraph("2. Create a hotfix branch — completely separate from Alice's work:")
    code_block("git checkout -b hotfix/login-button-not-working", language="bash")
    paragraph("3. Fix the bug in LoginController.cs, then save and share:")
    code_block(
        """git add src/Controllers/LoginController.cs
git commit -m "fix: login button now submits form correctly"
git push origin hotfix/login-button-not-working""",
        language="bash"
    )
    paragraph("4. After your hotfix is merged, get Alice's latest changes too:")
    code_block("git fetch origin\ngit rebase origin/main", language="bash")
    paragraph(
        "Both changes are now in the main codebase — no conflicts, no overwriting each other's work. "
        "Git tracked every line changed by everyone, independently."
    )
    paragraph(
        "Stash — save unfinished work temporarily: Suppose while you were mid-way through a new feature "
        "your boss asks you to quickly check something on another branch."
    )
    code_block(
        """git stash          # hides your unfinished changes safely
git checkout main  # switch to another branch
# ... do the check ...
git checkout feature/my-feature
git stash pop      # bring your unfinished changes back""",
        language="bash"
    )

    subsection("Using GIT inside Visual Studio IDE")
    paragraph("You don't need to use the terminal at all — Visual Studio has a full Git UI built in.")
    
    subsection("Open Git Changes")
    paragraph("View → Git Changes (Ctrl+0, Ctrl+G) — stage, unstage, and commit files visually.")
    
    subsection("Git Repository Window")
    paragraph("View → Git Repository — see branch history, compare commits, create branches.")
    
    subsection("Create Branch")
    paragraph('Click the branch name in the status bar (bottom-right) and select "New Branch".')
    
    subsection("Pull / Push / Fetch")
    paragraph("Git menu at the top → Pull, Push, Fetch — or use the sync icon in the status bar.")
    
    subsection("Resolve Merge Conflicts")
    paragraph("VS opens a 3-way merge editor — accept incoming, current, or both, side by side.")
    
    subsection("Create Pull Request")
    paragraph(
        'Git menu → "Create Pull Request" — opens your platform (Azure DevOps or GitHub) in the '
        "browser pre-filled."
    )
