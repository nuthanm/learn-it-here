import CodeBlock from "@/components/CodeBlock";
import ContentTable from "@/components/ContentTable";

export default function EFCoreOracle() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>EF Core + Oracle</h2>
      <p className="text-sm mb-1" style={{ color: "var(--muted)" }}>
        Use Entity Framework Core with Oracle for maintainable data access, migrations, and query composition.
      </p>
      <p className="text-sm mb-5" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Many teams combine EF Core for domain CRUD and Dapper/raw SQL for tuned reporting or complex SQL paths.
      </p>

      <h3 className="font-semibold text-sm mb-2" style={{ color: "var(--ink)" }}>Initial setup</h3>
      <CodeBlock language="bash">{`dotnet add package Oracle.EntityFrameworkCore
dotnet add package Microsoft.EntityFrameworkCore.Design`}</CodeBlock>
      <CodeBlock language="csharp">{`builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseOracle(builder.Configuration.GetConnectionString("Oracle")));`}</CodeBlock>

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>DbContext example</h3>
      <CodeBlock language="csharp">{`public class AppDbContext : DbContext
{
    public DbSet<Customer> Customers => Set<Customer>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Customer>(entity =>
        {
            entity.ToTable("CUSTOMERS");
            entity.HasKey(x => x.Id);
            entity.Property(x => x.Name).HasMaxLength(150).IsRequired();
        });
    }
}`}</CodeBlock>

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Migration commands</h3>
      <ContentTable
        headers={["Command", "Purpose"]}
        rows={[
          ["dotnet ef migrations add Init", "Create migration snapshot and migration file"],
          ["dotnet ef database update", "Apply pending migrations"],
          ["dotnet ef migrations list", "List migration history"],
          ["dotnet ef dbcontext scaffold …", "Reverse-engineer from existing Oracle schema"],
        ]}
      />

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Oracle mapping considerations</h3>
      <ContentTable
        headers={["Concern", "Recommendation"]}
        rows={[
          ["Identifier casing", "Use explicit table/column names to avoid implicit casing issues"],
          ["String sizes", "Set `HasMaxLength` consistently for predictable schema"],
          ["Date/time", "Prefer explicit date/time types and timezone strategy"],
          ["Decimal precision", "Configure precision/scale explicitly for monetary values"],
          ["Large datasets", "Use pagination (`Skip/Take`) and projection (`Select`)"],
        ]}
      />

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>When to mix Dapper</h3>
      <CodeBlock language="csharp">{`var orders = await connection.QueryAsync<OrderDto>(
    "SELECT * FROM ORDERS WHERE CUSTOMER_ID = :Id",
    new { Id = customerId });`}</CodeBlock>
      <p className="text-sm" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Keep EF Core for transactional aggregate updates, and use Dapper for high-throughput
        read/reporting paths that benefit from handcrafted SQL.
      </p>
    </div>
  );
}
