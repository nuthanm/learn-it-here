import CodeBlock from "@/components/CodeBlock";
import ContentTable from "@/components/ContentTable";

export default function DotNet() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>.NET</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Core .NET CLI commands, project templates, and dependency injection patterns.
      </p>
      <h3 className="font-semibold text-sm mb-2" style={{ color: "var(--ink)" }}>CLI essentials</h3>
      <ContentTable headers={["Command", "What it does"]} rows={[
        ["dotnet new webapi -n MyApi", "Create a new Web API project"],
        ["dotnet new blazorwasm -n MyApp", "Create a Blazor WASM project"],
        ["dotnet build", "Compile the project"],
        ["dotnet run", "Run the project"],
        ["dotnet test", "Execute tests"],
        ["dotnet publish -c Release", "Publish for deployment"],
        ["dotnet add package <name>", "Add a NuGet package"],
        ["dotnet list package", "List installed packages"],
      ]} />
      <h3 className="font-semibold text-sm mb-2 mt-4" style={{ color: "var(--ink)" }}>Dependency injection</h3>
      <CodeBlock language="csharp">{`// Program.cs
builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.AddTransient<IEmailService, SmtpEmailService>();
builder.Services.AddSingleton<IConfigService, ConfigService>();`}</CodeBlock>
    </div>
  );
}
