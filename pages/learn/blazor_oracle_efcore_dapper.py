"""Blazor sub-page: Oracle Data Access with EF Core and Dapper."""

import streamlit as st

from components.content import (
    code_block,
    paragraph,
    section_intro,
    section_title,
    subsection,
)


def render_blazor_oracle_efcore_dapper():
    """Sub-page of Blazor: Oracle Data Access with EF Core and Dapper."""

    section_title(
        "Oracle Data Access with EF Core and Dapper",
        "EF Core + Repository Pattern for writes. Dapper + Raw SQL for reads.",
    )
    section_intro(
        "This document explains how to use Oracle Database in a .NET application "
        "with two different data access approaches: EF Core + Repository Pattern for "
        "write operations, and Dapper + Raw SQL for read operations. This approach is "
        "beginner-friendly, clean, scalable, and commonly used in real-world enterprise "
        "applications."
    )

    # ── 1. Big Picture ───────────────────────────────────────────────────────
    subsection("1. Big Picture")
    paragraph(
        "In many applications, we perform two main types of database operations:"
    )
    paragraph("**Write operations**")
    paragraph("- Create data")
    paragraph("- Update data")
    paragraph("- Delete data")
    paragraph("**Read operations**")
    paragraph("- Show lists")
    paragraph("- Search data")
    paragraph("- Generate reports")
    paragraph("- Display dashboard data")
    paragraph(
        "Instead of using the same tool for everything, we can use the best tool for each job."
    )
    st.markdown(
        """
| Operation Type | Recommended Tool | Why |
|---|---|---|
| Create, Update, Delete | EF Core | Works well with domain entities and change tracking |
| Read, Reports, Lists | Dapper | Fast, flexible, and works well with raw SQL |
"""
    )

    # ── 2. Technology Stack ──────────────────────────────────────────────────
    subsection("2. Technology Stack")
    paragraph("The application uses:")
    paragraph("- **Oracle Database** as the database")
    paragraph("- **EF Core** for commands/write operations")
    paragraph("- **Dapper** for queries/read operations")
    paragraph("- **Repository Pattern** for clean write logic")
    paragraph("- **Raw SQL** for optimized read logic")

    # ── 3. Why EF Core for Write Operations? ────────────────────────────────
    subsection("3. Why Use EF Core for Write Operations?")
    paragraph(
        "EF Core is useful when we are working with business/domain entities."
    )
    paragraph("Examples of write operations:")
    paragraph("- Add a new student")
    paragraph("- Update student details")
    paragraph("- Delete a record")
    paragraph("- Save transportation event history")
    paragraph("EF Core helps with:")
    paragraph("- Tracking entity changes")
    paragraph("- Managing relationships between tables")
    paragraph("- Validating domain models")
    paragraph("- Writing cleaner object-oriented code")
    paragraph("**Example Write Flow**")
    code_block(
        """User submits form
        ↓
Application creates or updates domain entity
        ↓
Repository uses EF Core
        ↓
EF Core saves changes to Oracle database""",
        language="text",
    )

    # ── 4. Why Dapper for Read Operations? ──────────────────────────────────
    subsection("4. Why Use Dapper for Read Operations?")
    paragraph(
        "Dapper is useful when we want fast and flexible read queries."
    )
    paragraph("Examples of read operations:")
    paragraph("- Paginated list")
    paragraph("- Search results")
    paragraph("- Reports")
    paragraph("- Dashboard summaries")
    paragraph("- Read-only screens")
    paragraph(
        "Dapper allows us to write raw SQL directly. This is helpful because reports "
        "and list screens often need joins, filtering, sorting, pagination, and custom "
        "result shapes."
    )
    paragraph("**Example Read Flow**")
    code_block(
        """User opens list/report page
        ↓
Application calls query service
        ↓
Dapper runs raw SQL
        ↓
Data is returned as a read model/DTO
        ↓
UI displays the data""",
        language="text",
    )

    # ── 5. Commands and Queries ──────────────────────────────────────────────
    subsection("5. What Are Commands and Queries?")
    paragraph(
        "This approach separates the application into two responsibilities."
    )
    paragraph("**Commands** — used when data changes.")
    paragraph("Examples: Create student, Update student, Delete student, Add event history.")
    code_block("Domain Entities", language="text")
    paragraph("**Queries** — used when data is only read.")
    paragraph(
        "Examples: Get student list, Get event history list, Get report data, Get dropdown data."
    )
    code_block("Dapper + Raw SQL + Read Models", language="text")

    # ── 6. Folder Structure ──────────────────────────────────────────────────
    subsection("6. Recommended Folder Structure")
    paragraph("A simple project structure can look like this:")
    code_block(
        """Project
│
├── Domain
│   └── Entities
│       └── Student.cs
│
├── Application
│   ├── Commands
│   │   └── CreateStudentCommand.cs
│   │
│   ├── Queries
│   │   └── GetStudentsQuery.cs
│   │
│   └── DTOs
│       └── StudentListItemDto.cs
│
├── Infrastructure
│   ├── Data
│   │   └── AppDbContext.cs
│   │
│   ├── Repositories
│   │   └── StudentRepository.cs
│   │
│   └── Queries
│       └── StudentQueryService.cs
│
└── UI
    └── Pages / Components""",
        language="text",
    )

    # ── 7. Domain Entity Example ─────────────────────────────────────────────
    subsection("7. Domain Entity Example")
    paragraph(
        "A domain entity represents the main business object. Here, the entity "
        "controls how its own data is created and updated."
    )
    code_block(
        """public class Student
{
    public int Id { get; private set; }
    public string Name { get; private set; }
    public string Email { get; private set; }

    public Student(string name, string email)
    {
        Name = name;
        Email = email;
    }

    public void UpdateDetails(string name, string email)
    {
        Name = name;
        Email = email;
    }
}""",
        language="csharp",
    )

    # ── 8. EF Core DbContext for Oracle ──────────────────────────────────────
    subsection("8. EF Core DbContext Example for Oracle")
    paragraph("EF Core uses a DbContext to communicate with the database.")
    code_block(
        """public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options)
    {
    }

    public DbSet<Student> Students => Set<Student>();
}""",
        language="csharp",
    )
    paragraph("Oracle connection can be configured in Program.cs:")
    code_block(
        """builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseOracle(builder.Configuration.GetConnectionString("OracleConnection")));""",
        language="csharp",
    )
    paragraph("Example connection string in appsettings.json:")
    code_block(
        """{
  "ConnectionStrings": {
    "OracleConnection": "User Id=myuser;Password=mypassword;Data Source=localhost:1521/XEPDB1"
  }
}""",
        language="json",
    )

    # ── 9. Repository Pattern ────────────────────────────────────────────────
    subsection("9. Repository Pattern for Write Operations")
    paragraph(
        "The repository hides EF Core details from the rest of the application."
    )
    paragraph("**Repository Interface**")
    code_block(
        """public interface IStudentRepository
{
    Task<Student?> GetByIdAsync(int id);
    Task AddAsync(Student student);
    void Update(Student student);
    void Delete(Student student);
    Task SaveChangesAsync();
}""",
        language="csharp",
    )
    paragraph("**Repository Implementation**")
    code_block(
        """public class StudentRepository : IStudentRepository
{
    private readonly AppDbContext _dbContext;

    public StudentRepository(AppDbContext dbContext)
    {
        _dbContext = dbContext;
    }

    public async Task<Student?> GetByIdAsync(int id)
    {
        return await _dbContext.Students.FindAsync(id);
    }

    public async Task AddAsync(Student student)
    {
        await _dbContext.Students.AddAsync(student);
    }

    public void Update(Student student)
    {
        _dbContext.Students.Update(student);
    }

    public void Delete(Student student)
    {
        _dbContext.Students.Remove(student);
    }

    public async Task SaveChangesAsync()
    {
        await _dbContext.SaveChangesAsync();
    }
}""",
        language="csharp",
    )
    paragraph("Register the repository:")
    code_block(
        "builder.Services.AddScoped<IStudentRepository, StudentRepository>();",
        language="csharp",
    )

    # ── 10. Create Operation ─────────────────────────────────────────────────
    subsection("10. Create Operation Example Using EF Core")
    paragraph("This is a command because it changes data.")
    code_block(
        """public class CreateStudentService
{
    private readonly IStudentRepository _studentRepository;

    public CreateStudentService(IStudentRepository studentRepository)
    {
        _studentRepository = studentRepository;
    }

    public async Task CreateAsync(string name, string email)
    {
        var student = new Student(name, email);

        await _studentRepository.AddAsync(student);
        await _studentRepository.SaveChangesAsync();
    }
}""",
        language="csharp",
    )

    # ── 11. Update Operation ─────────────────────────────────────────────────
    subsection("11. Update Operation Example Using EF Core")
    code_block(
        """public async Task UpdateAsync(int id, string name, string email)
{
    var student = await _studentRepository.GetByIdAsync(id);

    if (student is null)
    {
        throw new Exception("Student not found.");
    }

    student.UpdateDetails(name, email);

    _studentRepository.Update(student);
    await _studentRepository.SaveChangesAsync();
}""",
        language="csharp",
    )

    # ── 12. Delete Operation ─────────────────────────────────────────────────
    subsection("12. Delete Operation Example Using EF Core")
    code_block(
        """public async Task DeleteAsync(int id)
{
    var student = await _studentRepository.GetByIdAsync(id);

    if (student is null)
    {
        throw new Exception("Student not found.");
    }

    _studentRepository.Delete(student);
    await _studentRepository.SaveChangesAsync();
}""",
        language="csharp",
    )

    # ── 13. Dapper Read Model ─────────────────────────────────────────────────
    subsection("13. Dapper for Read Operations")
    paragraph(
        "Dapper works directly with SQL. For read operations, we usually return DTOs "
        "or read models instead of domain entities."
    )
    paragraph("**Read Model Example**")
    code_block(
        """public class StudentListItemDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
}""",
        language="csharp",
    )

    # ── 14. Dapper Query Service ──────────────────────────────────────────────
    subsection("14. Dapper Query Service Example")
    code_block(
        """public class StudentQueryService
{
    private readonly string _connectionString;

    public StudentQueryService(IConfiguration configuration)
    {
        _connectionString = configuration.GetConnectionString("OracleConnection")!;
    }

    public async Task<IEnumerable<StudentListItemDto>> GetStudentsAsync()
    {
        using var connection = new OracleConnection(_connectionString);

        const string sql = \"\"\"
            SELECT
                ID AS Id,
                NAME AS Name,
                EMAIL AS Email
            FROM STUDENTS
            ORDER BY NAME
            \"\"\";

        return await connection.QueryAsync<StudentListItemDto>(sql);
    }
}""",
        language="csharp",
    )
    paragraph("Register the query service:")
    code_block(
        "builder.Services.AddScoped<StudentQueryService>();",
        language="csharp",
    )

    # ── 15. Pagination ────────────────────────────────────────────────────────
    subsection("15. Paginated List Using Dapper and Oracle")
    paragraph(
        "Pagination means loading data page by page. "
        "Page 1 shows records 1–10, page 2 shows records 11–20, and so on."
    )
    paragraph("**Paginated DTO**")
    code_block(
        """public class PagedResult<T>
{
    public IReadOnlyList<T> Items { get; set; } = [];
    public int TotalCount { get; set; }
    public int PageNumber { get; set; }
    public int PageSize { get; set; }
}""",
        language="csharp",
    )
    paragraph("**Dapper Pagination Query**")
    code_block(
        """public async Task<PagedResult<StudentListItemDto>> GetStudentsPagedAsync(
    int pageNumber,
    int pageSize)
{
    using var connection = new OracleConnection(_connectionString);

    var offset = (pageNumber - 1) * pageSize;

    const string dataSql = \"\"\"
        SELECT
            ID AS Id,
            NAME AS Name,
            EMAIL AS Email
        FROM STUDENTS
        ORDER BY NAME
        OFFSET :Offset ROWS FETCH NEXT :PageSize ROWS ONLY
        \"\"\";

    const string countSql = \"\"\"
        SELECT COUNT(*)
        FROM STUDENTS
        \"\"\";

    var items = await connection.QueryAsync<StudentListItemDto>(dataSql, new
    {
        Offset = offset,
        PageSize = pageSize
    });

    var totalCount = await connection.ExecuteScalarAsync<int>(countSql);

    return new PagedResult<StudentListItemDto>
    {
        Items = items.ToList(),
        TotalCount = totalCount,
        PageNumber = pageNumber,
        PageSize = pageSize
    };
}""",
        language="csharp",
    )

    # ── 16. Reports ───────────────────────────────────────────────────────────
    subsection("16. Reports Using Dapper")
    paragraph("Reports usually need custom SQL.")
    paragraph("**Example Report DTO**")
    code_block(
        """public class StudentReportDto
{
    public string SchoolName { get; set; } = string.Empty;
    public int TotalStudents { get; set; }
    public int ActiveStudents { get; set; }
}""",
        language="csharp",
    )
    paragraph("**Example Report Query**")
    code_block(
        """public async Task<IEnumerable<StudentReportDto>> GetStudentReportAsync()
{
    using var connection = new OracleConnection(_connectionString);

    const string sql = \"\"\"
        SELECT
            S.SCHOOL_NAME AS SchoolName,
            COUNT(*) AS TotalStudents,
            SUM(CASE WHEN ST.STATUS = 'ACTIVE' THEN 1 ELSE 0 END) AS ActiveStudents
        FROM STUDENTS ST
        INNER JOIN SCHOOLS S ON S.ID = ST.SCHOOL_ID
        GROUP BY S.SCHOOL_NAME
        ORDER BY S.SCHOOL_NAME
        \"\"\";

    return await connection.QueryAsync<StudentReportDto>(sql);
}""",
        language="csharp",
    )

    # ── 17. Important Rule ────────────────────────────────────────────────────
    subsection("17. Important Rule: Do Not Use Domain Entities for Reports")
    paragraph("For write operations, use domain entities. For read operations, use DTOs/read models.")
    paragraph("**Good:**")
    code_block(
        """Create Student → Student entity → EF Core
Student List → StudentListItemDto → Dapper
Student Report → StudentReportDto → Dapper""",
        language="text",
    )
    paragraph("**Avoid:**")
    code_block("Student Report → Student entity", language="text")
    paragraph(
        "Reports usually do not represent one real business entity. They are custom shapes of data."
    )

    # ── 18. Benefits ──────────────────────────────────────────────────────────
    subsection("18. Benefits of This Approach")
    st.markdown(
        """
| Benefit | Detail |
|---|---|
| **Cleaner Code** | Write logic and read logic are separated |
| **Better Performance** | Dapper is lightweight and fast for reports and lists |
| **Better Maintainability** | EF Core manages business entities while Dapper handles custom queries |
| **Easier Testing** | Repositories and query services can be tested separately |
| **Real-World Friendly** | This pattern is common in enterprise applications |
"""
    )

    # ── 19. Common Beginner Mistakes ─────────────────────────────────────────
    subsection("19. Common Beginner Mistakes")
    paragraph(
        "**Mistake 1: Using EF Core for Every Report** — EF Core is good, but complex "
        "reports are often easier and faster with SQL and Dapper."
    )
    paragraph(
        "**Mistake 2: Using Dapper for All Writes** — Dapper can write data, but EF Core "
        "is better when domain rules and entity relationships are important."
    )
    paragraph(
        "**Mistake 3: Returning Domain Entities to the UI** — Use DTOs for read screens. "
        "This keeps the UI simple and prevents exposing unnecessary database details."
    )
    paragraph(
        "**Mistake 4: Mixing SQL Everywhere** — Keep Dapper SQL inside query services. "
        "Do not spread SQL across UI components."
    )

    # ── 20. Recommended Development Steps ────────────────────────────────────
    subsection("20. Recommended Development Steps")
    paragraph("When building a new feature, follow this order.")
    paragraph("**For Create, Update, Delete:**")
    code_block(
        """1. Create domain entity
2. Create repository interface
3. Create repository implementation using EF Core
4. Create command/service method
5. Call command/service from UI""",
        language="text",
    )
    paragraph("**For Read/List/Report:**")
    code_block(
        """1. Create DTO/read model
2. Write SQL query
3. Create Dapper query service
4. Return DTO data
5. Display data in UI""",
        language="text",
    )

    # ── 21. Simple Example Summary ────────────────────────────────────────────
    subsection("21. Simple Example Summary")
    st.markdown(
        """
| Requirement | Use |
|---|---|
| Add student | EF Core Repository |
| Edit student | EF Core Repository |
| Delete student | EF Core Repository |
| Show student list | Dapper Query Service |
| Show paginated data | Dapper Query Service |
| Show report | Dapper Query Service |
"""
    )

    # ── 22. Final Architecture Summary ────────────────────────────────────────
    subsection("22. Final Architecture Summary")
    code_block(
        """UI / Blazor Component
        ↓
Application Service
        ↓
Commands ---------------- Queries
   ↓                         ↓
EF Core Repository        Dapper Query Service
   ↓                         ↓
Domain Entities           DTOs / Read Models
   ↓                         ↓
Oracle Database           Oracle Database""",
        language="text",
    )

    # ── 23. Key Takeaway ──────────────────────────────────────────────────────
    subsection("23. Key Takeaway")
    paragraph("Use this simple rule:")
    code_block(
        """If data changes, use EF Core with Repository.
If data is only displayed, use Dapper with raw SQL.""",
        language="text",
    )
    paragraph(
        "This gives a good balance between clean code, performance, and maintainability."
    )
