import CodeBlock from "@/components/CodeBlock";
import ContentTable from "@/components/ContentTable";

export default function DotNet() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>.NET</h2>
      <p className="text-sm mb-1" style={{ color: "var(--muted)" }}>
        Unified Microsoft development platform for APIs, web apps, background services, desktop, and cloud workloads.
      </p>
      <p className="text-sm mb-5" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        .NET gives you one SDK, one CLI, one runtime family, and a broad library ecosystem to build and deploy across platforms.
      </p>

      <h3 className="font-semibold text-sm mb-2" style={{ color: "var(--ink)" }}>Common templates</h3>
      <ContentTable
        headers={["Command", "Result"]}
        rows={[
          ["dotnet new webapi -n MyApi", "Create ASP.NET Core Web API project"],
          ["dotnet new mvc -n MyMvcApp", "Create MVC web app"],
          ["dotnet new blazorwasm -n MyBlazorClient", "Create Blazor WebAssembly app"],
          ["dotnet new classlib -n MyLibrary", "Create reusable class library"],
          ["dotnet new xunit -n MyTests", "Create xUnit test project"],
        ]}
      />

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>CLI essentials</h3>
      <ContentTable
        headers={["Command", "Purpose"]}
        rows={[
          ["dotnet restore", "Restore NuGet dependencies"],
          ["dotnet build", "Compile project/solution"],
          ["dotnet test", "Run unit/integration tests"],
          ["dotnet run", "Run current project"],
          ["dotnet publish -c Release", "Create deployable output"],
          ["dotnet add package <name>", "Add package reference"],
          ["dotnet list package", "List installed packages"],
        ]}
      />

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Dependency injection lifetimes</h3>
      <CodeBlock language="csharp">{`// Program.cs
builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.AddTransient<IEmailService, SmtpEmailService>();
builder.Services.AddSingleton<IConfigService, ConfigService>();`}</CodeBlock>
      <ContentTable
        headers={["Lifetime", "Behavior", "Typical use"]}
        rows={[
          ["Transient", "New instance each request", "Lightweight stateless services"],
          ["Scoped", "One instance per HTTP request", "Business services using DbContext"],
          ["Singleton", "One instance for application lifetime", "Caching/configuration services"],
        ]}
      />

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Release and deployment notes</h3>
      <ContentTable
        headers={["Mode", "When to choose"]}
        rows={[
          ["Framework-dependent", "Smaller package when target machines already have .NET runtime"],
          ["Self-contained", "Include runtime for controlled deployment environments"],
          ["Containerized", "Use Docker/Kubernetes for repeatable cloud deployments"],
          ["Native AOT (selected scenarios)", "Minimize cold-start and runtime footprint"],
        ]}
      />

      <p className="text-sm mt-4" style={{ color: "var(--muted)" }}>
        Further reading: {" "}
        <a href="https://learn.microsoft.com/en-us/dotnet/" target="_blank" rel="noopener noreferrer" className="font-semibold no-underline hover:underline" style={{ color: "var(--accent)" }}>Microsoft .NET docs</a>
      </p>
    </div>
  );
}
