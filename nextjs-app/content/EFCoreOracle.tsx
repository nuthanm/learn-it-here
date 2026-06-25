import CodeBlock from "@/components/CodeBlock";
import ContentTable from "@/components/ContentTable";

export default function EFCoreOracle() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>EF Core + Oracle</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Entity Framework Core with the Oracle provider. Code-first migrations, DbContext setup,
        and common query patterns.
      </p>
      <h3 className="font-semibold text-sm mb-2" style={{ color: "var(--ink)" }}>Install packages</h3>
      <CodeBlock language="bash">{`dotnet add package Oracle.EntityFrameworkCore`}</CodeBlock>
      <h3 className="font-semibold text-sm mb-2 mt-4" style={{ color: "var(--ink)" }}>DbContext</h3>
      <CodeBlock language="csharp">{`public class AppDbContext : DbContext
{
    public DbSet<Customer> Customers => Set<Customer>();

    protected override void OnConfiguring(DbContextOptionsBuilder opts)
        => opts.UseOracle("Data Source=mydb;User Id=admin;******;");
}`}</CodeBlock>
      <h3 className="font-semibold text-sm mb-2 mt-4" style={{ color: "var(--ink)" }}>Common commands</h3>
      <ContentTable headers={["Command", "Purpose"]} rows={[
        ["dotnet ef migrations add Init", "Create initial migration"],
        ["dotnet ef database update", "Apply pending migrations"],
        ["dotnet ef migrations list", "List applied / pending migrations"],
        ["dotnet ef dbcontext scaffold …", "Scaffold DbContext from existing DB"],
      ]} />
    </div>
  );
}
