import streamlit as st


def render_blazor_webforms_comparison():
    """Sub-page of Blazor: ASP.NET Web Forms Controls vs Blazor Equivalents."""

    # ── Back-to-parent button ────────────────────────────────────────────────
    if st.button("← Back to Blazor", key="blazor_subpage_back"):
        st.session_state.blazor_subpage = None
        st.rerun()

    st.markdown(
        """
<div class="content-card" style="border-left: 4px solid #512BD4;">
  <div class="card-title">📘 ASP.NET Web Forms Controls vs Blazor Equivalents</div>
  <div class="card-body">
This page provides a side-by-side comparison of common <b>ASP.NET Web Forms</b> server controls and
their idiomatic equivalents in <b>Blazor</b> (Server, SSR, and WebAssembly). Where the implementation
differs across Blazor hosting models, a <b>Note</b> is provided.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── 1. Basic Display & Text Controls ─────────────────────────────────────
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">1. Basic Display &amp; Text Controls</div>
  <div class="card-body">
<table class="shortcut-table">
  <tr><th>Control in ASP.NET Web Forms</th><th>Same pattern in Blazor</th><th>Purpose of this control</th></tr>
  <tr><td><code>&lt;asp:Label&gt;</code></td><td><code>&lt;span&gt;@Text&lt;/span&gt;</code> or <code>&lt;label&gt;@Text&lt;/label&gt;</code></td><td>Render static or data-bound text on the page.</td></tr>
  <tr><td><code>&lt;asp:Literal&gt;</code></td><td><code>@Html</code> raw output via <code>MarkupString</code> (<code>@((MarkupString)html)</code>)</td><td>Render plain text or raw HTML without an extra wrapper element.</td></tr>
  <tr><td><code>&lt;asp:HyperLink&gt;</code></td><td><code>&lt;a href="@Url"&gt;@Text&lt;/a&gt;</code> or <code>&lt;NavLink href="@Url"&gt;@Text&lt;/NavLink&gt;</code></td><td>Render a navigation link.</td></tr>
  <tr><td><code>&lt;asp:Image&gt;</code></td><td><code>&lt;img src="@Src" alt="@Alt" /&gt;</code></td><td>Render an image.</td></tr>
  <tr><td><code>&lt;asp:Panel&gt;</code></td><td><code>&lt;div&gt;...&lt;/div&gt;</code> plus <code>@if (condition) { ... }</code> for conditional visibility</td><td>Group related markup; show/hide a region.</td></tr>
  <tr><td><code>&lt;asp:PlaceHolder&gt;</code></td><td><code>@ChildContent</code> (a <code>RenderFragment</code> parameter)</td><td>Reserve a slot to inject content dynamically.</td></tr>
</table>
<br>
<b>Note (SSR vs Server vs WebAssembly):</b> Pure markup output (<code>Label</code>, <code>Literal</code>,
<code>HyperLink</code>, <code>Image</code>) behaves identically across hosting models because no
interactivity is required.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── 2. Buttons & Action Controls ─────────────────────────────────────────
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">2. Buttons &amp; Action Controls</div>
  <div class="card-body">
<table class="shortcut-table">
  <tr><th>Control in ASP.NET Web Forms</th><th>Same pattern in Blazor</th><th>Purpose of this control</th></tr>
  <tr><td><code>&lt;asp:Button&gt;</code></td><td><code>&lt;button type="button" @onclick="HandlerAsync"&gt;Text&lt;/button&gt;</code></td><td>Trigger a server-side action.</td></tr>
  <tr><td><code>&lt;asp:LinkButton&gt;</code></td><td><code>&lt;button type="button" class="btn btn-link" @onclick="HandlerAsync"&gt;Text&lt;/button&gt;</code></td><td>Render a link that performs a postback action.</td></tr>
  <tr><td><code>&lt;asp:ImageButton&gt;</code></td><td><code>&lt;button type="button" @onclick="HandlerAsync"&gt;&lt;img src="..." /&gt;&lt;/button&gt;</code></td><td>A clickable image that triggers an action.</td></tr>
</table>
<br>
<b>Note:</b><br>
🔹 <b>Blazor Server:</b> <code>@onclick</code> invokes the handler over the SignalR circuit.<br>
🔹 <b>Blazor WebAssembly:</b> <code>@onclick</code> runs the handler directly in the browser (no round trip).<br>
🔹 <b>Blazor SSR (Static Server Rendering, .NET 8+):</b> <code>@onclick</code> does <b>not</b> work on a
static server-rendered page. Use a <code>&lt;form&gt;</code> with an <code>[SupplyParameterFromForm]</code>
model and <code>OnPost</code>-style handlers, or opt the component into interactivity via
<code>@rendermode InteractiveServer</code> / <code>InteractiveWebAssembly</code> / <code>InteractiveAuto</code>.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── 3. Input Controls ────────────────────────────────────────────────────
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">3. Input Controls</div>
  <div class="card-body">
<table class="shortcut-table">
  <tr><th>Control in ASP.NET Web Forms</th><th>Same pattern in Blazor</th><th>Purpose of this control</th></tr>
  <tr><td><code>&lt;asp:TextBox&gt;</code></td><td><code>&lt;input @bind="Value" /&gt;</code> or <code>&lt;InputText @bind-Value="Model.Field" /&gt;</code></td><td>Single-line text input.</td></tr>
  <tr><td><code>&lt;asp:TextBox TextMode="MultiLine"&gt;</code></td><td><code>&lt;textarea @bind="Value" /&gt;</code> or <code>&lt;InputTextArea @bind-Value="..." /&gt;</code></td><td>Multi-line text input.</td></tr>
  <tr><td><code>&lt;asp:TextBox TextMode="Password"&gt;</code></td><td><code>&lt;input type="password" @bind="Value" /&gt;</code></td><td>Password input.</td></tr>
  <tr><td><code>&lt;asp:CheckBox&gt;</code></td><td><code>&lt;input type="checkbox" @bind="IsChecked" /&gt;</code> or <code>&lt;InputCheckbox @bind-Value="..." /&gt;</code></td><td>Boolean toggle.</td></tr>
  <tr><td><code>&lt;asp:RadioButton&gt;</code></td><td><code>&lt;input type="radio" name="g" value="A" @onchange="..." /&gt;</code> or <code>&lt;InputRadioGroup&gt;</code> + <code>&lt;InputRadio&gt;</code></td><td>Single choice from group.</td></tr>
  <tr><td><code>&lt;asp:DropDownList&gt;</code></td><td><code>&lt;select @bind="Selected"&gt; &lt;option ...&gt; &lt;/select&gt;</code> or <code>&lt;InputSelect @bind-Value="..."&gt;</code></td><td>Single selection from list.</td></tr>
  <tr><td><code>&lt;asp:ListBox&gt;</code></td><td><code>&lt;select size="N" multiple @bind="Selected"&gt;</code></td><td>Visible scrollable list (single/multi-select).</td></tr>
  <tr><td><code>&lt;asp:CheckBoxList&gt;</code></td><td><code>@foreach</code> rendering <code>&lt;input type="checkbox"&gt;</code> items</td><td>Group of checkboxes bound to a list.</td></tr>
  <tr><td><code>&lt;asp:RadioButtonList&gt;</code></td><td><code>&lt;InputRadioGroup&gt;</code> with <code>&lt;InputRadio&gt;</code> per option</td><td>Group of radio buttons bound to a list.</td></tr>
  <tr><td><code>&lt;asp:HiddenField&gt;</code></td><td><code>&lt;input type="hidden" @bind="Value" /&gt;</code></td><td>Persist data without showing it.</td></tr>
  <tr><td><code>&lt;asp:FileUpload&gt;</code></td><td><code>&lt;InputFile OnChange="OnFilesSelectedAsync" /&gt;</code></td><td>File selection / upload.</td></tr>
</table>
<br>
<b>Note:</b><br>
🔹 <b>Blazor Server:</b> Uploaded file streaming via <code>IBrowserFile</code> flows over SignalR —
increase <code>MaximumReceiveMessageSize</code> for large files.<br>
🔹 <b>Blazor WebAssembly:</b> Files stay in the browser; you typically <code>POST</code> them to a Web API.<br>
🔹 <b>Blazor SSR:</b> Two-way <code>@bind</code> requires interactivity; for purely static forms, use form
<code>POST</code> with <code>EditForm</code> + <code>[SupplyParameterFromForm]</code>.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── 4. Validation Controls ───────────────────────────────────────────────
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">4. Validation Controls</div>
  <div class="card-body">
<table class="shortcut-table">
  <tr><th>Control in ASP.NET Web Forms</th><th>Same pattern in Blazor</th><th>Purpose of this control</th></tr>
  <tr><td><code>&lt;asp:RequiredFieldValidator&gt;</code></td><td><code>[Required]</code> data annotation + <code>&lt;ValidationMessage&gt;</code></td><td>Ensure field is not empty.</td></tr>
  <tr><td><code>&lt;asp:RegularExpressionValidator&gt;</code></td><td><code>[RegularExpression(...)]</code> annotation</td><td>Pattern validation.</td></tr>
  <tr><td><code>&lt;asp:RangeValidator&gt;</code></td><td><code>[Range(min, max)]</code> annotation</td><td>Numeric / date range validation.</td></tr>
  <tr><td><code>&lt;asp:CompareValidator&gt;</code></td><td>Custom <code>IValidatableObject</code> or <code>[Compare]</code> (for password confirm)</td><td>Compare two values.</td></tr>
  <tr><td><code>&lt;asp:CustomValidator&gt;</code></td><td>Custom validator attribute or <code>EditContext.AddValidationMessage</code></td><td>Arbitrary validation logic.</td></tr>
  <tr><td><code>&lt;asp:ValidationSummary&gt;</code></td><td><code>&lt;ValidationSummary /&gt;</code> inside <code>&lt;EditForm&gt;</code></td><td>Show all validation errors in one place.</td></tr>
</table>
<br>
<b>Note:</b> All validation in Blazor is built on <code>EditForm</code> + <code>DataAnnotationsValidator</code>.
Behavior is the same across Server, SSR, and WebAssembly, but on <b>Blazor SSR</b> the validation runs on
form <code>POST</code> (no live per-keystroke validation) unless the form is rendered interactively.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── 5. Data-Bound / List Controls ────────────────────────────────────────
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">5. Data-Bound / List Controls</div>
  <div class="card-body">
<table class="shortcut-table">
  <tr><th>Control in ASP.NET Web Forms</th><th>Same pattern in Blazor</th><th>Purpose of this control</th></tr>
  <tr><td><code>&lt;asp:GridView&gt;</code></td><td><code>QuickGrid</code> (<code>Microsoft.AspNetCore.Components.QuickGrid</code>) or a manual <code>&lt;table&gt;</code> + <code>@foreach</code></td><td>Tabular data with sorting/paging.</td></tr>
  <tr><td><code>&lt;asp:DetailsView&gt;</code></td><td>Custom component rendering one record (<code>&lt;dl&gt;</code> or card layout)</td><td>Show one record's fields.</td></tr>
  <tr><td><code>&lt;asp:FormView&gt;</code></td><td>Custom component with <code>EditForm</code> + template</td><td>Templated single-record edit.</td></tr>
  <tr><td><code>&lt;asp:Repeater&gt;</code></td><td><code>@foreach (var item in Items) { ... }</code></td><td>Pure templated rendering of a list.</td></tr>
  <tr><td><code>&lt;asp:DataList&gt;</code></td><td><code>@foreach</code> with custom layout templates</td><td>Templated list with item layout.</td></tr>
  <tr><td><code>&lt;asp:ListView&gt;</code></td><td><code>@foreach</code> + <code>RenderFragment</code> templates / <code>Virtualize</code></td><td>Templated list with paging support.</td></tr>
  <tr><td><code>&lt;asp:Chart&gt;</code></td><td>Third-party (e.g., Syncfusion, Telerik, ChartJs.Blazor)</td><td>Render charts.</td></tr>
</table>
<br>
<b>Note:</b><br>
🔹 <b>Blazor WebAssembly:</b> Use <code>&lt;Virtualize&gt;</code> for very large lists to keep DOM small.<br>
🔹 <b>Blazor Server:</b> <code>&lt;Virtualize&gt;</code> works the same but each scroll fetch is a round trip over SignalR.<br>
🔹 <b>QuickGrid</b> with <code>EntityFrameworkAdapter</code> is server-only (needs DB access from the host).
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── 6. Navigation Controls ───────────────────────────────────────────────
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">6. Navigation Controls</div>
  <div class="card-body">
<table class="shortcut-table">
  <tr><th>Control in ASP.NET Web Forms</th><th>Same pattern in Blazor</th><th>Purpose of this control</th></tr>
  <tr><td><code>&lt;asp:Menu&gt;</code></td><td>Custom component rendering <code>&lt;ul&gt;</code> + <code>&lt;NavLink&gt;</code> (e.g., <code>NavMenu.razor</code>)</td><td>Site navigation menu.</td></tr>
  <tr><td><code>&lt;asp:TreeView&gt;</code></td><td>Custom recursive component or third-party tree component</td><td>Hierarchical navigation.</td></tr>
  <tr><td><code>&lt;asp:SiteMapPath&gt;</code> (Breadcrumb)</td><td>Custom <code>Breadcrumb</code> component reading <code>NavigationManager.Uri</code></td><td>Show current location in hierarchy.</td></tr>
  <tr><td><code>&lt;asp:HyperLink&gt;</code> / <code>Response.Redirect</code></td><td><code>&lt;NavLink&gt;</code> / <code>NavigationManager.NavigateTo("...")</code></td><td>Navigate between pages.</td></tr>
</table>
<br>
<b>Note:</b> <code>NavigationManager.NavigateTo</code> triggers a full reload only when
<code>forceLoad: true</code> is passed, or when navigating outside the Blazor app. In <b>SSR</b>,
navigation between non-interactive pages is a normal browser navigation.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── 7. Login / Security Controls ─────────────────────────────────────────
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">7. Login / Security Controls</div>
  <div class="card-body">
<table class="shortcut-table">
  <tr><th>Control in ASP.NET Web Forms</th><th>Same pattern in Blazor</th><th>Purpose of this control</th></tr>
  <tr><td><code>&lt;asp:Login&gt;</code></td><td>Custom <code>EditForm</code> calling ASP.NET Core Identity (<code>SignInManager</code>)</td><td>Username/password login form.</td></tr>
  <tr><td><code>&lt;asp:LoginView&gt;</code></td><td><code>&lt;AuthorizeView&gt;</code> with <code>&lt;Authorized&gt;</code> / <code>&lt;NotAuthorized&gt;</code></td><td>Show login/logout link based on auth state.</td></tr>
  <tr><td><code>&lt;asp:LoginName&gt;</code></td><td><code>&lt;AuthorizeView&gt;</code> → <code>@context.User.Identity?.Name</code></td><td>Display current user name.</td></tr>
  <tr><td><code>&lt;asp:LoginStatus&gt;</code></td><td><code>&lt;AuthorizeView&gt;</code> with Login/Logout <code>&lt;NavLink&gt;</code> in each branch</td><td>Show login or logout link based on state.</td></tr>
</table>
<br>
<b>Note:</b> Blazor authentication uses <code>AuthenticationStateProvider</code> + the
<code>&lt;CascadingAuthenticationState&gt;</code> + <code>&lt;AuthorizeView&gt;</code> pair. On
<b>Blazor Server</b> identity flows over the SignalR circuit; on <b>Blazor WebAssembly</b> the
client typically uses OIDC/JWT and calls a protected Web API; on <b>Blazor SSR</b> auth is enforced by
the standard ASP.NET Core middleware on each request.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── Bottom back button for convenience ───────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Blazor", key="blazor_subpage_back_bottom"):
        st.session_state.blazor_subpage = None
        st.rerun()
