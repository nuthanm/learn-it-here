"""GIT → Branching: a minimal-layout sub-page demonstrating the new primitives."""

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

    subsection("Further reading")
    link_list(
        [
            ("Branching strategies", "https://www.atlassian.com/git/tutorials/comparing-workflows"),
            ("git rebase docs", "https://git-scm.com/docs/git-rebase"),
        ]
    )
