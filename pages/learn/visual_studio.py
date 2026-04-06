import streamlit as st


def render_visual_studio():
    # Overview
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">💻 What is Visual Studio (Full IDE)?</div>
  <div class="card-body">
<b>Visual Studio</b> is Microsoft's flagship integrated development environment —
the most powerful tooling available for .NET, C#, ASP.NET, Azure, and enterprise applications.
It goes far beyond a text editor: it's a complete development workbench with debuggers,
profilers, designers, test runners, and deep Git integration built in.
<br><br>
Always install the <b>latest stable version</b> and keep it updated to access new C# language
features, improved IntelliSense, and the most recent .NET SDK tooling.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Real-world example — VS IDE
    st.markdown(
        """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🌍 Real-World Example — A Typical C# Developer's Morning</div>
  <div class="card-body">
<b>Scenario:</b> You're building a REST API for a hospital patient management system.
A third-party lab system emails you a JSON sample of the patient data they'll send you.
You need to create C# model classes that match it — and you have a bug to fix too.
<br><br>
<b>1. Generate C# classes from JSON in 10 seconds (Paste JSON as Classes):</b><br>
You receive this JSON from the lab:
<div class="cmd-block">{
  "patientId": "P-1042",
  "fullName": "Jane Smith",
  "dateOfBirth": "1985-04-15",
  "testResults": [
{ "testName": "Blood Sugar", "value": 5.4, "unit": "mmol/L" }
  ]
}</div>
Instead of writing the C# class by hand, copy the JSON, then in Visual Studio go to:
<b>Edit → Paste Special → Paste JSON as Classes</b>.
Visual Studio instantly generates:
<div class="cmd-block">public class PatientResult
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
}</div>
This saves 10–15 minutes of repetitive typing on every integration.
<br><br>
<b>2. Quick Actions (Ctrl+.) — fix errors without looking anything up:</b><br>
You write <code>patientService.GetById(id)</code> but <code>GetById</code> doesn't exist yet.
The red squiggle appears. Press <b>Ctrl+.</b> → "Generate method 'GetById'" — VS creates
the method stub in <code>PatientService.cs</code> automatically.
<br><br>
<b>3. Debugger — understand what's going wrong:</b><br>
A test patient record shows the wrong age. Instead of adding <code>Console.WriteLine</code>
everywhere, click the grey margin next to the age calculation line to set a <b>breakpoint</b>.
Press <b>F5</b>. When the code hits that line, execution pauses and you can hover over any
variable to see its exact value — catching the off-by-one error instantly.
<br><br>
<b>4. Test Explorer — run all tests with one click:</b><br>
After fixing the age bug, open <b>View → Test Explorer</b> and click "Run All".
All 47 unit tests finish in 3 seconds. 3 tests go red — those are the areas your fix
might have broken. You fix them before pushing anything.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Key features
    st.markdown(
        """<div class="content-card">
<div class="card-title">⚡ Key Productivity Features</div>
<div class="feature-grid">
  <div class="feature-pill">
<strong>🪄 Paste JSON as Classes</strong>
<p>Edit &rarr; Paste Special &rarr; <b>Paste JSON as Classes</b>.
   Copies JSON from clipboard and auto-generates matching C# model classes. Huge time-saver!</p>
  </div>
  <div class="feature-pill">
<strong>🪄 Paste XML as Classes</strong>
<p>Edit &rarr; Paste Special &rarr; <b>Paste XML as Classes</b>.
   Same idea for XML data — instant model generation.</p>
  </div>
  <div class="feature-pill">
<strong>💡 Quick Actions (Lightbulb)</strong>
<p>Press <b>Ctrl+.</b> anywhere to get context-aware suggestions:
   generate constructors, implement interfaces, extract methods, rename symbols.</p>
  </div>
  <div class="feature-pill">
<strong>🏗️ Generate from Usage</strong>
<p>Type a class or method that doesn't exist yet, press Ctrl+. and choose
   "Generate class / method" — VS creates the skeleton automatically.</p>
  </div>
  <div class="feature-pill">
<strong>🔬 Live Code Analysis</strong>
<p>Roslyn analysers flag issues, suggest improvements, and enforce code style in real time —
   no need to build first.</p>
  </div>
  <div class="feature-pill">
<strong>🧪 Test Explorer</strong>
<p>View &rarr; Test Explorer. Run, debug, and profile all xUnit / NUnit / MSTest tests
   directly from the IDE with green/red indicators per test.</p>
  </div>
  <div class="feature-pill">
<strong>📦 NuGet Package Manager</strong>
<p>Tools &rarr; NuGet Package Manager &rarr; Manage NuGet Packages for Solution —
   search, install, and update packages across all projects at once.</p>
  </div>
  <div class="feature-pill">
<strong>🗂️ Solution Explorer</strong>
<p>The backbone of VS — browse files, projects, and dependencies.
   Right-click a project for <b>Add &rarr; New Item</b>, scaffolding, and class diagrams.</p>
  </div>
  <div class="feature-pill">
<strong>📐 Class Diagram</strong>
<p>Right-click a project &rarr; Add &rarr; New Item &rarr; Class Diagram.
   Visual representation of all classes, interfaces, and their relationships.</p>
  </div>
  <div class="feature-pill">
<strong>🔍 Object Browser</strong>
<p>View &rarr; Object Browser — explore all types, members, and assemblies in your solution
   and referenced NuGet packages.</p>
  </div>
  <div class="feature-pill">
<strong>📊 Performance Profiler</strong>
<p>Debug &rarr; Performance Profiler — analyse CPU usage, memory allocations,
   and database query times without leaving VS.</p>
  </div>
  <div class="feature-pill">
<strong>🔄 Refactor Menu</strong>
<p>Right-click any symbol &rarr; Refactor: rename everywhere, extract interface,
   extract method, inline temporary variable, and more — safely across the whole solution.</p>
  </div>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # Productivity settings
    st.markdown(
        """<div class="content-card">
<div class="card-title">⚙️ Productivity Settings Worth Configuring</div>
<div class="feature-grid">
  <div class="feature-pill">
<strong>Font &amp; Editor Size</strong>
<p>Tools &rarr; Options &rarr; Environment &rarr; Fonts and Colors.
   Set font to <em>Cascadia Code</em> or <em>JetBrains Mono</em> at size 14–15 for ligatures.</p>
  </div>
  <div class="feature-pill">
<strong>IntelliSense Completion</strong>
<p>Tools &rarr; Options &rarr; Text Editor &rarr; C# &rarr; IntelliSense.
   Enable "Show completion list after character is deleted" and "Highlight matching portions".</p>
  </div>
  <div class="feature-pill">
<strong>Code Style &amp; Formatting</strong>
<p>Tools &rarr; Options &rarr; Text Editor &rarr; C# &rarr; Code Style.
   Configure naming conventions, prefer var vs explicit types, expression-bodied members.</p>
  </div>
  <div class="feature-pill">
<strong>Format on Save</strong>
<p>Use a <b>.editorconfig</b> file in the solution root to enforce formatting rules
   across the whole team automatically on save.</p>
  </div>
  <div class="feature-pill">
<strong>Word Wrap</strong>
<p>Edit &rarr; Advanced &rarr; Word Wrap (Ctrl+E, W). Prevents horizontal scrolling
   on long lines — great for wide monitors.</p>
  </div>
  <div class="feature-pill">
<strong>Column Guides</strong>
<p>Add <code>guidelines</code> extension or set column guides in .editorconfig
   to keep lines under 120 characters.</p>
  </div>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # Recommended extensions
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🔌 Extensions Worth Installing</div>
  <div class="feature-grid">
<div class="feature-pill">
  <strong>GitHub Copilot</strong>
  <p>AI pair programmer — suggests whole lines, methods, and even entire classes as you type.</p>
</div>
<div class="feature-pill">
  <strong>ReSharper / Rider</strong>
  <p>JetBrains' powerful refactoring and analysis tools. Deep code inspections, rename across solutions.</p>
</div>
<div class="feature-pill">
  <strong>CodeMaid</strong>
  <p>Cleans up code — removes unused usings, reorganises members, formats on save.</p>
</div>
<div class="feature-pill">
  <strong>Visual Studio IntelliCode</strong>
  <p>AI-assisted IntelliCode completions trained on open-source .NET code patterns.</p>
</div>
<div class="feature-pill">
  <strong>Web Essentials</strong>
  <p>Browser sync, BundlerMinifier, and CSS / JavaScript helpers for web projects.</p>
</div>
<div class="feature-pill">
  <strong>Productivity Power Tools</strong>
  <p>Double-click to select word, middle-click to close tabs, enhanced scrollbar — quality-of-life pack.</p>
</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Key shortcuts
    st.markdown(
        """<div class="content-card">
<div class="card-title">⌨️ Essential Keyboard Shortcuts</div>
<table class="shortcut-table">
<tr><th>Shortcut</th><th>Action</th></tr>
<tr><td>Ctrl+.</td><td>Quick Actions / Lightbulb fixes</td></tr>
<tr><td>Ctrl+R, R</td><td>Rename symbol everywhere</td></tr>
<tr><td>F12</td><td>Go to Definition</td></tr>
<tr><td>Alt+F12</td><td>Peek Definition (inline preview)</td></tr>
<tr><td>Shift+F12</td><td>Find All References</td></tr>
<tr><td>Ctrl+K, D</td><td>Format document</td></tr>
<tr><td>Ctrl+K, C / U</td><td>Comment / Uncomment selection</td></tr>
<tr><td>Ctrl+Shift+B</td><td>Build solution</td></tr>
<tr><td>F5 / Ctrl+F5</td><td>Debug / Run without debug</td></tr>
<tr><td>Ctrl+0, Ctrl+G</td><td>Open Git Changes window</td></tr>
<tr><td>Ctrl+T</td><td>Go to file / type / member</td></tr>
<tr><td>Ctrl+Q</td><td>Quick Launch — search VS menus</td></tr>
</table>
</div>""",
        unsafe_allow_html=True,
    )

