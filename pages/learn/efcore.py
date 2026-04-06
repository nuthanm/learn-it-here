import streamlit as st


def render_efcore():
    # Overview
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🗄️ EF Core with Oracle — Overview</div>
  <div class="card-body">
<b>Entity Framework Core (EF Core)</b> is Microsoft's modern, open-source
object-relational mapper (ORM) for .NET. When targeting an <b>Oracle Database</b>,
you use the official <b>Oracle.EntityFrameworkCore</b> provider maintained by Oracle
Corporation.<br><br>
EF Core with Oracle supports Code-First migrations, LINQ queries, stored procedures,
sequences, and most EF Core features — with some Oracle-specific conventions that
every team member <em>must</em> follow to keep the codebase consistent and correct.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Real-world example — EF Core + Oracle
    st.markdown(
        """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🌍 Real-World Example — Building a Customer Orders System</div>
  <div class="card-body">
<b>Scenario:</b> You're building a .NET 8 web API for an e-commerce company.
Their database is Oracle 19c. You need to store <b>customers</b> and their <b>orders</b>.
Here's the complete journey from zero to working code — the way it's done on a real project.
<br><br>
<b>Step 1 — Install the Oracle EF Core package:</b>
<pre class="cmd-block">dotnet add package Oracle.EntityFrameworkCore</pre>
<b>Step 2 — Define your C# entity classes (plain objects — no Oracle knowledge needed here):</b>
<pre class="cmd-block">public class Customer
{
public long Id { get; set; }           // maps to Oracle COLUMN "ID"
public string FullName { get; set; }   // maps to "FULL_NAME"
public string Email { get; set; }      // maps to "EMAIL"
public ICollection&lt;Order&gt; Orders { get; set; }
}

public class Order
{
public long Id { get; set; }
public long CustomerId { get; set; }
public decimal TotalAmount { get; set; }
public DateTime OrderDate { get; set; }
public Customer Customer { get; set; }
}</pre>
<b>Step 3 — Configure the DbContext (this is where Oracle rules are applied):</b>
<pre class="cmd-block">public class AppDbContext : DbContext
{
public DbSet&lt;Customer&gt; Customers { get; set; }
public DbSet&lt;Order&gt; Orders { get; set; }

protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity&lt;Customer&gt;(b =&gt;
    {
        b.ToTable("CUSTOMERS");                        // Oracle table name MUST be UPPERCASE
        b.HasKey(e =&gt; e.Id);
        b.Property(e =&gt; e.Id)
         .HasColumnName("ID")
         .HasColumnType("NUMBER(19)")
         .UseHiLo("SEQ_CUSTOMERS");                    // Oracle sequence for auto-increment IDs
        b.Property(e =&gt; e.FullName)
         .HasColumnName("FULL_NAME")
         .HasColumnType("VARCHAR2(200)")
         .IsRequired();
        b.Property(e =&gt; e.Email)
         .HasColumnName("EMAIL")
         .HasColumnType("VARCHAR2(300)")
         .IsRequired();
    });

    modelBuilder.Entity&lt;Order&gt;(b =&gt;
    {
        b.ToTable("ORDERS");
        b.HasKey(e =&gt; e.Id);
        b.Property(e =&gt; e.Id)
         .HasColumnName("ID")
         .HasColumnType("NUMBER(19)")
         .UseHiLo("SEQ_ORDERS");
        b.Property(e =&gt; e.TotalAmount)
         .HasColumnName("TOTAL_AMOUNT")
         .HasColumnType("NUMBER(18,4)");               // Always specify precision for decimals
        b.Property(e =&gt; e.OrderDate)
         .HasColumnName("ORDER_DATE")
         .HasColumnType("TIMESTAMP");
        b.Property(e =&gt; e.CustomerId)
         .HasColumnName("CUSTOMER_ID")
         .HasColumnType("NUMBER(19)");
        b.HasOne(e =&gt; e.Customer)
         .WithMany(c =&gt; c.Orders)
         .HasForeignKey(e =&gt; e.CustomerId);
    });
}
}</pre>
<b>Step 4 — Create and apply the migration (this creates the Oracle tables):</b>
<pre class="cmd-block">dotnet ef migrations add CreateCustomersAndOrders
dotnet ef database update</pre>
EF Core generates the Oracle-compatible SQL and runs it. The tables <code>CUSTOMERS</code>
and <code>ORDERS</code> are created in Oracle — complete with sequences and foreign keys.
<br><br>
<b>Step 5 — Query data in your API controller (plain C# — EF handles the Oracle SQL):</b>
<pre class="cmd-block">// Get all orders for customer ID 42, newest first
var orders = await _context.Orders
.Where(o =&gt; o.CustomerId == 42)
.OrderByDescending(o =&gt; o.OrderDate)
.ToListAsync();   // In web APIs, always prefer async DB calls to avoid blocking request threads.

// Add a new customer
var newCustomer = new Customer { FullName = "Jane Smith", Email = "jane@shop.com" };
_context.Customers.Add(newCustomer);
await _context.SaveChangesAsync();  // EF uses SEQ_CUSTOMERS to generate the ID automatically</pre>
<b>Why Oracle-specific rules matter:</b> If you used the default lowercase table name
<code>customers</code> instead of <code>CUSTOMERS</code>, Oracle would throw
<em>"ORA-00942: table or view does not exist"</em> because Oracle's default behavior
is case-sensitive with uppercase names. Following the naming conventions above prevents
this class of runtime errors entirely.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Installation
    st.markdown(
        """<div class="content-card">
<div class="card-title">📦 NuGet Package Setup</div>
<div class="card-body">
  Install the Oracle EF Core provider that matches your EF Core version:
  <br><br>
  <b>Package Manager Console</b>
  <pre class="cmd-block">Install-Package Oracle.EntityFrameworkCore</pre>
  <b>.NET CLI</b>
  <pre class="cmd-block">dotnet add package Oracle.EntityFrameworkCore</pre>
  <b>Version alignment (mandatory standard):</b>
  <table class="shortcut-table">
<tr><th>EF Core Version</th><th>Oracle.EntityFrameworkCore</th></tr>
<tr><td>EF Core 9.x</td><td>9.x.x</td></tr>
<tr><td>EF Core 8.x (LTS)</td><td>8.x.x</td></tr>
<tr><td>EF Core 7.x</td><td>7.x.x</td></tr>
<tr><td>EF Core 6.x (LTS)</td><td>6.x.x</td></tr>
  </table>
  Always keep EF Core and the Oracle provider on the <b>same major version</b>.
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # Connection string
    st.markdown(
        """<div class="content-card">
<div class="card-title">🔌 Connection String &amp; DbContext Registration</div>
<div class="card-body">
  <b>appsettings.json</b>
  <pre class="cmd-block">{
  "ConnectionStrings": {
"OracleDb": "User Id=myuser;Password=mypass;Data Source=myhost:1521/myservice;"
  }
}</pre>
  <b>Program.cs / Startup.cs registration (standard)</b>
  <pre class="cmd-block">builder.Services.AddDbContext&lt;AppDbContext&gt;(options =&gt;
options.UseOracle(
    builder.Configuration.GetConnectionString("OracleDb"),
    o =&gt; o.UseOracleSQLCompatibility(OracleSQLCompatibility.DatabaseVersion19)));
</pre>
  <ul>
<li>Always call <code>UseOracleSQLCompatibility</code> and target the correct Oracle DB version.</li>
<li>Store connection strings in <b>app secrets / environment variables</b>, never in source control.</li>
  </ul>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # Naming conventions
    st.markdown(
        """<div class="content-card">
<div class="card-title">📐 Naming Conventions (Mandatory Standards)</div>
<div class="card-body">
  Oracle historically uses <b>UPPERCASE</b> object names. Failing to follow these conventions
  causes case-sensitivity errors or "ORA-00942: table or view does not exist" at runtime.
  <table class="shortcut-table">
<tr><th>Object</th><th>Convention</th><th>Example</th></tr>
<tr><td>Table names</td><td>SCREAMING_SNAKE_CASE</td><td><code>CUSTOMER_ORDERS</code></td></tr>
<tr><td>Column names</td><td>SCREAMING_SNAKE_CASE</td><td><code>ORDER_DATE</code></td></tr>
<tr><td>Primary key column</td><td><code>ID</code></td><td><code>ID NUMBER</code></td></tr>
<tr><td>Sequence names</td><td><code>SEQ_&lt;TABLE&gt;</code></td><td><code>SEQ_CUSTOMER_ORDERS</code></td></tr>
<tr><td>Index names</td><td><code>IX_&lt;TABLE&gt;_&lt;COLS&gt;</code></td><td><code>IX_ORDERS_DATE</code></td></tr>
<tr><td>Foreign key names</td><td><code>FK_&lt;TABLE&gt;_&lt;REF&gt;</code></td><td><code>FK_ORDERS_CUSTOMER</code></td></tr>
<tr><td>Schema (owner)</td><td>UPPERCASE</td><td><code>MYSCHEMA</code></td></tr>
  </table>
  <br>Configure globally in <b>OnModelCreating</b>:
  <pre class="cmd-block">protected override void OnModelCreating(ModelBuilder modelBuilder)
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
}</pre>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # Data types
    st.markdown(
        """<div class="content-card">
<div class="card-title">🔢 Oracle Data-Type Mapping Standards</div>
<div class="card-body">
  Always specify Oracle-native column types explicitly in Fluent API or Data Annotations to
  avoid provider defaults that may differ across environments.
  <table class="shortcut-table">
<tr><th>.NET Type</th><th>Oracle Column Type</th><th>Fluent API Example</th></tr>
<tr><td>int / long</td><td>NUMBER(10) / NUMBER(19)</td><td><code>.HasColumnType("NUMBER(10)")</code></td></tr>
<tr><td>decimal / double</td><td>NUMBER(p,s)</td><td><code>.HasColumnType("NUMBER(18,4)")</code></td></tr>
<tr><td>string (short)</td><td>VARCHAR2(n)</td><td><code>.HasColumnType("VARCHAR2(200)")</code></td></tr>
<tr><td>string (long)</td><td>CLOB</td><td><code>.HasColumnType("CLOB")</code></td></tr>
<tr><td>DateTime</td><td>TIMESTAMP</td><td><code>.HasColumnType("TIMESTAMP")</code></td></tr>
<tr><td>DateOnly</td><td>DATE</td><td><code>.HasColumnType("DATE")</code></td></tr>
<tr><td>bool</td><td>NUMBER(1) 0/1</td><td><code>.HasColumnType("NUMBER(1)")</code></td></tr>
<tr><td>Guid</td><td>RAW(16)</td><td><code>.HasColumnType("RAW(16)")</code></td></tr>
<tr><td>byte[]</td><td>BLOB</td><td><code>.HasColumnType("BLOB")</code></td></tr>
  </table>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # Sequences and IDs
    st.markdown(
        """<div class="content-card">
<div class="card-title">🔑 Primary Keys &amp; Sequences (Standard)</div>
<div class="card-body">
  Oracle does not support <code>IDENTITY</code> columns in all versions.
  Use <b>Sequences</b> for auto-generated numeric PKs — this is the team standard.
  <pre class="cmd-block">// Entity
public class Order
{
public long Id { get; set; }
// ...
}

// Fluent API in OnModelCreating
modelBuilder.Entity&lt;Order&gt;(b =&gt;
{
b.ToTable("ORDERS");
b.HasKey(e =&gt; e.Id);
b.Property(e =&gt; e.Id)
 .HasColumnName("ID")
 .HasColumnType("NUMBER(19)")
 .UseHiLo("SEQ_ORDERS");   // HiLo uses a sequence under the hood
});</pre>
  <ul>
<li>Prefer <b>HiLo</b> pattern (<code>UseHiLo</code>) over <code>UseSequence</code> for better insert performance.</li>
<li>Name every sequence <code>SEQ_&lt;TABLENAME&gt;</code>.</li>
<li>For <b>GUID</b> PKs use <code>RAW(16)</code> and set <code>ValueGeneratedOnAdd</code> with a client-side <code>Guid.NewGuid()</code> default.</li>
  </ul>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # Migrations
    st.markdown(
        """<div class="content-card">
<div class="card-title">🔄 Migrations — Standards &amp; Commands</div>
<div class="card-body">
  <table class="shortcut-table">
<tr><th>Task</th><th>Command</th></tr>
<tr><td>Add a new migration</td><td><code>dotnet ef migrations add &lt;Name&gt;</code></td></tr>
<tr><td>Apply migrations to DB</td><td><code>dotnet ef database update</code></td></tr>
<tr><td>Generate SQL script</td><td><code>dotnet ef migrations script --idempotent</code></td></tr>
<tr><td>Remove last migration</td><td><code>dotnet ef migrations remove</code></td></tr>
<tr><td>List migrations</td><td><code>dotnet ef migrations list</code></td></tr>
  </table>
  <br><b>Team Standards:</b>
  <ul>
<li>Always review the generated migration file before applying — Oracle SQL differs from SQL Server.</li>
<li>Use <code>--idempotent</code> scripts for DBA-applied deployments in Production.</li>
<li>Never auto-run <code>database update</code> in Production from application startup; use controlled scripts.</li>
<li>Keep migration names descriptive: <code>AddCustomerEmailIndex</code>, not <code>Migration1</code>.</li>
<li>Every migration must be peer-reviewed before merging to the main branch.</li>
  </ul>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # Stored Procedures
    st.markdown(
        """<div class="content-card">
<div class="card-title">⚙️ Stored Procedures &amp; Raw SQL</div>
<div class="card-body">
  <b>Calling a stored procedure:</b>
  <pre class="cmd-block">var result = await context.Database
.ExecuteSqlRawAsync(
    "BEGIN MY_SCHEMA.UPDATE_STATUS(:p_id, :p_status); END;",
    new OracleParameter("p_id", orderId),
    new OracleParameter("p_status", newStatus));
</pre>
  <b>Mapping a procedure result to an entity:</b>
  <pre class="cmd-block">var orders = await context.Orders
.FromSqlRaw("SELECT * FROM TABLE(MY_SCHEMA.GET_ORDERS(:p_cust))",
    new OracleParameter("p_cust", customerId))
.ToListAsync();
</pre>
  <b>Standards:</b>
  <ul>
<li>Always use <b>named parameters</b> (<code>:param_name</code>) — never positional.</li>
<li>Prefix every parameter binding with <code>:</code> (Oracle syntax, not <code>@</code>).</li>
<li>Use <code>OracleParameter</code> from <code>Oracle.ManagedDataAccess.Client</code> — never raw string interpolation (SQL injection risk).</li>
<li>Document stored procedure signatures in the same PR as the EF mapping.</li>
  </ul>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # Best practices
    st.markdown(
        """<div class="content-card">
<div class="card-title">✅ Best Practices Everyone Must Follow</div>
<div class="feature-grid">
  <div class="feature-pill">
<strong>🔠 Always Uppercase Names</strong>
<p>Configure table and column names as UPPERCASE in <code>OnModelCreating</code>. Never rely on default casing.</p>
  </div>
  <div class="feature-pill">
<strong>📌 Explicit Column Types</strong>
<p>Always specify Oracle column types in Fluent API. Never leave them implicit — defaults differ between providers.</p>
  </div>
  <div class="feature-pill">
<strong>🧪 Test Migrations Locally</strong>
<p>Run migrations against a local or dev Oracle instance before raising a PR. Attach the idempotent SQL script to the PR.</p>
  </div>
  <div class="feature-pill">
<strong>🚫 No Raw String Queries</strong>
<p>Always use parameterised queries (<code>FromSqlRaw</code> + <code>OracleParameter</code>). String interpolation in SQL is forbidden.</p>
  </div>
  <div class="feature-pill">
<strong>⏱️ Async All the Way</strong>
<p>Use <code>ToListAsync</code>, <code>FirstOrDefaultAsync</code>, <code>SaveChangesAsync</code>. Blocking calls on a DB thread pool are banned.</p>
  </div>
  <div class="feature-pill">
<strong>🧹 Dispose DbContext</strong>
<p>Always resolve <code>DbContext</code> via DI with scoped lifetime. Never create it with <code>new</code> manually.</p>
  </div>
  <div class="feature-pill">
<strong>📏 Schema Per Module</strong>
<p>Each bounded context or module uses its own Oracle schema. Cross-schema queries must be documented and approved.</p>
  </div>
  <div class="feature-pill">
<strong>🔒 Secrets Out of Source</strong>
<p>Oracle credentials belong in Azure Key Vault / environment secrets. Never hardcode in appsettings.json committed to Git.</p>
  </div>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # Quick-reference table
    st.markdown(
        """<div class="content-card">
<div class="card-title">📋 Quick-Reference Checklist</div>
<div class="card-body">
<table class="shortcut-table">
  <tr><th>#</th><th>Standard</th><th>Why It Matters</th></tr>
  <tr><td>1</td><td>Match Oracle.EntityFrameworkCore version to EF Core version</td><td>Prevents runtime incompatibility</td></tr>
  <tr><td>2</td><td>Use UPPERCASE table &amp; column names</td><td>Avoids ORA-00942 errors</td></tr>
  <tr><td>3</td><td>Specify Oracle column types explicitly</td><td>Data integrity &amp; portability</td></tr>
  <tr><td>4</td><td>Use HiLo sequences for numeric PKs</td><td>Reduces round-trips, improves insert speed</td></tr>
  <tr><td>5</td><td>Use named Oracle parameters (:name)</td><td>Security &amp; clarity</td></tr>
  <tr><td>6</td><td>Review migration SQL before applying</td><td>Oracle DDL differs from SQL Server</td></tr>
  <tr><td>7</td><td>Never auto-migrate in Production startup</td><td>Prevents accidental data loss</td></tr>
  <tr><td>8</td><td>Use scoped DbContext via DI</td><td>Prevents connection leaks</td></tr>
  <tr><td>9</td><td>All DB calls must be async</td><td>Scalability &amp; thread-pool health</td></tr>
  <tr><td>10</td><td>Store credentials in secrets/Key Vault</td><td>Security compliance</td></tr>
</table>
</div>
</div>""",
        unsafe_allow_html=True,
    )

