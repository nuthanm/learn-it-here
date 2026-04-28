"""Blazor → Web Forms vs Blazor: URL-routed sub-page.

Reachable at `?section=blazor&sub=webforms-comparison` via the Learning Hub.
Navigation back to the Blazor overview is provided by the breadcrumb and the
left-rail "Overview" link, mirroring the GIT → Basics / Branching pattern.
"""

import streamlit as st

from components.content import (
    paragraph,
    section_intro,
    section_title,
    subsection,
)


def render():
    """Sub-page of Blazor: ASP.NET Web Forms Controls vs Blazor Equivalents."""

    section_title(
        "ASP.NET Web Forms Controls vs Blazor Equivalents",
        "Side-by-side mapping of common Web Forms server controls to their idiomatic Blazor equivalents.",
    )
    section_intro(
        "This page compares ASP.NET Web Forms server controls with their idiomatic equivalents "
        "in Blazor (Server, SSR, and WebAssembly). Where the implementation differs across "
        "Blazor hosting models, a Note is provided."
    )

    subsection("1. Basic Display & Text Controls")
    st.markdown(
        """
| Control in ASP.NET Web Forms | Same pattern in Blazor | Purpose of this control |
| --- | --- | --- |
| `<asp:Label>` | `<span>@Text</span>` or `<label>@Text</label>` | Render static or data-bound text on the page. |
| `<asp:Literal>` | `@Html` raw output via `MarkupString` (`@((MarkupString)html)`) | Render plain text or raw HTML without an extra wrapper element. |
| `<asp:HyperLink>` | `<a href="@Url">@Text</a>` or `<NavLink href="@Url">@Text</NavLink>` | Render a navigation link. |
| `<asp:Image>` | `<img src="@Src" alt="@Alt" />` | Render an image. |
| `<asp:Panel>` | `<div>...</div>` plus `@if (condition) { ... }` for conditional visibility | Group related markup; show/hide a region. |
| `<asp:PlaceHolder>` | `@ChildContent` (a `RenderFragment` parameter) | Reserve a slot to inject content dynamically. |
"""
    )
    paragraph(
        "Note (SSR vs Server vs WebAssembly): Pure markup output (Label, Literal, HyperLink, Image) "
        "behaves identically across hosting models because no interactivity is required."
    )

    subsection("2. Buttons & Action Controls")
    st.markdown(
        """
| Control in ASP.NET Web Forms | Same pattern in Blazor | Purpose of this control |
| --- | --- | --- |
| `<asp:Button>` | `<button type="button" @onclick="HandlerAsync">Text</button>` | Trigger a server-side action. |
| `<asp:LinkButton>` | `<button type="button" class="btn btn-link" @onclick="HandlerAsync">Text</button>` | Render a link that performs a postback action. |
| `<asp:ImageButton>` | `<button type="button" @onclick="HandlerAsync"><img src="..." /></button>` | A clickable image that triggers an action. |
"""
    )
    paragraph(
        "Note: Blazor Server — @onclick invokes the handler over the SignalR circuit. "
        "Blazor WebAssembly — @onclick runs the handler directly in the browser (no round trip). "
        "Blazor SSR (Static Server Rendering, .NET 8+) — @onclick does not work on a static "
        "server-rendered page. Use a <form> with a [SupplyParameterFromForm] model and OnPost-style "
        "handlers, or opt the component into interactivity via @rendermode InteractiveServer / "
        "InteractiveWebAssembly / InteractiveAuto."
    )

    subsection("3. Input Controls")
    st.markdown(
        """
| Control in ASP.NET Web Forms | Same pattern in Blazor | Purpose of this control |
| --- | --- | --- |
| `<asp:TextBox>` | `<input @bind="Value" />` or `<InputText @bind-Value="Model.Field" />` | Single-line text input. |
| `<asp:TextBox TextMode="MultiLine">` | `<textarea @bind="Value" />` or `<InputTextArea @bind-Value="..." />` | Multi-line text input. |
| `<asp:TextBox TextMode="Password">` | `<input type="password" @bind="Value" />` | Password input. |
| `<asp:CheckBox>` | `<input type="checkbox" @bind="IsChecked" />` or `<InputCheckbox @bind-Value="..." />` | Boolean toggle. |
| `<asp:RadioButton>` | `<input type="radio" name="g" value="A" @onchange="..." />` or `<InputRadioGroup>` + `<InputRadio>` | Single choice from group. |
| `<asp:DropDownList>` | `<select @bind="Selected"> <option ...> </select>` or `<InputSelect @bind-Value="...">` | Single selection from list. |
| `<asp:ListBox>` | `<select size="N" multiple @bind="Selected">` | Visible scrollable list (single/multi-select). |
| `<asp:CheckBoxList>` | `@foreach` rendering `<input type="checkbox">` items | Group of checkboxes bound to a list. |
| `<asp:RadioButtonList>` | `<InputRadioGroup>` with `<InputRadio>` per option | Group of radio buttons bound to a list. |
| `<asp:HiddenField>` | `<input type="hidden" @bind="Value" />` | Persist data without showing it. |
| `<asp:FileUpload>` | `<InputFile OnChange="OnFilesSelectedAsync" />` | File selection / upload. |
"""
    )
    paragraph(
        "Note: Blazor Server — uploaded file streaming via IBrowserFile flows over SignalR; "
        "increase MaximumReceiveMessageSize for large files. Blazor WebAssembly — files stay in "
        "the browser; you typically POST them to a Web API. Blazor SSR — two-way @bind requires "
        "interactivity; for purely static forms, use form POST with EditForm + [SupplyParameterFromForm]."
    )

    subsection("4. Validation Controls")
    st.markdown(
        """
| Control in ASP.NET Web Forms | Same pattern in Blazor | Purpose of this control |
| --- | --- | --- |
| `<asp:RequiredFieldValidator>` | `[Required]` data annotation + `<ValidationMessage>` | Ensure field is not empty. |
| `<asp:RegularExpressionValidator>` | `[RegularExpression(...)]` annotation | Pattern validation. |
| `<asp:RangeValidator>` | `[Range(min, max)]` annotation | Numeric / date range validation. |
| `<asp:CompareValidator>` | Custom `IValidatableObject` or `[Compare]` (for password confirm) | Compare two values. |
| `<asp:CustomValidator>` | Custom validator attribute or `EditContext.AddValidationMessage` | Arbitrary validation logic. |
| `<asp:ValidationSummary>` | `<ValidationSummary />` inside `<EditForm>` | Show all validation errors in one place. |
"""
    )
    paragraph(
        "Note: All validation in Blazor is built on EditForm + DataAnnotationsValidator. Behavior "
        "is the same across Server, SSR, and WebAssembly, but on Blazor SSR the validation runs "
        "on form POST (no live per-keystroke validation) unless the form is rendered interactively."
    )

    subsection("5. Data-Bound / List Controls")
    st.markdown(
        """
| Control in ASP.NET Web Forms | Same pattern in Blazor | Purpose of this control |
| --- | --- | --- |
| `<asp:GridView>` | `QuickGrid` (`Microsoft.AspNetCore.Components.QuickGrid`) or a manual `<table>` + `@foreach` | Tabular data with sorting/paging. |
| `<asp:DetailsView>` | Custom component rendering one record (`<dl>` or card layout) | Show one record's fields. |
| `<asp:FormView>` | Custom component with `EditForm` + template | Templated single-record edit. |
| `<asp:Repeater>` | `@foreach (var item in Items) { ... }` | Pure templated rendering of a list. |
| `<asp:DataList>` | `@foreach` with custom layout templates | Templated list with item layout. |
| `<asp:ListView>` | `@foreach` + `RenderFragment` templates / `Virtualize` | Templated list with paging support. |
| `<asp:Chart>` | Third-party (e.g., Syncfusion, Telerik, ChartJs.Blazor) | Render charts. |
"""
    )
    paragraph(
        "Note: Blazor WebAssembly — use <Virtualize> for very large lists to keep DOM small. "
        "Blazor Server — <Virtualize> works the same but each scroll fetch is a round trip over "
        "SignalR. QuickGrid with EntityFrameworkAdapter is server-only (needs DB access from the host)."
    )

    subsection("6. Navigation Controls")
    st.markdown(
        """
| Control in ASP.NET Web Forms | Same pattern in Blazor | Purpose of this control |
| --- | --- | --- |
| `<asp:Menu>` | Custom component rendering `<ul>` + `<NavLink>` (e.g., `NavMenu.razor`) | Site navigation menu. |
| `<asp:TreeView>` | Custom recursive component or third-party tree component | Hierarchical navigation. |
| `<asp:SiteMapPath>` (Breadcrumb) | Custom `Breadcrumb` component reading `NavigationManager.Uri` | Show current location in hierarchy. |
| `<asp:HyperLink>` / `Response.Redirect` | `<NavLink>` / `NavigationManager.NavigateTo("...")` | Navigate between pages. |
"""
    )
    paragraph(
        "Note: NavigationManager.NavigateTo triggers a full reload only when forceLoad: true is "
        "passed, or when navigating outside the Blazor app. In SSR, navigation between "
        "non-interactive pages is a normal browser navigation."
    )

    subsection("7. Login / Security Controls")
    st.markdown(
        """
| Control in ASP.NET Web Forms | Same pattern in Blazor | Purpose of this control |
| --- | --- | --- |
| `<asp:Login>` | Custom `EditForm` calling ASP.NET Core Identity (`SignInManager`) | Username/password login form. |
| `<asp:LoginView>` | `<AuthorizeView>` with `<Authorized>` / `<NotAuthorized>` | Show login/logout link based on auth state. |
| `<asp:LoginName>` | `<AuthorizeView>` → `@context.User.Identity?.Name` | Display current user name. |
| `<asp:LoginStatus>` | `<AuthorizeView>` with Login/Logout `<NavLink>` in each branch | Show login or logout link based on state. |
"""
    )
    paragraph(
        "Note: Blazor authentication uses AuthenticationStateProvider + the "
        "<CascadingAuthenticationState> + <AuthorizeView> pair. On Blazor Server identity flows "
        "over the SignalR circuit; on Blazor WebAssembly the client typically uses OIDC/JWT and "
        "calls a protected Web API; on Blazor SSR auth is enforced by the standard ASP.NET Core "
        "middleware on each request."
    )
