import CodeBlock from "@/components/CodeBlock";
import ContentTable from "@/components/ContentTable";

export function BlazorOverview() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>Blazor</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Build interactive web UIs with C# instead of JavaScript. Blazor runs on WebAssembly
        (client) or on the server via SignalR — or both with Blazor Auto.
      </p>
      <ContentTable headers={["Hosting model", "Runs", "Best for"]} rows={[
        ["Blazor Server", "On the server (SignalR)", "Low-latency intranet apps, simple data access"],
        ["Blazor WASM", "In the browser (WebAssembly)", "Offline-capable SPAs, CDN deployment"],
        ["Blazor Auto", "Server first, then WASM", "Fast first load + eventual offline capability"],
      ]} />
    </div>
  );
}

export function WebFormsVsBlazor() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>Web Forms vs Blazor</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Migrating from ASP.NET Web Forms to Blazor? Here&apos;s a side-by-side comparison of concepts.
      </p>
      <ContentTable headers={["Web Forms concept", "Blazor equivalent"]} rows={[
        ["`.aspx` page", "`.razor` component"],
        ["Code-behind (`.aspx.cs`)", "Inline `@code { }` block or partial class"],
        ["PostBack", "Event handler (`@onclick`, `@onchange`)"],
        ["ViewState", "Component state (`private` fields / parameters)"],
        ["UpdatePanel", "Conditional render (`@if`, component re-render)"],
        ["Master Page", "Layout component (`MainLayout.razor`)"],
        ["User Control (`.ascx`)", "Child component (`.razor`)"],
        ["Session / Application state", "Cascading values, `IMemoryCache`, `ProtectedSessionStorage`"],
      ]} />
    </div>
  );
}

export function FluentUIBlazor() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>Fluent UI Blazor</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Microsoft&apos;s Fluent UI component library brings the Microsoft design system to Blazor.
      </p>
      <h3 className="font-semibold text-sm mb-2" style={{ color: "var(--ink)" }}>Setup</h3>
      <CodeBlock language="bash">{`dotnet add package Microsoft.FluentUI.AspNetCore.Components`}</CodeBlock>
      <h3 className="font-semibold text-sm mb-2 mt-4" style={{ color: "var(--ink)" }}>Register in Program.cs</h3>
      <CodeBlock language="csharp">{`builder.Services.AddFluentUIComponents();`}</CodeBlock>
      <h3 className="font-semibold text-sm mb-2 mt-4" style={{ color: "var(--ink)" }}>Example component</h3>
      <CodeBlock language="html">{`<FluentButton Appearance="Appearance.Accent" @onclick="Save">Save</FluentButton>
<FluentTextField @bind-Value="model.Name" Label="Full name" />`}</CodeBlock>
    </div>
  );
}

export function BlazorCQRS() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>CQRS Pattern with Blazor Auto</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        CQRS (Command Query Responsibility Segregation) separates read and write operations.
        Combined with MediatR, it keeps Blazor components thin and focused.
      </p>
      <h3 className="font-semibold text-sm mb-2" style={{ color: "var(--ink)" }}>Query example</h3>
      <CodeBlock language="csharp">{`public record GetOrdersQuery(int UserId) : IRequest<List<OrderDto>>;

public class GetOrdersHandler : IRequestHandler<GetOrdersQuery, List<OrderDto>>
{
    private readonly IOrderRepository _repo;
    public GetOrdersHandler(IOrderRepository repo) => _repo = repo;

    public Task<List<OrderDto>> Handle(GetOrdersQuery query, CancellationToken ct)
        => _repo.GetByUserAsync(query.UserId, ct);
}`}</CodeBlock>
      <h3 className="font-semibold text-sm mb-2 mt-4" style={{ color: "var(--ink)" }}>Blazor component</h3>
      <CodeBlock language="html">{`@inject IMediator Mediator

@if (orders is not null)
{
    <FluentDataGrid Items="@orders.AsQueryable()" />
}

@code {
    private List<OrderDto>? orders;
    protected override async Task OnInitializedAsync()
        => orders = await Mediator.Send(new GetOrdersQuery(UserId));
}`}</CodeBlock>
    </div>
  );
}

export function BlazorOracleEfCoreDapper() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>Oracle Data Access with EF Core and Dapper</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Use EF Core for CRUD and Dapper for complex raw queries — both connecting to Oracle.
      </p>
      <h3 className="font-semibold text-sm mb-2" style={{ color: "var(--ink)" }}>Setup</h3>
      <CodeBlock language="bash">{`dotnet add package Oracle.EntityFrameworkCore
dotnet add package Dapper`}</CodeBlock>
      <h3 className="font-semibold text-sm mb-2 mt-4" style={{ color: "var(--ink)" }}>DbContext registration</h3>
      <CodeBlock language="csharp">{`builder.Services.AddDbContext<AppDbContext>(opt =>
    opt.UseOracle(builder.Configuration.GetConnectionString("Oracle")));`}</CodeBlock>
      <h3 className="font-semibold text-sm mb-2 mt-4" style={{ color: "var(--ink)" }}>Dapper raw query</h3>
      <CodeBlock language="csharp">{`var orders = await connection.QueryAsync<Order>(
    "SELECT * FROM ORDERS WHERE CUSTOMER_ID = :Id",
    new { Id = customerId });`}</CodeBlock>
    </div>
  );
}
