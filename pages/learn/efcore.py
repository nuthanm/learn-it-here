"""EF Core with Oracle — minimal-layout content page."""

import streamlit as st

from components.content import (
    code_block,
    link_list,
    paragraph,
    section_intro,
    section_title,
    subsection,
)


def render_efcore():
    section_title(
        "EF Core with Oracle",
        "Practical standards for using Entity Framework Core against an Oracle database.",
    )
    section_intro(
        "Entity Framework Core (EF Core) is Microsoft's modern, open-source ORM for .NET. "
        "When targeting an Oracle Database, you use the official Oracle.EntityFrameworkCore "
        "provider maintained by Oracle Corporation."
    )

    subsection("Overview")
    paragraph(
        "EF Core with Oracle supports Code-First migrations, LINQ queries, stored procedures, "
        "sequences, and most EF Core features — with some Oracle-specific conventions that "
        "every team member must follow to keep the codebase consistent and correct."
    )

    subsection("Real-world example — building a Customer Orders system")
    paragraph(
        "Scenario: you're building a .NET 8 web API for an e-commerce company. Their database "
        "is Oracle 19c. You need to store customers and their orders. Here's the complete "
        "journey from zero to working code — the way it's done on a real project."
    )

    paragraph("Step 1 — Install the Oracle EF Core package:")
    code_block("dotnet add package Oracle.EntityFrameworkCore", language="bash")

    paragraph("Step 2 — Define your C# entity classes (plain objects — no Oracle knowledge needed here):")
    code_block(
        """public class Customer
{
    public long Id { get; set; }           // maps to Oracle COLUMN "ID"
    public string FullName { get; set; }   // maps to "FULL_NAME"
    public string Email { get; set; }      // maps to "EMAIL"
    public ICollection<Order> Orders { get; set; }
}

public class Order
{
    public long Id { get; set; }
    public long CustomerId { get; set; }
    public decimal TotalAmount { get; set; }
    public DateTime OrderDate { get; set; }
    public Customer Customer { get; set; }
}""",
        language="csharp",
    )

    paragraph("Step 3 — Configure the DbContext (this is where Oracle rules are applied):")
    code_block(
        """public class AppDbContext : DbContext
{
    public DbSet<Customer> Customers { get; set; }
    public DbSet<Order> Orders { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Customer>(b =>
        {
            b.ToTable("CUSTOMERS");                        // Oracle table name MUST be UPPERCASE
            b.HasKey(e => e.Id);
            b.Property(e => e.Id)
             .HasColumnName("ID")
             .HasColumnType("NUMBER(19)")
             .UseHiLo("SEQ_CUSTOMERS");                    // Oracle sequence for auto-increment IDs
            b.Property(e => e.FullName)
             .HasColumnName("FULL_NAME")
             .HasColumnType("VARCHAR2(200)")
             .IsRequired();
            b.Property(e => e.Email)
             .HasColumnName("EMAIL")
             .HasColumnType("VARCHAR2(300)")
             .IsRequired();
        });

        modelBuilder.Entity<Order>(b =>
        {
            b.ToTable("ORDERS");
            b.HasKey(e => e.Id);
            b.Property(e => e.Id)
             .HasColumnName("ID")
             .HasColumnType("NUMBER(19)")
             .UseHiLo("SEQ_ORDERS");
            b.Property(e => e.TotalAmount)
             .HasColumnName("TOTAL_AMOUNT")
             .HasColumnType("NUMBER(18,4)");               // Always specify precision for decimals
            b.Property(e => e.OrderDate)
             .HasColumnName("ORDER_DATE")
             .HasColumnType("TIMESTAMP");
            b.Property(e => e.CustomerId)
             .HasColumnName("CUSTOMER_ID")
             .HasColumnType("NUMBER(19)");
            b.HasOne(e => e.Customer)
             .WithMany(c => c.Orders)
             .HasForeignKey(e => e.CustomerId);
        });
    }
}""",
        language="csharp",
    )

    paragraph("Step 4 — Create and apply the migration (this creates the Oracle tables):")
    code_block(
        "dotnet ef migrations add CreateCustomersAndOrders\ndotnet ef database update",
        language="bash",
    )
    paragraph(
        "EF Core generates the Oracle-compatible SQL and runs it. The tables CUSTOMERS and "
        "ORDERS are created in Oracle — complete with sequences and foreign keys."
    )

    paragraph("Step 5 — Query data in your API controller (plain C# — EF handles the Oracle SQL):")
    code_block(
        """// Get all orders for customer ID 42, newest first
var orders = await _context.Orders
    .Where(o => o.CustomerId == 42)
    .OrderByDescending(o => o.OrderDate)
    .ToListAsync();   // In web APIs, always prefer async DB calls to avoid blocking request threads.

// Add a new customer
var newCustomer = new Customer { FullName = "Jane Smith", Email = "jane@shop.com" };
_context.Customers.Add(newCustomer);
await _context.SaveChangesAsync();  // EF uses SEQ_CUSTOMERS to generate the ID automatically""",
        language="csharp",
    )
    paragraph(
        "Why Oracle-specific rules matter: if you used the default lowercase table name "
        "\"customers\" instead of \"CUSTOMERS\", Oracle would throw "
        "\"ORA-00942: table or view does not exist\" because Oracle's default behavior is "
        "case-sensitive with uppercase names. Following the naming conventions above prevents "
        "this class of runtime errors entirely."
    )

    subsection("NuGet package setup")
    paragraph("Install the Oracle EF Core provider that matches your EF Core version.")
    paragraph("Package Manager Console:")
    code_block("Install-Package Oracle.EntityFrameworkCore", language="powershell")
    paragraph(".NET CLI:")
    code_block("dotnet add package Oracle.EntityFrameworkCore", language="bash")

    paragraph("Version alignment (mandatory standard):")
    st.markdown(
        """| EF Core Version | Oracle.EntityFrameworkCore |
| --- | --- |
| EF Core 9.x | 9.x.x |
| EF Core 8.x (LTS) | 8.x.x |
| EF Core 7.x | 7.x.x |
| EF Core 6.x (LTS) | 6.x.x |"""
    )
    paragraph("Always keep EF Core and the Oracle provider on the same major version.")

    subsection("Connection string and DbContext registration")
    paragraph("appsettings.json:")
    code_block(
        """{
  "ConnectionStrings": {
    "OracleDb": "User Id=myuser;Password=mypass;Data Source=myhost:1521/myservice;"
  }
}""",
        language="json",
    )
    paragraph("Program.cs / Startup.cs registration (standard):")
    code_block(
        """builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseOracle(
        builder.Configuration.GetConnectionString("OracleDb"),
        o => o.UseOracleSQLCompatibility(OracleSQLCompatibility.DatabaseVersion19)));""",
        language="csharp",
    )
    paragraph(
        "Always call UseOracleSQLCompatibility and target the correct Oracle DB version. "
        "Store connection strings in app secrets or environment variables, never in source control."
    )

    subsection("Naming conventions (mandatory standards)")
    paragraph(
        "Oracle historically uses UPPERCASE object names. Failing to follow these conventions "
        "causes case-sensitivity errors or \"ORA-00942: table or view does not exist\" at runtime."
    )
    st.markdown(
        """| Object | Convention | Example |
| --- | --- | --- |
| Table names | SCREAMING_SNAKE_CASE | `CUSTOMER_ORDERS` |
| Column names | SCREAMING_SNAKE_CASE | `ORDER_DATE` |
| Primary key column | `ID` | `ID NUMBER` |
| Sequence names | `SEQ_<TABLE>` | `SEQ_CUSTOMER_ORDERS` |
| Index names | `IX_<TABLE>_<COLS>` | `IX_ORDERS_DATE` |
| Foreign key names | `FK_<TABLE>_<REF>` | `FK_ORDERS_CUSTOMER` |
| Schema (owner) | UPPERCASE | `MYSCHEMA` |"""
    )
    paragraph("Configure globally in OnModelCreating:")
    code_block(
        """protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    // Apply UPPERCASE naming to every entity
    foreach (var entity in modelBuilder.Model.GetEntityTypes())
    {
        entity.SetTableName(entity.GetTableName()!.ToUpper());
        foreach (var prop in entity.GetProperties())
        {
            var colName = prop.GetColumnName();
            if (colName != null)
                prop.SetColumnName(colName.ToUpper());
        }
    }
}""",
        language="csharp",
    )

    subsection("Oracle data-type mapping standards")
    paragraph(
        "Always specify Oracle-native column types explicitly in Fluent API or Data Annotations "
        "to avoid provider defaults that may differ across environments."
    )
    st.markdown(
        """| .NET Type | Oracle Column Type | Fluent API Example |
| --- | --- | --- |
| int / long | NUMBER(10) / NUMBER(19) | `.HasColumnType("NUMBER(10)")` |
| decimal / double | NUMBER(p,s) | `.HasColumnType("NUMBER(18,4)")` |
| string (short) | VARCHAR2(n) | `.HasColumnType("VARCHAR2(200)")` |
| string (long) | CLOB | `.HasColumnType("CLOB")` |
| DateTime | TIMESTAMP | `.HasColumnType("TIMESTAMP")` |
| DateOnly | DATE | `.HasColumnType("DATE")` |
| bool | NUMBER(1) 0/1 | `.HasColumnType("NUMBER(1)")` |
| Guid | RAW(16) | `.HasColumnType("RAW(16)")` |
| byte[] | BLOB | `.HasColumnType("BLOB")` |"""
    )

    subsection("Primary keys and sequences (standard)")
    paragraph(
        "Oracle does not support IDENTITY columns in all versions. Use Sequences for "
        "auto-generated numeric PKs — this is the team standard."
    )
    code_block(
        """// Entity
public class Order
{
    public long Id { get; set; }
    // ...
}

// Fluent API in OnModelCreating
modelBuilder.Entity<Order>(b =>
{
    b.ToTable("ORDERS");
    b.HasKey(e => e.Id);
    b.Property(e => e.Id)
     .HasColumnName("ID")
     .HasColumnType("NUMBER(19)")
     .UseHiLo("SEQ_ORDERS");   // HiLo uses a sequence under the hood
});""",
        language="csharp",
    )
    paragraph(
        "Prefer the HiLo pattern (UseHiLo) over UseSequence for better insert performance. "
        "Name every sequence SEQ_<TABLENAME>. For GUID PKs use RAW(16) and set "
        "ValueGeneratedOnAdd with a client-side Guid.NewGuid() default."
    )

    subsection("Migrations — standards and commands")
    st.markdown(
        """| Task | Command |
| --- | --- |
| Add a new migration | `dotnet ef migrations add <Name>` |
| Apply migrations to DB | `dotnet ef database update` |
| Generate SQL script | `dotnet ef migrations script --idempotent` |
| Remove last migration | `dotnet ef migrations remove` |
| List migrations | `dotnet ef migrations list` |"""
    )
    paragraph("Team standards:")
    paragraph(
        "Always review the generated migration file before applying — Oracle SQL differs from SQL Server."
    )
    paragraph("Use --idempotent scripts for DBA-applied deployments in Production.")
    paragraph(
        "Never auto-run database update in Production from application startup; use controlled scripts."
    )
    paragraph("Keep migration names descriptive: AddCustomerEmailIndex, not Migration1.")
    paragraph("Every migration must be peer-reviewed before merging to the main branch.")

    subsection("Stored procedures and raw SQL")
    paragraph("Calling a stored procedure:")
    code_block(
        """var result = await context.Database
    .ExecuteSqlRawAsync(
        "BEGIN MY_SCHEMA.UPDATE_STATUS(:p_id, :p_status); END;",
        new OracleParameter("p_id", orderId),
        new OracleParameter("p_status", newStatus));""",
        language="csharp",
    )
    paragraph("Mapping a procedure result to an entity:")
    code_block(
        """var orders = await context.Orders
    .FromSqlRaw("SELECT * FROM TABLE(MY_SCHEMA.GET_ORDERS(:p_cust))",
        new OracleParameter("p_cust", customerId))
    .ToListAsync();""",
        language="csharp",
    )
    paragraph("Standards:")
    paragraph("Always use named parameters (:param_name) — never positional.")
    paragraph("Prefix every parameter binding with : (Oracle syntax, not @).")
    paragraph(
        "Use OracleParameter from Oracle.ManagedDataAccess.Client — never raw string "
        "interpolation (SQL injection risk)."
    )
    paragraph("Document stored procedure signatures in the same PR as the EF mapping.")

    subsection("Best practices everyone must follow")

    subsection("Always uppercase names")
    paragraph(
        "Configure table and column names as UPPERCASE in OnModelCreating. Never rely on default casing."
    )

    subsection("Explicit column types")
    paragraph(
        "Always specify Oracle column types in Fluent API. Never leave them implicit — "
        "defaults differ between providers."
    )

    subsection("Test migrations locally")
    paragraph(
        "Run migrations against a local or dev Oracle instance before raising a PR. "
        "Attach the idempotent SQL script to the PR."
    )

    subsection("No raw string queries")
    paragraph(
        "Always use parameterised queries (FromSqlRaw + OracleParameter). String "
        "interpolation in SQL is forbidden."
    )

    subsection("Async all the way")
    paragraph(
        "Use ToListAsync, FirstOrDefaultAsync, SaveChangesAsync. Blocking calls on a DB "
        "thread pool are banned."
    )

    subsection("Dispose DbContext")
    paragraph(
        "Always resolve DbContext via DI with scoped lifetime. Never create it with new manually."
    )

    subsection("Schema per module")
    paragraph(
        "Each bounded context or module uses its own Oracle schema. Cross-schema queries "
        "must be documented and approved."
    )

    subsection("Secrets out of source")
    paragraph(
        "Oracle credentials belong in Azure Key Vault or environment secrets. Never hardcode "
        "in appsettings.json committed to Git."
    )

    subsection("Quick-reference checklist")
    st.markdown(
        """| # | Standard | Why It Matters |
| --- | --- | --- |
| 1 | Match Oracle.EntityFrameworkCore version to EF Core version | Prevents runtime incompatibility |
| 2 | Use UPPERCASE table & column names | Avoids ORA-00942 errors |
| 3 | Specify Oracle column types explicitly | Data integrity & portability |
| 4 | Use HiLo sequences for numeric PKs | Reduces round-trips, improves insert speed |
| 5 | Use named Oracle parameters (:name) | Security & clarity |
| 6 | Review migration SQL before applying | Oracle DDL differs from SQL Server |
| 7 | Never auto-migrate in Production startup | Prevents accidental data loss |
| 8 | Use scoped DbContext via DI | Prevents connection leaks |
| 9 | All DB calls must be async | Scalability & thread-pool health |
| 10 | Store credentials in secrets/Key Vault | Security compliance |"""
    )
