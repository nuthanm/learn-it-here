"""Blazor sub-page: CQRS Pattern with Blazor Auto, Oracle, EF Core, and Dapper."""

import streamlit as st

from components.content import (
    code_block,
    paragraph,
    section_intro,
    section_title,
    subsection,
)


def render_blazor_cqrs():
    """Sub-page: CQRS Pattern — from UI to API with Blazor Auto, Oracle, EF Core, Dapper."""

    section_title(
        "CQRS Pattern with Blazor Auto",
        "Command Query Responsibility Segregation — from UI to API with Oracle, EF Core, and Dapper.",
    )
    section_intro(
        "This guide explains what the CQRS pattern is, why it exists, and how to implement it "
        "step by step in a Blazor Auto application backed by an Oracle database. "
        "It is written for complete beginners — no prior knowledge of architecture patterns is required."
    )

    # ── 1. What Is CQRS? ─────────────────────────────────────────────────────
    subsection("1. What Is CQRS? (For Complete Beginners)")
    paragraph(
        "CQRS stands for Command Query Responsibility Segregation. "
        "The name sounds complicated, but the core idea is very simple:"
    )
    paragraph(
        "**Commands** change data. A command is any action that creates, updates, or deletes something. "
        "Think of it as giving an order: 'Add this student', 'Update that email', 'Delete this record'."
    )
    paragraph(
        "**Queries** read data. A query is any action that retrieves information without changing anything. "
        "Think of it as asking a question: 'Show me the student list', 'What is this student's email?'"
    )
    paragraph(
        "CQRS says: keep these two responsibilities in completely separate code paths. "
        "Do not mix reading and writing in the same class or method."
    )
    paragraph(
        "Simple analogy: Imagine a restaurant. The waiter who takes your order (command) is a different person "
        "from the waiter who brings your food to the table (query). Each person is focused on one job. "
        "That separation makes everything faster, cleaner, and easier to understand."
    )

    # ── 2. Why Use CQRS? ─────────────────────────────────────────────────────
    subsection("2. Why Use CQRS? — The Problem It Solves")
    paragraph(
        "In a traditional application, one class does everything: it saves data AND reads data. "
        "This works fine for small apps, but it causes problems as the app grows."
    )
    paragraph("Problems with mixing reads and writes in one place:")
    paragraph("- **Performance**: Read queries are usually much simpler than write logic. Sharing the same model forces unnecessary complexity on reads.")
    paragraph("- **Complexity**: The class gets bigger and harder to understand over time.")
    paragraph("- **Testing**: It is harder to test a class that does many things at once.")
    paragraph("- **Scaling**: Reads and writes often have different scaling needs. CQRS lets you scale them independently.")
    paragraph("Benefits CQRS brings:")
    st.markdown(
        """
| Benefit | Explanation |
|---|---|
| **Single responsibility** | Each handler does exactly one thing |
| **Easier to read** | You immediately know if code changes data or only reads it |
| **Better performance** | Read side uses fast, direct SQL (Dapper). Write side uses EF Core change tracking |
| **Easier to test** | Handlers are small, focused classes — easy to unit test |
| **Scales independently** | Read and write databases can be separated later if needed |
| **Works well with MediatR** | The popular MediatR library plugs directly into this pattern |
"""
    )

    # ── 3. When To Use CQRS ──────────────────────────────────────────────────
    subsection("3. When to Use CQRS — and When Not To")
    paragraph("**Use CQRS when:**")
    paragraph("- Your application has complex business rules on the write side.")
    paragraph("- Your read side needs fast, custom queries (reports, dashboards, paginated lists).")
    paragraph("- You want to make your code easy to test and maintain.")
    paragraph("- Your team is growing and you want clear separation of work.")
    paragraph("- You plan to scale reads and writes differently in the future.")
    paragraph("**Avoid CQRS when:**")
    paragraph("- Your app is very small (CRUD only, no business logic). CQRS adds structure that may be overkill.")
    paragraph("- You are building a quick prototype. Use a simpler approach first.")
    paragraph("- Your team is brand new to .NET and needs to learn basics first.")
    st.markdown(
        """
| Scenario | Recommendation |
|---|---|
| Small CRUD app, 1–3 tables | Repository Pattern is enough |
| Medium app with business rules | CQRS is a great fit |
| Large enterprise app with reports | CQRS is strongly recommended |
| Microservices | CQRS is a natural fit |
"""
    )

    # ── 4. CQRS Workflow ─────────────────────────────────────────────────────
    subsection("4. CQRS Workflow — Step by Step")
    paragraph(
        "The following diagram shows how a request flows through a CQRS application. "
        "Both commands and queries go through MediatR, which routes each request to the correct handler."
    )
    code_block(
        """┌─────────────────────────────────────────────────────────────────────┐
│                        BLAZOR AUTO UI                                  │
│  (Fluent UI components — FluentTextField, FluentButton, FluentDataGrid)│
└──────────────────────┬──────────────────────────────┬──────────────────┘
                       │                              │
              User submits form               User views a list/report
                       │                              │
              ┌────────▼────────┐           ┌─────────▼────────┐
              │    COMMAND       │           │      QUERY        │
              │  CreateStudent   │           │  GetStudentsList  │
              │  UpdateStudent   │           │  GetStudentById   │
              │  DeleteStudent   │           │  GetDashboard     │
              └────────┬────────┘           └─────────┬────────┘
                       │                              │
              ┌────────▼────────────────────────────────────────┐
              │                   MediatR                        │
              │   Routes each message to the correct Handler     │
              └────────┬────────────────────────┬───────────────┘
                       │                        │
         ┌─────────────▼──────┐     ┌───────────▼─────────────┐
         │  Command Handler    │     │    Query Handler         │
         │  (uses EF Core)     │     │    (uses Dapper)         │
         └─────────────┬──────┘     └───────────┬─────────────┘
                       │                        │
              ┌────────▼────────┐    ┌──────────▼──────────────┐
              │  Oracle DB       │    │  Oracle DB               │
              │  (via EF Core)   │    │  (via Dapper + raw SQL)  │
              └─────────────────┘    └─────────────────────────┘""",
        language="text",
    )
    paragraph(
        "Key insight: commands go through EF Core because we need entity tracking and business rules. "
        "Queries go through Dapper because we need speed and flexible SQL."
    )

    # ── 5. CQRS vs Repository Pattern ───────────────────────────────────────
    subsection("5. CQRS vs Repository Pattern — What Is the Difference?")
    paragraph(
        "You may have already heard about the Repository Pattern. Both are architecture patterns, "
        "and they are often used together. Here is how they compare:"
    )
    st.markdown(
        """
| Aspect | Repository Pattern | CQRS |
|---|---|---|
| **Main idea** | Abstract the data layer behind an interface | Separate read and write responsibilities entirely |
| **Focus** | How data is accessed | How operations are structured (command vs query) |
| **Handlers** | No concept of handlers | Each action has its own dedicated handler class |
| **Read side** | Uses the same repository | Uses a separate query model and service (often Dapper) |
| **Write side** | Repository with EF Core | Command handler with EF Core |
| **Works together?** | Yes — repositories are often used inside command handlers | Yes — CQRS uses repositories for the write side |
| **Complexity** | Medium | Medium-High |
| **Best for** | Apps that need clean data access | Apps with clear business operations and complex reads |
"""
    )
    paragraph(
        "Think of it this way: Repository Pattern organizes *how* you access the database. "
        "CQRS organizes *what* your application does (and separates doing from reading)."
    )

    # ── 6. Technology Stack ──────────────────────────────────────────────────
    subsection("6. Technology Stack Used in This Guide")
    st.markdown(
        """
| Technology | Role | Why |
|---|---|---|
| **Blazor Auto** | UI + hosting model | Automatically chooses Server or WebAssembly rendering per session |
| **Fluent UI Blazor** | UI component library | Polished, accessible Microsoft Design System controls |
| **Minimal API** | HTTP API layer | Lightweight API endpoints that connect UI to application logic |
| **MediatR** | CQRS messaging library | Routes commands and queries to their handlers automatically |
| **EF Core + Oracle** | Write side (commands) | Change tracking, entity management, Oracle database access |
| **Dapper + Oracle** | Read side (queries) | Fast, raw SQL queries returning lightweight DTOs |
| **FluentValidation** | Input validation | Clean, testable validation rules for commands |
"""
    )

    # ── 7. What Is Blazor Auto? ──────────────────────────────────────────────
    subsection("7. What Is Blazor Auto? (Quick Explanation)")
    paragraph(
        "Blazor Auto is a rendering mode introduced in .NET 8. "
        "When a user first opens the page, it uses Blazor Server (fast initial load). "
        "While the page is loading, the .NET WebAssembly runtime downloads in the background. "
        "Once WebAssembly is ready, the page silently upgrades to Blazor WebAssembly. "
        "The user sees no change — it just gets faster automatically."
    )
    paragraph("You enable Auto mode per component or per page:")
    code_block(
        """@rendermode InteractiveAuto""",
        language="csharp",
    )
    paragraph(
        "For CQRS apps, Blazor Auto means your UI calls an API (Minimal API or Controller). "
        "The API layer handles the MediatR commands and queries. "
        "The UI stays thin — it only sends requests and displays results."
    )

    # ── 8. Project Structure ─────────────────────────────────────────────────
    subsection("8. Project Structure — How to Organize the Solution")
    paragraph(
        "A clean CQRS solution typically uses multiple projects to separate concerns. "
        "Here is the recommended structure:"
    )
    code_block(
        """MyApp.sln
│
├── MyApp.Web                    ← Blazor Auto project (UI + API host)
│   ├── Components
│   │   ├── Layout
│   │   │   └── MainLayout.razor
│   │   └── Pages
│   │       ├── Students
│   │       │   ├── StudentList.razor       ← Read: FluentDataGrid
│   │       │   └── StudentForm.razor       ← Write: FluentTextField, FluentButton
│   │       └── Home.razor
│   ├── Endpoints
│   │   └── StudentEndpoints.cs             ← Minimal API endpoints
│   └── Program.cs
│
├── MyApp.Application            ← CQRS: Commands, Queries, Handlers
│   ├── Students
│   │   ├── Commands
│   │   │   ├── CreateStudentCommand.cs
│   │   │   ├── CreateStudentHandler.cs
│   │   │   ├── UpdateStudentCommand.cs
│   │   │   ├── UpdateStudentHandler.cs
│   │   │   ├── DeleteStudentCommand.cs
│   │   │   └── DeleteStudentHandler.cs
│   │   ├── Queries
│   │   │   ├── GetStudentsQuery.cs
│   │   │   ├── GetStudentsHandler.cs
│   │   │   ├── GetStudentByIdQuery.cs
│   │   │   └── GetStudentByIdHandler.cs
│   │   └── DTOs
│   │       └── StudentDto.cs
│   └── Common
│       └── PagedResult.cs
│
├── MyApp.Domain                 ← Business entities
│   └── Entities
│       └── Student.cs
│
└── MyApp.Infrastructure         ← EF Core, Dapper, Oracle config
    ├── Data
    │   └── AppDbContext.cs
    ├── Repositories
    │   ├── IStudentRepository.cs
    │   └── StudentRepository.cs
    └── Queries
        └── StudentQueryService.cs""",
        language="text",
    )

    # ── 9. NuGet Packages ────────────────────────────────────────────────────
    subsection("9. NuGet Packages to Install")
    paragraph("Install these packages in the correct projects:")
    st.markdown(
        """
| Package | Project | Purpose |
|---|---|---|
| `MediatR` | Application | CQRS messaging dispatcher |
| `MediatR.Extensions.Microsoft.DependencyInjection` | Web / Application | Register MediatR with DI |
| `FluentValidation.DependencyInjectionExtensions` | Application | Validate commands before handling |
| `Oracle.EntityFrameworkCore` | Infrastructure | EF Core provider for Oracle |
| `Dapper` | Infrastructure | Micro-ORM for fast read queries |
| `Oracle.ManagedDataAccess.Core` | Infrastructure | Oracle connection for Dapper |
| `Microsoft.FluentUI.AspNetCore.Components` | Web | Fluent UI Blazor components |
| `Microsoft.FluentUI.AspNetCore.Components.Icons` | Web | Fluent UI icon set |
"""
    )
    paragraph("Install via the .NET CLI (run inside the project folder):")
    code_block(
        """# Application project
dotnet add package MediatR
dotnet add package FluentValidation.DependencyInjectionExtensions

# Infrastructure project
dotnet add package Oracle.EntityFrameworkCore
dotnet add package Dapper
dotnet add package Oracle.ManagedDataAccess.Core

# Web project
dotnet add package MediatR.Extensions.Microsoft.DependencyInjection
dotnet add package Microsoft.FluentUI.AspNetCore.Components
dotnet add package Microsoft.FluentUI.AspNetCore.Components.Icons""",
        language="bash",
    )

    # ── 10. Domain Entity ─────────────────────────────────────────────────────
    subsection("10. Domain Entity — Student.cs")
    paragraph(
        "The domain entity is the core business object. "
        "It contains the data and the rules that protect that data. "
        "Notice that setters are private — you can only change the entity through its methods."
    )
    code_block(
        """// MyApp.Domain/Entities/Student.cs
namespace MyApp.Domain.Entities;

public class Student
{
    public int Id { get; private set; }
    public string Name { get; private set; } = string.Empty;
    public string Email { get; private set; } = string.Empty;
    public DateTime CreatedAt { get; private set; }

    // EF Core needs a parameterless constructor (keep it private/protected)
    private Student() { }

    // Factory method — this is how you create a new student
    public static Student Create(string name, string email)
    {
        return new Student
        {
            Name = name,
            Email = email,
            CreatedAt = DateTime.UtcNow
        };
    }

    // Update method — controls how a student can be modified
    public void UpdateDetails(string name, string email)
    {
        Name = name;
        Email = email;
    }
}""",
        language="csharp",
    )

    # ── 11. EF Core DbContext ─────────────────────────────────────────────────
    subsection("11. EF Core DbContext — AppDbContext.cs")
    paragraph(
        "The DbContext is the gateway between your C# objects and Oracle. "
        "EF Core uses it to track changes and generate SQL automatically."
    )
    code_block(
        """// MyApp.Infrastructure/Data/AppDbContext.cs
using Microsoft.EntityFrameworkCore;
using MyApp.Domain.Entities;

namespace MyApp.Infrastructure.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options) { }

    public DbSet<Student> Students => Set<Student>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Student>(entity =>
        {
            entity.ToTable("STUDENTS");               // Oracle table name (uppercase)
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Id).HasColumnName("ID").ValueGeneratedOnAdd();
            entity.Property(e => e.Name).HasColumnName("NAME").HasMaxLength(200).IsRequired();
            entity.Property(e => e.Email).HasColumnName("EMAIL").HasMaxLength(300).IsRequired();
            entity.Property(e => e.CreatedAt).HasColumnName("CREATED_AT");
        });
    }
}""",
        language="csharp",
    )
    paragraph("Configure Oracle connection in Program.cs:")
    code_block(
        """builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseOracle(builder.Configuration.GetConnectionString("OracleConnection")));""",
        language="csharp",
    )
    paragraph("Connection string in appsettings.json:")
    code_block(
        """{
  "ConnectionStrings": {
    "OracleConnection": "User Id=myuser;Password=mypassword;Data Source=localhost:1521/XEPDB1"
  }
}""",
        language="json",
    )

    # ── 12. Repository ────────────────────────────────────────────────────────
    subsection("12. Repository — Used by Command Handlers")
    paragraph(
        "Command handlers do not call EF Core directly. "
        "They go through a repository interface. "
        "This makes the handler easier to test — you can swap in a fake repository in tests."
    )
    code_block(
        """// MyApp.Infrastructure/Repositories/IStudentRepository.cs
namespace MyApp.Infrastructure.Repositories;

public interface IStudentRepository
{
    Task<Student?> GetByIdAsync(int id);
    Task AddAsync(Student student);
    void Update(Student student);
    void Delete(Student student);
    Task SaveChangesAsync();
}""",
        language="csharp",
    )
    code_block(
        """// MyApp.Infrastructure/Repositories/StudentRepository.cs
using Microsoft.EntityFrameworkCore;
using MyApp.Domain.Entities;
using MyApp.Infrastructure.Data;

namespace MyApp.Infrastructure.Repositories;

public class StudentRepository : IStudentRepository
{
    private readonly AppDbContext _context;

    public StudentRepository(AppDbContext context)
    {
        _context = context;
    }

    public async Task<Student?> GetByIdAsync(int id)
        => await _context.Students.FindAsync(id);

    public async Task AddAsync(Student student)
        => await _context.Students.AddAsync(student);

    public void Update(Student student)
        => _context.Students.Update(student);

    public void Delete(Student student)
        => _context.Students.Remove(student);

    public async Task SaveChangesAsync()
        => await _context.SaveChangesAsync();
}""",
        language="csharp",
    )
    paragraph("Register the repository in Program.cs:")
    code_block(
        "builder.Services.AddScoped<IStudentRepository, StudentRepository>();",
        language="csharp",
    )

    # ── 13. DTOs ───────────────────────────────────────────────────────────────
    subsection("13. DTOs — Data Transfer Objects for the Read Side")
    paragraph(
        "A DTO (Data Transfer Object) is a simple class that carries data between layers. "
        "On the read side, we never return domain entities directly to the UI. "
        "We return DTOs — lightweight objects shaped for what the screen needs."
    )
    code_block(
        """// MyApp.Application/Students/DTOs/StudentDto.cs
namespace MyApp.Application.Students.DTOs;

// Used for list screens and reports
public class StudentDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string CreatedAt { get; set; } = string.Empty;
}""",
        language="csharp",
    )
    code_block(
        """// MyApp.Application/Common/PagedResult.cs
namespace MyApp.Application.Common;

public class PagedResult<T>
{
    public IReadOnlyList<T> Items { get; set; } = [];
    public int TotalCount { get; set; }
    public int PageNumber { get; set; }
    public int PageSize { get; set; }
    public int TotalPages => (int)Math.Ceiling((double)TotalCount / PageSize);
}""",
        language="csharp",
    )

    # ── 14. Commands ──────────────────────────────────────────────────────────
    subsection("14. Commands — The Write Side (EF Core)")
    paragraph(
        "Each command is a class that represents one action. "
        "The command carries the input data. "
        "The handler does the actual work. "
        "This separation means you can change the handler without touching the command, and vice versa."
    )
    paragraph("**Create Student Command and Handler**")
    code_block(
        """// MyApp.Application/Students/Commands/CreateStudentCommand.cs
using MediatR;

namespace MyApp.Application.Students.Commands;

// The command: carries the input data
public record CreateStudentCommand(string Name, string Email) : IRequest<int>;

// The handler: does the actual work
public class CreateStudentHandler : IRequestHandler<CreateStudentCommand, int>
{
    private readonly IStudentRepository _repository;

    public CreateStudentHandler(IStudentRepository repository)
    {
        _repository = repository;
    }

    public async Task<int> Handle(CreateStudentCommand request, CancellationToken ct)
    {
        // Create the domain entity using its factory method
        var student = Student.Create(request.Name, request.Email);

        // Save to Oracle via EF Core
        await _repository.AddAsync(student);
        await _repository.SaveChangesAsync();

        // Return the new ID to the caller
        return student.Id;
    }
}""",
        language="csharp",
    )
    paragraph("**Update Student Command and Handler**")
    code_block(
        """// MyApp.Application/Students/Commands/UpdateStudentCommand.cs
using MediatR;

namespace MyApp.Application.Students.Commands;

public record UpdateStudentCommand(int Id, string Name, string Email) : IRequest;

public class UpdateStudentHandler : IRequestHandler<UpdateStudentCommand>
{
    private readonly IStudentRepository _repository;

    public UpdateStudentHandler(IStudentRepository repository)
    {
        _repository = repository;
    }

    public async Task Handle(UpdateStudentCommand request, CancellationToken ct)
    {
        var student = await _repository.GetByIdAsync(request.Id)
            ?? throw new KeyNotFoundException($"Student {request.Id} not found.");

        student.UpdateDetails(request.Name, request.Email);
        _repository.Update(student);
        await _repository.SaveChangesAsync();
    }
}""",
        language="csharp",
    )
    paragraph("**Delete Student Command and Handler**")
    code_block(
        """// MyApp.Application/Students/Commands/DeleteStudentCommand.cs
using MediatR;

namespace MyApp.Application.Students.Commands;

public record DeleteStudentCommand(int Id) : IRequest;

public class DeleteStudentHandler : IRequestHandler<DeleteStudentCommand>
{
    private readonly IStudentRepository _repository;

    public DeleteStudentHandler(IStudentRepository repository)
    {
        _repository = repository;
    }

    public async Task Handle(DeleteStudentCommand request, CancellationToken ct)
    {
        var student = await _repository.GetByIdAsync(request.Id)
            ?? throw new KeyNotFoundException($"Student {request.Id} not found.");

        _repository.Delete(student);
        await _repository.SaveChangesAsync();
    }
}""",
        language="csharp",
    )

    # ── 15. Queries ───────────────────────────────────────────────────────────
    subsection("15. Queries — The Read Side (Dapper + Oracle)")
    paragraph(
        "Queries are handled completely separately from commands. "
        "They use Dapper to run raw SQL directly against Oracle. "
        "This is much faster for lists, reports, and dashboards than using EF Core."
    )
    paragraph("**Get Students List Query and Handler (Paginated)**")
    code_block(
        """// MyApp.Application/Students/Queries/GetStudentsQuery.cs
using Dapper;
using MediatR;
using Microsoft.Extensions.Configuration;
using Oracle.ManagedDataAccess.Client;

namespace MyApp.Application.Students.Queries;

// The query: carries the input parameters
public record GetStudentsQuery(int PageNumber = 1, int PageSize = 10)
    : IRequest<PagedResult<StudentDto>>;

// The handler: reads data from Oracle using Dapper
public class GetStudentsHandler
    : IRequestHandler<GetStudentsQuery, PagedResult<StudentDto>>
{
    private readonly string _connectionString;

    public GetStudentsHandler(IConfiguration configuration)
    {
        _connectionString =
            configuration.GetConnectionString("OracleConnection")!;
    }

    public async Task<PagedResult<StudentDto>> Handle(
        GetStudentsQuery request, CancellationToken ct)
    {
        await using var connection = new OracleConnection(_connectionString);

        var offset = (request.PageNumber - 1) * request.PageSize;

        const string dataSql = \"\"\"
            SELECT
                ID          AS Id,
                NAME        AS Name,
                EMAIL       AS Email,
                TO_CHAR(CREATED_AT, 'DD Mon YYYY') AS CreatedAt
            FROM STUDENTS
            ORDER BY NAME
            OFFSET :Offset ROWS FETCH NEXT :PageSize ROWS ONLY
            \"\"\";

        const string countSql = "SELECT COUNT(*) FROM STUDENTS";

        var items = await connection.QueryAsync<StudentDto>(
            dataSql, new { Offset = offset, request.PageSize });

        var totalCount = await connection.ExecuteScalarAsync<int>(countSql);

        return new PagedResult<StudentDto>
        {
            Items    = items.ToList(),
            TotalCount = totalCount,
            PageNumber = request.PageNumber,
            PageSize   = request.PageSize
        };
    }
}""",
        language="csharp",
    )
    paragraph("**Get Student By ID Query and Handler**")
    code_block(
        """// MyApp.Application/Students/Queries/GetStudentByIdQuery.cs
using Dapper;
using MediatR;
using Microsoft.Extensions.Configuration;
using Oracle.ManagedDataAccess.Client;

namespace MyApp.Application.Students.Queries;

public record GetStudentByIdQuery(int Id) : IRequest<StudentDto?>;

public class GetStudentByIdHandler : IRequestHandler<GetStudentByIdQuery, StudentDto?>
{
    private readonly string _connectionString;

    public GetStudentByIdHandler(IConfiguration configuration)
    {
        _connectionString =
            configuration.GetConnectionString("OracleConnection")!;
    }

    public async Task<StudentDto?> Handle(
        GetStudentByIdQuery request, CancellationToken ct)
    {
        await using var connection = new OracleConnection(_connectionString);

        const string sql = \"\"\"
            SELECT
                ID    AS Id,
                NAME  AS Name,
                EMAIL AS Email,
                TO_CHAR(CREATED_AT, 'DD Mon YYYY') AS CreatedAt
            FROM STUDENTS
            WHERE ID = :Id
            \"\"\";

        return await connection.QuerySingleOrDefaultAsync<StudentDto>(
            sql, new { request.Id });
    }
}""",
        language="csharp",
    )

    # ── 16. FluentValidation ──────────────────────────────────────────────────
    subsection("16. FluentValidation — Validate Commands Before They Run")
    paragraph(
        "FluentValidation lets you write validation rules as clean classes. "
        "Register a MediatR pipeline behaviour so every command is validated automatically "
        "before the handler even runs. If validation fails, the API returns an error — "
        "no invalid data ever reaches the database."
    )
    code_block(
        """// MyApp.Application/Students/Commands/CreateStudentValidator.cs
using FluentValidation;

namespace MyApp.Application.Students.Commands;

public class CreateStudentValidator : AbstractValidator<CreateStudentCommand>
{
    public CreateStudentValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required.")
            .MaximumLength(200).WithMessage("Name cannot exceed 200 characters.");

        RuleFor(x => x.Email)
            .NotEmpty().WithMessage("Email is required.")
            .EmailAddress().WithMessage("Enter a valid email address.")
            .MaximumLength(300).WithMessage("Email cannot exceed 300 characters.");
    }
}""",
        language="csharp",
    )
    paragraph("Register validators and MediatR in Program.cs:")
    code_block(
        """// In Program.cs
builder.Services.AddMediatR(cfg =>
    cfg.RegisterServicesFromAssembly(typeof(CreateStudentCommand).Assembly));

builder.Services.AddValidatorsFromAssembly(typeof(CreateStudentValidator).Assembly);""",
        language="csharp",
    )

    # ── 17. Minimal API Endpoints ─────────────────────────────────────────────
    subsection("17. Minimal API Endpoints — The API Layer")
    paragraph(
        "The Minimal API layer receives HTTP requests from the Blazor UI and delegates to MediatR. "
        "The endpoints are thin — they do not contain any business logic. "
        "They only validate the HTTP request, send the correct command or query, and return the result."
    )
    code_block(
        """// MyApp.Web/Endpoints/StudentEndpoints.cs
using MediatR;
using MyApp.Application.Students.Commands;
using MyApp.Application.Students.Queries;

namespace MyApp.Web.Endpoints;

public static class StudentEndpoints
{
    public static void MapStudentEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/students").WithTags("Students");

        // GET /api/students?pageNumber=1&pageSize=10
        group.MapGet("/", async (IMediator mediator, int pageNumber = 1, int pageSize = 10) =>
        {
            var result = await mediator.Send(new GetStudentsQuery(pageNumber, pageSize));
            return Results.Ok(result);
        });

        // GET /api/students/{id}
        group.MapGet("/{id:int}", async (IMediator mediator, int id) =>
        {
            var result = await mediator.Send(new GetStudentByIdQuery(id));
            return result is null ? Results.NotFound() : Results.Ok(result);
        });

        // POST /api/students
        group.MapPost("/", async (IMediator mediator, CreateStudentCommand command) =>
        {
            var newId = await mediator.Send(command);
            return Results.Created($"/api/students/{newId}", new { id = newId });
        });

        // PUT /api/students/{id}
        group.MapPut("/{id:int}", async (IMediator mediator, int id, UpdateStudentCommand command) =>
        {
            if (id != command.Id)
                return Results.BadRequest("ID in URL and body must match.");

            await mediator.Send(command);
            return Results.NoContent();
        });

        // DELETE /api/students/{id}
        group.MapDelete("/{id:int}", async (IMediator mediator, int id) =>
        {
            await mediator.Send(new DeleteStudentCommand(id));
            return Results.NoContent();
        });
    }
}""",
        language="csharp",
    )
    paragraph("Register the endpoints in Program.cs:")
    code_block(
        """// In Program.cs
var app = builder.Build();
app.MapStudentEndpoints();
app.Run();""",
        language="csharp",
    )

    # ── 18. Blazor Auto UI ────────────────────────────────────────────────────
    subsection("18. Blazor Auto UI — Student List Page (Fluent UI)")
    paragraph(
        "The Blazor UI calls the API using HttpClient. "
        "It uses Fluent UI components for all controls. "
        "The page is marked as InteractiveAuto — Blazor handles the rendering mode automatically."
    )
    code_block(
        """@* Pages/Students/StudentList.razor *@
@page "/students"
@rendermode InteractiveAuto
@inject HttpClient Http
@inject NavigationManager Nav

<PageTitle>Students</PageTitle>

<FluentStack Orientation="Orientation.Vertical" VerticalGap="16">

    <FluentStack Orientation="Orientation.Horizontal" HorizontalGap="12">
        <h2>Students</h2>
        <FluentSpacer />
        <FluentButton Appearance="Appearance.Accent"
                      OnClick="@(() => Nav.NavigateTo("/students/new"))">
            + Add Student
        </FluentButton>
    </FluentStack>

    @if (_loading)
    {
        <FluentProgressRing />
    }
    else if (_error is not null)
    {
        <FluentMessageBar Intent="MessageIntent.Error">@_error</FluentMessageBar>
    }
    else
    {
        <FluentDataGrid Items="@_students.Items.AsQueryable()"
                        TGridItem="StudentDto"
                        Pagination="@_pagination">
            <PropertyColumn Property="@(s => s.Name)" Title="Name" Sortable="true" />
            <PropertyColumn Property="@(s => s.Email)" Title="Email" />
            <PropertyColumn Property="@(s => s.CreatedAt)" Title="Created" />
            <TemplateColumn Title="Actions">
                <FluentButton Appearance="Appearance.Outline"
                              OnClick="@(() => Nav.NavigateTo($"/students/{context.Id}/edit"))">
                    Edit
                </FluentButton>
                <FluentButton Appearance="Appearance.Outline"
                              OnClick="@(() => DeleteAsync(context.Id))">
                    Delete
                </FluentButton>
            </TemplateColumn>
        </FluentDataGrid>

        <FluentPaginator State="@_pagination" />
    }

</FluentStack>

@code {
    private PagedResult<StudentDto>? _students;
    private PaginationState _pagination = new() { ItemsPerPage = 10 };
    private bool _loading = true;
    private string? _error;

    protected override async Task OnInitializedAsync()
    {
        await LoadAsync();
    }

    private async Task LoadAsync(int page = 1)
    {
        _loading = true;
        _error   = null;
        try
        {
            _students = await Http.GetFromJsonAsync<PagedResult<StudentDto>>(
                $"api/students?pageNumber={page}&pageSize=10");
        }
        catch (Exception ex)
        {
            _error = $"Failed to load students: {ex.Message}";
        }
        finally
        {
            _loading = false;
        }
    }

    private async Task DeleteAsync(int id)
    {
        await Http.DeleteAsync($"api/students/{id}");
        await LoadAsync();
    }
}""",
        language="csharp",
    )

    # ── 19. Blazor Auto UI – Form ─────────────────────────────────────────────
    subsection("19. Blazor Auto UI — Add / Edit Student Form (Fluent UI)")
    paragraph(
        "The form page handles both create and edit in one component. "
        "If an ID is present in the URL, it loads the existing data. Otherwise, it creates a new student."
    )
    code_block(
        """@* Pages/Students/StudentForm.razor *@
@page "/students/new"
@page "/students/{Id:int}/edit"
@rendermode InteractiveAuto
@inject HttpClient Http
@inject NavigationManager Nav

<PageTitle>@(Id.HasValue ? "Edit Student" : "New Student")</PageTitle>

<FluentCard Style="max-width: 500px; padding: 24px;">

    <h3>@(Id.HasValue ? "Edit Student" : "Add Student")</h3>

    <EditForm Model="@_model" OnValidSubmit="HandleSubmitAsync">
        <DataAnnotationsValidator />

        <FluentStack Orientation="Orientation.Vertical" VerticalGap="12">

            <FluentTextField Label="Full Name"
                             @bind-Value="_model.Name"
                             Placeholder="Enter full name"
                             Style="width: 100%" />
            <ValidationMessage For="@(() => _model.Name)" />

            <FluentTextField Label="Email"
                             @bind-Value="_model.Email"
                             Placeholder="Enter email address"
                             Style="width: 100%" />
            <ValidationMessage For="@(() => _model.Email)" />

            @if (_error is not null)
            {
                <FluentMessageBar Intent="MessageIntent.Error">@_error</FluentMessageBar>
            }

            <FluentStack Orientation="Orientation.Horizontal" HorizontalGap="8">
                <FluentButton Type="ButtonType.Submit"
                              Appearance="Appearance.Accent"
                              Loading="@_saving">
                    @(Id.HasValue ? "Save Changes" : "Create Student")
                </FluentButton>
                <FluentButton Appearance="Appearance.Outline"
                              OnClick="@(() => Nav.NavigateTo("/students"))">
                    Cancel
                </FluentButton>
            </FluentStack>

        </FluentStack>
    </EditForm>

</FluentCard>

@code {
    [Parameter] public int? Id { get; set; }

    private StudentFormModel _model = new();
    private bool _saving;
    private string? _error;

    protected override async Task OnInitializedAsync()
    {
        if (Id.HasValue)
        {
            var dto = await Http.GetFromJsonAsync<StudentDto>($"api/students/{Id}");
            if (dto is not null)
            {
                _model.Name  = dto.Name;
                _model.Email = dto.Email;
            }
        }
    }

    private async Task HandleSubmitAsync()
    {
        _saving = true;
        _error  = null;
        try
        {
            if (Id.HasValue)
            {
                await Http.PutAsJsonAsync(
                    $"api/students/{Id}",
                    new { Id = Id.Value, _model.Name, _model.Email });
            }
            else
            {
                await Http.PostAsJsonAsync(
                    "api/students",
                    new { _model.Name, _model.Email });
            }
            Nav.NavigateTo("/students");
        }
        catch (Exception ex)
        {
            _error = $"Save failed: {ex.Message}";
        }
        finally
        {
            _saving = false;
        }
    }

    private class StudentFormModel
    {
        [Required(ErrorMessage = "Name is required.")]
        [MaxLength(200, ErrorMessage = "Name cannot exceed 200 characters.")]
        public string Name { get; set; } = string.Empty;

        [Required(ErrorMessage = "Email is required.")]
        [EmailAddress(ErrorMessage = "Enter a valid email address.")]
        [MaxLength(300, ErrorMessage = "Email cannot exceed 300 characters.")]
        public string Email { get; set; } = string.Empty;
    }
}""",
        language="csharp",
    )

    # ── 20. Program.cs – Full Setup ───────────────────────────────────────────
    subsection("20. Complete Program.cs Setup")
    paragraph(
        "This is what the full Program.cs looks like when everything is wired together."
    )
    code_block(
        """// MyApp.Web/Program.cs
using MyApp.Application.Students.Commands;
using MyApp.Application.Students.Queries;
using MyApp.Infrastructure.Data;
using MyApp.Infrastructure.Repositories;
using MyApp.Web.Endpoints;
using FluentValidation;
using MediatR;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// ── Blazor ────────────────────────────────────────────────────────────────
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents()
    .AddInteractiveWebAssemblyComponents();

// ── Fluent UI ─────────────────────────────────────────────────────────────
builder.Services.AddFluentUIComponents();

// ── EF Core + Oracle ──────────────────────────────────────────────────────
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseOracle(builder.Configuration.GetConnectionString("OracleConnection")));

// ── Repository ────────────────────────────────────────────────────────────
builder.Services.AddScoped<IStudentRepository, StudentRepository>();

// ── MediatR (scans Application assembly) ─────────────────────────────────
builder.Services.AddMediatR(cfg =>
    cfg.RegisterServicesFromAssembly(typeof(CreateStudentCommand).Assembly));

// ── FluentValidation ──────────────────────────────────────────────────────
builder.Services.AddValidatorsFromAssembly(
    typeof(CreateStudentValidator).Assembly);

// ── HttpClient for Blazor components ─────────────────────────────────────
builder.Services.AddScoped(sp =>
    new HttpClient { BaseAddress = new Uri(builder.Configuration["ApiBase"]!) });

var app = builder.Build();

// ── Middleware ────────────────────────────────────────────────────────────
if (!app.Environment.IsDevelopment())
    app.UseHsts();

app.UseHttpsRedirection();
app.UseAntiforgery();

app.MapStaticAssets();
app.MapRazorComponents<App>()
   .AddInteractiveServerRenderMode()
   .AddInteractiveWebAssemblyRenderMode();

// ── API Endpoints ─────────────────────────────────────────────────────────
app.MapStudentEndpoints();

app.Run();""",
        language="csharp",
    )

    # ── 21. Full Request Flow ──────────────────────────────────────────────────
    subsection("21. Full Request Flow — End to End")
    paragraph("Here is what happens when a user clicks 'Create Student' in the browser:")
    code_block(
        """Step 1  User fills in the form (FluentTextField) and clicks FluentButton

Step 2  Blazor calls Http.PostAsJsonAsync("api/students", { Name, Email })

Step 3  Minimal API receives POST /api/students
        → Deserialises JSON into CreateStudentCommand

Step 4  Endpoint calls mediator.Send(command)

Step 5  MediatR routes the command to CreateStudentHandler
        (automatic — no if/else needed)

Step 6  CreateStudentHandler:
        a) Calls Student.Create(name, email)   → creates domain entity
        b) Calls _repository.AddAsync(student) → EF Core tracks the new entity
        c) Calls _repository.SaveChangesAsync()
           → EF Core generates INSERT INTO STUDENTS ... and runs it on Oracle

Step 7  Handler returns the new ID

Step 8  Minimal API returns HTTP 201 Created with the new ID in the response

Step 9  Blazor navigates back to the student list

Step 10 List page calls Http.GetFromJsonAsync("api/students?pageNumber=1&pageSize=10")

Step 11 MediatR routes to GetStudentsHandler
        → Dapper runs SELECT ... FROM STUDENTS OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY
        → Returns List<StudentDto>

Step 12 FluentDataGrid displays the updated list""",
        language="text",
    )

    # ── 22. Summary Table ──────────────────────────────────────────────────────
    subsection("22. CQRS Responsibility Summary")
    st.markdown(
        """
| Layer | File | Responsibility |
|---|---|---|
| **UI** | `StudentList.razor` | Show list, delete button → calls API |
| **UI** | `StudentForm.razor` | Form with Fluent UI → calls API |
| **API** | `StudentEndpoints.cs` | HTTP routing → delegates to MediatR |
| **Command** | `CreateStudentCommand.cs` | Carries create input |
| **Command Handler** | `CreateStudentHandler.cs` | Creates entity, saves via EF Core |
| **Command** | `UpdateStudentCommand.cs` | Carries update input |
| **Command Handler** | `UpdateStudentHandler.cs` | Loads entity, updates, saves via EF Core |
| **Command** | `DeleteStudentCommand.cs` | Carries delete ID |
| **Command Handler** | `DeleteStudentHandler.cs` | Loads entity, deletes via EF Core |
| **Query** | `GetStudentsQuery.cs` | Carries page number and page size |
| **Query Handler** | `GetStudentsHandler.cs` | Runs paginated SQL via Dapper |
| **Query** | `GetStudentByIdQuery.cs` | Carries student ID |
| **Query Handler** | `GetStudentByIdHandler.cs` | Runs single-row SQL via Dapper |
| **Domain** | `Student.cs` | Business entity with rules |
| **Infrastructure** | `AppDbContext.cs` | EF Core Oracle gateway |
| **Infrastructure** | `StudentRepository.cs` | EF Core write access |
"""
    )

    # ── 23. Common Beginner Mistakes ──────────────────────────────────────────
    subsection("23. Common Beginner Mistakes")
    paragraph(
        "**Mistake 1: Putting business logic in the endpoint** — "
        "The endpoint should only route. Business rules belong in the command handler."
    )
    paragraph(
        "**Mistake 2: Using EF Core on the query side** — "
        "EF Core is slower for reads because it tracks entities. Use Dapper for queries."
    )
    paragraph(
        "**Mistake 3: Returning domain entities from query handlers** — "
        "Return DTOs. Domain entities contain private setters and rules that do not belong in the UI."
    )
    paragraph(
        "**Mistake 4: One big handler that does everything** — "
        "Each handler must do exactly one thing. If a handler does two things, split it."
    )
    paragraph(
        "**Mistake 5: Skipping validation** — "
        "Always validate commands with FluentValidation before they reach the handler. "
        "Never rely on the UI alone for validation."
    )

    # ── 24. Benefits ──────────────────────────────────────────────────────────
    subsection("24. Summary of Benefits")
    st.markdown(
        """
| Benefit | How CQRS Delivers It |
|---|---|
| **Clean code** | Each class has one job — easy to read and maintain |
| **Performance** | Dapper handles reads with raw SQL — much faster for lists and reports |
| **Testability** | Handlers are small and isolated — easy to unit test with mock repositories |
| **Scalability** | Read and write sides can be scaled or even deployed separately if needed |
| **Consistency** | MediatR + handlers enforce a consistent structure across the whole team |
| **Auditability** | Every change is a named command — easy to log, replay, or audit |
"""
    )

    # ── 25. Recommended Development Steps ────────────────────────────────────
    subsection("25. Recommended Development Steps for a New Feature")
    paragraph("When adding any new feature, follow this order:")
    code_block(
        """For a new entity (e.g., Course):

Write side:
  1. Create domain entity  (Domain/Entities/Course.cs)
  2. Add DbSet to DbContext and configure mapping
  3. Create repository interface and implementation
  4. Create CreateCourseCommand + CreateCourseHandler
  5. Create UpdateCourseCommand + UpdateCourseHandler
  6. Create DeleteCourseCommand + DeleteCourseHandler
  7. Add validators for each command
  8. Add Minimal API endpoints for write operations

Read side:
  9. Create CourseDto
  10. Create GetCoursesQuery + GetCoursesHandler (Dapper)
  11. Create GetCourseByIdQuery + GetCourseByIdHandler (Dapper)
  12. Add Minimal API endpoints for read operations

UI:
  13. Create CourseList.razor (FluentDataGrid + FluentButton)
  14. Create CourseForm.razor (FluentTextField + FluentButton + EditForm)
  15. Wire navigation between list and form""",
        language="text",
    )
