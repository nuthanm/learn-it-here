import streamlit as st


def render_dotnet():
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🟣 What is .NET? (For Complete Beginners)</div>
  <div class="card-body">
<b>.NET</b> (pronounced "dot net") is a <em>free, open-source developer platform</em> created by
Microsoft. Think of it as a powerful toolbox that lets you build all kinds of software —
websites, mobile apps, desktop apps, games, cloud services, and more — using a common set
of tools and languages (mainly <b>C#</b>, F#, and VB.NET).<br><br>
<b>Why should you learn it?</b><br>
✅ Used by millions of developers worldwide<br>
✅ Backed by Microsoft and a huge open-source community<br>
✅ Runs on Windows, macOS, and Linux<br>
✅ Excellent performance — one of the fastest web frameworks in the world<br>
✅ Great job market demand<br><br>
<b>Simple analogy:</b> If programming is like cooking, .NET is the professional kitchen
(with all utensils, ovens, and recipes) — C# is the chef who works in that kitchen.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">📜 .NET Release History &amp; Associated C# Versions</div>
  <div class="card-body">
Every version of .NET comes paired with a version of C# — the primary language used to write .NET apps.
Here's the full picture from the very beginning:<br><br>
<table class="shortcut-table">
  <tr><th>.NET Version</th><th>Release Year</th><th>C# Version</th><th>Support Type</th><th>Key Highlights</th></tr>
  <tr><td>.NET Framework 1.0</td><td>2002</td><td>C# 1.0</td><td>End of Life</td><td>The very first .NET — Windows only, introduced CLR &amp; BCL</td></tr>
  <tr><td>.NET Framework 1.1</td><td>2003</td><td>C# 1.2</td><td>End of Life</td><td>Bug fixes, ASP.NET improvements</td></tr>
  <tr><td>.NET Framework 2.0</td><td>2005</td><td>C# 2.0</td><td>End of Life</td><td>Generics, anonymous methods, nullable types</td></tr>
  <tr><td>.NET Framework 3.0</td><td>2006</td><td>C# 2.0</td><td>End of Life</td><td>WPF, WCF, WF introduced</td></tr>
  <tr><td>.NET Framework 3.5</td><td>2007</td><td>C# 3.0</td><td>End of Life</td><td>LINQ, lambda expressions, extension methods</td></tr>
  <tr><td>.NET Framework 4.0</td><td>2010</td><td>C# 4.0</td><td>End of Life</td><td>TPL (Task Parallel Library), dynamic keyword</td></tr>
  <tr><td>.NET Framework 4.5</td><td>2012</td><td>C# 5.0</td><td>End of Life</td><td>async/await introduced</td></tr>
  <tr><td>.NET Framework 4.6</td><td>2015</td><td>C# 6.0</td><td>End of Life</td><td>RyuJIT compiler, string interpolation</td></tr>
  <tr><td>.NET Framework 4.7</td><td>2017</td><td>C# 7.x</td><td>End of Life</td><td>Tuples, pattern matching, local functions</td></tr>
  <tr><td>.NET Framework 4.8</td><td>2019</td><td>C# 7.3</td><td>Maintenance</td><td>Last ever .NET Framework — still supported on Windows</td></tr>
  <tr><td><b>.NET Core 1.0</b></td><td>2016</td><td>C# 6.0</td><td>End of Life</td><td>First cross-platform .NET — Linux/macOS support!</td></tr>
  <tr><td>.NET Core 2.0</td><td>2017</td><td>C# 7.1</td><td>End of Life</td><td>.NET Standard 2.0 support, massive API expansion</td></tr>
  <tr><td>.NET Core 2.1</td><td>2018</td><td>C# 7.3</td><td>End of Life</td><td>LTS release, Span&lt;T&gt;, SignalR</td></tr>
  <tr><td>.NET Core 3.0</td><td>2019</td><td>C# 8.0</td><td>End of Life</td><td>WPF/WinForms on Core, Blazor Server</td></tr>
  <tr><td>.NET Core 3.1</td><td>2019</td><td>C# 8.0</td><td>End of Life (2022)</td><td>LTS — most used Core version; gRPC support</td></tr>
  <tr><td><b>.NET 5</b></td><td>2020</td><td>C# 9.0</td><td>End of Life</td><td>Unified .NET — merged Core + Framework vision; no "Core" branding</td></tr>
  <tr><td><b>.NET 6</b></td><td>2021</td><td>C# 10.0</td><td>End of Life (2024)</td><td>LTS — minimal APIs, .NET MAUI preview, hot reload</td></tr>
  <tr><td>.NET 7</td><td>2022</td><td>C# 11.0</td><td>End of Life</td><td>STS — rate limiting, output caching, regex improvements</td></tr>
  <tr><td><b>.NET 8</b></td><td>2023</td><td>C# 12.0</td><td><b>LTS ✅ Current</b></td><td>Native AOT, Blazor United, primary constructors, collection expressions</td></tr>
  <tr><td>.NET 9</td><td>2024</td><td>C# 13.0</td><td>STS</td><td>LINQ improvements, params spans, Task.WhenEach</td></tr>
  <tr><td><b>.NET 10</b></td><td>2025 (Nov)</td><td>C# 14.0</td><td><b>LTS (Upcoming)</b></td><td>In development — next long-term support release</td></tr>
</table>
<br>
<b>LTS</b> = Long-Term Support (3 years). <b>STS</b> = Standard-Term Support (18 months).
<b>Rule of thumb:</b> Use an LTS version for production apps — currently <b>.NET 8</b>.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">⚖️ .NET Framework vs .NET Standard vs .NET (Core / 5+)</div>
  <div class="card-body">
This is one of the most confusing things for beginners — three names that all say ".NET"!
Let's break it down with plain English and a comparison table.<br><br>
<b>Think of it this way:</b><br>
🏠 <b>.NET Framework</b> = An old house (Windows-only, comfy but can't be moved)<br>
📐 <b>.NET Standard</b> = A set of blueprints (a contract that different .NETs agree to follow)<br>
🚀 <b>.NET (Core / 5+)</b> = The new modern building (cross-platform, fast, the future)<br><br>
<table class="shortcut-table">
  <tr><th>Feature</th><th>.NET Framework</th><th>.NET Standard</th><th>.NET (Core / 5+)</th></tr>
  <tr><td>What it is</td><td>Original full Windows .NET</td><td>A specification/interface (not a runtime)</td><td>Modern, unified cross-platform .NET</td></tr>
  <tr><td>Runs on</td><td>Windows only</td><td>N/A — it's a standard, not a runtime</td><td>Windows, macOS, Linux</td></tr>
  <tr><td>Status</td><td>Maintenance (no new features)</td><td>Superseded by .NET 5+ (still used in libraries)</td><td>Active — all future development here</td></tr>
  <tr><td>Latest version</td><td>4.8.1</td><td>2.1</td><td>.NET 9 (LTS: .NET 8)</td></tr>
  <tr><td>Who should use it</td><td>Legacy apps that can't migrate</td><td>Library authors targeting multiple runtimes</td><td>Everyone building new apps</td></tr>
  <tr><td>Performance</td><td>Good</td><td>N/A</td><td>Excellent (much faster)</td></tr>
  <tr><td>Open Source</td><td>Partially</td><td>Yes</td><td>Yes (fully open source)</td></tr>
  <tr><td>WinForms / WPF</td><td>✅ Full support</td><td>❌ Not a runtime</td><td>✅ Supported since .NET Core 3.0</td></tr>
  <tr><td>ASP.NET / Web API</td><td>✅ ASP.NET 4.x</td><td>❌ Not a runtime</td><td>✅ ASP.NET Core (much faster)</td></tr>
  <tr><td>NuGet packages</td><td>Targets net4x</td><td>Targets netstandard2.x</td><td>Targets net6, net7, net8 etc.</td></tr>
</table>
<br>
<b>When do you see .NET Standard today?</b> When you look at a NuGet library that says
<code>netstandard2.0</code> — it means that library works in both .NET Framework AND .NET Core/5+.
It's a compatibility bridge. For <em>new libraries</em>, target .NET 8 directly.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🏗️ Anatomy of a .NET Console Program</div>
  <div class="card-body">
Here's the simplest possible .NET program (.NET 6+ with top-level statements), with every line explained:
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<div class="cmd-block">
<span class="cmd-comment">// File: Program.cs  — this is the entry point of your app</span>
&#8203;
<span class="cmd-comment">// 1. 'using' brings in a namespace so you can use its classes without full path</span>
using System;
&#8203;
<span class="cmd-comment">// 2. 'namespace' groups your code logically (like a folder for code)</span>
namespace MyFirstApp
{
<span class="cmd-comment">// 3. 'class' is a blueprint for objects</span>
class Program
{
    <span class="cmd-comment">// 4. Main() is where your program starts running</span>
    static void Main(string[] args)
    {
        <span class="cmd-comment">// 5. Console.WriteLine prints text to the screen + newline</span>
        Console.WriteLine("Hello, .NET World! 🐼");
&#8203;
        <span class="cmd-comment">// 6. Variables store data — 'string' holds text</span>
        string name = "Developer";
        int age = 25;
&#8203;
        <span class="cmd-comment">// 7. String interpolation — $ prefix lets you embed variables</span>
        Console.WriteLine($"Name: {name}, Age: {age}");
&#8203;
        <span class="cmd-comment">// 8. Console.ReadLine() waits for user to type something</span>
        Console.Write("Press Enter to exit...");
        Console.ReadLine();
    }
}
}
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🚀 How to Create &amp; Run Your First .NET App</div>
  <div class="card-body">
<b>Step 1 — Install the .NET SDK:</b> Download from <a href="https://dotnet.microsoft.com/download" target="_blank">dotnet.microsoft.com/download</a><br>
After installing, open a terminal and verify:
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<div class="cmd-block">
<span class="cmd-comment"># Check .NET is installed and see the version</span>
dotnet --version
&#8203;
<span class="cmd-comment"># Create a new console application</span>
dotnet new console -n MyFirstApp
cd MyFirstApp
&#8203;
<span class="cmd-comment"># Run the app</span>
dotnet run
&#8203;
<span class="cmd-comment"># Build without running</span>
dotnet build
&#8203;
<span class="cmd-comment"># List all available project templates</span>
dotnet new list
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">📋 Quick Reference — What to Use When</div>
  <div class="card-body">
<table class="shortcut-table">
  <tr><th>Situation</th><th>Use This</th></tr>
  <tr><td>Building a new web API or website</td><td>ASP.NET Core (.NET 8)</td></tr>
  <tr><td>Building a Windows desktop app</td><td>WPF or WinForms on .NET 8</td></tr>
  <tr><td>Building a cross-platform desktop app</td><td>.NET MAUI</td></tr>
  <tr><td>Building a browser app in C#</td><td>Blazor WebAssembly</td></tr>
  <tr><td>Maintaining an old Windows-only app</td><td>.NET Framework 4.8 (maintenance mode)</td></tr>
  <tr><td>Creating a NuGet library for broad compatibility</td><td>Target netstandard2.0 or net8</td></tr>
  <tr><td>Cloud / microservices</td><td>.NET 8 with Docker</td></tr>
</table>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

