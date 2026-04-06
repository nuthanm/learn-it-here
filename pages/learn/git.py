import streamlit as st


def render_git():
    # Overview
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🔧 What is GIT?</div>
  <div class="card-body">
<b>Git</b> is a <em>distributed version control system</em> that tracks changes in source code
during software development. It lets multiple developers collaborate simultaneously,
maintains a complete history of every change, and supports powerful branching and merging
workflows — all without needing a constant connection to a central server.
<br><br>
Git lives on your machine. The platforms below are <em>cloud hosting services</em> that store
your Git repositories and add collaboration features like pull requests, pipelines, and boards.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Real-world example
    st.markdown(
        """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🌍 Real-World Example — Your First Day on a Team Project</div>
  <div class="card-body">
<b>Scenario:</b> You just joined a company building an online shopping website.
Five other developers are already working on it. Your task: <em>add a "Forgot Password" feature</em>.
<br><br>
Without Git, you would copy the entire project folder, make changes, and then try to manually
merge your changes back — a nightmare when five people do this at once. Git solves this entirely.
<br><br>
<b>Here's exactly what you do:</b>
<br><br>
<b>Step 1 — Get the project onto your laptop:</b>
<pre class="cmd-block">git clone https://github.com/mycompany/shopping-website.git
cd shopping-website</pre>
Now you have a full copy of the project. Everyone else is working on their own copies too.
<br><br>
<b>Step 2 — Create your own workspace (branch) so you don't disturb others:</b>
<pre class="cmd-block">git checkout -b feature/forgot-password</pre>
Think of a branch like a personal notebook. Your changes go here without touching the main codebase.
<br><br>
<b>Step 3 — Write your code. Then save your progress:</b>
<pre class="cmd-block">git add .
git commit -m "feat: add forgot password email flow"</pre>
A commit is like a save point in a video game — you can always go back to it.
<br><br>
<b>Step 4 — Share your work with the team:</b>
<pre class="cmd-block">git push origin feature/forgot-password</pre>
Your branch is now on GitHub/Azure DevOps. You open a <b>Pull Request</b> and a teammate reviews it.
After approval it gets merged into the main codebase — safely, with a full history of every change you made.
<br><br>
<b>Why this matters:</b> If your code breaks something, Git lets the team roll back to the last
good state in seconds. No files are ever lost.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Supported platforms
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🌐 Supported Platforms</div>
  <div class="card-body">
Git works the same way locally regardless of which platform hosts your remote repository.
Each platform adds its own collaboration and CI/CD features on top.
  </div>
  <div class="platform-row">
<div class="platform-badge">🐙 <span>GitHub<br><small style="font-weight:400;color:#64748B">Open-source leader, GitHub Actions CI/CD, GitHub Copilot</small></span></div>
<div class="platform-badge">🔷 <span>Azure DevOps<br><small style="font-weight:400;color:#64748B">Microsoft ecosystem, Boards + Pipelines + Repos</small></span></div>
<div class="platform-badge">🪣 <span>Bitbucket<br><small style="font-weight:400;color:#64748B">Atlassian ecosystem, integrates with JIRA natively</small></span></div>
<div class="platform-badge">🦊 <span>GitLab<br><small style="font-weight:400;color:#64748B">All-in-one DevOps platform, built-in CI/CD pipelines</small></span></div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Workflow diagram
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🗺️ Workflow Diagram — Clone to Push</div>
  <div class="card-body">
This is the standard day-to-day workflow every developer follows, from getting the
codebase to your machine all the way to merging your changes back.
  </div>
  <div class="wf-diagram">
<div class="wf-node">📥 Clone / Pull</div>
<div class="wf-arrow">→</div>
<div class="wf-node">🌿 Create Branch</div>
<div class="wf-arrow">→</div>
<div class="wf-node">✏️ Write Code</div>
<div class="wf-arrow">→</div>
<div class="wf-node">📦 Stage Changes</div>
<div class="wf-arrow">→</div>
<div class="wf-node">💾 Commit</div>
<div class="wf-arrow">→</div>
<div class="wf-node">🚀 Push</div>
<div class="wf-arrow">→</div>
<div class="wf-node-green">🔍 Pull Request</div>
<div class="wf-arrow">→</div>
<div class="wf-node-green">✅ Code Review</div>
<div class="wf-arrow">→</div>
<div class="wf-node-green">🔀 Merge</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Commands
    st.markdown(
        """<div class="content-card">
<div class="card-title">⌨️ Commands We Use Regularly</div>
<div class="card-body">These are the commands you'll run day-to-day — from getting the repo to pushing your work back up.</div>
<div class="card-section-title">Starting Out</div>
<div class="cmd-block">
<span class="cmd-comment"># Clone the repository to your local machine</span>
git clone https://github.com/your-org/your-repo.git
&#8203;
<span class="cmd-comment"># Navigate into the project folder</span>
cd your-repo
&#8203;
<span class="cmd-comment"># Check current branch and status</span>
git status
git branch
</div>
<div class="card-section-title">Daily Workflow</div>
<div class="cmd-block">
<span class="cmd-comment"># Always pull latest changes before starting work</span>
git fetch origin
git pull origin main
&#8203;
<span class="cmd-comment"># Create and switch to a new feature branch</span>
git checkout -b feature/my-feature-name
&#8203;
<span class="cmd-comment"># See what has changed</span>
git status
git diff
&#8203;
<span class="cmd-comment"># Stage your changes (all files, or a specific file)</span>
git add .
git add src/MyFile.cs
&#8203;
<span class="cmd-comment"># Commit with a clear message</span>
git commit -m "feat: add user login endpoint"
&#8203;
<span class="cmd-comment"># Push your branch to the remote</span>
git push origin feature/my-feature-name
</div>
<div class="card-section-title">Keeping Your Branch Up to Date</div>
<div class="cmd-block">
<span class="cmd-comment"># Option 1: Rebase on main (keeps history clean — preferred)</span>
git fetch origin
git rebase origin/main
&#8203;
<span class="cmd-comment"># Option 2: Merge main into your branch</span>
git merge origin/main
&#8203;
<span class="cmd-comment"># Undo staged changes (before commit)</span>
git reset HEAD src/MyFile.cs
&#8203;
<span class="cmd-comment"># Temporarily stash unfinished work and come back later</span>
git stash
git stash pop
</div>
<div class="card-section-title">Useful Inspection Commands</div>
<div class="cmd-block">
<span class="cmd-comment"># Last 10 commits on current branch</span>
git log --oneline -10
&#8203;
<span class="cmd-comment"># See changes between your branch and main</span>
git diff main..HEAD
&#8203;
<span class="cmd-comment"># Show all local and remote branches</span>
git branch -a
&#8203;
<span class="cmd-comment"># Delete a local branch after merging</span>
git branch -d feature/my-feature-name
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # Real-world Git scenario
    st.markdown(
        """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🌍 Real-World Example — Fixing a Bug While Someone Else Adds a Feature</div>
  <div class="card-body">
<b>Scenario:</b> Your teammate Alice is adding a new payment page. At the same time,
your manager calls and says "the login button is broken in production — fix it NOW!"
<br><br>
You don't want to disturb Alice's half-finished payment work. Here's how Git handles this perfectly:
<br><br>
<b>1. Get the very latest code:</b>
<pre class="cmd-block">git fetch origin
git pull origin main</pre>
<b>2. Create a hotfix branch — completely separate from Alice's work:</b>
<pre class="cmd-block">git checkout -b hotfix/login-button-not-working</pre>
<b>3. Fix the bug in LoginController.cs, then save and share:</b>
<pre class="cmd-block">git add src/Controllers/LoginController.cs
git commit -m "fix: login button now submits form correctly"
git push origin hotfix/login-button-not-working</pre>
<b>4. After your hotfix is merged, get Alice's latest changes too:</b>
<pre class="cmd-block">git fetch origin
git rebase origin/main</pre>
Both changes are now in the main codebase — no conflicts, no overwriting each other's work.
Git tracked every line changed by everyone, independently.
<br><br>
<b>Stash — save unfinished work temporarily:</b> Suppose while you were mid-way through a new
feature your boss asks you to quickly check something on another branch. Use:
<pre class="cmd-block">git stash          # hides your unfinished changes safely
git checkout main  # switch to another branch
# ... do the check ...
git checkout feature/my-feature
git stash pop      # bring your unfinished changes back</pre>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # VS IDE Integration
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">💻 Using GIT inside Visual Studio IDE</div>
  <div class="card-body">
You don't need to use the terminal at all — Visual Studio has a full Git UI built in.
  </div>
  <div class="feature-grid">
<div class="feature-pill">
  <strong>Open Git Changes</strong>
  <p>View &rarr; Git Changes (Ctrl+0, Ctrl+G) — stage, unstage, and commit files visually.</p>
</div>
<div class="feature-pill">
  <strong>Git Repository Window</strong>
  <p>View &rarr; Git Repository — see branch history, compare commits, create branches.</p>
</div>
<div class="feature-pill">
  <strong>Create Branch</strong>
  <p>Click the branch name in the status bar (bottom-right) and select "New Branch".</p>
</div>
<div class="feature-pill">
  <strong>Pull / Push / Fetch</strong>
  <p>Git menu at the top &rarr; Pull, Push, Fetch — or use the sync icon in the status bar.</p>
</div>
<div class="feature-pill">
  <strong>Resolve Merge Conflicts</strong>
  <p>VS opens a 3-way merge editor — accept incoming, current, or both, side by side.</p>
</div>
<div class="feature-pill">
  <strong>Create Pull Request</strong>
  <p>Git menu &rarr; "Create Pull Request" — opens your platform (Azure DevOps / GitHub) in the browser pre-filled.</p>
</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

