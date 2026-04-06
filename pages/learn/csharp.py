import streamlit as st


def render_csharp():
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">💠 What is C#? (For Complete Beginners)</div>
  <div class="card-body">
<b>C#</b> (pronounced "C sharp") is a modern, object-oriented programming language created by
Microsoft in 2000. It was designed by <b>Anders Hejlsberg</b> (who also designed TypeScript and
previously Turbo Pascal &amp; Delphi).<br><br>
C# runs on the <b>.NET platform</b> — Microsoft's powerful developer toolkit. Think of .NET as
a professional kitchen and C# as the chef's language: structured, expressive, and incredibly
powerful.<br><br>
<b>🏠 Layman terms:</b> Imagine you want to give instructions to a robot (your computer). C# is
a language that the robot understands perfectly — and it's designed to be clear, logical, and
hard to misuse. It's like writing a recipe: step-by-step instructions that the robot follows
exactly.<br><br>
<b>What can you build with C#?</b><br>
✅ Web apps &amp; APIs (ASP.NET Core)<br>
✅ Desktop apps (WPF, WinForms, MAUI)<br>
✅ Mobile apps (Xamarin / .NET MAUI)<br>
✅ Games (Unity — the world's most popular game engine)<br>
✅ Cloud services (Azure)<br>
✅ IoT &amp; embedded systems<br>
✅ AI/ML pipelines with ML.NET<br><br>
<b>🏆 Competitors &amp; Comparison</b><br>
<table class="shortcut-table">
  <tr><th>Language</th><th>Creator</th><th>Primary Use</th><th>How C# compares</th></tr>
  <tr><td><b>Java</b></td><td>Oracle / Sun</td><td>Enterprise, Android</td><td>C# has more modern syntax, better async support, better tooling on Windows</td></tr>
  <tr><td><b>Python</b></td><td>Guido van Rossum</td><td>Data science, scripting, AI</td><td>C# is faster and statically typed; Python is easier for quick scripts</td></tr>
  <tr><td><b>C++</b></td><td>Bjarne Stroustrup</td><td>Systems, games (raw performance)</td><td>C# is much safer (managed memory), easier to write; C++ is faster but complex</td></tr>
  <tr><td><b>TypeScript / JS</b></td><td>Microsoft / Netscape</td><td>Web front-end, Node.js</td><td>C# is a backend/full-stack alternative; TypeScript is browser-first</td></tr>
  <tr><td><b>Go (Golang)</b></td><td>Google</td><td>Cloud, microservices, CLIs</td><td>Go is simpler &amp; minimal; C# is more feature-rich and enterprise-friendly</td></tr>
  <tr><td><b>Kotlin</b></td><td>JetBrains / Google</td><td>Android, JVM</td><td>Very similar modern feel; C# targets .NET, Kotlin targets JVM/Android</td></tr>
  <tr><td><b>Swift</b></td><td>Apple</td><td>iOS, macOS apps</td><td>Swift is Apple-ecosystem only; C# is cross-platform</td></tr>
</table>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">⚡ What Makes C# Special? (What Others Can't Easily Do)</div>
  <div class="card-body">
<div class="feature-grid">
  <div class="feature-pill">
    <strong>🔗 Unified Full-Stack</strong>
    <p>Build front-end (Blazor), back-end (ASP.NET), mobile (MAUI), and games (Unity) — all in the same language.</p>
  </div>
  <div class="feature-pill">
    <strong>⚡ async/await Pioneer</strong>
    <p>C# popularised async/await (2012 — before JS, Python, or Kotlin added it). Asynchronous code reads like synchronous code.</p>
  </div>
  <div class="feature-pill">
    <strong>🧩 LINQ</strong>
    <p>Language-Integrated Query — query arrays, databases, XML, JSON with SQL-like syntax directly in C# code. No other mainstream language has this built-in.</p>
  </div>
  <div class="feature-pill">
    <strong>🛡️ Nullable Reference Types</strong>
    <p>C# 8 introduced compile-time null-safety — the compiler warns you before you cause a NullReferenceException at runtime.</p>
  </div>
  <div class="feature-pill">
    <strong>🏎️ Records &amp; Immutability</strong>
    <p>C# 9 added record types — immutable data objects with value equality built-in. Less boilerplate than Java POJOs or Python dataclasses.</p>
  </div>
  <div class="feature-pill">
    <strong>🎮 Unity Game Development</strong>
    <p>C# is the scripting language for Unity — used to build 60%+ of all mobile games worldwide.</p>
  </div>
  <div class="feature-pill">
    <strong>🔬 Pattern Matching</strong>
    <p>Advanced switch expressions, positional patterns, property patterns — cleaner than if/else chains, more powerful than Java's instanceof.</p>
  </div>
  <div class="feature-pill">
    <strong>📦 NuGet Ecosystem</strong>
    <p>Over 300,000 open-source packages on NuGet.org — the .NET package manager integrates seamlessly into Visual Studio.</p>
  </div>
  <div class="feature-pill">
    <strong>🖥️ Native AOT &amp; Performance</strong>
    <p>C# / .NET 8 supports Native AOT compilation — produces tiny, fast executables without needing the .NET runtime installed.</p>
  </div>
</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🎯 Why Should You Learn C#?</div>
  <div class="card-body">
<b>For job seekers:</b><br>
✅ Consistently top 5 in the TIOBE programming language index<br>
✅ High demand in enterprise, finance, healthcare, gaming, government sectors<br>
✅ Microsoft Azure cloud = massive C# / .NET ecosystem<br>
✅ Average salary: $95,000–$145,000/year (USA, 2025–2026)<br><br>
<b>For students &amp; career changers:</b><br>
✅ One of the best-structured languages to <em>learn programming fundamentals</em><br>
✅ Strongly typed — the compiler catches your mistakes before they run<br>
✅ Excellent documentation (Microsoft Docs / learn.microsoft.com)<br>
✅ Free tools: Visual Studio Community, VS Code, .NET SDK — all free<br><br>
<b>For game developers:</b><br>
✅ Unity uses C# — learn it once, build games for PC, mobile, console, AR/VR<br><br>
<b>🏠 Layman analogy:</b> Learning C# is like learning to drive a Mercedes — once you know it,
you can drive anything. And it's in huge demand everywhere.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🌍 What is C# Compatible With?</div>
  <div class="card-body">
<b>Operating Systems:</b>
<div class="platform-row">
  <div class="platform-badge">🪟 Windows</div>
  <div class="platform-badge">🐧 Linux</div>
  <div class="platform-badge">🍎 macOS</div>
  <div class="platform-badge">📱 Android (MAUI)</div>
  <div class="platform-badge">📱 iOS (MAUI)</div>
  <div class="platform-badge">☁️ Azure Cloud</div>
  <div class="platform-badge">🐳 Docker / Kubernetes</div>
  <div class="platform-badge">🎮 Xbox / Console</div>
</div>
<br>
<b>Frameworks &amp; Runtimes:</b><br>
<table class="shortcut-table">
  <tr><th>Framework</th><th>Use Case</th></tr>
  <tr><td>ASP.NET Core</td><td>Web APIs, MVC websites, Razor Pages</td></tr>
  <tr><td>Blazor</td><td>Interactive web UI in C# (browser + server)</td></tr>
  <tr><td>.NET MAUI</td><td>Cross-platform mobile &amp; desktop (Android, iOS, Windows, macOS)</td></tr>
  <tr><td>WPF / WinForms</td><td>Windows desktop apps</td></tr>
  <tr><td>Unity</td><td>2D/3D games across all platforms</td></tr>
  <tr><td>ML.NET</td><td>Machine learning &amp; AI</td></tr>
  <tr><td>Azure Functions</td><td>Serverless cloud computing</td></tr>
  <tr><td>gRPC / SignalR</td><td>Real-time communication &amp; microservices</td></tr>
</table>
<br>
<b>Databases C# works with:</b> SQL Server, Oracle, PostgreSQL, MySQL, SQLite, MongoDB, Redis, CosmosDB — via EF Core or raw ADO.NET.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🏗️ What Types of Apps Are Best Built with C#?</div>
  <div class="card-body">
<div class="feature-grid">
  <div class="feature-pill">
    <strong>🌐 Web APIs &amp; Microservices</strong>
    <p>ASP.NET Core is one of the fastest web frameworks. Used by Stack Overflow, Microsoft, and thousands of enterprises.</p>
  </div>
  <div class="feature-pill">
    <strong>🏢 Enterprise Line-of-Business Apps</strong>
    <p>CRM, ERP, inventory systems — C# with WPF or ASP.NET is the go-to in corporate environments.</p>
  </div>
  <div class="feature-pill">
    <strong>🎮 Video Games (Unity)</strong>
    <p>Pokémon GO, Cuphead, Cities: Skylines, Among Us — all built with Unity + C#.</p>
  </div>
  <div class="feature-pill">
    <strong>📱 Cross-Platform Mobile Apps</strong>
    <p>.NET MAUI: one codebase → iOS + Android + Windows + macOS apps.</p>
  </div>
  <div class="feature-pill">
    <strong>☁️ Cloud &amp; Serverless</strong>
    <p>Azure Functions, Azure App Services — C# is Azure's first-class citizen.</p>
  </div>
  <div class="feature-pill">
    <strong>🖥️ Windows Desktop Apps</strong>
    <p>WPF (rich UI) and WinForms (classic) remain popular for internal business tools.</p>
  </div>
  <div class="feature-pill">
    <strong>🤖 AI / ML</strong>
    <p>ML.NET for machine learning pipelines; integration with Python AI models via REST.</p>
  </div>
  <div class="feature-pill">
    <strong>🔧 Dev Tools &amp; CLIs</strong>
    <p>Roslyn compiler, PowerShell, NuGet — all built in C#/.NET.</p>
  </div>
</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">⚠️ Challenges of Learning C#</div>
  <div class="card-body">
<table class="shortcut-table">
  <tr><th>#</th><th>Challenge</th><th>Why it's tricky</th><th>How to overcome it</th></tr>
  <tr><td>1</td><td>Understanding types &amp; generics</td><td>C# is strongly typed — you must declare what type every variable is</td><td>Practice with simple examples; the compiler is your teacher</td></tr>
  <tr><td>2</td><td>OOP concepts (classes, interfaces)</td><td>Object-Oriented Programming has many abstract concepts</td><td>Build small real projects (a bank account class, a to-do list)</td></tr>
  <tr><td>3</td><td>async/await &amp; threading</td><td>Asynchronous code can feel confusing at first</td><td>Start with simple async methods, avoid manual threading early</td></tr>
  <tr><td>4</td><td>Understanding .NET vs C#</td><td>Beginners confuse the language (C#) with the platform (.NET)</td><td>Think: C# = the language; .NET = the platform it runs on</td></tr>
  <tr><td>5</td><td>Visual Studio complexity</td><td>VS has hundreds of features — overwhelming at first</td><td>Learn only what you need: create project → write code → run it</td></tr>
  <tr><td>6</td><td>Dependency Injection</td><td>A key .NET pattern that beginners find confusing</td><td>Learn it after you understand interfaces and constructors</td></tr>
  <tr><td>7</td><td>LINQ learning curve</td><td>LINQ syntax (lambdas, method chains) is unfamiliar at first</td><td>Start with simple .Where() and .Select() calls</td></tr>
  <tr><td>8</td><td>C# version differences</td><td>Articles may use C# 5 code vs C# 12 code — looks very different</td><td>Always check the C# version the tutorial targets</td></tr>
</table>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🚀 How to Learn C# (Complete Beginner Roadmap)</div>
  <div class="card-body">
<b>🏠 Layman analogy:</b> Learning C# is like learning to cook. Start with boiling water,
then make an omelette, then a full meal — don't try a 5-course dinner on day one!<br><br>
<b>Phase 1 — Install &amp; Hello World (Day 1–3)</b><br>
<div class="wf-diagram">
  <div class="wf-node">Install .NET SDK</div>
  <div class="wf-arrow">→</div>
  <div class="wf-node">Install VS Code or Visual Studio</div>
  <div class="wf-arrow">→</div>
  <div class="wf-node">dotnet new console</div>
  <div class="wf-arrow">→</div>
  <div class="wf-node-green">Run Hello World ✅</div>
</div>
<br>
<b>Phase 2 — Core Language Basics (Week 1–3)</b><br>
Variables &amp; types → Operators → if/else → loops (for, while, foreach) → methods → arrays<br><br>
<b>Phase 3 — Object-Oriented Programming (Week 4–6)</b><br>
Classes → Objects → Constructors → Properties → Inheritance → Interfaces → Abstract classes<br><br>
<b>Phase 4 — Intermediate C# (Month 2)</b><br>
Generics → Collections (List, Dictionary) → LINQ → Exception handling → File I/O → async/await<br><br>
<b>Phase 5 — Real Framework (Month 3+)</b><br>
Pick ONE: ASP.NET Core (web) OR Unity (games) OR WPF (desktop) and build a project<br><br>
<b>🎓 Free Learning Resources:</b><br>
✅ <b>learn.microsoft.com/dotnet/csharp</b> — official Microsoft C# tour (best starting point)<br>
✅ <b>dotnet.microsoft.com/learn</b> — free interactive browser-based tutorials<br>
✅ <b>CS50 (Harvard)</b> — free intro to programming using C#<br>
✅ <b>YouTube: Tim Corey, Nick Chapsas, IAmTimCorey</b> — top C# instructors<br>
✅ <b>freeCodeCamp C# Certification</b> — free structured course<br><br>
<b>💡 Tip for non-technical beginners:</b> Don't learn C# in isolation — pick a project that
excites you (a small game, a personal expense tracker, a website) and learn what you need to
build it. Purpose-driven learning is 10× faster.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">📜 C# Version Timeline — Evolution from 1.0 to 13.0</div>
  <div class="card-body">
<table class="shortcut-table">
  <tr><th>C# Version</th><th>.NET Version</th><th>Year</th><th>Headline Features</th></tr>
  <tr><td><b>C# 1.0</b></td><td>.NET Framework 1.0</td><td>2002</td><td>Classes, interfaces, delegates, events, properties, value types, garbage collection</td></tr>
  <tr><td><b>C# 2.0</b></td><td>.NET Framework 2.0</td><td>2005</td><td>Generics, iterators (yield), nullable types, anonymous methods, partial classes</td></tr>
  <tr><td><b>C# 3.0</b></td><td>.NET Framework 3.5</td><td>2007</td><td>LINQ, lambda expressions, extension methods, auto-properties, anonymous types, var</td></tr>
  <tr><td><b>C# 4.0</b></td><td>.NET Framework 4.0</td><td>2010</td><td>dynamic keyword, optional/named parameters, covariance &amp; contravariance</td></tr>
  <tr><td><b>C# 5.0</b></td><td>.NET Framework 4.5</td><td>2012</td><td>async/await — the biggest game-changer for non-blocking code</td></tr>
  <tr><td><b>C# 6.0</b></td><td>.NET Framework 4.6 / .NET Core 1.0</td><td>2015</td><td>String interpolation ($""), null-conditional (?.), expression-bodied members, nameof</td></tr>
  <tr><td><b>C# 7.0–7.3</b></td><td>.NET Framework 4.7 / .NET Core 2.x</td><td>2017</td><td>Tuples, out variables, pattern matching (is), local functions, throw expressions</td></tr>
  <tr><td><b>C# 8.0</b></td><td>.NET Core 3.0 / 3.1</td><td>2019</td><td>Nullable reference types, switch expressions, ranges &amp; indices (^, ..), async streams</td></tr>
  <tr><td><b>C# 9.0</b></td><td>.NET 5</td><td>2020</td><td>Records, init-only setters, top-level statements, pattern matching enhancements</td></tr>
  <tr><td><b>C# 10.0</b></td><td>.NET 6</td><td>2021</td><td>Global using, file-scoped namespaces, record structs, constant interpolated strings</td></tr>
  <tr><td><b>C# 11.0</b></td><td>.NET 7</td><td>2022</td><td>Required members, raw string literals, list patterns, generic attributes, UTF-8 strings</td></tr>
  <tr><td><b>C# 12.0</b></td><td>.NET 8 ✅ LTS</td><td>2023</td><td>Primary constructors, collection expressions, inline arrays, default lambda params</td></tr>
  <tr><td><b>C# 13.0</b></td><td>.NET 9</td><td>2024</td><td>params collections, new lock type, field keyword in properties, iterator async improvements</td></tr>
  <tr><td><b>C# 14.0</b></td><td>.NET 10 (LTS, Nov 2025)</td><td>2025</td><td>In development — upcoming features being drafted in language design GitHub</td></tr>
</table>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🔄 C# Feature Evolution — Same Topic Across All Versions</div>
  <div class="card-body">
Tracking how <b>"printing a person's name and age"</b> evolved across C# versions shows why
newer syntax exists and what problem it solves.<br><br>

<b>📌 C# 1.0 — String concatenation (2002)</b>
<div class="cmd-block">
string name = "Alice";
int age = 30;
Console.WriteLine("Name: " + name + ", Age: " + age);
// ❌ Issue: verbose, hard to read, error-prone with many variables
</div>
<b>📌 C# 5.0 — String.Format (improvement, ~2012)</b>
<div class="cmd-block">
Console.WriteLine(String.Format("Name: {0}, Age: {1}", name, age));
// Better, but {0} {1} placeholders are still confusing
</div>
<b>📌 C# 6.0 — String Interpolation ✅ (2015)</b>
<div class="cmd-block">
Console.WriteLine($"Name: {name}, Age: {age}");
// ✅ Clean, readable — variables inline with the string
// 🏠 Layman: Like filling in blanks in a sentence: "Name: [name], Age: [age]"
</div>
<b>📌 C# 9.0 — Top-level statements (2020)</b>
<div class="cmd-block">
// No class or Main method needed!
string name = "Alice";
int age = 30;
Console.WriteLine($"Name: {name}, Age: {age}");
// ✅ Perfect for scripts and beginners — less boilerplate
</div>
<hr style="border:none;border-top:1px solid #ddd;margin:1.2rem 0">

<b>📌 Tracking "Null Checking" evolution</b><br><br>
<b>C# 1.0–5.0 — Classic null check</b>
<div class="cmd-block">
if (user != null)
{
Console.WriteLine(user.Name);
}
// ❌ Easy to forget, causes NullReferenceException at runtime
</div>
<b>C# 6.0 — Null-conditional operator (?.) (2015)</b>
<div class="cmd-block">
Console.WriteLine(user?.Name);
// ✅ If user is null, returns null instead of crashing
// 🏠 Layman: "If the person exists, tell me their name; otherwise say nothing"
</div>
<b>C# 6.0 — Null-coalescing (??)</b>
<div class="cmd-block">
string displayName = user?.Name ?? "Guest";
// ✅ "Use user's name, OR if null, use 'Guest'"
</div>
<b>C# 8.0 — Nullable reference types (compile-time safety)</b>
<div class="cmd-block">
// In .csproj: &lt;Nullable&gt;enable&lt;/Nullable&gt;
string? name = null;   // ✅ explicitly nullable
string  name2 = null;  // ❌ Compiler WARNING — this should never be null!
</div>
<hr style="border:none;border-top:1px solid #ddd;margin:1.2rem 0">

<b>📌 Tracking "Data class / model" evolution</b><br><br>
<b>C# 1.0–8.0 — Classic class with properties</b>
<div class="cmd-block">
public class Person
{
public string Name { get; set; }
public int Age { get; set; }
// Need to manually write Equals(), GetHashCode(), ToString()
}
</div>
<b>C# 9.0 — Record types ✅ (2020)</b>
<div class="cmd-block">
public record Person(string Name, int Age);
// ✅ One line! Auto-generates constructor, Equals, GetHashCode, ToString
// ✅ Immutable by default
// 🏠 Layman: A record is like a stamped official form — once filled, it doesn't change
&#8203;
var p1 = new Person("Alice", 30);
var p2 = new Person("Alice", 30);
Console.WriteLine(p1 == p2); // true — value equality!
// In a regular class, this would be false (reference equality)
</div>
<b>C# 9.0 — with expressions (non-destructive mutation)</b>
<div class="cmd-block">
var p3 = p1 with { Age = 31 };
// Creates a new Person with everything from p1, but Age = 31
// ✅ Immutable data + easy "update"
</div>
<hr style="border:none;border-top:1px solid #ddd;margin:1.2rem 0">

<b>📌 Tracking "Switch / branching" evolution</b><br><br>
<b>C# 1.0 — Classic switch</b>
<div class="cmd-block">
string day = "Monday";
string type;
switch (day)
{
case "Saturday":
case "Sunday":
    type = "Weekend";
    break;
default:
    type = "Weekday";
    break;
}
</div>
<b>C# 8.0 — Switch expression ✅ (2019)</b>
<div class="cmd-block">
string type = day switch
{
"Saturday" or "Sunday" => "Weekend",
_ => "Weekday"
};
// ✅ Concise, returns a value, no 'break' needed
// 🏠 Layman: Like a lookup table — "for this input, give me that output"
</div>
<b>C# 8.0 — Property pattern matching</b>
<div class="cmd-block">
string category = person switch
{
{ Age: < 18 }             => "Minor",
{ Age: >= 18, Age: < 65 } => "Adult",
_                         => "Senior"
};
// ✅ Reads like English rules
</div>
<hr style="border:none;border-top:1px solid #ddd;margin:1.2rem 0">

<b>📌 Tracking "Async programming" evolution</b><br><br>
<b>C# 1.0–4.0 — Callbacks / BeginInvoke (painful)</b>
<div class="cmd-block">
// Old way — callbacks make "callback hell"
webClient.DownloadStringCompleted += (s, e) => {
Console.WriteLine(e.Result);  // runs when done
};
webClient.DownloadStringAsync(new Uri("https://example.com"));
// ❌ Hard to read, hard to debug, hard to chain
</div>
<b>C# 5.0 — async/await ✅ (2012 — game changer!)</b>
<div class="cmd-block">
async Task FetchDataAsync()
{
string result = await httpClient.GetStringAsync("https://example.com");
Console.WriteLine(result);
}
// ✅ Reads like synchronous code — no callbacks!
// 🏠 Layman: Like ordering food at a restaurant — you sit, wait (await), and your
//   food arrives (result) without blocking everyone else in the restaurant
</div>
<hr style="border:none;border-top:1px solid #ddd;margin:1.2rem 0">

<b>📌 Tracking "Collections / Filtering" evolution (LINQ)</b><br><br>
<b>C# 1.0–2.0 — Manual loop filtering</b>
<div class="cmd-block">
List&lt;int&gt; numbers = new List&lt;int&gt; { 1, 2, 3, 4, 5, 6 };
List&lt;int&gt; evens = new List&lt;int&gt;();
foreach (int n in numbers)
{
if (n % 2 == 0) evens.Add(n);
}
</div>
<b>C# 3.0 — LINQ ✅ (2007)</b>
<div class="cmd-block">
var evens = numbers.Where(n => n % 2 == 0).ToList();
// ✅ One line, expressive
// 🏠 Layman: "Give me only the items WHERE my condition is true"
&#8203;
// Query syntax (SQL-like):
var evens2 = (from n in numbers where n % 2 == 0 select n).ToList();
</div>
<b>C# 12.0 — Collection expressions ✅ (2023)</b>
<div class="cmd-block">
int[] nums = [1, 2, 3, 4, 5];   // ✅ New [ ] syntax — same for arrays, lists, spans
List&lt;int&gt; more = [1, 2, ..nums]; // ✅ Spread operator — merge collections easily
</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🎓 What a New .NET Developer Must Be Strong In</div>
  <div class="card-body">
These are the <b>non-negotiable foundations</b> that every C# / .NET developer is expected to
understand deeply — not just know the syntax, but <em>understand why</em>.<br><br>
<table class="shortcut-table">
  <tr><th>Priority</th><th>Topic</th><th>Why it matters</th><th>🏠 Layman analogy</th></tr>
  <tr><td>🔴 Must</td><td>Value types vs Reference types</td><td>Determines how variables are copied, passed, and stored in memory</td><td>A house (reference) vs a house blueprint (value)</td></tr>
  <tr><td>🔴 Must</td><td>Classes, Objects, Constructors</td><td>Everything in C# is an object — foundation of OOP</td><td>A class is a cookie cutter; objects are the cookies</td></tr>
  <tr><td>🔴 Must</td><td>Interfaces</td><td>Used everywhere in .NET for abstraction and dependency injection</td><td>A contract: "I promise to have these methods"</td></tr>
  <tr><td>🔴 Must</td><td>async/await</td><td>Every modern API, database call, HTTP request is async</td><td>Ordering food without blocking the restaurant kitchen</td></tr>
  <tr><td>🔴 Must</td><td>LINQ (basic)</td><td>Used in every .NET codebase to query collections and databases</td><td>SQL for your in-memory lists</td></tr>
  <tr><td>🔴 Must</td><td>Exception handling (try/catch/finally)</td><td>Production code must handle failures gracefully</td><td>A safety net under a tightrope walker</td></tr>
  <tr><td>🔴 Must</td><td>Generics (List&lt;T&gt;, Dictionary&lt;K,V&gt;)</td><td>Reusable, type-safe code — used constantly</td><td>A box that works for any type of item</td></tr>
  <tr><td>🟡 Should</td><td>Dependency Injection (DI)</td><td>The .NET DI container is used in every ASP.NET Core app</td><td>A vending machine — request what you need, get it</td></tr>
  <tr><td>🟡 Should</td><td>Delegates &amp; Events</td><td>Foundation of UI frameworks (WPF, WinForms) and callbacks</td><td>A referee who calls players when needed</td></tr>
  <tr><td>🟡 Should</td><td>Nullable reference types</td><td>Helps write null-safe code — huge source of runtime bugs otherwise</td><td>Marking "this can be empty" clearly on a form</td></tr>
  <tr><td>🟡 Should</td><td>Records &amp; immutability</td><td>Modern C# style for data transfer objects (DTOs)</td><td>A sealed certificate — can't be changed after issuing</td></tr>
  <tr><td>🟡 Should</td><td>Pattern matching</td><td>Cleaner conditionals — used heavily in modern C# codebases</td><td>A smart sorting machine that routes items by rules</td></tr>
  <tr><td>🟢 Nice</td><td>Reflection</td><td>Inspect types at runtime — used in frameworks, serialisation</td><td>An x-ray machine for code</td></tr>
  <tr><td>🟢 Nice</td><td>Span&lt;T&gt; / Memory&lt;T&gt;</td><td>High-performance zero-allocation slicing of buffers</td><td>A window into a larger array — no copying</td></tr>
</table>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🔬 Anatomy of a C# Program — Every Part Explained</div>
  <div class="card-body">
Let's dissect this complete C# program and label every concept:<br><br>
<div class="cmd-block">
// ① Using directive — imports a namespace (like "import" in Python / Java)
using System;
using System.Collections.Generic;
&#8203;
// ② Namespace — groups related classes together (like a folder)
namespace MyApp.Learning
{
// ③ Class — a blueprint / template for creating objects
//    "public" = accessible from other code
public class BankAccount
{
    // ④ Field — a private variable that stores state inside the class
    private decimal _balance;
&#8203;
    // ⑤ Property — controlled access to a field (get/set)
    //    "public" = readable from outside, "private set" = only settable inside
    public string Owner { get; private set; }
&#8203;
    // ⑥ Constructor — special method called when an object is created
    //    "this" refers to the current instance
    public BankAccount(string owner, decimal initialBalance)
    {
        Owner    = owner;        // ← set the property
        _balance = initialBalance;
    }
&#8203;
    // ⑦ Method — a named action the class can perform
    //    returns void (nothing), takes a decimal parameter
    public void Deposit(decimal amount)
    {
        // ⑧ Exception handling — catch and handle errors gracefully
        if (amount &lt;= 0)
            throw new ArgumentException("Amount must be positive.");
&#8203;
        _balance += amount;
        // ⑨ String interpolation — embed expressions inside strings
        Console.WriteLine($"Deposited {amount:C}. New balance: {_balance:C}");
    }
&#8203;
    // ⑩ Expression-bodied method (C# 6+) — one-liner method
    public decimal GetBalance() =&gt; _balance;
}
&#8203;
// ⑪ Derived class — inherits from BankAccount (Inheritance)
public class SavingsAccount : BankAccount
{
    // ⑫ Auto-property with init-only setter (C# 9)
    public decimal InterestRate { get; init; }
&#8203;
    public SavingsAccount(string owner, decimal balance, decimal rate)
        : base(owner, balance)      // ← calls the parent constructor
    {
        InterestRate = rate;
    }
&#8203;
    // ⑬ Method override — customise inherited behaviour
    public void ApplyInterest()
    {
        decimal interest = GetBalance() * InterestRate;
        Deposit(interest);
    }
}
&#8203;
// ⑭ Interface — a contract: any class implementing this MUST have these members
public interface IReportable
{
    void PrintReport();
}
&#8203;
// ⑮ Record — immutable data type (C# 9), auto-generates Equals/ToString
public record Transaction(string Type, decimal Amount, DateTime Date);
&#8203;
// ⑯ Program entry point
public class Program
{
    // ⑰ Main method — where execution begins
    //    async Task = supports awaiting async operations
    public static async Task Main(string[] args)
    {
        // ⑱ Object instantiation — create an instance from the class blueprint
        var account = new SavingsAccount("Alice", 1000m, 0.05m);
&#8203;
        account.Deposit(500m);
        account.ApplyInterest();
&#8203;
        // ⑲ var keyword — type inferred by compiler (C# 3+)
        var balance = account.GetBalance();
&#8203;
        // ⑳ LINQ — query a collection with lambda expressions
        var transactions = new List&lt;Transaction&gt;
        {
            new("Deposit",  500m,  DateTime.Now),
            new("Interest", 75m,   DateTime.Now),
        };
&#8203;
        // Filter: only deposits
        var deposits = transactions.Where(t =&gt; t.Type == "Deposit").ToList();
&#8203;
        // ㉑ async/await — non-blocking I/O operation
        await Task.Delay(10); // simulate async work
&#8203;
        Console.WriteLine($"Final balance for {account.Owner}: {balance:C}");
    }
}
}
</div>
<br>
<b>📖 Concept Index:</b><br>
<table class="shortcut-table">
  <tr><th>Symbol</th><th>Concept</th><th>🏠 Layman Explanation</th></tr>
  <tr><td>①</td><td>using directive</td><td>Like plugging in a toolbox before using its tools</td></tr>
  <tr><td>②</td><td>Namespace</td><td>A folder/category to organise related code</td></tr>
  <tr><td>③</td><td>Class</td><td>A blueprint — defines what an object looks like and can do</td></tr>
  <tr><td>④</td><td>Field (private)</td><td>A secret drawer inside the object — only it can access it directly</td></tr>
  <tr><td>⑤</td><td>Property (get/set)</td><td>A controlled window into the secret drawer — you choose who can read/write</td></tr>
  <tr><td>⑥</td><td>Constructor</td><td>The setup instructions when you first build the object</td></tr>
  <tr><td>⑦</td><td>Method</td><td>An action/verb — what the object can do</td></tr>
  <tr><td>⑧</td><td>Exception handling</td><td>A safety net — "if something goes wrong, do this instead of crashing"</td></tr>
  <tr><td>⑨</td><td>String interpolation</td><td>Fill-in-the-blank for text: "Hello, {name}!"</td></tr>
  <tr><td>⑩</td><td>Expression-bodied member</td><td>A shorthand one-liner for simple methods</td></tr>
  <tr><td>⑪</td><td>Inheritance</td><td>A child class gets everything from the parent and adds its own things</td></tr>
  <tr><td>⑫</td><td>init-only property</td><td>Can only be set during object creation — locked afterwards</td></tr>
  <tr><td>⑬</td><td>Method override</td><td>The child rewrites a parent method to behave differently</td></tr>
  <tr><td>⑭</td><td>Interface</td><td>A signed contract: "I promise to provide these capabilities"</td></tr>
  <tr><td>⑮</td><td>Record</td><td>A sealed, official form — values set once, never changed</td></tr>
  <tr><td>⑯–⑰</td><td>Program entry / Main</td><td>The front door of your program — execution starts here</td></tr>
  <tr><td>⑱</td><td>Object instantiation (new)</td><td>Using the blueprint to build an actual object</td></tr>
  <tr><td>⑲</td><td>var keyword</td><td>Let the compiler figure out the type — you don't need to spell it out</td></tr>
  <tr><td>⑳</td><td>LINQ + lambda</td><td>A filter/query sentence: "From this list, give me items WHERE …"</td></tr>
  <tr><td>㉑</td><td>async/await</td><td>Wait for a slow task without freezing everything else</td></tr>
</table>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">📚 Key C# Concepts — Technical + Layman Explanations</div>
  <div class="card-body">

<div class="card-section-title">1. VALUE TYPES vs REFERENCE TYPES</div>
<b>Technical:</b> Value types (int, bool, struct, enum) are stored on the <em>stack</em> and
copied when assigned. Reference types (class, string, array) are stored on the <em>heap</em>
and passing them passes a reference (pointer) to the same object.<br>
<b>🏠 Layman:</b> Value type = handing someone a photocopy of a document (they get their own copy).
Reference type = sharing a Google Doc link (both people see and edit the same document).<br>
<div class="cmd-block">
int a = 5;
int b = a;    // b is a COPY — changing b doesn't affect a
b = 10;
Console.WriteLine(a); // 5 — unchanged ✅
&#8203;
var list1 = new List&lt;int&gt; { 1, 2, 3 };
var list2 = list1;    // list2 POINTS to the same list
list2.Add(4);
Console.WriteLine(list1.Count); // 4 — list1 also changed! ⚠️
</div>

<div class="card-section-title">2. GENERICS</div>
<b>Technical:</b> Generics allow you to write type-safe, reusable code using a type
parameter (&lt;T&gt;). The compiler enforces the type at compile time — no runtime casting needed.<br>
<b>🏠 Layman:</b> A generic box: "This box holds exactly one type of thing — you decide which
type when you order the box. After that, you can only put that type in."<br>
<div class="cmd-block">
// Without generics — dangerous (any object, cast required)
ArrayList oldList = new ArrayList();
oldList.Add(42);
oldList.Add("oops");        // compiles but runtime crash if you expect int!
&#8203;
// With generics — safe ✅
List&lt;int&gt; safeList = new List&lt;int&gt;();
safeList.Add(42);
// safeList.Add("oops");    // ❌ Compile-time error — caught before it runs!
&#8203;
// Generic method
T Max&lt;T&gt;(T a, T b) where T : IComparable&lt;T&gt;
=&gt; a.CompareTo(b) &gt; 0 ? a : b;
&#8203;
Console.WriteLine(Max(3, 7));              // 7
Console.WriteLine(Max("apple", "banana")); // banana
</div>

<div class="card-section-title">3. DELEGATES &amp; EVENTS</div>
<b>Technical:</b> A delegate is a type-safe function pointer — a variable that holds a
reference to a method. Events are a publisher/subscriber pattern built on delegates.<br>
<b>🏠 Layman:</b> A delegate is like a job posting: "I need someone who can take an int and
return a string." Any method matching that description can fill the role.
An event is like a doorbell: when pressed, all registered listeners are notified.<br>
<div class="cmd-block">
// Delegate type declaration
delegate string Formatter(int value);
&#8203;
// Methods that match the delegate signature
string ToHex(int n)    =&gt; $"0x{n:X}";
string ToBinary(int n) =&gt; Convert.ToString(n, 2);
&#8203;
Formatter fmt = ToHex;
Console.WriteLine(fmt(255)); // 0xFF
&#8203;
fmt = ToBinary;
Console.WriteLine(fmt(10));  // 1010
&#8203;
// Built-in delegate types: Action (void), Func (returns value), Predicate (bool)
Action&lt;string&gt; greet    = name =&gt; Console.WriteLine($"Hello, {name}!");
Func&lt;int, int, int&gt; add = (a, b) =&gt; a + b;
greet("Alice");               // Hello, Alice!
Console.WriteLine(add(3, 4)); // 7
</div>

<div class="card-section-title">4. LINQ (Language Integrated Query)</div>
<b>Technical:</b> LINQ provides declarative query syntax for any IEnumerable&lt;T&gt; or
IQueryable&lt;T&gt; source — collections, databases (EF Core), XML, JSON.<br>
<b>🏠 Layman:</b> LINQ is like SQL for your C# lists. "Give me all customers FROM my list
WHERE their city is London, ORDER BY name, and take only the TOP 5."<br>
<div class="cmd-block">
var people = new List&lt;(string Name, int Age, string City)&gt;
{
("Alice", 30, "London"),
("Bob",   25, "Paris"),
("Carol", 35, "London"),
("Dave",  28, "Berlin"),
};
&#8203;
// Method syntax (most common)
var londonAdults = people
.Where(p =&gt; p.City == "London" &amp;&amp; p.Age &gt;= 30)
.OrderBy(p =&gt; p.Name)
.Select(p =&gt; p.Name)
.ToList();
// Result: ["Alice", "Carol"]
&#8203;
// Aggregation
int    totalAge = people.Sum(p =&gt; p.Age);      // 118
double avgAge   = people.Average(p =&gt; p.Age);  // 29.5
int    oldest   = people.Max(p =&gt; p.Age);      // 35
</div>

<div class="card-section-title">5. ASYNC / AWAIT</div>
<b>Technical:</b> async/await is syntactic sugar over the Task Parallel Library (TPL).
An async method returns Task or Task&lt;T&gt;. The await keyword yields control back to the
caller while waiting for the awaited task — without blocking the thread.<br>
<b>🏠 Layman:</b> Imagine a waiter at a restaurant. Without async, the waiter stands at your
table until your food is cooked (blocking everyone). With async, the waiter takes your order,
goes to serve others, and comes back when your food is ready.<br>
<div class="cmd-block">
async Task&lt;string&gt; FetchWebPageAsync(string url)
{
using var client = new HttpClient();
// Await = "start this, come back when done, don't block"
string content = await client.GetStringAsync(url);
return content.Substring(0, 200);
}
&#8203;
// Run multiple async tasks in parallel
async Task RunParallelAsync()
{
var task1 = FetchWebPageAsync("https://example.com");
var task2 = FetchWebPageAsync("https://microsoft.com");
&#8203;
// Wait for BOTH to complete simultaneously
string[] results = await Task.WhenAll(task1, task2);
Console.WriteLine($"Got {results.Length} pages");
}
</div>

<div class="card-section-title">6. DEPENDENCY INJECTION (DI)</div>
<b>Technical:</b> DI is a design pattern where dependencies (services) are injected into a
class via its constructor rather than the class creating them. .NET has a built-in DI container
(IServiceCollection / IServiceProvider).<br>
<b>🏠 Layman:</b> Instead of a chef buying their own ingredients (tight coupling), the
restaurant manager delivers them to the kitchen (injection). The chef doesn't need to know
where the ingredients come from — they just use them.<br>
<div class="cmd-block">
// Interface (the contract)
public interface IEmailService
{
Task SendAsync(string to, string subject, string body);
}
&#8203;
// Real implementation
public class SmtpEmailService : IEmailService
{
public async Task SendAsync(string to, string subject, string body)
    =&gt; await Task.Run(() =&gt; Console.WriteLine($"Sending email to {to}"));
}
&#8203;
// Consumer — receives IEmailService via constructor injection
public class OrderService
{
private readonly IEmailService _email;
&#8203;
public OrderService(IEmailService email) =&gt; _email = email;
&#8203;
public async Task PlaceOrderAsync(string customerEmail)
{
    await _email.SendAsync(customerEmail, "Order confirmed", "Thanks!");
}
}
&#8203;
// Registration in ASP.NET Core (Program.cs)
// builder.Services.AddScoped&lt;IEmailService, SmtpEmailService&gt;();
// ✅ Swap SmtpEmailService for MockEmailService in tests — zero code changes!
</div>

<div class="card-section-title">7. EXCEPTION HANDLING</div>
<b>Technical:</b> Exceptions propagate up the call stack until caught by a try/catch block.
finally always runs (cleanup). Custom exceptions inherit from Exception.<br>
<b>🏠 Layman:</b> Exception handling is like a safety net in a circus. If an acrobat
(method) falls (throws an exception), the net (catch) catches them. The stage crew
(finally) always tidies up, regardless of what happened.<br>
<div class="cmd-block">
public decimal Divide(decimal a, decimal b)
{
if (b == 0)
    throw new DivideByZeroException("Cannot divide by zero!");
return a / b;
}
&#8203;
try
{
decimal result = Divide(10, 0);
Console.WriteLine(result);
}
catch (DivideByZeroException ex)
{
Console.WriteLine($"Math error: {ex.Message}"); // handled ✅
}
catch (Exception ex)
{
Console.WriteLine($"Unexpected: {ex.Message}"); // catch-all fallback
}
finally
{
Console.WriteLine("This always runs — good for cleanup (close files, etc.)");
}
&#8203;
// Custom exception
public class InsufficientFundsException : Exception
{
public decimal RequiredAmount { get; }
public InsufficientFundsException(decimal amount)
    : base($"Need {amount:C} more in your account.") =&gt; RequiredAmount = amount;
}
</div>

<div class="card-section-title">8. PATTERN MATCHING (C# 7–12)</div>
<b>Technical:</b> Pattern matching allows conditional logic based on the shape/type/value of
data using is, switch expressions, property patterns, list patterns, and relational patterns.<br>
<b>🏠 Layman:</b> Pattern matching is like a smart sorting machine at a post office. Instead
of writing many separate "if it's a large box, do X; if it's a small envelope, do Y" rules,
you write one clear set of patterns and the machine routes each parcel automatically.<br>
<div class="cmd-block">
object shape = new Circle(5.0);
&#8203;
// Type pattern (C# 7)
if (shape is Circle c)
Console.WriteLine($"Area: {Math.PI * c.Radius * c.Radius:F2}");
&#8203;
// Switch expression with property pattern (C# 8)
double area = shape switch
{
Circle    { Radius: var r }              =&gt; Math.PI * r * r,
Rectangle { Width: var w, Height: var h } =&gt; w * h,
Triangle  { Base: var b, Height: var h }  =&gt; 0.5 * b * h,
null =&gt; throw new ArgumentNullException(nameof(shape)),
_    =&gt; throw new NotSupportedException("Unknown shape")
};
&#8203;
// List pattern (C# 11)
int[] nums = { 1, 2, 3 };
string desc = nums switch
{
[]          =&gt; "empty",
[var x]     =&gt; $"single: {x}",
[1, 2, ..]  =&gt; "starts with 1, 2",
_           =&gt; "other"
};
</div>

  </div>
</div>
""",
        unsafe_allow_html=True,
    )

