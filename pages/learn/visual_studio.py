"""Visual Studio IDE: a minimal-layout page using shared content primitives."""

from components.content import (
    code_block,
    link_list,
    paragraph,
    section_intro,
    section_title,
    subsection,
)


def render_visual_studio():
    section_title(
        "Visual Studio IDE",
        "Microsoft's flagship IDE for .NET, C#, ASP.NET, Azure, and enterprise apps.",
    )
    section_intro(
        "Visual Studio is far more than a text editor: it's a complete development "
        "workbench with debuggers, profilers, designers, test runners, and deep Git "
        "integration built in. Always install the latest stable version and keep it "
        "updated to access new C# language features, improved IntelliSense, and the "
        "most recent .NET SDK tooling."
    )

    subsection("Real-world example — a typical C# developer's morning")
    paragraph(
        "Scenario: you're building a REST API for a hospital patient management system. "
        "A third-party lab system emails you a JSON sample of the patient data they'll "
        "send you. You need to create C# model classes that match it — and you have a "
        "bug to fix too."
    )

    paragraph("1. Generate C# classes from JSON in 10 seconds (Paste JSON as Classes). You receive this JSON from the lab:")
    code_block(
        """{
  "patientId": "P-1042",
  "fullName": "Jane Smith",
  "dateOfBirth": "1985-04-15",
  "testResults": [
    { "testName": "Blood Sugar", "value": 5.4, "unit": "mmol/L" }
  ]
}""",
        language="json",
    )
    paragraph(
        "Instead of writing the C# class by hand, copy the JSON, then in Visual Studio "
        "go to: Edit → Paste Special → Paste JSON as Classes. Visual Studio instantly "
        "generates:"
    )
    code_block(
        """public class PatientResult
{
    public string PatientId { get; set; }
    public string FullName { get; set; }
    public string DateOfBirth { get; set; }
    public TestResult[] TestResults { get; set; }
}

public class TestResult
{
    public string TestName { get; set; }
    public float Value { get; set; }
    public string Unit { get; set; }
}""",
        language="csharp",
    )
    paragraph("This saves 10–15 minutes of repetitive typing on every integration.")

    paragraph(
        "2. Quick Actions (Ctrl+.) — fix errors without looking anything up. You write "
        "patientService.GetById(id) but GetById doesn't exist yet. The red squiggle "
        "appears. Press Ctrl+. → \"Generate method 'GetById'\" — VS creates the method "
        "stub in PatientService.cs automatically."
    )

    paragraph(
        "3. Debugger — understand what's going wrong. A test patient record shows the "
        "wrong age. Instead of adding Console.WriteLine everywhere, click the grey "
        "margin next to the age calculation line to set a breakpoint. Press F5. When "
        "the code hits that line, execution pauses and you can hover over any variable "
        "to see its exact value — catching the off-by-one error instantly."
    )

    paragraph(
        "4. Test Explorer — run all tests with one click. After fixing the age bug, "
        "open View → Test Explorer and click \"Run All\". All 47 unit tests finish in "
        "3 seconds. 3 tests go red — those are the areas your fix might have broken. "
        "You fix them before pushing anything."
    )

    subsection("Key productivity features")

    subsection("Paste JSON as Classes")
    paragraph(
        "Edit → Paste Special → Paste JSON as Classes. Copies JSON from clipboard and "
        "auto-generates matching C# model classes. A huge time-saver."
    )

    subsection("Paste XML as Classes")
    paragraph(
        "Edit → Paste Special → Paste XML as Classes. Same idea for XML data — instant "
        "model generation."
    )

    subsection("Quick Actions (Lightbulb)")
    paragraph(
        "Press Ctrl+. anywhere to get context-aware suggestions: generate constructors, "
        "implement interfaces, extract methods, rename symbols."
    )

    subsection("Generate from usage")
    paragraph(
        "Type a class or method that doesn't exist yet, press Ctrl+. and choose "
        "\"Generate class / method\" — VS creates the skeleton automatically."
    )

    subsection("Live code analysis")
    paragraph(
        "Roslyn analysers flag issues, suggest improvements, and enforce code style in "
        "real time — no need to build first."
    )

    subsection("Test Explorer")
    paragraph(
        "View → Test Explorer. Run, debug, and profile all xUnit / NUnit / MSTest tests "
        "directly from the IDE with green/red indicators per test."
    )

    subsection("NuGet Package Manager")
    paragraph(
        "Tools → NuGet Package Manager → Manage NuGet Packages for Solution — search, "
        "install, and update packages across all projects at once."
    )

    subsection("Solution Explorer")
    paragraph(
        "The backbone of VS — browse files, projects, and dependencies. Right-click a "
        "project for Add → New Item, scaffolding, and class diagrams."
    )

    subsection("Class Diagram")
    paragraph(
        "Right-click a project → Add → New Item → Class Diagram. A visual representation "
        "of all classes, interfaces, and their relationships."
    )

    subsection("Object Browser")
    paragraph(
        "View → Object Browser — explore all types, members, and assemblies in your "
        "solution and referenced NuGet packages."
    )

    subsection("Performance Profiler")
    paragraph(
        "Debug → Performance Profiler — analyse CPU usage, memory allocations, and "
        "database query times without leaving VS."
    )

    subsection("Refactor menu")
    paragraph(
        "Right-click any symbol → Refactor: rename everywhere, extract interface, "
        "extract method, inline temporary variable, and more — safely across the whole "
        "solution."
    )

    subsection("Productivity settings worth configuring")

    subsection("Font and editor size")
    paragraph(
        "Tools → Options → Environment → Fonts and Colors. Set font to Cascadia Code "
        "or JetBrains Mono at size 14–15 for ligatures."
    )

    subsection("IntelliSense completion")
    paragraph(
        "Tools → Options → Text Editor → C# → IntelliSense. Enable \"Show completion "
        "list after character is deleted\" and \"Highlight matching portions\"."
    )

    subsection("Code style and formatting")
    paragraph(
        "Tools → Options → Text Editor → C# → Code Style. Configure naming conventions, "
        "prefer var vs explicit types, expression-bodied members."
    )

    subsection("Format on save")
    paragraph(
        "Use a .editorconfig file in the solution root to enforce formatting rules "
        "across the whole team automatically on save."
    )

    subsection("Word wrap")
    paragraph(
        "Edit → Advanced → Word Wrap (Ctrl+E, W). Prevents horizontal scrolling on "
        "long lines — great for wide monitors."
    )

    subsection("Column guides")
    paragraph(
        "Add the guidelines extension or set column guides in .editorconfig to keep "
        "lines under 120 characters."
    )

    subsection("Extensions worth installing")

    subsection("GitHub Copilot")
    paragraph(
        "AI pair programmer — suggests whole lines, methods, and even entire classes "
        "as you type."
    )

    subsection("ReSharper / Rider")
    paragraph(
        "JetBrains' powerful refactoring and analysis tools. Deep code inspections, "
        "rename across solutions."
    )

    subsection("CodeMaid")
    paragraph(
        "Cleans up code — removes unused usings, reorganises members, formats on save."
    )

    subsection("Visual Studio IntelliCode")
    paragraph(
        "AI-assisted IntelliCode completions trained on open-source .NET code patterns."
    )

    subsection("Web Essentials")
    paragraph(
        "Browser sync, BundlerMinifier, and CSS / JavaScript helpers for web projects."
    )

    subsection("Productivity Power Tools")
    paragraph(
        "Double-click to select word, middle-click to close tabs, enhanced scrollbar — "
        "a quality-of-life pack."
    )

    subsection("Essential keyboard shortcuts")
    code_block(
        """Ctrl+.            Quick Actions / Lightbulb fixes
Ctrl+R, R         Rename symbol everywhere
F12               Go to Definition
Alt+F12           Peek Definition (inline preview)
Shift+F12         Find All References
Ctrl+K, D         Format document
Ctrl+K, C / U     Comment / Uncomment selection
Ctrl+Shift+B      Build solution
F5 / Ctrl+F5      Debug / Run without debug
Ctrl+0, Ctrl+G    Open Git Changes window
Ctrl+T            Go to file / type / member
Ctrl+Q            Quick Launch — search VS menus""",
        language="",
    )

    subsection("Further reading")
    link_list(
        [
            (
                "Visual Studio documentation",
                "https://learn.microsoft.com/en-us/visualstudio/",
                "official Microsoft docs",
            ),
            (
                "Download Visual Studio",
                "https://visualstudio.microsoft.com/downloads/",
            ),
            (
                "Default keyboard shortcuts",
                "https://learn.microsoft.com/en-us/visualstudio/ide/default-keyboard-shortcuts-in-visual-studio",
            ),
        ]
    )
