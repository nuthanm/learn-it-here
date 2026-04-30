"""Blazor sub-page: Fluent UI Blazor — beginner-friendly guide."""

import streamlit as st

from components.content import (
    code_block,
    paragraph,
    section_intro,
    section_title,
    subsection,
)


def render_blazor_fluent_ui():
    """Sub-page: Microsoft Fluent UI Blazor — setup, usage, and common issues."""

    section_title(
        "Fluent UI Blazor Components",
        "Install, configure, and use Microsoft's Fluent Design System inside your Blazor app — step by step.",
    )
    section_intro(
        "Fluent UI Blazor is a free component library made by Microsoft. "
        "It gives you polished, accessible controls (buttons, grids, dialogs, and more) "
        "that follow the Fluent Design System — the same design language used in Microsoft 365. "
        "This guide is written for people who are new to Blazor and just want to get things working."
    )

    # ── Quick comparison ─────────────────────────────────────────────────────
    subsection("1. How Does Fluent UI Fit In? (Quick Comparison)")
    paragraph(
        "If you have worked with classic ASP.NET Web Forms, or plain Blazor without a component "
        "library, the table below shows where Fluent UI sits in the picture."
    )
    st.markdown(
        """
| Area | ASPX / Web Forms | Plain Blazor | Fluent UI Blazor |
|---|---|---|---|
| UI model | Server controls, ViewState, postbacks | Component-based Razor + C# | Razor components styled with Fluent Design |
| Button | `<asp:Button>` | `<button @onclick="...">` | `<FluentButton OnClick="...">` |
| Text input | `<asp:TextBox>` | `<InputText>` or `<input>` | `<FluentTextField>` |
| Drop-down | `<asp:DropDownList>` | `<InputSelect>` or `<select>` | `<FluentSelect>` |
| Data table | `<asp:GridView>` | HTML `<table>` + `@foreach` | `<FluentDataGrid>` |
| Card / panel | `<asp:Panel>` | `<div>` | `<FluentCard>` |
| Layout | Tables, `<div>` + CSS | `<div>` + CSS | `<FluentStack>` |
| Styling | CSS, Bootstrap, themes | CSS, Bootstrap, isolated CSS | Fluent Design System |
| Extra setup needed? | No | No | Yes — NuGet package + service + assets |
"""
    )
    paragraph(
        "Key takeaway: Fluent UI is not a replacement for Blazor — it is a component library "
        "that runs on top of Blazor. You still write normal Blazor code; you just use "
        "`<FluentButton>` instead of `<button>`, and so on."
    )

    # ── Concept mapping ──────────────────────────────────────────────────────
    subsection("2. Concept Mapping — ASPX → Blazor → Fluent UI")
    st.markdown(
        """
| ASPX / Web Forms | Blazor Equivalent | Fluent UI Equivalent |
|---|---|---|
| `<asp:Button>` | `<button @onclick="Handler">` | `<FluentButton OnClick="Handler">` |
| `<asp:Label>` | `@value` (text interpolation) | `<FluentLabel>` or text inside Fluent components |
| `<asp:TextBox>` | `<InputText>` or `<input>` | `<FluentTextField>` |
| `<asp:DropDownList>` | `<InputSelect>` or `<select>` | `<FluentSelect>` |
| `<asp:GridView>` | HTML table or custom component | `<FluentDataGrid>` |
| `<asp:Panel>` | `<div>` or child component | `<FluentCard>`, `<FluentStack>` |
| `<asp:Repeater>` | `@foreach` loop | `@foreach` with Fluent components |
| `<asp:ValidationSummary>` | Blazor validation components | Fluent validation UI + Blazor validation |
| `OnClick="Button_Click"` | `@onclick="Handler"` | `OnClick="Handler"` |
| CodeBehind | `@code` block or partial class | `@code` block or partial class |
| ViewState | Component state fields | Component state fields |
| PostBack | Blazor event callback + re-render | Blazor event callback + re-render |
"""
    )

    # ── Prerequisites ─────────────────────────────────────────────────────────
    subsection("3. Prerequisites — What You Need Before Starting")
    paragraph("Make sure you have all of the following before installing Fluent UI:")
    st.markdown(
        """
| Requirement | Where to get it |
|---|---|
| Visual Studio 2022 (or VS Code) | https://visualstudio.microsoft.com |
| .NET 8 SDK (or newer) | https://dotnet.microsoft.com/download |
| A Blazor project (Server, WASM, or Web App) | `dotnet new blazor -n MyApp` |
| NuGet access (internet or internal feed) | Built into Visual Studio / dotnet CLI |
"""
    )
    paragraph(
        "Recommended knowledge: basic C#, Razor syntax, dependency injection basics, and HTML. "
        "You do not need to know JavaScript to use Fluent UI."
    )

    # ── Installation ─────────────────────────────────────────────────────────
    subsection("4. Installation — Four Steps to Get Fluent UI Working")

    paragraph(
        "Step 1 — Install the NuGet package. "
        "Run this command inside your project folder (where the .csproj file lives):"
    )
    code_block(
        "dotnet add package Microsoft.FluentUI.AspNetCore.Components",
        language="bash",
        label="Terminal / Package Manager Console",
    )
    paragraph("To pin a specific version:")
    code_block(
        "dotnet add package Microsoft.FluentUI.AspNetCore.Components --version 4.14.1",
        language="bash",
    )
    paragraph(
        "Or add it directly in your .csproj file inside an `<ItemGroup>` tag:"
    )
    code_block(
        """<ItemGroup>
  <PackageReference Include="Microsoft.FluentUI.AspNetCore.Components" Version="4.14.1" />
</ItemGroup>""",
        language="xml",
        label="YourProject.csproj",
    )

    paragraph(
        "Step 2 — Register the services. "
        "Open Program.cs and add two lines:"
    )
    code_block(
        """using Microsoft.FluentUI.AspNetCore.Components;  // add this using
using ServerInteractivity.Components;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

builder.Services.AddFluentUIComponents();  // add this line

var app = builder.Build();
""",
        language="csharp",
        label="Program.cs",
    )

    paragraph(
        "Step 3 — Add the namespace to _Imports.razor. "
        "This means you can use `<FluentButton>` on any page without a long `@using` line at the top."
    )
    code_block(
        "@using Microsoft.FluentUI.AspNetCore.Components",
        language="razor",
        label="_Imports.razor",
    )

    paragraph(
        "Step 4 — Add the CSS and JavaScript to App.razor "
        "(the root shell file, not a page component)."
    )
    code_block(
        """<head>
    <!-- Fluent UI reboot CSS — normalises browser default styles -->
    <link rel="stylesheet"
          href="@Assets[\\"_content/Microsoft.FluentUI.AspNetCore.Components/css/reboot.css\\"]" />
    <HeadOutlet />
</head>

<body>
    <Routes />

    <!-- Fluent UI JS module — must come BEFORE blazor.web.js -->
    <script type="module"
            src="@Assets[\\"_content/Microsoft.FluentUI.AspNetCore.Components/Microsoft.FluentUI.AspNetCore.Components.lib.module.js\\"]">
    </script>

    <script src="@Assets[\\"_framework/blazor.web.js\\"]"></script>
</body>""",
        language="razor",
        label="App.razor",
    )

    # ── Usage examples ────────────────────────────────────────────────────────
    subsection("5. Basic Usage Examples")

    paragraph("FluentButton — a simple button with an accent style:")
    code_block(
        """<FluentButton Appearance="Appearance.Accent" OnClick="SayHello">
    Click me
</FluentButton>

@code {
    private void SayHello()
    {
        Console.WriteLine("Hello from Fluent UI!");
    }
}""",
        language="razor",
    )

    paragraph("FluentTextField — a labelled text input bound to a C# field:")
    code_block(
        """<FluentTextField Label="Your name" @bind-Value="_name" />
<p>Hello, @_name!</p>

@code {
    private string _name = string.Empty;
}""",
        language="razor",
    )

    paragraph("FluentSelect — a drop-down list:")
    code_block(
        """<FluentSelect Label="Pick a colour" @bind-Value="_colour">
    <FluentOption Value="red">Red</FluentOption>
    <FluentOption Value="green">Green</FluentOption>
    <FluentOption Value="blue">Blue</FluentOption>
</FluentSelect>

<p>You chose: @_colour</p>

@code {
    private string _colour = "red";
}""",
        language="razor",
    )

    paragraph("FluentCard + FluentStack — group content in a card with vertical spacing:")
    code_block(
        """<FluentCard Width="400px">
    <FluentStack Orientation="Orientation.Vertical" VerticalGap="12">
        <h3>Welcome</h3>
        <p>This is inside a Fluent card.</p>
        <FluentButton Appearance="Appearance.Accent">Get started</FluentButton>
    </FluentStack>
</FluentCard>""",
        language="razor",
    )

    paragraph("FluentDataGrid — display a list of objects as a table:")
    code_block(
        """<FluentDataGrid Items="_people.AsQueryable()">
    <PropertyColumn Title="Name"  Property="@(p => p.Name)" />
    <PropertyColumn Title="Email" Property="@(p => p.Email)" />
</FluentDataGrid>

@code {
    private record Person(string Name, string Email);

    private readonly List<Person> _people = new()
    {
        new("Alice", "alice@example.com"),
        new("Bob",   "bob@example.com"),
    };
}""",
        language="razor",
    )

    # ── Full page example ─────────────────────────────────────────────────────
    subsection("6. Full Page Example — Show / Hide a History Grid")
    paragraph(
        "This end-to-end example shows a parent page and a child component communicating "
        "through Blazor parameters and EventCallback — all using Fluent UI components."
    )
    paragraph("Parent page (Pages/FluentHistory.razor):")
    code_block(
        """@page "/fluent-history"
@rendermode InteractiveServer

<PageTitle>Fluent History</PageTitle>

<FluentCard Width="100%">
    <FluentStack Orientation="Orientation.Vertical" VerticalGap="16">

        <FluentButton Appearance="Appearance.Accent" OnClick="ShowHistory">
            Show History
        </FluentButton>

        @if (_showHistory)
        {
            <!-- Pass data down and listen for the Close event from the child -->
            <HistoryGrid Items="_items" OnClose="HideHistory" />
        }

    </FluentStack>
</FluentCard>

@code {
    private bool _showHistory;

    private readonly List<HistoryItem> _items = new()
    {
        new HistoryItem { Date = "04/28/2025", Status = "New",     UpdatedBy = "Admin" },
        new HistoryItem { Date = "04/01/2025", Status = "Pending", UpdatedBy = "System" },
    };

    private void ShowHistory() => _showHistory = true;
    private void HideHistory() => _showHistory = false;
}""",
        language="razor",
        label="Pages/FluentHistory.razor",
    )

    paragraph("Child component (Components/HistoryGrid.razor):")
    code_block(
        """<!-- No @page here — this is a reusable component, not a page -->

<FluentCard Width="100%">
    <FluentStack Orientation="Orientation.Vertical" VerticalGap="12">

        @if (Items.Count > 0)
        {
            <FluentDataGrid Items="Items.AsQueryable()">
                <PropertyColumn Title="Date"       Property="@(x => x.Date)" />
                <PropertyColumn Title="Status"     Property="@(x => x.Status)" />
                <PropertyColumn Title="Updated By" Property="@(x => x.UpdatedBy)" />
            </FluentDataGrid>
        }
        else
        {
            <FluentMessageBar Intent="MessageIntent.Info">
                No history records found.
            </FluentMessageBar>
        }

        <FluentButton Appearance="Appearance.Neutral" OnClick="HandleClose">
            Close
        </FluentButton>

    </FluentStack>
</FluentCard>

@code {
    [Parameter] public List<HistoryItem> Items  { get; set; } = new();
    [Parameter] public EventCallback    OnClose { get; set; }

    private Task HandleClose() => OnClose.InvokeAsync();
}""",
        language="razor",
        label="Components/HistoryGrid.razor",
    )

    paragraph("The shared data model:")
    code_block(
        """public class HistoryItem
{
    public string Date      { get; set; } = string.Empty;
    public string Status    { get; set; } = string.Empty;
    public string UpdatedBy { get; set; } = string.Empty;
}""",
        language="csharp",
        label="Models/HistoryItem.cs",
    )

    # ── Common issues ─────────────────────────────────────────────────────────
    subsection("7. Common Issues and How to Fix Them")
    paragraph(
        "These are the problems that new users run into most often. "
        "Read through them before you spend time debugging."
    )

    st.markdown(
        """
| # | Symptom | Most likely cause | Fix |
|---|---|---|---|
| 1 | `<FluentButton>` is not recognised / shows as plain text | `@using` line missing from `_Imports.razor` | Add `@using Microsoft.FluentUI.AspNetCore.Components` to `_Imports.razor` |
| 2 | Fluent UI components appear unstyled (no CSS) | `reboot.css` not linked in `App.razor` | Add `<link rel="stylesheet" href="@Assets[\\"...\\"]/css/reboot.css" />` inside `<head>` in `App.razor` |
| 3 | Icons show as blank squares or missing | `Microsoft.FluentUI.AspNetCore.Components.Icons` package not installed | Install it: `dotnet add package Microsoft.FluentUI.AspNetCore.Components.Icons` |
| 4 | `AddFluentUIComponents()` — method not found | Using statement missing in `Program.cs` | Add `using Microsoft.FluentUI.AspNetCore.Components;` at the top of `Program.cs` |
| 5 | `@bind-Value` on `<FluentTextField>` gives a compile error | Wrong binding syntax | Use `@bind-Value` (capital V), not `@bind-value`. Blazor is case-sensitive. |
| 6 | `<FluentDataGrid>` compile error: `Items` must be `IQueryable<T>` | Passing a `List<T>` directly | Call `.AsQueryable()` on your list: `Items="_myList.AsQueryable()"` |
| 7 | Buttons / inputs do nothing when clicked | Component is rendered in Static SSR mode (no interactivity) | Add `@rendermode InteractiveServer` (or `InteractiveAuto`) to the page or the component |
| 8 | JS errors in the browser console about Fluent UI | Fluent UI script not loaded, or loaded after `blazor.web.js` | Move `<script type="module" src="...lib.module.js">` **before** `<script src="...blazor.web.js">` in `App.razor` |
| 9 | `FluentMessageBar` or `FluentToast` does not show | Missing `<FluentToastProvider>` / `<FluentMessageBarProvider>` in the layout | Add the provider component to `MainLayout.razor` (see docs for each provider) |
| 10 | Hot-reload does not pick up Fluent UI style changes | Static asset caching | Stop and restart `dotnet watch` / `dotnet run`; clear browser cache |
"""
    )

    subsection("7a. Issue Deep-Dive: Components Render But Do Not Respond to Clicks")
    paragraph(
        "This is the single most common beginner confusion. Here is why it happens and "
        "exactly how to fix it."
    )
    paragraph(
        "Why it happens: In .NET 8 Blazor Web Apps, the default render mode is Static SSR. "
        "In Static SSR the page is HTML-only — Blazor's SignalR circuit is not connected, "
        "so event handlers such as `OnClick` are simply ignored."
    )
    paragraph("How to fix it — add `@rendermode InteractiveServer` to the top of the page:")
    code_block(
        """@page "/my-page"
@rendermode InteractiveServer   <!-- THIS LINE enables click handlers -->

<FluentButton OnClick="DoSomething">Click me</FluentButton>

@code {
    private void DoSomething() { /* now this works */ }
}""",
        language="razor",
    )
    paragraph(
        "Alternative: add the render mode at the component level in the parent so that only "
        "the interactive part re-renders, while the outer page stays static:"
    )
    code_block(
        """<!-- Parent page (static SSR is fine here) -->
@page "/my-page"

<h1>My Page</h1>

<!-- Only this component is interactive -->
<MyInteractiveWidget @rendermode="InteractiveServer" />""",
        language="razor",
    )

    subsection("7b. Issue Deep-Dive: FluentDataGrid Does Not Compile")
    paragraph("Two common compile errors and their fixes:")
    code_block(
        """// ERROR: cannot convert List<T> to IQueryable<T>
<FluentDataGrid Items="_myList">          <!-- wrong -->

// FIX: call .AsQueryable()
<FluentDataGrid Items="_myList.AsQueryable()">  <!-- correct -->""",
        language="razor",
    )
    code_block(
        """// ERROR: 'PropertyColumn' does not exist in the current context
// FIX: make sure the NuGet package is installed AND _Imports.razor has:
@using Microsoft.FluentUI.AspNetCore.Components""",
        language="razor",
    )

    # ── Lifecycle comparison ─────────────────────────────────────────────────
    subsection("8. Lifecycle: ASPX → Blazor → Fluent UI")
    st.markdown(
        """
| Concept | ASPX / Web Forms | Blazor | Fluent UI Blazor |
|---|---|---|---|
| Initial load | `Page_Load` | `OnInitialized` / `OnInitializedAsync` | Same as Blazor |
| UI event | Server postback | Event callback | Event callback |
| State persistence | ViewState / Session | Component fields / services | Component fields / services |
| Parent-child communication | Control references, server events | `[Parameter]`, `EventCallback` | `[Parameter]`, `EventCallback` |
| Data binding | Server control binding | Razor binding | Razor binding with Fluent components |
| Re-render | Full or partial postback | Render tree diff | Render tree diff |
"""
    )

    # ── Migration guidance ────────────────────────────────────────────────────
    subsection("9. Migrating From ASPX to Fluent UI Blazor")
    paragraph(
        "If you have an existing Web Forms page and want to migrate it to Fluent UI Blazor, "
        "follow these steps in order."
    )
    st.markdown(
        """
1. **Identify the controls** on the ASPX page and their events (button clicks, grid data binding, etc.).
2. **Extract the data model** — create a plain C# class to hold the data (replacing ViewState).
3. **Create a `.razor` component** in your Blazor project.
4. **Replace postback events** with Blazor event handlers (`@onclick` → `OnClick`).
5. **Replace ViewState** with `private bool` or `private` fields in the `@code` block.
6. **Replace ASPX controls** with Fluent UI equivalents (see the mapping table in section 2).
7. **Test** data loading, button clicks, and parent-child communication.
"""
    )
    st.markdown(
        """
| Existing ASPX feature | Blazor migration | Fluent UI migration |
|---|---|---|
| `GridView` history table | `@foreach` table | `<FluentDataGrid>` |
| `Button` with postback | `@onclick` method | `<FluentButton OnClick="...">` |
| `Panel.Visible = true/false` | `@if` conditional rendering | `@if` with `<FluentCard>` |
| Code-behind event handler | Razor component method | Razor component method |
| ViewState flag (`bool`) | `private bool` field | `private bool` field |
"""
    )

    # ── Best practices ────────────────────────────────────────────────────────
    subsection("10. Best Practices")
    st.markdown(
        """
| # | Practice | Why it matters |
|---|---|---|
| 1 | Use `<FluentStack>` for layout | Avoids many nested `<div>` elements and keeps layout readable |
| 2 | Use `<FluentCard>` for grouped content | Provides consistent spacing and visual grouping |
| 3 | Use `<FluentButton>` instead of `<button>` | Ensures consistent Fluent styling and accessibility |
| 4 | Use `<FluentDataGrid>` for tables | Built-in sorting, paging, virtualisation support |
| 5 | Keep `[Parameter]` inputs on child components | Makes components reusable and testable |
| 6 | Use `EventCallback` for child-to-parent events | Correct Blazor pattern; auto-calls `StateHasChanged` |
| 7 | Avoid `StateHasChanged()` after normal UI events | Blazor already re-renders after event callbacks; calling it again wastes a render |
| 8 | Prefer `async` methods for data loading | Keeps UI responsive; use `OnInitializedAsync` |
| 9 | Avoid mixing Bootstrap and Fluent UI heavily | Pick one design system per page to keep styles consistent |
| 10 | Add `@rendermode InteractiveServer` when you need clicks | Without it buttons do nothing in Static SSR |
"""
    )
