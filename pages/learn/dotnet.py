""".NET learning page rendered with the minimal content primitives."""

import streamlit as st

from components.content import (
    code_block,
    link_list,
    paragraph,
    section_intro,
    section_title,
    subsection,
)


def render_dotnet():
    section_title(
        ".NET",
        "A free, open-source developer platform from Microsoft for building almost anything.",
    )

    section_intro(
        '.NET (pronounced "dot net") lets you build websites, mobile apps, desktop apps, '
        "games, cloud services, and more using a common set of tools and languages "
        "(mainly C#, F#, and VB.NET)."
    )

    subsection("What is .NET? (For complete beginners)")
    paragraph(
        ".NET is a free, open-source developer platform created by Microsoft. Think of it "
        "as a powerful toolbox that lets you build all kinds of software using a shared "
        "runtime, base class library, and tooling."
    )
    paragraph("Why should you learn it?")
    link_list(
        [
            "Used by millions of developers worldwide",
            "Backed by Microsoft and a huge open-source community",
            "Runs on Windows, macOS, and Linux",
            "Excellent performance — one of the fastest web frameworks in the world",
            "Great job market demand",
        ]
    )
    paragraph(
        "Simple analogy: if programming is like cooking, .NET is the professional kitchen "
        "(with all utensils, ovens, and recipes) — C# is the chef who works in that kitchen."
    )

    subsection("Supported platforms")
    link_list(["Windows", "macOS", "Linux", "Android", "iOS", "Browser (WebAssembly)"])

    subsection(".NET release history & associated C# versions")
    paragraph(
        "Every version of .NET comes paired with a version of C# — the primary language "
        "used to write .NET apps. Here's the full picture from the very beginning:"
    )
    st.markdown(
        """
| .NET Version | Release Year | C# Version | Support Type | Key Highlights |
|---|---|---|---|---|
| .NET Framework 1.0 | 2002 | C# 1.0 | End of Life | The very first .NET — Windows only, introduced CLR & BCL |
| .NET Framework 1.1 | 2003 | C# 1.2 | End of Life | Bug fixes, ASP.NET improvements |
| .NET Framework 2.0 | 2005 | C# 2.0 | End of Life | Generics, anonymous methods, nullable types |
| .NET Framework 3.0 | 2006 | C# 2.0 | End of Life | WPF, WCF, WF introduced |
| .NET Framework 3.5 | 2007 | C# 3.0 | End of Life | LINQ, lambda expressions, extension methods |
| .NET Framework 4.0 | 2010 | C# 4.0 | End of Life | TPL (Task Parallel Library), dynamic keyword |
| .NET Framework 4.5 | 2012 | C# 5.0 | End of Life | async/await introduced |
| .NET Framework 4.6 | 2015 | C# 6.0 | End of Life | RyuJIT compiler, string interpolation |
| .NET Framework 4.7 | 2017 | C# 7.x | End of Life | Tuples, pattern matching, local functions |
| .NET Framework 4.8 | 2019 | C# 7.3 | Maintenance | Last ever .NET Framework — still supported on Windows |
| **.NET Core 1.0** | 2016 | C# 6.0 | End of Life | First cross-platform .NET — Linux/macOS support |
| .NET Core 2.0 | 2017 | C# 7.1 | End of Life | .NET Standard 2.0 support, massive API expansion |
| .NET Core 2.1 | 2018 | C# 7.3 | End of Life | LTS release, Span&lt;T&gt;, SignalR |
| .NET Core 3.0 | 2019 | C# 8.0 | End of Life | WPF/WinForms on Core, Blazor Server |
| .NET Core 3.1 | 2019 | C# 8.0 | End of Life (2022) | LTS — most used Core version; gRPC support |
| **.NET 5** | 2020 | C# 9.0 | End of Life | Unified .NET — merged Core + Framework vision; no "Core" branding |
| **.NET 6** | 2021 | C# 10.0 | End of Life (2024) | LTS — minimal APIs, .NET MAUI preview, hot reload |
| .NET 7 | 2022 | C# 11.0 | End of Life | STS — rate limiting, output caching, regex improvements |
| **.NET 8** | 2023 | C# 12.0 | **LTS — Current** | Native AOT, Blazor United, primary constructors, collection expressions |
| .NET 9 | 2024 | C# 13.0 | STS | LINQ improvements, params spans, Task.WhenEach |
| **.NET 10** | 2025 (Nov) | C# 14.0 | **LTS (Upcoming)** | In development — next long-term support release |
"""
    )
    paragraph(
        "LTS = Long-Term Support (3 years). STS = Standard-Term Support (18 months). "
        "Rule of thumb: use an LTS version for production apps — currently .NET 8."
    )

    subsection(".NET Framework vs .NET Standard vs .NET (Core / 5+)")
    paragraph(
        "This is one of the most confusing things for beginners — three names that all "
        'say ".NET". Here\'s the plain-English breakdown.'
    )
    paragraph(
        "Think of it this way: .NET Framework is an old house (Windows-only, comfy but "
        "can't be moved). .NET Standard is a set of blueprints (a contract that different "
        ".NETs agree to follow). .NET (Core / 5+) is the new modern building "
        "(cross-platform, fast, the future)."
    )
    st.markdown(
        """
| Feature | .NET Framework | .NET Standard | .NET (Core / 5+) |
|---|---|---|---|
| What it is | Original full Windows .NET | A specification/interface (not a runtime) | Modern, unified cross-platform .NET |
| Runs on | Windows only | N/A — it's a standard, not a runtime | Windows, macOS, Linux |
| Status | Maintenance (no new features) | Superseded by .NET 5+ (still used in libraries) | Active — all future development here |
| Latest version | 4.8.1 | 2.1 | .NET 9 (LTS: .NET 8) |
| Who should use it | Legacy apps that can't migrate | Library authors targeting multiple runtimes | Everyone building new apps |
| Performance | Good | N/A | Excellent (much faster) |
| Open Source | Partially | Yes | Yes (fully open source) |
| WinForms / WPF | Full support | Not a runtime | Supported since .NET Core 3.0 |
| ASP.NET / Web API | ASP.NET 4.x | Not a runtime | ASP.NET Core (much faster) |
| NuGet packages | Targets net4x | Targets netstandard2.x | Targets net6, net7, net8 etc. |
"""
    )
    paragraph(
        "When do you see .NET Standard today? When you look at a NuGet library that says "
        "netstandard2.0 — it means that library works in both .NET Framework AND .NET "
        "Core/5+. It's a compatibility bridge. For new libraries, target .NET 8 directly."
    )

    subsection("Anatomy of a .NET console program")
    paragraph(
        "Here's a simple .NET console program with every line explained. This is the "
        "classic style; .NET 6+ also supports top-level statements that omit the "
        "namespace and Main boilerplate."
    )
    code_block(
        """// File: Program.cs  — this is the entry point of your app

// 1. 'using' brings in a namespace so you can use its classes without full path
using System;

// 2. 'namespace' groups your code logically (like a folder for code)
namespace MyFirstApp
{
    // 3. 'class' is a blueprint for objects
    class Program
    {
        // 4. Main() is where your program starts running
        static void Main(string[] args)
        {
            // 5. Console.WriteLine prints text to the screen + newline
            Console.WriteLine("Hello, .NET World!");

            // 6. Variables store data — 'string' holds text
            string name = "Developer";
            int age = 25;

            // 7. String interpolation — $ prefix lets you embed variables
            Console.WriteLine($"Name: {name}, Age: {age}");

            // 8. Console.ReadLine() waits for user to type something
            Console.Write("Press Enter to exit...");
            Console.ReadLine();
        }
    }
}""",
        language="csharp",
    )

    subsection("How to create & run your first .NET app")
    paragraph(
        "Step 1 — Install the .NET SDK from the official download page, then verify the "
        "installation from a terminal."
    )
    code_block(
        """# Check .NET is installed and see the version
dotnet --version

# Create a new console application
dotnet new console -n MyFirstApp
cd MyFirstApp

# Run the app
dotnet run

# Build without running
dotnet build

# List all available project templates
dotnet new list""",
        language="bash",
    )
    paragraph("Typical workflow: install SDK -> dotnet new -> edit code -> dotnet run.")

    subsection("Quick reference — what to use when")
    st.markdown(
        """
| Situation | Use This |
|---|---|
| Building a new web API or website | ASP.NET Core (.NET 8) |
| Building a Windows desktop app | WPF or WinForms on .NET 8 |
| Building a cross-platform desktop app | .NET MAUI |
| Building a browser app in C# | Blazor WebAssembly |
| Maintaining an old Windows-only app | .NET Framework 4.8 (maintenance mode) |
| Creating a NuGet library for broad compatibility | Target netstandard2.0 or net8 |
| Cloud / microservices | .NET 8 with Docker |
"""
    )

    subsection("Further reading")
    link_list(
        [
            (
                "Download .NET SDK",
                "https://dotnet.microsoft.com/download",
                "official installers for Windows, macOS, Linux",
            ),
            (
                ".NET documentation",
                "https://learn.microsoft.com/dotnet/",
                "the canonical reference from Microsoft",
            ),
            (
                "C# language reference",
                "https://learn.microsoft.com/dotnet/csharp/",
                "language guide and tutorials",
            ),
            (
                ".NET release schedule",
                "https://dotnet.microsoft.com/platform/support/policy/dotnet-core",
                "support policy and LTS / STS dates",
            ),
        ]
    )
