import streamlit as st


def render_blazor():
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🔥 What is Blazor? (For Complete Beginners)</div>
  <div class="card-body">
<b>Blazor</b> is Microsoft's framework that lets you build <em>interactive web UIs using C#</em>
instead of JavaScript. With Blazor, the same C# skills you use for back-end development can
now power your front-end web experience.<br><br>
<b>Simple analogy:</b> Normally, web browsers only speak "JavaScript". Blazor gives you a
translator (WebAssembly) so the browser can now also understand C# — letting you write
web apps entirely in the language you already know.<br><br>
<b>Why should you learn Blazor?</b><br>
✅ Write full-stack web apps in pure C# — no JavaScript required<br>
✅ Share code between front-end and back-end (same models, same validation)<br>
✅ Backed by Microsoft — integrated into .NET 8<br>
✅ Component-based architecture (similar to React/Angular concepts)<br>
✅ Huge growth in adoption — more and more companies use it
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">📜 Blazor History — From Beginning to Today</div>
  <div class="card-body">
<table class="shortcut-table">
  <tr><th>Year</th><th>Milestone</th><th>What Changed</th></tr>
  <tr><td>2017</td><td>Steve Sanderson's experimental prototype</td><td>Proof-of-concept: C# running in browser via WebAssembly</td></tr>
  <tr><td>2018</td><td>Blazor announced at NDC Oslo</td><td>Microsoft officially backs the project</td></tr>
  <tr><td>2019 (.NET Core 3.0)</td><td><b>Blazor Server released</b> (production-ready)</td><td>First official Blazor model — runs on server via SignalR</td></tr>
  <tr><td>2020 (.NET 5)</td><td><b>Blazor WebAssembly released</b> (production-ready)</td><td>C# runs directly in the browser — no server needed for UI</td></tr>
  <tr><td>2022 (.NET 6)</td><td>Blazor improvements</td><td>Hot reload, better performance, .NET MAUI Blazor hybrid</td></tr>
  <tr><td>2023 (.NET 7)</td><td>Enhanced navigation, streaming rendering</td><td>Better UX, improved SEO, empty Blazor WASM template</td></tr>
  <tr><td>2023 (.NET 8)</td><td><b>Blazor United / Full-Stack Blazor</b></td><td>Merged Server + WASM into one model with render mode selection per component</td></tr>
  <tr><td>2024 (.NET 9)</td><td>Blazor Web App enhancements</td><td>Reconnection UI, improved form handling, faster WASM startup</td></tr>
</table>
<br>
<b>What replaced what?</b><br>
🔴 <b>Web Forms (ASP.NET)</b> → replaced by <b>Blazor Server</b> (for server-side interactive UIs)<br>
🔴 <b>Silverlight / Flash</b> → replaced by <b>Blazor WebAssembly</b> (for rich browser apps without plugins)<br>
🔴 <b>JavaScript SPA frameworks (React/Angular/Vue)</b> → Blazor WASM is the C# alternative
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">⚖️ Blazor Server vs Blazor WebAssembly — Side-by-Side</div>
  <div class="card-body">
<table class="shortcut-table">
  <tr><th>Feature</th><th>Blazor Server</th><th>Blazor WebAssembly (WASM)</th></tr>
  <tr><td>Where does C# run?</td><td>On the <b>server</b></td><td>In the <b>browser</b> (via WebAssembly)</td></tr>
  <tr><td>How UI updates reach browser</td><td>SignalR (WebSocket) connection</td><td>Direct DOM updates in browser</td></tr>
  <tr><td>Initial load time</td><td>⚡ Very fast (small download)</td><td>🐢 Slower (downloads .NET runtime)</td></tr>
  <tr><td>Works offline?</td><td>❌ No — needs server connection</td><td>✅ Yes — once downloaded</td></tr>
  <tr><td>Server scalability</td><td>⚠️ One connection per user</td><td>✅ Stateless — scales easily</td></tr>
  <tr><td>Access to server resources</td><td>✅ Direct DB/file access</td><td>❌ Must call an API</td></tr>
  <tr><td>Latency for interactions</td><td>⚠️ Small delay (network round-trip)</td><td>✅ Instant (local execution)</td></tr>
  <tr><td>Security</td><td>✅ Code stays on server (not exposed)</td><td>⚠️ Code runs in browser (decompilable)</td></tr>
  <tr><td>Best for</td><td>Internal tools, admin panels, dashboards</td><td>Public apps, PWAs, offline scenarios</td></tr>
  <tr><td>.NET template</td><td>dotnet new blazorserver</td><td>dotnet new blazorwasm</td></tr>
</table>
<br>
<b>.NET 8 Blazor Web App</b> — the new default template merges both! You can choose the
rendering mode <em>per page or per component</em>: Static SSR, Interactive Server, Interactive WASM,
or Auto (tries WASM, falls back to Server). This is the recommended way for new projects.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🏗️ Anatomy of a Blazor Component</div>
  <div class="card-body">
