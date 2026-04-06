import streamlit as st


def render_vscode():
    # Overview
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">📝 What is VS Code?</div>
  <div class="card-body">
<b>Visual Studio Code</b> is a lightweight but extremely powerful source-code editor from
Microsoft. It runs on Windows, macOS, and Linux and is ideal for front-end development,
scripting, PowerShell, Python, Docker files, and quick code edits.
<br><br>
With the right extensions it becomes a fully capable environment for C#/.NET development too.
Its extension marketplace has over 50,000 extensions — there's almost nothing you can't do in it.
Unlike the full Visual Studio IDE, VS Code starts in under a second and never feels heavy.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Real-world example — VS Code
    st.markdown(
        """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🌍 Real-World Example — Daily Tasks Made Faster in VS Code</div>
  <div class="card-body">
<b>Scenario:</b> You're a junior developer maintaining a website's front-end.
No heavy IDE needed — VS Code is all you need. Here's how its features help you every day:
<br><br>
<b>1. Multi-Cursor Editing — rename the same thing in 10 places at once:</b><br>
Your team decides to rename the CSS class <code>btn-blue</code> to <code>btn-primary</code>
across an HTML file. Instead of using Find &amp; Replace and carefully crafting a regex pattern,
click on <code>btn-blue</code> and press <b>Ctrl+Shift+L</b>.
Every single occurrence gets its own cursor. Type <code>btn-primary</code> — all 10 are changed
simultaneously in one keystroke. Done in 3 seconds.
<br><br>
<b>2. Integrated Terminal — no window switching:</b><br>
You're editing a Python script and want to run it. Press <b>Ctrl+`</b>.
A terminal opens right inside VS Code, already in the same folder as your file.
Type <code>python script.py</code> and see the output immediately — without switching to
a separate terminal window or losing your place in the code.
<br><br>
<b>3. Live Share — pair programming with a teammate in another city:</b><br>
Your colleague in London is stuck on a bug. Instead of screen-sharing (laggy, read-only),
install the <b>Live Share</b> extension, click "Share", and send her the link.
She now sees your file, can edit it, and you both see each other's cursors in real time —
just like Google Docs, but for code. No files to email, no VPN needed.
<br><br>
<b>4. Remote Development — edit code running on a server, from your laptop:</b><br>
Your company's Python data pipeline runs on a Linux server. Instead of SSH-ing in and
using <code>nano</code>, install the <b>Remote - SSH</b> extension. Connect to the server
with one click. VS Code opens the server's files as if they were local — with full
IntelliSense, syntax highlighting, and Git support. You edit, save, and run everything
without leaving your laptop's comfortable setup.
<br><br>
<b>5. Command Palette — find any command without memorising menus:</b><br>
Forgot how to format a JSON file? Press <b>Ctrl+Shift+P</b>, type "format", and
"Format Document" appears instantly. Press Enter. The entire file is formatted.
The Command Palette gives you access to literally every VS Code feature by searching for it.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Key features
    st.markdown(
        """<div class="content-card">
<div class="card-title">⚡ Key Features</div>
<div class="feature-grid">
  <div class="feature-pill">
<strong>🖱️ Multi-Cursor Editing</strong>
<p><b>Alt+Click</b> to add cursors. <b>Ctrl+D</b> selects the next occurrence.
   <b>Ctrl+Shift+L</b> selects all occurrences. Edit many places at once!</p>
  </div>
  <div class="feature-pill">
<strong>🎨 Command Palette</strong>
<p><b>Ctrl+Shift+P</b> opens every command VS Code can run — format, lint, git, settings, extensions.</p>
  </div>
  <div class="feature-pill">
<strong>🖥️ Integrated Terminal</strong>
<p><b>Ctrl+`</b> opens a full terminal right in the editor. Run builds, git commands,
   npm scripts without switching windows.</p>
  </div>
  <div class="feature-pill">
<strong>🌐 Live Share</strong>
<p>Real-time collaborative editing with teammates — they see your cursor, you see theirs.
   Great for pair programming and code reviews.</p>
  </div>
  <div class="feature-pill">
<strong>🔌 Remote Development</strong>
<p>Edit code running on a remote SSH server, inside WSL (Linux on Windows),
   or inside Docker containers — seamlessly.</p>
  </div>
  <div class="feature-pill">
<strong>✂️ Code Snippets</strong>
<p>Type a prefix (e.g., <em>prop</em>, <em>ctor</em>, <em>for</em>) and press Tab to
   expand full code templates. You can create custom snippets too.</p>
  </div>
  <div class="feature-pill">
<strong>🧘 Zen Mode</strong>
<p><b>Ctrl+K Z</b> hides all UI — just your code on a clean background.
   Perfect for focused writing or presentations.</p>
  </div>
  <div class="feature-pill">
<strong>🔍 IntelliSense</strong>
<p>Powered by language servers (LSP). C# Dev Kit, Pylance, ESLint etc.
   give you completions, signatures, and hover docs just like the full IDE.</p>
  </div>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # Recommended extensions
    st.markdown(
        """<div class="content-card">
<div class="card-title">🔌 Recommended Extensions</div>
<div class="feature-grid">
  <div class="feature-pill">
<strong>C# Dev Kit (Microsoft)</strong>
<p>Full .NET / C# support — IntelliSense, refactoring, Test Explorer, and Solution Explorer inside VS Code.</p>
  </div>
  <div class="feature-pill">
<strong>GitLens</strong>
<p>Supercharges VS Code's built-in Git — inline blame, rich history, branch comparison, PR integration.</p>
  </div>
  <div class="feature-pill">
<strong>REST Client / Thunder Client</strong>
<p>Test HTTP APIs by writing <code>.http</code> files or using a GUI — no need to leave the editor.</p>
  </div>
  <div class="feature-pill">
<strong>Prettier</strong>
<p>Opinionated code formatter for JS/TS/CSS/JSON/Markdown. Format on save with zero configuration.</p>
  </div>
  <div class="feature-pill">
<strong>GitHub Copilot</strong>
<p>AI pair programmer — completes functions, writes tests, and explains code from comments.</p>
  </div>
  <div class="feature-pill">
<strong>ESLint / Pylint</strong>
<p>Language-specific linting with inline highlights for JavaScript/TypeScript and Python respectively.</p>
  </div>
  <div class="feature-pill">
<strong>Todo Tree</strong>
<p>Scans all files for TODO / FIXME / HACK comments and lists them in a sidebar panel.</p>
  </div>
  <div class="feature-pill">
<strong>Bracket Pair Colorizer</strong>
<p>Matching brackets are coloured the same — makes nested code much easier to read at a glance.</p>
  </div>
  <div class="feature-pill">
<strong>Path Intellisense</strong>
<p>Autocompletes file paths as you type <code>import</code> or reference statements.</p>
  </div>
  <div class="feature-pill">
<strong>Docker</strong>
<p>Browse containers, images, and registries. Build and run Dockerfiles from the explorer panel.</p>
  </div>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # Settings
    st.markdown(
        """<div class="content-card">
<div class="card-title">⚙️ Recommended settings.json</div>
<div class="card-body">Open with <b>Ctrl+Shift+P</b> &rarr; "Open User Settings (JSON)"</div>
<div class="json-block">{
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
}</div>
</div>""",
        unsafe_allow_html=True,
    )

    # Shortcuts
    st.markdown(
        """<div class="content-card">
<div class="card-title">⌨️ Essential Keyboard Shortcuts</div>
<table class="shortcut-table">
<tr><th>Shortcut</th><th>Action</th></tr>
<tr><td>Ctrl+P</td><td>Quick file open (fuzzy search)</td></tr>
<tr><td>Ctrl+Shift+P</td><td>Command Palette — search all commands</td></tr>
<tr><td>Ctrl+`</td><td>Toggle integrated terminal</td></tr>
<tr><td>Ctrl+B</td><td>Toggle sidebar visibility</td></tr>
<tr><td>Ctrl+/</td><td>Toggle line comment</td></tr>
<tr><td>Alt+↑ / Alt+↓</td><td>Move current line up / down</td></tr>
<tr><td>Shift+Alt+↓</td><td>Duplicate current line below</td></tr>
<tr><td>Ctrl+D</td><td>Select next occurrence of current word</td></tr>
<tr><td>Ctrl+Shift+L</td><td>Select ALL occurrences of current word</td></tr>
<tr><td>F12</td><td>Go to Definition</td></tr>
<tr><td>Shift+F12</td><td>Find All References</td></tr>
<tr><td>F2</td><td>Rename symbol everywhere</td></tr>
<tr><td>Ctrl+K Z</td><td>Zen mode (distraction-free)</td></tr>
<tr><td>Ctrl+Shift+`</td><td>New terminal instance</td></tr>
</table>
</div>""",
        unsafe_allow_html=True,
    )

