"""VS Code: a minimal-layout page using the shared content primitives."""

import streamlit as st

from components.content import (
    code_block,
    link_list,
    paragraph,
    section_intro,
    section_title,
    subsection,
)


def render_vscode():
    section_title(
        "VS Code",
        "A lightweight, extensible editor that scales from quick edits to full-stack development.",
    )
    section_intro(
        "Visual Studio Code is a fast, cross-platform source-code editor from Microsoft. "
        "It runs on Windows, macOS, and Linux and is ideal for front-end work, scripting, "
        "PowerShell, Python, Docker files, and quick code edits."
    )

    subsection("What is VS Code?")
    paragraph(
        "Visual Studio Code is a lightweight but extremely powerful source-code editor from "
        "Microsoft. With the right extensions it becomes a fully capable environment for "
        "C#/.NET development too. Its extension marketplace has over 50,000 extensions — "
        "there's almost nothing you can't do in it. Unlike the full Visual Studio IDE, "
        "VS Code starts in under a second and never feels heavy."
    )

    subsection("Real-world example — daily tasks made faster")
    paragraph(
        "Scenario: you're a junior developer maintaining a website's front-end. No heavy "
        "IDE needed — VS Code is all you need. Here's how its features help you every day."
    )

    paragraph(
        "1. Multi-cursor editing — rename the same thing in 10 places at once. Your team "
        "decides to rename the CSS class btn-blue to btn-primary across an HTML file. "
        "Instead of using Find & Replace and carefully crafting a regex pattern, click on "
        "btn-blue and press Ctrl+Shift+L. Every single occurrence gets its own cursor. "
        "Type btn-primary — all 10 are changed simultaneously in one keystroke. Done in 3 seconds."
    )
    paragraph(
        "2. Integrated terminal — no window switching. You're editing a Python script and "
        "want to run it. Press Ctrl+`. A terminal opens right inside VS Code, already in "
        "the same folder as your file. Type python script.py and see the output immediately "
        "— without switching to a separate terminal window or losing your place in the code."
    )
    paragraph(
        "3. Live Share — pair programming with a teammate in another city. Your colleague "
        "in London is stuck on a bug. Instead of screen-sharing (laggy, read-only), install "
        "the Live Share extension, click \"Share\", and send her the link. She now sees your "
        "file, can edit it, and you both see each other's cursors in real time — just like "
        "Google Docs, but for code. No files to email, no VPN needed."
    )
    paragraph(
        "4. Remote development — edit code running on a server, from your laptop. Your "
        "company's Python data pipeline runs on a Linux server. Instead of SSH-ing in and "
        "using nano, install the Remote - SSH extension. Connect to the server with one "
        "click. VS Code opens the server's files as if they were local — with full "
        "IntelliSense, syntax highlighting, and Git support. You edit, save, and run "
        "everything without leaving your laptop's comfortable setup."
    )
    paragraph(
        "5. Command Palette — find any command without memorising menus. Forgot how to "
        "format a JSON file? Press Ctrl+Shift+P, type \"format\", and \"Format Document\" "
        "appears instantly. Press Enter. The entire file is formatted. The Command Palette "
        "gives you access to literally every VS Code feature by searching for it."
    )

    subsection("Built-in features quick reference")
    st.markdown(
        """
| Feature | Shortcut / How to use | What it does |
|---|---|---|
| **Multi-cursor editing** | Alt+Click to add cursors · Ctrl+D next · Ctrl+Shift+L all | Edit many places simultaneously — rename a CSS class in 10 spots in one keystroke |
| **Command Palette** | Ctrl+Shift+P | Access every VS Code command by searching — format, lint, git, settings, extensions |
| **Integrated terminal** | Ctrl+` | Full terminal right in the editor — run builds, git, npm scripts without switching windows |
| **Live Share** | Install extension → Share | Real-time collaborative editing — teammates see your cursor, you see theirs |
| **Remote development** | Install Remote - SSH / WSL / Dev Containers extension | Edit code running on a server, WSL, or Docker container as if it were local |
| **Code snippets** | Type prefix (e.g. `prop`, `ctor`, `for`) + Tab | Expand full code templates; create custom snippets for repetitive patterns |
| **Zen mode** | Ctrl+K Z | Hides all UI — just code on a clean background; perfect for focused sessions |
| **IntelliSense** | Automatic (powered by language servers) | Completions, signatures, and hover docs for C#, Python, JS, and more |
"""
    )

    subsection("Extensions worth installing")
    st.markdown(
        """
| Extension | What it does | Best for |
|---|---|---|
| **C# Dev Kit** (Microsoft) | Full .NET / C# support — IntelliSense, refactoring, Test Explorer, Solution Explorer | Any C# / .NET developer using VS Code |
| **GitHub Copilot** | AI pair programmer — completes functions, writes tests, explains code | Everyone — free for students / OSS, paid for professional use |
| **GitLens** | Inline blame, rich history, branch comparison, PR integration on top of built-in Git | Teams wanting deep Git visibility |
| **REST Client / Thunder Client** | Test HTTP APIs with `.http` files or a GUI — no need to leave the editor | Backend and API developers |
| **Prettier** | Opinionated code formatter for JS/TS/CSS/JSON/Markdown with format-on-save | Front-end and full-stack developers |
| **ESLint / Pylint** | Language-specific linting with inline highlights for JS/TS and Python | JavaScript, TypeScript, and Python developers |
| **Todo Tree** | Scans all files for TODO / FIXME / HACK comments and lists them in a sidebar | Keeping track of technical debt across large repos |
| **Bracket Pair Colorizer** | Matching brackets get the same colour — nested code is much easier to read | Any developer working with deeply nested code |
| **Path Intellisense** | Autocompletes file paths as you type import or reference statements | Reducing typos in import paths |
| **Docker** | Browse containers, images, registries; build and run Dockerfiles from the explorer | Developers working with Docker and containerised apps |
"""
    )

    subsection("Recommended settings.json")
    paragraph(
        "Open with Ctrl+Shift+P then choose \"Open User Settings (JSON)\"."
    )
    code_block(
        """{
  "editor.fontSize": 14,
  "editor.fontFamily": "'Cascadia Code', 'JetBrains Mono', Consolas, monospace",
  "editor.fontLigatures": true,
  "editor.tabSize": 4,
  "editor.formatOnSave": true,
  "editor.wordWrap": "on",
  "editor.minimap.enabled": false,
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": true,
  "editor.suggestSelection": "first",
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "workbench.colorTheme": "One Dark Pro",
  "workbench.iconTheme": "material-icon-theme",
  "git.autofetch": true,
  "git.confirmSync": false,
  "[csharp]": {
    "editor.defaultFormatter": "ms-dotnettools.csharp"
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}""",
        language="json",
    )

    subsection("Essential keyboard shortcuts")
    st.markdown(
        """
| Shortcut | Action |
|---|---|
| Ctrl+P | Quick file open (fuzzy search) |
| Ctrl+Shift+P | Command Palette — search all commands |
| Ctrl+` | Toggle integrated terminal |
| Ctrl+B | Toggle sidebar visibility |
| Ctrl+/ | Toggle line comment |
| Alt+Up / Alt+Down | Move current line up / down |
| Shift+Alt+Down | Duplicate current line below |
| Ctrl+D | Select next occurrence of current word |
| Ctrl+Shift+L | Select ALL occurrences of current word |
| F12 | Go to Definition |
| Shift+F12 | Find All References |
| F2 | Rename symbol everywhere |
| Ctrl+K Z | Zen mode (distraction-free) |
| Ctrl+Shift+` | New terminal instance |
"""
    )

    subsection("Further reading")
    link_list(
        [
            ("VS Code documentation", "https://code.visualstudio.com/docs", "official docs"),
            ("Tips and Tricks", "https://code.visualstudio.com/docs/getstarted/tips-and-tricks"),
            ("Extension Marketplace", "https://marketplace.visualstudio.com/vscode"),
            ("Keyboard shortcuts reference", "https://code.visualstudio.com/docs/getstarted/keybindings"),
        ]
    )