A Blazor component is a <code>.razor</code> file that combines HTML markup, C# code, and CSS styling
in one place. Here's every part explained:
  </div>
</div>
<div class="cmd-block">
<span class="cmd-comment">&lt;!-- File: Counter.razor — a simple counter component --&gt;</span>
&#8203;
<span class="cmd-comment">&lt;!-- ① @page directive — URL route for this component --&gt;</span>
@page "/counter"
&#8203;
<span class="cmd-comment">&lt;!-- ② @using / @inject — import namespaces or inject services --&gt;</span>
@using MyApp.Services
@inject ILogger&lt;Counter&gt; Logger
&#8203;
<span class="cmd-comment">&lt;!-- ③ HTML template — standard HTML + Razor syntax --&gt;</span>
&lt;h1&gt;🔢 Counter&lt;/h1&gt;
&#8203;
&lt;p&gt;Current count: &lt;strong&gt;@currentCount&lt;/strong&gt;&lt;/p&gt;
&#8203;
<span class="cmd-comment">&lt;!-- ④ @onclick — event binding — calls C# method on click --&gt;</span>
&lt;button class="btn btn-primary" @onclick="IncrementCount"&gt;
Click me!
&lt;/button&gt;
&#8203;
&lt;button class="btn btn-secondary" @onclick="ResetCount"&gt;
Reset
&lt;/button&gt;
&#8203;
<span class="cmd-comment">&lt;!-- ⑤ @code block — C# code lives here --&gt;</span>
@code {
<span class="cmd-comment">// ⑥ Private field — holds state for this component</span>
private int currentCount = 0;
&#8203;
<span class="cmd-comment">// ⑦ [Parameter] — accepts values from a parent component</span>
[Parameter]
public int StartValue { get; set; } = 0;
&#8203;
<span class="cmd-comment">// ⑧ OnInitialized — lifecycle method, runs when component first loads</span>
protected override void OnInitialized()
{
    currentCount = StartValue;
    Logger.LogInformation("Counter initialized at {Value}", StartValue);
}
&#8203;
<span class="cmd-comment">// ⑨ Event handler method</span>
private void IncrementCount()
{
    currentCount++;
    Logger.LogInformation("Count incremented to {Value}", currentCount);
}
&#8203;
private void ResetCount() =&gt; currentCount = StartValue;
}
&#8203;
<span class="cmd-comment">&lt;!-- ⑩ Optional: scoped CSS — in Counter.razor.css file --&gt;</span>
<span class="cmd-comment">&lt;!-- h1 { color: #1A1A1A; } /* only applies to this component */ --&gt;</span>
</div>
<div class="content-card">
  <div class="card-title">🚀 How to Create &amp; Run a Blazor App</div>
  <div class="card-body">
<b>Prerequisites:</b> .NET 8 SDK installed (<code>dotnet --version</code> to check)
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    tabs_blazor = st.tabs(["Blazor Web App (.NET 8)", "Blazor Server (.NET 7-)", "Blazor WASM (.NET 7-)"])

    with tabs_blazor[0]:
        st.markdown(
            """
<div class="cmd-block">
<span class="cmd-comment"># ── Blazor Web App — Recommended for .NET 8+ (unified model) ──</span>
&#8203;
<span class="cmd-comment"># Create new Blazor Web App</span>
dotnet new blazor -n MyBlazorApp
cd MyBlazorApp
&#8203;
<span class="cmd-comment"># Run the app (opens in browser at https://localhost:5001)</span>
dotnet run
&#8203;
<span class="cmd-comment"># Run with hot reload (auto-refreshes on file save)</span>
dotnet watch run
</div>
<br>
<div class="cmd-block">
<span class="cmd-comment">// Program.cs — the startup file (.NET 8 Blazor Web App)</span>
var builder = WebApplication.CreateBuilder(args);
&#8203;
<span class="cmd-comment">// Add Blazor services — InteractiveServer enables server-side interactivity</span>
builder.Services.AddRazorComponents()
.AddInteractiveServerComponents()      <span class="cmd-comment">// for server render mode</span>
.AddInteractiveWebAssemblyComponents(); <span class="cmd-comment">// for WASM render mode</span>
&#8203;
var app = builder.Build();
&#8203;
app.UseStaticFiles();
app.UseAntiforgery();
&#8203;
<span class="cmd-comment">// Map Razor components — App.razor is the root component</span>
app.MapRazorComponents&lt;App&gt;()
.AddInteractiveServerRenderMode()
.AddInteractiveWebAssemblyRenderMode();
&#8203;
app.Run();
</div>
""",
            unsafe_allow_html=True,
        )

    with tabs_blazor[1]:
        st.markdown(
            """
<div class="cmd-block">
<span class="cmd-comment"># ── Blazor Server (.NET 6/7 style) ──────────────────────────────</span>
&#8203;
dotnet new blazorserver -n MyBlazorServer
cd MyBlazorServer
dotnet run
</div>
<br>
<div class="cmd-block">
<span class="cmd-comment">// Program.cs — Blazor Server (.NET 6/7)</span>
var builder = WebApplication.CreateBuilder(args);
&#8203;
<span class="cmd-comment">// AddServerSideBlazor registers SignalR + Blazor rendering pipeline</span>
builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();
&#8203;
<span class="cmd-comment">// Register your own services here</span>
builder.Services.AddSingleton&lt;WeatherForecastService&gt;();
&#8203;
var app = builder.Build();
&#8203;
app.UseStaticFiles();
app.UseRouting();
&#8203;
app.MapBlazorHub();              <span class="cmd-comment">// SignalR endpoint for Blazor</span>
app.MapFallbackToPage("/_Host"); <span class="cmd-comment">// fallback to _Host.cshtml</span>
&#8203;
app.Run();
</div>
""",
            unsafe_allow_html=True,
        )

    with tabs_blazor[2]:
        st.markdown(
            """
<div class="cmd-block">
<span class="cmd-comment"># ── Blazor WebAssembly (standalone, .NET 6/7 style) ─────────────</span>
&#8203;
dotnet new blazorwasm -n MyBlazorWasm
cd MyBlazorWasm
dotnet run
&#8203;
<span class="cmd-comment"># Hosted (with ASP.NET Core back-end API)</span>
dotnet new blazorwasm --hosted -n MyBlazorWasmHosted
</div>
<br>
<div class="cmd-block">
<span class="cmd-comment">// Program.cs — Blazor WASM (runs in browser)</span>
using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
&#8203;
var builder = WebAssemblyHostBuilder.CreateDefault(args);
&#8203;
<span class="cmd-comment">// App is the root component; #app is the HTML element it renders into</span>
builder.RootComponents.Add&lt;App&gt;("#app");
builder.RootComponents.Add&lt;HeadOutlet&gt;("head::after");
&#8203;
<span class="cmd-comment">// HttpClient for calling APIs — base address is the current host</span>
builder.Services.AddScoped(sp =&gt; new HttpClient {
BaseAddress = new Uri(builder.HostEnvironment.BaseAddress)
});
&#8203;
await builder.Build().RunAsync();
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">📁 Blazor Project Structure — What Every File Does</div>
  <div class="card-body">
<table class="shortcut-table">
  <tr><th>File / Folder</th><th>Purpose</th></tr>
  <tr><td>Program.cs</td><td>App startup, service registration, middleware pipeline</td></tr>
  <tr><td>App.razor</td><td>Root component — sets up routing</td></tr>
  <tr><td>Routes.razor (.NET 8)</td><td>Router configuration</td></tr>
  <tr><td>Pages/</td><td>Page components (have @page directive)</td></tr>
  <tr><td>Components/ (or Shared/)</td><td>Reusable components (no @page directive)</td></tr>
  <tr><td>wwwroot/</td><td>Static files: CSS, images, JavaScript</td></tr>
  <tr><td>wwwroot/app.css</td><td>Global CSS styles</td></tr>
  <tr><td>ComponentName.razor.css</td><td>Scoped CSS — only applies to that component</td></tr>
  <tr><td>appsettings.json</td><td>Configuration settings</td></tr>
  <tr><td>_Imports.razor</td><td>@using statements for all components (like a global using file)</td></tr>
</table>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">⚠️ Key Things to Be Aware Of in Blazor</div>
  <div class="card-body">
<table class="shortcut-table">
  <tr><th>#</th><th>Topic</th><th>What to Know</th></tr>
  <tr><td>1</td><td>Component lifecycle</td><td>Learn OnInitialized, OnParametersSet, OnAfterRender — called at specific moments</td></tr>
  <tr><td>2</td><td>StateHasChanged()</td><td>Call this to force UI re-render when state changes outside event handlers</td></tr>
  <tr><td>3</td><td>@bind directive</td><td>Two-way data binding: @bind="myVariable" syncs input value and C# field</td></tr>
  <tr><td>4</td><td>EventCallback</td><td>Use EventCallback&lt;T&gt; to pass events from child to parent components</td></tr>
  <tr><td>5</td><td>Cascading Parameters</td><td>Share data through a component tree without passing through every level</td></tr>
  <tr><td>6</td><td>JavaScript Interop</td><td>Call JS from C# with IJSRuntime.InvokeAsync — needed for browser APIs</td></tr>
  <tr><td>7</td><td>WASM first load</td><td>First load is slow (downloads .NET runtime ~5–10MB) — use loading spinner</td></tr>
  <tr><td>8</td><td>Authentication</td><td>Use AuthenticationStateProvider; Blazor supports cookie, JWT, OIDC auth</td></tr>
  <tr><td>9</td><td>Render modes (.NET 8)</td><td>@rendermode InteractiveServer / InteractiveWebAssembly / InteractiveAuto</td></tr>
  <tr><td>10</td><td>No direct DOM access</td><td>Don't manipulate DOM with JS directly — let Blazor manage it</td></tr>
</table>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

