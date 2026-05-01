"""GIT → Branching: a minimal-layout sub-page demonstrating the new primitives."""

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
        "GIT — Branching",
        "Work in isolation, then merge cleanly.",
    )
    section_intro(
        "Branches let you develop features without disturbing the main codebase. "
        "Create one, switch to it, push it, and open a pull request when ready."
    )

    subsection("Create and switch to a branch")
    code_block("git checkout -b feature/forgot-password", language="bash")

    subsection("List branches")
    code_block("git branch        # local\ngit branch -a     # local + remote", language="bash")

    subsection("Merge a branch")
    paragraph("Bring another branch's history into your current branch:")
    code_block("git checkout main\ngit pull\ngit merge feature/forgot-password", language="bash")

    subsection("Rebase instead of merge")
    paragraph(
        "Rebase replays your commits on top of the target branch — cleaner history, "
        "but never rebase a branch that's already shared with others."
    )
    code_block("git checkout feature/forgot-password\ngit rebase main", language="bash")

    subsection("Delete a finished branch")
    code_block("git branch -d feature/forgot-password", language="bash")

    subsection("Quick-reference cheat sheet")
    st.markdown(
        """
| Command | What it does |
|---|---|
| `git branch` | List all local branches |
| `git branch -a` | List local and remote branches |
| `git checkout -b <name>` | Create a new branch and switch to it |
| `git switch <name>` | Switch to an existing branch (modern syntax) |
| `git switch -c <name>` | Create and switch to a new branch (modern syntax) |
| `git push -u origin <name>` | Push new branch to remote and set tracking |
| `git merge <branch>` | Merge the named branch into your current branch |
| `git rebase <branch>` | Replay your commits on top of the named branch |
| `git branch -d <name>` | Delete a local branch (safe — won't delete unmerged) |
| `git branch -D <name>` | Force-delete a local branch (even if unmerged) |
| `git push origin --delete <name>` | Delete the branch on the remote |
| `git fetch --prune` | Remove local references to deleted remote branches |
| `git cherry-pick <sha>` | Apply a single commit from another branch |
"""
    )

    subsection("Merge vs Rebase — when to use which")
    st.markdown(
        """
| Approach | When to use | Effect on history |
|---|---|---|
| **Merge** | Integrating a finished feature into main; keeping full context | Creates a merge commit; non-linear but complete history |
| **Rebase** | Keeping your feature branch up to date with main before a PR | Linear history; cleaner `git log` — but rewrites commits |
| **Squash merge** | Keeping main's history clean; squashing WIP commits | All feature commits become one commit on main |
"""
    )

    subsection("Further reading")
    link_list(
        [
            ("Branching strategies", "https://www.atlassian.com/git/tutorials/comparing-workflows"),
            ("git rebase docs", "https://git-scm.com/docs/git-rebase"),
        ]
    )
