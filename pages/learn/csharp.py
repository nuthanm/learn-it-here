"""C# learn page rendered with the minimal content primitives."""

import streamlit as st

from components.content import (
    code_block,
    link_list,
    paragraph,
    section_intro,
    section_title,
    subsection,
)


def render_csharp():
    section_title(
        "C#",
        "Modern, object-oriented language for the .NET platform.",
    )

    # ------------------------------------------------------------------
    # What is C#?
    # ------------------------------------------------------------------
    section_intro(
        'C# (pronounced "C sharp") is a modern, object-oriented programming language '
        "created by Microsoft in 2000. It was designed by Anders Hejlsberg, who also "
        "designed TypeScript and previously Turbo Pascal and Delphi."
    )

    subsection("What is C#?")
    paragraph(
        "C# runs on the .NET platform — Microsoft's developer toolkit. Think of .NET as "
        "a professional kitchen and C# as the chef's language: structured, expressive, "
        "and powerful."
    )
    paragraph(
        "Layman terms: imagine you want to give instructions to a robot (your computer). "
        "C# is a language the robot understands perfectly — clear, logical, and hard to "
        "misuse. It's like writing a recipe: step-by-step instructions the robot follows "
        "exactly."
    )

    subsection("What can you build with C#?")
    paragraph(
        "Web apps and APIs (ASP.NET Core), desktop apps (WPF, WinForms, MAUI), mobile "
        "apps (Xamarin / .NET MAUI), games (Unity — the world's most popular game "
        "engine), cloud services (Azure), IoT and embedded systems, and AI/ML pipelines "
        "with ML.NET."
    )

    subsection("Competitors and comparison")
    st.markdown(
        """
| Language | Creator | Primary Use | How C# compares |
| --- | --- | --- | --- |
| **Java** | Oracle / Sun | Enterprise, Android | C# has more modern syntax, better async support, better tooling on Windows |
| **Python** | Guido van Rossum | Data science, scripting, AI | C# is faster and statically typed; Python is easier for quick scripts |
| **C++** | Bjarne Stroustrup | Systems, games (raw performance) | C# is much safer (managed memory), easier to write; C++ is faster but complex |
| **TypeScript / JS** | Microsoft / Netscape | Web front-end, Node.js | C# is a backend/full-stack alternative; TypeScript is browser-first |
| **Go (Golang)** | Google | Cloud, microservices, CLIs | Go is simpler and minimal; C# is more feature-rich and enterprise-friendly |
| **Kotlin** | JetBrains / Google | Android, JVM | Very similar modern feel; C# targets .NET, Kotlin targets JVM/Android |
| **Swift** | Apple | iOS, macOS apps | Swift is Apple-ecosystem only; C# is cross-platform |
"""
    )

    # ------------------------------------------------------------------
    # What makes C# special?
    # ------------------------------------------------------------------
    subsection("What makes C# special?")
    paragraph("Capabilities that set C# apart from other mainstream languages:")

    subsection("Unified full-stack")
    paragraph(
        "Build front-end (Blazor), back-end (ASP.NET), mobile (MAUI), and games (Unity) "
        "— all in the same language."
    )

    subsection("async/await pioneer")
    paragraph(
        "C# popularised async/await in 2012 — before JS, Python, or Kotlin added it. "
        "Asynchronous code reads like synchronous code."
    )

    subsection("LINQ")
    paragraph(
        "Language-Integrated Query lets you query arrays, databases, XML, and JSON with "
        "SQL-like syntax directly in C# code. No other mainstream language has this "
        "built in."
    )

    subsection("Nullable reference types")
    paragraph(
        "C# 8 introduced compile-time null-safety — the compiler warns you before you "
        "cause a NullReferenceException at runtime."
    )

    subsection("Records and immutability")
    paragraph(
        "C# 9 added record types — immutable data objects with value equality built in. "
        "Less boilerplate than Java POJOs or Python dataclasses."
    )

    subsection("Unity game development")
    paragraph(
        "C# is the scripting language for Unity — used to build over 60% of all mobile "
        "games worldwide."
    )

    subsection("Pattern matching")
    paragraph(
        "Advanced switch expressions, positional patterns, and property patterns — "
        "cleaner than if/else chains, more powerful than Java's instanceof."
    )

    subsection("NuGet ecosystem")
    paragraph(
        "Over 300,000 open-source packages on NuGet.org — the .NET package manager "
        "integrates seamlessly into Visual Studio."
    )

    subsection("Native AOT and performance")
    paragraph(
        "C# / .NET 8 supports Native AOT compilation — produces tiny, fast executables "
        "without needing the .NET runtime installed."
    )

    # ------------------------------------------------------------------
    # Why learn C#?
    # ------------------------------------------------------------------
    subsection("Why should you learn C#?")
    paragraph(
        "For job seekers: consistently top 5 in the TIOBE programming language index, "
        "with high demand in enterprise, finance, healthcare, gaming, and government "
        "sectors. Microsoft Azure cloud is a massive C# / .NET ecosystem. Average "
        "salary in the USA (2025–2026) ranges from $95,000 to $145,000 per year."
    )
    paragraph(
        "For students and career changers: one of the best-structured languages to "
        "learn programming fundamentals. Strongly typed — the compiler catches your "
        "mistakes before they run. Excellent documentation at learn.microsoft.com. "
        "Free tools: Visual Studio Community, VS Code, and the .NET SDK."
    )
    paragraph(
        "For game developers: Unity uses C# — learn it once and build games for PC, "
        "mobile, console, AR, and VR."
    )
    paragraph(
        "Layman analogy: learning C# is like learning to drive a Mercedes — once you "
        "know it, you can drive anything. And it's in huge demand everywhere."
    )

    # ------------------------------------------------------------------
    # Compatibility
    # ------------------------------------------------------------------
    subsection("What is C# compatible with?")
    paragraph("Operating systems and platforms:")
    link_list(
        [
            "Windows",
            "Linux",
            "macOS",
            "Android (via .NET MAUI)",
            "iOS (via .NET MAUI)",
            "Azure Cloud",
            "Docker / Kubernetes",
            "Xbox / consoles",
        ]
    )

    subsection("Frameworks and runtimes")
    st.markdown(
        """
| Framework | Use Case |
| --- | --- |
| ASP.NET Core | Web APIs, MVC websites, Razor Pages |
| Blazor | Interactive web UI in C# (browser + server) |
| .NET MAUI | Cross-platform mobile and desktop (Android, iOS, Windows, macOS) |
| WPF / WinForms | Windows desktop apps |
| Unity | 2D / 3D games across all platforms |
| ML.NET | Machine learning and AI |
| Azure Functions | Serverless cloud computing |
| gRPC / SignalR | Real-time communication and microservices |
"""
    )

    subsection("Databases C# works with")
    paragraph(
        "SQL Server, Oracle, PostgreSQL, MySQL, SQLite, MongoDB, Redis, and CosmosDB — "
        "via EF Core or raw ADO.NET."
    )

    # ------------------------------------------------------------------
    # Best-fit app types
    # ------------------------------------------------------------------
    subsection("What types of apps are best built with C#?")

    subsection("Web APIs and microservices")
    paragraph(
        "ASP.NET Core is one of the fastest web frameworks. Used by Stack Overflow, "
        "Microsoft, and thousands of enterprises."
    )

    subsection("Enterprise line-of-business apps")
    paragraph(
        "CRM, ERP, and inventory systems — C# with WPF or ASP.NET is the go-to in "
        "corporate environments."
    )

    subsection("Video games (Unity)")
    paragraph(
        "Pokémon GO, Cuphead, Cities: Skylines, and Among Us are all built with Unity and C#."
    )

    subsection("Cross-platform mobile apps")
    paragraph(".NET MAUI: one codebase produces iOS, Android, Windows, and macOS apps.")

    subsection("Cloud and serverless")
    paragraph("Azure Functions and Azure App Services — C# is Azure's first-class citizen.")

    subsection("Windows desktop apps")
    paragraph("WPF (rich UI) and WinForms (classic) remain popular for internal business tools.")

    subsection("AI and ML")
    paragraph("ML.NET for machine learning pipelines; integration with Python AI models via REST.")

    subsection("Dev tools and CLIs")
    paragraph("Roslyn compiler, PowerShell, and NuGet are all built in C# / .NET.")

    # ------------------------------------------------------------------
    # Challenges
    # ------------------------------------------------------------------
    subsection("Challenges of learning C#")
    st.markdown(
        """
| # | Challenge | Why it's tricky | How to overcome it |
| --- | --- | --- | --- |
| 1 | Understanding types and generics | C# is strongly typed — you must declare what type every variable is | Practice with simple examples; the compiler is your teacher |
| 2 | OOP concepts (classes, interfaces) | Object-oriented programming has many abstract concepts | Build small real projects (a bank account class, a to-do list) |
| 3 | async/await and threading | Asynchronous code can feel confusing at first | Start with simple async methods; avoid manual threading early |
| 4 | Understanding .NET vs C# | Beginners confuse the language (C#) with the platform (.NET) | Think: C# is the language; .NET is the platform it runs on |
| 5 | Visual Studio complexity | VS has hundreds of features — overwhelming at first | Learn only what you need: create project, write code, run it |
| 6 | Dependency Injection | A key .NET pattern that beginners find confusing | Learn it after you understand interfaces and constructors |
| 7 | LINQ learning curve | LINQ syntax (lambdas, method chains) is unfamiliar at first | Start with simple .Where() and .Select() calls |
| 8 | C# version differences | Articles may use C# 5 code vs C# 12 code — looks very different | Always check the C# version the tutorial targets |
"""
    )

    # ------------------------------------------------------------------
    # Roadmap
    # ------------------------------------------------------------------
    subsection("How to learn C# — a beginner roadmap")
    paragraph(
        "Layman analogy: learning C# is like learning to cook. Start with boiling "
        "water, then make an omelette, then a full meal — don't try a five-course "
        "dinner on day one."
    )

    subsection("Phase 1 — Install and Hello World (days 1–3)")
    paragraph(
        "Install the .NET SDK, then VS Code or Visual Studio, then run "
        "`dotnet new console` and execute your first Hello World program."
    )

    subsection("Phase 2 — Core language basics (weeks 1–3)")
    paragraph(
        "Variables and types, operators, if/else, loops (for, while, foreach), methods, and arrays."
    )

    subsection("Phase 3 — Object-oriented programming (weeks 4–6)")
    paragraph(
        "Classes, objects, constructors, properties, inheritance, interfaces, and abstract classes."
    )

    subsection("Phase 4 — Intermediate C# (month 2)")
    paragraph(
        "Generics, collections (List, Dictionary), LINQ, exception handling, file I/O, "
        "and async/await."
    )

    subsection("Phase 5 — A real framework (month 3 onwards)")
    paragraph("Pick one: ASP.NET Core (web), Unity (games), or WPF (desktop) and build a project.")

    subsection("Free learning resources")
    link_list(
        [
            (
                "learn.microsoft.com/dotnet/csharp",
                "https://learn.microsoft.com/dotnet/csharp",
                "official Microsoft C# tour — best starting point",
            ),
            (
                "dotnet.microsoft.com/learn",
                "https://dotnet.microsoft.com/learn",
                "free interactive browser-based tutorials",
            ),
            (
                "CS50 (Harvard)",
                "https://cs50.harvard.edu/",
                "free intro to programming",
            ),
            (
                "Tim Corey on YouTube",
                "https://www.youtube.com/@IAmTimCorey",
                "top C# instructor",
            ),
            (
                "Nick Chapsas on YouTube",
                "https://www.youtube.com/@nickchapsas",
                "modern C# / .NET deep dives",
            ),
            (
                "freeCodeCamp C# certification",
                "https://www.freecodecamp.org/learn/foundational-c-sharp-with-microsoft/",
                "free structured course",
            ),
        ]
    )

    paragraph(
        "Tip for non-technical beginners: don't learn C# in isolation — pick a project "
        "that excites you (a small game, a personal expense tracker, a website) and "
        "learn what you need to build it. Purpose-driven learning is much faster."
    )

    # ------------------------------------------------------------------
    # Version timeline
    # ------------------------------------------------------------------
    subsection("C# version timeline — from 1.0 to 14.0")
    st.markdown(
        """
| C# Version | .NET Version | Year | Headline Features |
| --- | --- | --- | --- |
| **C# 1.0** | .NET Framework 1.0 | 2002 | Classes, interfaces, delegates, events, properties, value types, garbage collection |
| **C# 2.0** | .NET Framework 2.0 | 2005 | Generics, iterators (yield), nullable types, anonymous methods, partial classes |
| **C# 3.0** | .NET Framework 3.5 | 2007 | LINQ, lambda expressions, extension methods, auto-properties, anonymous types, var |
| **C# 4.0** | .NET Framework 4.0 | 2010 | dynamic keyword, optional/named parameters, covariance and contravariance |
| **C# 5.0** | .NET Framework 4.5 | 2012 | async/await — the biggest game-changer for non-blocking code |
| **C# 6.0** | .NET Framework 4.6 / .NET Core 1.0 | 2015 | String interpolation ($""), null-conditional (?.), expression-bodied members, nameof |
| **C# 7.0–7.3** | .NET Framework 4.7 / .NET Core 2.x | 2017 | Tuples, out variables, pattern matching (is), local functions, throw expressions |
| **C# 8.0** | .NET Core 3.0 / 3.1 | 2019 | Nullable reference types, switch expressions, ranges and indices (^, ..), async streams |
| **C# 9.0** | .NET 5 | 2020 | Records, init-only setters, top-level statements, pattern matching enhancements |
| **C# 10.0** | .NET 6 | 2021 | Global using, file-scoped namespaces, record structs, constant interpolated strings |
| **C# 11.0** | .NET 7 | 2022 | Required members, raw string literals, list patterns, generic attributes, UTF-8 strings |
| **C# 12.0** | .NET 8 (LTS) | 2023 | Primary constructors, collection expressions, inline arrays, default lambda params |
| **C# 13.0** | .NET 9 | 2024 | params collections, new lock type, field keyword in properties, iterator async improvements |
| **C# 14.0** | .NET 10 (LTS, Nov 2025) | 2025 | In development — upcoming features being drafted in language design GitHub |
"""
    )

    # ------------------------------------------------------------------
    # Feature evolution tabs
    # ------------------------------------------------------------------
    subsection("C# feature evolution — same topic across versions")
    paragraph(
        "Tracking how the same concept evolved across C# versions shows why newer "
        "syntax exists and what problem each version solved. Select a topic:"
    )

    tabs_evo = st.tabs(
        [
            "Strings",
            "Null Handling",
            "Data Models",
            "Switch",
            "Async / Await",
            "Collections",
        ]
    )

    with tabs_evo[0]:
        paragraph('Tracking "printing a person\'s name and age" across versions.')

        code_block(
            'string name = "Alice";\n'
            "int age = 30;\n"
            'Console.WriteLine("Name: " + name + ", Age: " + age);\n'
            "// Issue: verbose, hard to read, error-prone with many variables",
            language="csharp",
            label="C# 1.0 — string concatenation (2002)",
        )

        code_block(
            'Console.WriteLine(String.Format("Name: {0}, Age: {1}", name, age));\n'
            "// Better, but {0} {1} placeholders are still confusing",
            language="csharp",
            label="C# 5.0 — String.Format (improvement, ~2012)",
        )

        code_block(
            'Console.WriteLine($"Name: {name}, Age: {age}");\n'
            "// Clean, readable — variables inline with the string\n"
            "// Layman: like filling in blanks in a sentence",
            language="csharp",
            label="C# 6.0 — string interpolation (2015)",
        )

        code_block(
            "// No class or Main method needed!\n"
            'string name = "Alice";\n'
            "int age = 30;\n"
            'Console.WriteLine($"Name: {name}, Age: {age}");\n'
            "// Perfect for scripts and beginners — less boilerplate",
            language="csharp",
            label="C# 9.0 — top-level statements (2020)",
        )

    with tabs_evo[1]:
        paragraph('Tracking "null checking" across versions.')

        code_block(
            "if (user != null)\n"
            "{\n"
            "    Console.WriteLine(user.Name);\n"
            "}\n"
            "// Easy to forget, causes NullReferenceException at runtime",
            language="csharp",
            label="C# 1.0–5.0 — classic null check",
        )

        code_block(
            "Console.WriteLine(user?.Name);\n"
            "// If user is null, returns null instead of crashing\n"
            '// Layman: "if the person exists, tell me their name; otherwise say nothing"',
            language="csharp",
            label="C# 6.0 — null-conditional operator (?.) (2015)",
        )

        code_block(
            'string displayName = user?.Name ?? "Guest";\n'
            "// \"Use user's name, OR if null, use 'Guest'\"",
            language="csharp",
            label="C# 6.0 — null-coalescing (??)",
        )

        code_block(
            "// In .csproj: <Nullable>enable</Nullable>\n"
            "string? name = null;   // explicitly nullable\n"
            "string  name2 = null;  // Compiler WARNING — this should never be null!",
            language="csharp",
            label="C# 8.0 — nullable reference types (compile-time safety)",
        )

    with tabs_evo[2]:
        paragraph('Tracking "data class / model" across versions.')

        code_block(
            "public class Person\n"
            "{\n"
            "    public string Name { get; set; }\n"
            "    public int Age { get; set; }\n"
            "    // Need to manually write Equals(), GetHashCode(), ToString()\n"
            "}",
            language="csharp",
            label="C# 1.0–8.0 — classic class with properties",
        )

        code_block(
            "public record Person(string Name, int Age);\n"
            "// One line! Auto-generates constructor, Equals, GetHashCode, ToString\n"
            "// Immutable by default\n"
            "// Layman: a record is like a stamped official form — once filled, it doesn't change\n"
            "\n"
            'var p1 = new Person("Alice", 30);\n'
            'var p2 = new Person("Alice", 30);\n'
            "Console.WriteLine(p1 == p2); // true — value equality!\n"
            "// In a regular class, this would be false (reference equality)",
            language="csharp",
            label="C# 9.0 — record types (2020)",
        )

        code_block(
            "var p3 = p1 with { Age = 31 };\n"
            "// Creates a new Person with everything from p1, but Age = 31\n"
            '// Immutable data + easy "update"',
            language="csharp",
            label="C# 9.0 — with expressions (non-destructive mutation)",
        )

    with tabs_evo[3]:
        paragraph('Tracking "switch / branching" across versions.')

        code_block(
            'string day = "Monday";\n'
            "string type;\n"
            "switch (day)\n"
            "{\n"
            '    case "Saturday":\n'
            '    case "Sunday":\n'
            '        type = "Weekend";\n'
            "        break;\n"
            "    default:\n"
            '        type = "Weekday";\n'
            "        break;\n"
            "}",
            language="csharp",
            label="C# 1.0 — classic switch",
        )

        code_block(
            "string type = day switch\n"
            "{\n"
            '    "Saturday" or "Sunday" => "Weekend",\n'
            '    _ => "Weekday"\n'
            "};\n"
            "// Concise, returns a value, no 'break' needed\n"
            '// Layman: like a lookup table — "for this input, give me that output"',
            language="csharp",
            label="C# 8.0 — switch expression (2019)",
        )

        code_block(
            "string category = person switch\n"
            "{\n"
            '    { Age: < 18 }             => "Minor",\n'
            '    { Age: >= 18, Age: < 65 } => "Adult",\n'
            '    _                         => "Senior"\n'
            "};\n"
            "// Reads like English rules",
            language="csharp",
            label="C# 8.0 — property pattern matching",
        )

    with tabs_evo[4]:
        paragraph('Tracking "async programming" across versions.')

        code_block(
            '// Old way — callbacks make "callback hell"\n'
            "webClient.DownloadStringCompleted += (s, e) => {\n"
            "    Console.WriteLine(e.Result);  // runs when done\n"
            "};\n"
            'webClient.DownloadStringAsync(new Uri("https://example.com"));\n'
            "// Hard to read, hard to debug, hard to chain",
            language="csharp",
            label="C# 1.0–4.0 — callbacks / BeginInvoke (painful)",
        )

        code_block(
            "async Task FetchDataAsync()\n"
            "{\n"
            '    string result = await httpClient.GetStringAsync("https://example.com");\n'
            "    Console.WriteLine(result);\n"
            "}\n"
            "// Reads like synchronous code — no callbacks!\n"
            "// Layman: like ordering food at a restaurant — you sit, wait (await),\n"
            "//   and your food arrives (result) without blocking everyone else",
            language="csharp",
            label="C# 5.0 — async/await (2012, game changer)",
        )

    with tabs_evo[5]:
        paragraph('Tracking "collections / filtering" across versions (LINQ).')

        code_block(
            "List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };\n"
            "List<int> evens = new List<int>();\n"
            "foreach (int n in numbers)\n"
            "{\n"
            "    if (n % 2 == 0) evens.Add(n);\n"
            "}",
            language="csharp",
            label="C# 1.0–2.0 — manual loop filtering",
        )

        code_block(
            "var evens = numbers.Where(n => n % 2 == 0).ToList();\n"
            "// One line, expressive\n"
            '// Layman: "give me only the items WHERE my condition is true"\n'
            "\n"
            "// Query syntax (SQL-like):\n"
            "var evens2 = (from n in numbers where n % 2 == 0 select n).ToList();",
            language="csharp",
            label="C# 3.0 — LINQ (2007)",
        )

        code_block(
            "int[] nums = [1, 2, 3, 4, 5];   // new [ ] syntax — same for arrays, lists, spans\n"
            "List<int> more = [1, 2, ..nums]; // spread operator — merge collections easily",
            language="csharp",
            label="C# 12.0 — collection expressions (2023)",
        )

    # ------------------------------------------------------------------
    # Foundations a new developer must know
    # ------------------------------------------------------------------
    subsection("What a new .NET developer must be strong in")
    paragraph(
        "These are the non-negotiable foundations every C# / .NET developer is expected "
        "to understand deeply — not just the syntax, but the why."
    )
    st.markdown(
        """
| Priority | Topic | Why it matters | Layman analogy |
| --- | --- | --- | --- |
| Must | Value types vs Reference types | Determines how variables are copied, passed, and stored in memory | A house (reference) vs a house blueprint (value) |
| Must | Classes, Objects, Constructors | Everything in C# is an object — foundation of OOP | A class is a cookie cutter; objects are the cookies |
| Must | Interfaces | Used everywhere in .NET for abstraction and dependency injection | A contract: "I promise to have these methods" |
| Must | async/await | Every modern API, database call, HTTP request is async | Ordering food without blocking the restaurant kitchen |
| Must | LINQ (basic) | Used in every .NET codebase to query collections and databases | SQL for your in-memory lists |
| Must | Exception handling (try/catch/finally) | Production code must handle failures gracefully | A safety net under a tightrope walker |
| Must | Generics (List<T>, Dictionary<K,V>) | Reusable, type-safe code — used constantly | A box that works for any type of item |
| Should | Dependency Injection (DI) | The .NET DI container is used in every ASP.NET Core app | A vending machine — request what you need, get it |
| Should | Delegates and Events | Foundation of UI frameworks (WPF, WinForms) and callbacks | A referee who calls players when needed |
| Should | Nullable reference types | Helps write null-safe code — huge source of runtime bugs otherwise | Marking "this can be empty" clearly on a form |
| Should | Records and immutability | Modern C# style for data transfer objects (DTOs) | A sealed certificate — can't be changed after issuing |
| Should | Pattern matching | Cleaner conditionals — used heavily in modern C# codebases | A smart sorting machine that routes items by rules |
| Nice | Reflection | Inspect types at runtime — used in frameworks, serialisation | An x-ray machine for code |
| Nice | Span<T> / Memory<T> | High-performance zero-allocation slicing of buffers | A window into a larger array — no copying |
"""
    )

    # ------------------------------------------------------------------
    # Anatomy of a C# program
    # ------------------------------------------------------------------
    subsection("Anatomy of a C# program — every part explained")
    paragraph("Let's dissect this complete C# program and label every concept:")

    code_block(
        '// (1) Using directive — imports a namespace (like "import" in Python / Java)\n'
        "using System;\n"
        "using System.Collections.Generic;\n"
        "\n"
        "// (2) Namespace — groups related classes together (like a folder)\n"
        "namespace MyApp.Learning\n"
        "{\n"
        "    // (3) Class — a blueprint / template for creating objects\n"
        '    //     "public" = accessible from other code\n'
        "    public class BankAccount\n"
        "    {\n"
        "        // (4) Field — a private variable that stores state inside the class\n"
        "        private decimal _balance;\n"
        "\n"
        "        // (5) Property — controlled access to a field (get/set)\n"
        '        //     "public" = readable from outside, "private set" = only settable inside\n'
        "        public string Owner { get; private set; }\n"
        "\n"
        "        // (6) Constructor — special method called when an object is created\n"
        '        //     "this" refers to the current instance\n'
        "        public BankAccount(string owner, decimal initialBalance)\n"
        "        {\n"
        "            Owner    = owner;        // set the property\n"
        "            _balance = initialBalance;\n"
        "        }\n"
        "\n"
        "        // (7) Method — a named action the class can perform\n"
        "        //     returns void (nothing), takes a decimal parameter\n"
        "        public void Deposit(decimal amount)\n"
        "        {\n"
        "            // (8) Exception handling — catch and handle errors gracefully\n"
        "            if (amount <= 0)\n"
        '                throw new ArgumentException("Amount must be positive.");\n'
        "\n"
        "            _balance += amount;\n"
        "            // (9) String interpolation — embed expressions inside strings\n"
        '            Console.WriteLine($"Deposited {amount:C}. New balance: {_balance:C}");\n'
        "        }\n"
        "\n"
        "        // (10) Expression-bodied method (C# 6+) — one-liner method\n"
        "        public decimal GetBalance() => _balance;\n"
        "    }\n"
        "\n"
        "    // (11) Derived class — inherits from BankAccount (Inheritance)\n"
        "    public class SavingsAccount : BankAccount\n"
        "    {\n"
        "        // (12) Auto-property with init-only setter (C# 9)\n"
        "        public decimal InterestRate { get; init; }\n"
        "\n"
        "        public SavingsAccount(string owner, decimal balance, decimal rate)\n"
        "            : base(owner, balance)      // calls the parent constructor\n"
        "        {\n"
        "            InterestRate = rate;\n"
        "        }\n"
        "\n"
        "        // (13) Method override — customise inherited behaviour\n"
        "        public void ApplyInterest()\n"
        "        {\n"
        "            decimal interest = GetBalance() * InterestRate;\n"
        "            Deposit(interest);\n"
        "        }\n"
        "    }\n"
        "\n"
        "    // (14) Interface — a contract: any class implementing this MUST have these members\n"
        "    public interface IReportable\n"
        "    {\n"
        "        void PrintReport();\n"
        "    }\n"
        "\n"
        "    // (15) Record — immutable data type (C# 9), auto-generates Equals/ToString\n"
        "    public record Transaction(string Type, decimal Amount, DateTime Date);\n"
        "\n"
        "    // (16) Program entry point\n"
        "    public class Program\n"
        "    {\n"
        "        // (17) Main method — where execution begins\n"
        "        //      async Task = supports awaiting async operations\n"
        "        public static async Task Main(string[] args)\n"
        "        {\n"
        "            // (18) Object instantiation — create an instance from the class blueprint\n"
        '            var account = new SavingsAccount("Alice", 1000m, 0.05m);\n'
        "\n"
        "            account.Deposit(500m);\n"
        "            account.ApplyInterest();\n"
        "\n"
        "            // (19) var keyword — type inferred by compiler (C# 3+)\n"
        "            var balance = account.GetBalance();\n"
        "\n"
        "            // (20) LINQ — query a collection with lambda expressions\n"
        "            var transactions = new List<Transaction>\n"
        "            {\n"
        '                new("Deposit",  500m,  DateTime.Now),\n'
        '                new("Interest", 75m,   DateTime.Now),\n'
        "            };\n"
        "\n"
        "            // Filter: only deposits\n"
        '            var deposits = transactions.Where(t => t.Type == "Deposit").ToList();\n'
        "\n"
        "            // (21) async/await — non-blocking I/O operation\n"
        "            await Task.Delay(10); // simulate async work\n"
        "\n"
        '            Console.WriteLine($"Final balance for {account.Owner}: {balance:C}");\n'
        "        }\n"
        "    }\n"
        "}",
        language="csharp",
    )

    subsection("Concept index")
    st.markdown(
        """
| Symbol | Concept | Layman explanation |
| --- | --- | --- |
| (1) | using directive | Like plugging in a toolbox before using its tools |
| (2) | Namespace | A folder/category to organise related code |
| (3) | Class | A blueprint — defines what an object looks like and can do |
| (4) | Field (private) | A secret drawer inside the object — only it can access it directly |
| (5) | Property (get/set) | A controlled window into the secret drawer — you choose who can read/write |
| (6) | Constructor | The setup instructions when you first build the object |
| (7) | Method | An action/verb — what the object can do |
| (8) | Exception handling | A safety net — "if something goes wrong, do this instead of crashing" |
| (9) | String interpolation | Fill-in-the-blank for text: "Hello, {name}!" |
| (10) | Expression-bodied member | A shorthand one-liner for simple methods |
| (11) | Inheritance | A child class gets everything from the parent and adds its own things |
| (12) | init-only property | Can only be set during object creation — locked afterwards |
| (13) | Method override | The child rewrites a parent method to behave differently |
| (14) | Interface | A signed contract: "I promise to provide these capabilities" |
| (15) | Record | A sealed, official form — values set once, never changed |
| (16)–(17) | Program entry / Main | The front door of your program — execution starts here |
| (18) | Object instantiation (new) | Using the blueprint to build an actual object |
| (19) | var keyword | Let the compiler figure out the type — you don't need to spell it out |
| (20) | LINQ + lambda | A filter/query sentence: "From this list, give me items WHERE …" |
| (21) | async/await | Wait for a slow task without freezing everything else |
"""
    )

    # ------------------------------------------------------------------
    # Key C# concepts (technical + layman)
    # ------------------------------------------------------------------
    subsection("Key C# concepts — technical and layman explanations")

    subsection("1. Value types vs reference types")
    paragraph(
        "Technical: value types (int, bool, struct, enum) are stored on the stack and "
        "copied when assigned. Reference types (class, string, array) are stored on the "
        "heap, and passing them passes a reference (pointer) to the same object."
    )
    paragraph(
        "Layman: a value type is like handing someone a photocopy of a document (they "
        "get their own copy). A reference type is like sharing a Google Doc link (both "
        "people see and edit the same document)."
    )
    code_block(
        "int a = 5;\n"
        "int b = a;    // b is a COPY — changing b doesn't affect a\n"
        "b = 10;\n"
        "Console.WriteLine(a); // 5 — unchanged\n"
        "\n"
        "var list1 = new List<int> { 1, 2, 3 };\n"
        "var list2 = list1;    // list2 POINTS to the same list\n"
        "list2.Add(4);\n"
        "Console.WriteLine(list1.Count); // 4 — list1 also changed!",
        language="csharp",
    )

    subsection("2. Generics")
    paragraph(
        "Technical: generics let you write type-safe, reusable code using a type "
        "parameter (<T>). The compiler enforces the type at compile time — no runtime "
        "casting needed."
    )
    paragraph(
        'Layman: a generic box says "this box holds exactly one type of thing — you '
        "decide which type when you order the box. After that, you can only put that "
        'type in."'
    )
    code_block(
        "// Without generics — dangerous (any object, cast required)\n"
        "ArrayList oldList = new ArrayList();\n"
        "oldList.Add(42);\n"
        'oldList.Add("oops");        // compiles but runtime crash if you expect int!\n'
        "\n"
        "// With generics — safe\n"
        "List<int> safeList = new List<int>();\n"
        "safeList.Add(42);\n"
        '// safeList.Add("oops");    // Compile-time error — caught before it runs!\n'
        "\n"
        "// Generic method\n"
        "T Max<T>(T a, T b) where T : IComparable<T>\n"
        "    => a.CompareTo(b) > 0 ? a : b;\n"
        "\n"
        "Console.WriteLine(Max(3, 7));              // 7\n"
        'Console.WriteLine(Max("apple", "banana")); // banana',
        language="csharp",
    )

    subsection("3. Delegates and events")
    paragraph(
        "Technical: a delegate is a type-safe function pointer — a variable that holds "
        "a reference to a method. Events are a publisher/subscriber pattern built on "
        "delegates."
    )
    paragraph(
        'Layman: a delegate is like a job posting: "I need someone who can take an int '
        'and return a string." Any method matching that description can fill the role. '
        "An event is like a doorbell: when pressed, all registered listeners are "
        "notified."
    )
    code_block(
        "// Delegate type declaration\n"
        "delegate string Formatter(int value);\n"
        "\n"
        "// Methods that match the delegate signature\n"
        'string ToHex(int n)    => $"0x{n:X}";\n'
        "string ToBinary(int n) => Convert.ToString(n, 2);\n"
        "\n"
        "Formatter fmt = ToHex;\n"
        "Console.WriteLine(fmt(255)); // 0xFF\n"
        "\n"
        "fmt = ToBinary;\n"
        "Console.WriteLine(fmt(10));  // 1010\n"
        "\n"
        "// Built-in delegate types: Action (void), Func (returns value), Predicate (bool)\n"
        'Action<string> greet    = name => Console.WriteLine($"Hello, {name}!");\n'
        "Func<int, int, int> add = (a, b) => a + b;\n"
        'greet("Alice");               // Hello, Alice!\n'
        "Console.WriteLine(add(3, 4)); // 7",
        language="csharp",
    )

    subsection("4. LINQ (Language Integrated Query)")
    paragraph(
        "Technical: LINQ provides declarative query syntax for any IEnumerable<T> or "
        "IQueryable<T> source — collections, databases (EF Core), XML, JSON."
    )
    paragraph(
        'Layman: LINQ is like SQL for your C# lists. "Give me all customers from my '
        'list where their city is London, ordered by name, and take only the top 5."'
    )
    code_block(
        "var people = new List<(string Name, int Age, string City)>\n"
        "{\n"
        '    ("Alice", 30, "London"),\n'
        '    ("Bob",   25, "Paris"),\n'
        '    ("Carol", 35, "London"),\n'
        '    ("Dave",  28, "Berlin"),\n'
        "};\n"
        "\n"
        "// Method syntax (most common)\n"
        "var londonAdults = people\n"
        '    .Where(p => p.City == "London" && p.Age >= 30)\n'
        "    .OrderBy(p => p.Name)\n"
        "    .Select(p => p.Name)\n"
        "    .ToList();\n"
        '// Result: ["Alice", "Carol"]\n'
        "\n"
        "// Aggregation\n"
        "int    totalAge = people.Sum(p => p.Age);      // 118\n"
        "double avgAge   = people.Average(p => p.Age);  // 29.5\n"
        "int    oldest   = people.Max(p => p.Age);      // 35",
        language="csharp",
    )

    subsection("5. async / await")
    paragraph(
        "Technical: async/await is syntactic sugar over the Task Parallel Library "
        "(TPL). An async method returns Task or Task<T>. The await keyword yields "
        "control back to the caller while waiting for the awaited task — without "
        "blocking the thread."
    )
    paragraph(
        "Layman: imagine a waiter at a restaurant. Without async, the waiter stands at "
        "your table until your food is cooked (blocking everyone). With async, the "
        "waiter takes your order, goes to serve others, and comes back when your food "
        "is ready."
    )
    code_block(
        "async Task<string> FetchWebPageAsync(string url)\n"
        "{\n"
        "    using var client = new HttpClient();\n"
        '    // Await = "start this, come back when done, don\'t block"\n'
        "    string content = await client.GetStringAsync(url);\n"
        "    return content.Substring(0, 200);\n"
        "}\n"
        "\n"
        "// Run multiple async tasks in parallel\n"
        "async Task RunParallelAsync()\n"
        "{\n"
        '    var task1 = FetchWebPageAsync("https://example.com");\n'
        '    var task2 = FetchWebPageAsync("https://microsoft.com");\n'
        "\n"
        "    // Wait for BOTH to complete simultaneously\n"
        "    string[] results = await Task.WhenAll(task1, task2);\n"
        '    Console.WriteLine($"Got {results.Length} pages");\n'
        "}",
        language="csharp",
    )

    subsection("6. Dependency Injection (DI)")
    paragraph(
        "Technical: DI is a design pattern where dependencies (services) are injected "
        "into a class via its constructor rather than the class creating them. .NET "
        "has a built-in DI container (IServiceCollection / IServiceProvider)."
    )
    paragraph(
        "Layman: instead of a chef buying their own ingredients (tight coupling), the "
        "restaurant manager delivers them to the kitchen (injection). The chef doesn't "
        "need to know where the ingredients come from — they just use them."
    )
    code_block(
        "// Interface (the contract)\n"
        "public interface IEmailService\n"
        "{\n"
        "    Task SendAsync(string to, string subject, string body);\n"
        "}\n"
        "\n"
        "// Real implementation\n"
        "public class SmtpEmailService : IEmailService\n"
        "{\n"
        "    public async Task SendAsync(string to, string subject, string body)\n"
        '        => await Task.Run(() => Console.WriteLine($"Sending email to {to}"));\n'
        "}\n"
        "\n"
        "// Consumer — receives IEmailService via constructor injection\n"
        "public class OrderService\n"
        "{\n"
        "    private readonly IEmailService _email;\n"
        "\n"
        "    public OrderService(IEmailService email) => _email = email;\n"
        "\n"
        "    public async Task PlaceOrderAsync(string customerEmail)\n"
        "    {\n"
        '        await _email.SendAsync(customerEmail, "Order confirmed", "Thanks!");\n'
        "    }\n"
        "}\n"
        "\n"
        "// Registration in ASP.NET Core (Program.cs)\n"
        "// builder.Services.AddScoped<IEmailService, SmtpEmailService>();\n"
        "// Swap SmtpEmailService for MockEmailService in tests — zero code changes!",
        language="csharp",
    )

    subsection("7. Exception handling")
    paragraph(
        "Technical: exceptions propagate up the call stack until caught by a try/catch "
        "block. finally always runs (cleanup). Custom exceptions inherit from Exception."
    )
    paragraph(
        "Layman: exception handling is like a safety net in a circus. If an acrobat "
        "(method) falls (throws an exception), the net (catch) catches them. The stage "
        "crew (finally) always tidies up, regardless of what happened."
    )
    code_block(
        "public decimal Divide(decimal a, decimal b)\n"
        "{\n"
        "    if (b == 0)\n"
        '        throw new DivideByZeroException("Cannot divide by zero!");\n'
        "    return a / b;\n"
        "}\n"
        "\n"
        "try\n"
        "{\n"
        "    decimal result = Divide(10, 0);\n"
        "    Console.WriteLine(result);\n"
        "}\n"
        "catch (DivideByZeroException ex)\n"
        "{\n"
        '    Console.WriteLine($"Math error: {ex.Message}"); // handled\n'
        "}\n"
        "catch (Exception ex)\n"
        "{\n"
        '    Console.WriteLine($"Unexpected: {ex.Message}"); // catch-all fallback\n'
        "}\n"
        "finally\n"
        "{\n"
        '    Console.WriteLine("This always runs — good for cleanup (close files, etc.)");\n'
        "}\n"
        "\n"
        "// Custom exception\n"
        "public class InsufficientFundsException : Exception\n"
        "{\n"
        "    public decimal RequiredAmount { get; }\n"
        "    public InsufficientFundsException(decimal amount)\n"
        '        : base($"Need {amount:C} more in your account.") => RequiredAmount = amount;\n'
        "}",
        language="csharp",
    )

    subsection("8. Pattern matching (C# 7–12)")
    paragraph(
        "Technical: pattern matching allows conditional logic based on the "
        "shape/type/value of data using is, switch expressions, property patterns, "
        "list patterns, and relational patterns."
    )
    paragraph(
        "Layman: pattern matching is like a smart sorting machine at a post office. "
        "Instead of writing many separate \"if it's a large box, do X; if it's a small "
        'envelope, do Y" rules, you write one clear set of patterns and the machine '
        "routes each parcel automatically."
    )
    code_block(
        "object shape = new Circle(5.0);\n"
        "\n"
        "// Type pattern (C# 7)\n"
        "if (shape is Circle c)\n"
        '    Console.WriteLine($"Area: {Math.PI * c.Radius * c.Radius:F2}");\n'
        "\n"
        "// Switch expression with property pattern (C# 8)\n"
        "double area = shape switch\n"
        "{\n"
        "    Circle    { Radius: var r }               => Math.PI * r * r,\n"
        "    Rectangle { Width: var w, Height: var h } => w * h,\n"
        "    Triangle  { Base: var b, Height: var h }  => 0.5 * b * h,\n"
        "    null => throw new ArgumentNullException(nameof(shape)),\n"
        '    _    => throw new NotSupportedException("Unknown shape")\n'
        "};\n"
        "\n"
        "// List pattern (C# 11)\n"
        "int[] nums = { 1, 2, 3 };\n"
        "string desc = nums switch\n"
        "{\n"
        '    []          => "empty",\n'
        '    [var x]     => $"single: {x}",\n'
        '    [1, 2, ..]  => "starts with 1, 2",\n'
        '    _           => "other"\n'
        "};",
        language="csharp",
    )
