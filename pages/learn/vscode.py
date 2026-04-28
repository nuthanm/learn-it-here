"""VS Code: a minimal-layout page using the shared content primitives."""

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

    subsection("Multi-cursor editing")
    paragraph(
        "Alt+Click to add cursors. Ctrl+D selects the next occurrence. Ctrl+Shift+L selects "
        "all occurrences. Edit many places at once."
    )

    subsection("Command Palette")
    paragraph(
        "Ctrl+Shift+P opens every command VS Code can run — format, lint, git, settings, extensions."
    )

    subsection("Integrated terminal")
    paragraph(
        "Ctrl+` opens a full terminal right in the editor. Run builds, git commands, and "
        "npm scripts without switching windows."
    )

    subsection("Live Share")
    paragraph(
        "Real-time collaborative editing with teammates — they see your cursor, you see "
        "theirs. Great for pair programming and code reviews."
    )

    subsection("Remote development")
    paragraph(
        "Edit code running on a remote SSH server, inside WSL (Linux on Windows), or "
        "inside Docker containers — seamlessly."
    )

    subsection("Code snippets")
    paragraph(
        "Type a prefix (e.g., prop, ctor, for) and press Tab to expand full code templates. "
        "You can create custom snippets too."
    )

    subsection("Zen mode")
    paragraph(
        "Ctrl+K Z hides all UI — just your code on a clean background. Perfect for focused "
        "writing or presentations."
    )

    subsection("IntelliSense")
    paragraph(
        "Powered by language servers (LSP). C# Dev Kit, Pylance, ESLint and others give "
        "you completions, signatures, and hover docs just like the full IDE."
    )

    subsection("C# Dev Kit (Microsoft)")
    paragraph(
        "Full .NET / C# support — IntelliSense, refactoring, Test Explorer, and Solution "
        "Explorer inside VS Code."
    )

    subsection("GitLens")
    paragraph(
        "Supercharges VS Code's built-in Git — inline blame, rich history, branch "
        "comparison, PR integration."
    )

    subsection("REST Client / Thunder Client")
    paragraph(
        "Test HTTP APIs by writing .http files or using a GUI — no need to leave the editor."
    )

    subsection("Prettier")
    paragraph(
        "Opinionated code formatter for JS/TS/CSS/JSON/Markdown. Format on save with zero "
        "configuration."
    )

    subsection("GitHub Copilot")
    paragraph(
        "AI pair programmer — completes functions, writes tests, and explains code from comments."
    )

    subsection("ESLint / Pylint")
    paragraph(
        "Language-specific linting with inline highlights for JavaScript/TypeScript and "
        "Python respectively."
    )

    subsection("Todo Tree")
    paragraph(
        "Scans all files for TODO / FIXME / HACK comments and lists them in a sidebar panel."
    )

    subsection("Bracket Pair Colorizer")
    paragraph(
        "Matching brackets are coloured the same — makes nested code much easier to read "
        "at a glance."
    )

    subsection("Path Intellisense")
    paragraph(
        "Autocompletes file paths as you type import or reference statements."
    )

    subsection("Docker")
    paragraph(
        "Browse containers, images, and registries. Build and run Dockerfiles from the "
        "explorer panel."
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
    code_block(
        """Shortcut          Action
----------------  ---------------------------------------------
Ctrl+P            Quick file open (fuzzy search)
Ctrl+Shift+P      Command Palette — search all commands
Ctrl+`            Toggle integrated terminal
Ctrl+B            Toggle sidebar visibility
Ctrl+/            Toggle line comment
Alt+Up / Alt+Dn   Move current line up / down
Shift+Alt+Down    Duplicate current line below
Ctrl+D            Select next occurrence of current word
Ctrl+Shift+L      Select ALL occurrences of current word
F12               Go to Definition
Shift+F12         Find All References
F2                Rename symbol everywhere
Ctrl+K Z          Zen mode (distraction-free)
Ctrl+Shift+`      New terminal instance""",
        language="",
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
