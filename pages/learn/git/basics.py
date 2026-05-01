"""GIT → Basics: a minimal-layout sub-page demonstrating the new primitives."""

import streamlit as st

from components.content import (
    code_block,
    link_list,
    paragraph,
    section_intro,
    section_title,
    subsection,
)


def render():
    section_title(
        "GIT — Basics",
        "Foundational commands you'll use every single day.",
    )
    section_intro(
        "Git is a distributed version control system. These commands cover the "
        "everyday loop: get the code, see what changed, save your work, share it."
    )

    subsection("Get the code")
    paragraph("Clone a remote repository onto your machine:")
    code_block("git clone https://github.com/example/repo.git", language="bash")

    subsection("See what changed")
    paragraph("Inspect the working tree and view a compact log of recent commits:")
    code_block("git status\ngit log --oneline -n 10", language="bash")

    subsection("Save your progress")
    paragraph("Stage files and record a commit with a meaningful message:")
    code_block(
        'git add .\ngit commit -m "feat: add forgot password flow"',
        language="bash",
    )

    subsection("Share your work")
    paragraph("Push your branch to the remote so others can review it:")
    code_block("git push origin feature/forgot-password", language="bash")

    subsection("Quick-reference cheat sheet")
    st.markdown(
        """
| Command | What it does |
|---|---|
| `git clone <url>` | Copy a remote repository to your local machine |
| `git status` | Show which files are modified, staged, or untracked |
| `git diff` | Show line-by-line changes not yet staged |
| `git add .` | Stage all changed files for the next commit |
| `git add <file>` | Stage a single file |
| `git commit -m "message"` | Save staged changes as a new commit |
| `git push origin <branch>` | Upload your local commits to the remote branch |
| `git pull` | Fetch remote changes and merge them into your current branch |
| `git log --oneline` | Compact one-line history of recent commits |
| `git log --oneline --graph` | Visual branch/merge history in the terminal |
| `git show <sha>` | Show the changes introduced by a specific commit |
| `git stash` | Temporarily shelve uncommitted changes |
| `git stash pop` | Re-apply the most recently stashed changes |
"""
    )

    subsection("Further reading")
    link_list(
        [
            ("Pro Git book (free)", "https://git-scm.com/book", "the canonical reference"),
            ("Git cheatsheet (GitHub)", "https://education.github.com/git-cheat-sheet-education.pdf"),
        ]
    )
