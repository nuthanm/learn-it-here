"""Learn → Blazor: minimal-layout page using shared content primitives.

Sub-pages (e.g. Web Forms vs Blazor) live as siblings in this package and are
routed via the URL (`?section=blazor&sub=<slug>`) by the Learning Hub, exactly
like the GIT section. See `config.py` → `LEARN_SECTIONS` for the registration.
"""

import streamlit as st

from components.content import (
    code_block,
    paragraph,
    section_intro,
    section_title,
    subsection,
)
from config import PAGE_LEARN, _url_for


def render_blazor():
    section_title(
        "Blazor",
        "Microsoft's framework for building interactive web UIs in C# instead of JavaScript.",
    )
    section_intro(
        "Blazor lets you write full-stack web apps in pure C# — sharing models, "
        "validation, and logic between client and server, with a component model "
        "familiar to React/Angular developers."
    )

    # ── Sub-page link (URL-based, like GIT → Basics / Branching) ─────────────
    subsection("ASP.NET Web Forms Controls vs Blazor Equivalents")
    paragraph(
        "Coming from classic ASP.NET Web Forms? See a side-by-side comparison of "
        "common Web Forms server controls and their idiomatic equivalents in Blazor "
        "(Server, SSR, and WebAssembly), with notes on hosting-model differences."
    )
    _sub_url = _url_for(page=PAGE_LEARN, section="blazor", sub="webforms-comparison")
    st.markdown(
        f'<a class="topic-link" href="{_sub_url}" target="_self">'
        f"Open: Web Forms Controls vs Blazor Equivalents →</a>",
        unsafe_allow_html=True,
    )

    # ── What is Blazor? ──────────────────────────────────────────────────────
    subsection("What is Blazor? (For Complete Beginners)")
    paragraph(
        "Blazor is Microsoft's framework that lets you build interactive web UIs "
        "using C# instead of JavaScript. With Blazor, the same C# skills you use "
        "for back-end development can now power your front-end web experience."
    )
    paragraph(
        "Simple analogy: Normally, web browsers only speak JavaScript. Blazor gives "
        "you a translator (WebAssembly) so the browser can now also understand C# — "
        "letting you write web apps entirely in the language you already know."
    )
    paragraph("Why should you learn Blazor?")
    paragraph("- Write full-stack web apps in pure C# — no JavaScript required.")
    paragraph("- Share code between front-end and back-end (same models, same validation).")
    paragraph("- Backed by Microsoft — integrated into .NET 8.")
    paragraph("- Component-based architecture (similar to React/Angular concepts).")
    paragraph("- Huge growth in adoption — more and more companies use it.")

    # ── History ──────────────────────────────────────────────────────────────
    subsection("Blazor History — From Beginning to Today")
    st.markdown(
        """
| Year | Milestone | What Changed |
|---|---|---|
| 2017 | Steve Sanderson's experimental prototype | Proof-of-concept: C# running in browser via WebAssembly |
| 2018 | Blazor announced at NDC Oslo | Microsoft officially backs the project |
| 2019 (.NET Core 3.0) | **Blazor Server released** (production-ready) | First official Blazor model — runs on server via SignalR |
| 2020 (.NET 5) | **Blazor WebAssembly released** (production-ready) | C# runs directly in the browser — no server needed for UI |
| 2022 (.NET 6) | Blazor improvements | Hot reload, better performance, .NET MAUI Blazor hybrid |
| 2023 (.NET 7) | Enhanced navigation, streaming rendering | Better UX, improved SEO, empty Blazor WASM template |
| 2023 (.NET 8) | **Blazor United / Full-Stack Blazor** | Merged Server + WASM into one model with render mode selection per component |
| 2024 (.NET 9) | Blazor Web App enhancements | Reconnection UI, improved form handling, faster WASM startup |
"""
    )
    paragraph("What replaced what?")
    paragraph("- Web Forms (ASP.NET) → replaced by Blazor Server (for server-side interactive UIs).")
    paragraph("- Silverlight / Flash → replaced by Blazor WebAssembly (for rich browser apps without plugins).")
    paragraph("- JavaScript SPA frameworks (React/Angular/Vue) → Blazor WASM is the C# alternative.")

    # ── Server vs WASM ───────────────────────────────────────────────────────
    subsection("Blazor Server vs Blazor WebAssembly — Side-by-Side")
    st.markdown(
        """
| Feature | Blazor Server | Blazor WebAssembly (WASM) |
|---|---|---|
| Where does C# run? | On the **server** | In the **browser** (via WebAssembly) |
| How UI updates reach browser | SignalR (WebSocket) connection | Direct DOM updates in browser |
| Initial load time | Very fast (small download) | Slower (downloads .NET runtime) |
| Works offline? | No — needs server connection | Yes — once downloaded |
| Server scalability | One connection per user | Stateless — scales easily |
| Access to server resources | Direct DB/file access | Must call an API |
| Latency for interactions | Small delay (network round-trip) | Instant (local execution) |
| Security | Code stays on server (not exposed) | Code runs in browser (decompilable) |
| Best for | Internal tools, admin panels, dashboards | Public apps, PWAs, offline scenarios |
| .NET template | `dotnet new blazorserver` | `dotnet new blazorwasm` |
"""
    )
    paragraph(
        ".NET 8 Blazor Web App — the new default template merges both. You can "
        "choose the rendering mode per page or per component: Static SSR, "
        "Interactive Server, Interactive WASM, or Auto (tries WASM, falls back "
        "to Server). This is the recommended way for new projects."
    )

    # ── Anatomy of a component ───────────────────────────────────────────────
    subsection("Anatomy of a Blazor Component")
    paragraph(
        "A Blazor component is a .razor file that combines HTML markup, C# code, "
        "and CSS styling in one place. Here is every part explained:"
    )
    code_block(
        """<!-- File: Counter.razor — a simple counter component -->

<!-- (1) @page directive — URL route for this component -->
@page "/counter"

<!-- (2) @using / @inject — import namespaces or inject services -->
@using MyApp.Services
@inject ILogger<Counter> Logger

<!-- (3) HTML template — standard HTML + Razor syntax -->
<h1>Counter</h1>

<p>Current count: <strong>@currentCount</strong></p>

<!-- (4) @onclick — event binding — calls C# method on click -->
<button class="btn btn-primary" @onclick="IncrementCount">
    Click me!
</button>

<button class="btn btn-secondary" @onclick="ResetCount">
    Reset
</button>

<!-- (5) @code block — C# code lives here -->
@code {
    // (6) Private field — holds state for this component
    private int currentCount = 0;

    // (7) [Parameter] — accepts values from a parent component
    [Parameter]
    public int StartValue { get; set; } = 0;

    // (8) OnInitialized — lifecycle method, runs when component first loads
    protected override void OnInitialized()
    {
        currentCount = StartValue;
        Logger.LogInformation("Counter initialized at {Value}", StartValue);
    }

    // (9) Event handler method
    private void IncrementCount()
    {
        currentCount++;
        Logger.LogInformation("Count incremented to {Value}", currentCount);
    }

    private void ResetCount() => currentCount = StartValue;
}

<!-- (10) Optional: scoped CSS — in Counter.razor.css file -->
<!-- h1 { color: #1A1A1A; } /* only applies to this component */ -->
""",
        language="razor",
    )

    # ── Create & run ─────────────────────────────────────────────────────────
    subsection("How to Create & Run a Blazor App")
    paragraph("Prerequisites: .NET 8 SDK installed (run `dotnet --version` to check).")

    paragraph("Blazor Web App (.NET 8) — recommended unified model:")
    code_block(
        """# ── Blazor Web App — Recommended for .NET 8+ (unified model) ──

# Create new Blazor Web App
dotnet new blazor -n MyBlazorApp
cd MyBlazorApp

# Run the app (opens in browser at https://localhost:5001)
dotnet run

# Run with hot reload (auto-refreshes on file save)
dotnet watch run
""",
        language="bash",
    )
    code_block(
        """// Program.cs — the startup file (.NET 8 Blazor Web App)
var builder = WebApplication.CreateBuilder(args);

// Add Blazor services — InteractiveServer enables server-side interactivity
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents()       // for server render mode
    .AddInteractiveWebAssemblyComponents(); // for WASM render mode

var app = builder.Build();

app.UseStaticFiles();
app.UseAntiforgery();

// Map Razor components — App.razor is the root component
app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode()
    .AddInteractiveWebAssemblyRenderMode();

app.Run();
""",
        language="csharp",
    )

    paragraph("Blazor Server (.NET 6/7 style):")
    code_block(
        """# ── Blazor Server (.NET 6/7 style) ──────────────────────────────

dotnet new blazorserver -n MyBlazorServer
cd MyBlazorServer
dotnet run
""",
        language="bash",
    )
    code_block(
        """// Program.cs — Blazor Server (.NET 6/7)
var builder = WebApplication.CreateBuilder(args);

// AddServerSideBlazor registers SignalR + Blazor rendering pipeline
builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();

// Register your own services here
builder.Services.AddSingleton<WeatherForecastService>();

var app = builder.Build();

app.UseStaticFiles();
app.UseRouting();

app.MapBlazorHub();              // SignalR endpoint for Blazor
app.MapFallbackToPage("/_Host"); // fallback to _Host.cshtml

app.Run();
""",
        language="csharp",
    )

    paragraph("Blazor WebAssembly (standalone, .NET 6/7 style):")
    code_block(
        """# ── Blazor WebAssembly (standalone, .NET 6/7 style) ─────────────

dotnet new blazorwasm -n MyBlazorWasm
cd MyBlazorWasm
dotnet run

# Hosted (with ASP.NET Core back-end API)
dotnet new blazorwasm --hosted -n MyBlazorWasmHosted
""",
        language="bash",
    )
    code_block(
        """// Program.cs — Blazor WASM (runs in browser)
using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;

var builder = WebAssemblyHostBuilder.CreateDefault(args);

// App is the root component; #app is the HTML element it renders into
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

// HttpClient for calling APIs — base address is the current host
builder.Services.AddScoped(sp => new HttpClient {
    BaseAddress = new Uri(builder.HostEnvironment.BaseAddress)
});

await builder.Build().RunAsync();
""",
        language="csharp",
    )

    # ── Project structure ────────────────────────────────────────────────────
    subsection("Blazor Project Structure — What Every File Does")
    st.markdown(
        """
| File / Folder | Purpose |
|---|---|
| `Program.cs` | App startup, service registration, middleware pipeline |
| `App.razor` | Root component — sets up routing |
| `Routes.razor` (.NET 8) | Router configuration |
| `Pages/` | Page components (have `@page` directive) |
| `Components/` (or `Shared/`) | Reusable components (no `@page` directive) |
| `wwwroot/` | Static files: CSS, images, JavaScript |
| `wwwroot/app.css` | Global CSS styles |
| `ComponentName.razor.css` | Scoped CSS — only applies to that component |
| `appsettings.json` | Configuration settings |
| `_Imports.razor` | `@using` statements for all components (like a global using file) |
"""
    )

    # ── Request workflow ─────────────────────────────────────────────────────
    subsection("Request Workflow — What Happens When You Visit a URL?")
    paragraph(
        "Let's trace exactly what happens when a user visits "
        "`learnithere.com/weather` in a Blazor app, step by step from the browser "
        "all the way to the rendered page."
    )
    st.markdown(
        """
| Step | What Happens | File / Component Involved |
|---|---|---|
| **(1) Browser Request** | User navigates to `/weather`. The browser sends an HTTP request to the server (Blazor Server) or routes locally (WASM). | Browser / HTTP layer |
| **(2) Server Responds** | ASP.NET Core middleware pipeline processes the request. `Program.cs` maps Razor components — `App` is the root. | `Program.cs` |
| **(3) App.razor Loads** | `App.razor` is the root component. It renders a `<Router>` that scans all assemblies for components with an `@page` directive. | `App.razor` |
| **(4) Router Matches Route** | The Router finds `Weather.razor` because it has `@page "/weather"`. If no match is found, the `<NotFound>` content is shown instead. | `Router` inside `App.razor` |
| **(5) RouteView Renders Page** | `<RouteView>` renders the matched component (`Weather.razor`) inside the layout defined by `DefaultLayout`. | `Weather.razor`, `MainLayout.razor` |
| **(6) Component Lifecycle Runs** | Blazor calls lifecycle methods on the component: `OnInitialized` → `OnParametersSet` → `OnAfterRender`. Data is fetched and state is set up here. | `Weather.razor` `@code { }` block |
| **(7) UI Is Rendered** | Blazor generates the HTML from the component's markup + C# state and sends it to the browser DOM. For Blazor Server, updates flow over SignalR. | Blazor rendering engine |
"""
    )

    # ── App.razor explained ──────────────────────────────────────────────────
    subsection("App.razor — The Root Component Explained")
    paragraph(
        "App.razor is always the entry point for Blazor routing. Here is what its "
        "typical content looks like and what each part does:"
    )
    code_block(
        """<!-- App.razor — root component, sets up the Router -->

<Router AppAssembly="@typeof(App).Assembly">

    <!-- (1) Found — rendered when the Router finds a matching @page route -->
    <Found Context="routeData">

        <!-- RouteView renders the matched page inside DefaultLayout -->
        <RouteView RouteData="@routeData" DefaultLayout="@typeof(MainLayout)" />

        <!-- FocusOnNavigate moves keyboard focus to the <h1> on page change -->
        <FocusOnNavigate RouteData="@routeData" Selector="h1" />

    </Found>

    <!-- (2) NotFound — rendered when no @page directive matches the URL -->
    <NotFound>
        <PageTitle>Not found</PageTitle>
        <LayoutView Layout="@typeof(MainLayout)">
            <p role="alert">Sorry, there's nothing at this address.</p>
        </LayoutView>
    </NotFound>

</Router>
""",
        language="razor",
    )
    paragraph("Key attributes explained:")
    paragraph("- `AppAssembly=\"@typeof(App).Assembly\"` — tells the Router which assembly to scan for `@page` routes.")
    paragraph("- `DefaultLayout=\"@typeof(MainLayout)\"` — wraps every page in `MainLayout.razor` (nav bar, footer, etc.) unless overridden.")
    paragraph("- `<RouteView>` — the component that physically renders the matched page.")
    paragraph("- `<FocusOnNavigate>` — accessibility helper; moves focus to the heading after navigation.")
    paragraph("- `<NotFound>` — fallback for 404-style mismatches — no redirect, just renders in-place.")

    # ── End-to-end example ───────────────────────────────────────────────────
    subsection("Example End-to-End: learnithere.com/weather")
    paragraph(
        "Here is the complete picture of what happens when `/weather` is visited, "
        "mapped to real files:"
    )
    code_block(
        """URL:  learnithere.com/weather

// (1) Program.cs  ──────────────────────────────────────────────────
app.MapRazorComponents<App>()   // App.razor is the root
   .AddInteractiveServerRenderMode();

// (2) App.razor  ───────────────────────────────────────────────────
<Router AppAssembly="@typeof(App).Assembly">  // scans for @page routes
    <Found Context="routeData">
        <RouteView RouteData="@routeData"     // "/weather" matched!
                   DefaultLayout="@typeof(MainLayout)" />
    </Found>
</Router>

// (3) MainLayout.razor  ────────────────────────────────────────────
<NavMenu />                      // sidebar/top nav rendered
@Body                            // ← Weather page renders here

// (4) Weather.razor  ───────────────────────────────────────────────
@page "/weather"                 // matched by the Router

<h1>Weather</h1>
<p>Today's forecast: @forecast</p>

@code {
    private string? forecast;

    // (5) Lifecycle: called once when component first loads
    protected override async Task OnInitializedAsync()
    {
        forecast = await WeatherService.GetForecastAsync();
    }
}

// (6) Browser displays rendered HTML ──────────────────────────────
//    (Blazor Server: updates via SignalR WebSocket)
//    (Blazor WASM:  direct DOM update in browser)
""",
        language="razor",
    )

    # ── Things to be aware of ────────────────────────────────────────────────
    subsection("Key Things to Be Aware Of in Blazor")
    st.markdown(
        """
| # | Topic | What to Know |
|---|---|---|
| 1 | Component lifecycle | Learn `OnInitialized`, `OnParametersSet`, `OnAfterRender` — called at specific moments |
| 2 | `StateHasChanged()` | Call this to force UI re-render when state changes outside event handlers |
| 3 | `@bind` directive | Two-way data binding: `@bind="myVariable"` syncs input value and C# field |
| 4 | EventCallback | Use `EventCallback<T>` to pass events from child to parent components |
| 5 | Cascading Parameters | Share data through a component tree without passing through every level |
| 6 | JavaScript Interop | Call JS from C# with `IJSRuntime.InvokeAsync` — needed for browser APIs |
| 7 | WASM first load | First load is slow (downloads .NET runtime ~5–10MB) — use loading spinner |
| 8 | Authentication | Use `AuthenticationStateProvider`; Blazor supports cookie, JWT, OIDC auth |
| 9 | Render modes (.NET 8) | `@rendermode InteractiveServer / InteractiveWebAssembly / InteractiveAuto` |
| 10 | No direct DOM access | Don't manipulate DOM with JS directly — let Blazor manage it |
"""
    )
