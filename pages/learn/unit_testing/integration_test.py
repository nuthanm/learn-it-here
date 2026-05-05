"""Unit Testing → Integration Test sub-page: beginner-friendly intro to integration testing."""

import streamlit as st

from components.content import (
    code_block,
    paragraph,
    section_intro,
    section_title,
    subsection,
)


def render():
    section_title(
        "Integration Test",
        "Verify that multiple components work correctly together — end-to-end.",
    )
    section_intro(
        "Unit tests prove that each piece of logic works in isolation. Integration tests "
        "prove that the pieces work together: the HTTP controller calls the service, the "
        "service talks to the database, and the database stores what you sent. "
        "They are slower than unit tests but catch a completely different class of bug."
    )

    subsection("Unit test vs integration test — what is the difference?")
    st.markdown(
        """
| Aspect | Unit Test | Integration Test |
|---|---|---|
| What it tests | One method / class in isolation | Multiple layers working together |
| Dependencies | All faked (mocks/stubs) | Real (or in-memory) database, real HTTP stack |
| Speed | Very fast (< 1 ms each) | Slower (10 ms – 1 s each) |
| Failure message | Points to exact line | Points to the interaction between components |
| When to use | Every business rule, validation, calculation | Save/Submit/Approve flows, API contracts, DB queries |
| .NET tooling | xUnit / NUnit / MSTest alone | xUnit + `WebApplicationFactory` + EF Core in-memory / SQLite |
"""
    )

    subsection("The integration test pyramid")
    paragraph(
        "Think of testing as a pyramid. Unit tests form the wide base — you write "
        "many of them because they are cheap. Integration tests sit in the middle — "
        "fewer, but they cover the connections. End-to-end (browser) tests are at the "
        "top — fewest, most expensive."
    )
    paragraph("- **Many** unit tests — fast, targeted, run on every save.")
    paragraph("- **Some** integration tests — cover critical flows, run on every pull request.")
    paragraph("- **Few** end-to-end tests — cover the most important user journeys, run nightly.")

    subsection("Setting up integration tests in ASP.NET Core")
    paragraph(
        "`WebApplicationFactory<TEntryPoint>` lets you spin up a real in-memory instance "
        "of your ASP.NET application — the full middleware pipeline, real controllers, "
        "real services — but with an in-memory or SQLite database so nothing hits production."
    )
    code_block(
        """# Add required packages to the test project
dotnet add package Microsoft.AspNetCore.Mvc.Testing
dotnet add package Microsoft.EntityFrameworkCore.InMemory""",
        language="bash",
    )
    code_block(
        """// FormApp.Tests/IntegrationTests/CustomWebApplicationFactory.cs
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using FormApp.Infrastructure;   // where AppDbContext lives

public class CustomWebApplicationFactory : WebApplicationFactory<Program>
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            // Remove the real database registration
            var descriptor = services.SingleOrDefault(
                d => d.ServiceType == typeof(DbContextOptions<AppDbContext>));
            if (descriptor != null)
                services.Remove(descriptor);

            // Replace it with an in-memory database (unique name per test run)
            services.AddDbContext<AppDbContext>(options =>
                options.UseInMemoryDatabase("TestDb_" + Guid.NewGuid()));
        });
    }
}""",
        language="csharp",
    )

    subsection("Integration test: Save endpoint — happy path")
    paragraph(
        "We POST a form with Admin Comments to the Save endpoint and assert that the "
        "HTTP response is 200 OK and the database record has status Saved."
    )
    code_block(
        """// FormApp.Tests/IntegrationTests/FormSaveTests.cs
using System.Net;
using System.Net.Http.Json;
using Microsoft.Extensions.DependencyInjection;
using Xunit;
using FormApp.Infrastructure;
using FormApp.Core;

public class FormSaveTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly HttpClient _client;
    private readonly CustomWebApplicationFactory _factory;

    public FormSaveTests(CustomWebApplicationFactory factory)
    {
        _factory = factory;
        _client  = factory.CreateClient();
    }

    [Fact]
    public async Task PostSave_WithAdminComments_Returns200AndSetsSavedStatus()
    {
        // Arrange: seed a draft form into the in-memory DB
        int formId;
        using (var scope = _factory.Services.CreateScope())
        {
            var db   = scope.ServiceProvider.GetRequiredService<AppDbContext>();
            var form = new FormModel { AdminComments = "", Status = FormStatus.Draft };
            db.Forms.Add(form);
            await db.SaveChangesAsync();
            formId = form.Id;
        }

        var payload = new { FormId = formId, AdminComments = "All reviewed" };

        // Act
        var response = await _client.PostAsJsonAsync("/api/form/save", payload);

        // Assert HTTP layer
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        // Assert database layer
        using (var scope = _factory.Services.CreateScope())
        {
            var db   = scope.ServiceProvider.GetRequiredService<AppDbContext>();
            var form = await db.Forms.FindAsync(formId);

            Assert.NotNull(form);
            Assert.Equal(FormStatus.Saved, form.Status);
        }
    }
}""",
        language="csharp",
    )

    subsection("Integration test: Save endpoint — validation failure")
    paragraph(
        "When Admin Comments are empty the endpoint must return 400 Bad Request "
        "and must NOT change the form status in the database."
    )
    code_block(
        """[Fact]
public async Task PostSave_WithEmptyAdminComments_Returns400AndDoesNotChangeStatus()
{
    // Arrange
    int formId;
    using (var scope = _factory.Services.CreateScope())
    {
        var db   = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        var form = new FormModel { AdminComments = "", Status = FormStatus.Draft };
        db.Forms.Add(form);
        await db.SaveChangesAsync();
        formId = form.Id;
    }

    var payload = new { FormId = formId, AdminComments = "" };  // empty!

    // Act
    var response = await _client.PostAsJsonAsync("/api/form/save", payload);

    // Assert HTTP layer
    Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);

    // Assert DB was not modified
    using (var scope = _factory.Services.CreateScope())
    {
        var db   = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        var form = await db.Forms.FindAsync(formId);

        Assert.Equal(FormStatus.Draft, form!.Status);  // unchanged
    }
}""",
        language="csharp",
    )

    subsection("Integration test: Send for Approval flow")
    paragraph(
        "A form must move from Draft → Saved → Submitted in two separate API calls. "
        "This test verifies the full two-step flow."
    )
    code_block(
        """[Fact]
public async Task FullSaveAndSendForApproval_Flow_SetsStatusToSubmitted()
{
    // Arrange
    int formId;
    using (var scope = _factory.Services.CreateScope())
    {
        var db   = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        var form = new FormModel { AdminComments = "", Status = FormStatus.Draft };
        db.Forms.Add(form);
        await db.SaveChangesAsync();
        formId = form.Id;
    }

    // Step 1: Save
    await _client.PostAsJsonAsync("/api/form/save", new
    {
        FormId = formId,
        AdminComments = "Initial review complete"
    });

    // Step 2: Send for Approval
    var sendResponse = await _client.PostAsJsonAsync("/api/form/send-for-approval", new
    {
        FormId = formId
    });

    // Assert final HTTP response
    Assert.Equal(HttpStatusCode.OK, sendResponse.StatusCode);

    // Assert final database state
    using (var scope = _factory.Services.CreateScope())
    {
        var db   = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        var form = await db.Forms.FindAsync(formId);

        Assert.Equal(FormStatus.Submitted, form!.Status);
    }
}""",
        language="csharp",
    )

    subsection("Integration test: Manager Approve flow")
    paragraph(
        "After the form is Submitted, a Manager logs in (passed as a header here for "
        "simplicity) and calls the Approve endpoint. We verify the status becomes Approved."
    )
    code_block(
        """[Fact]
public async Task ManagerApprove_AfterSubmit_SetsStatusToApproved()
{
    // Arrange: seed a Submitted form directly
    int formId;
    using (var scope = _factory.Services.CreateScope())
    {
        var db   = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        var form = new FormModel
        {
            AdminComments   = "All good",
            ManagerComments = "",
            Status          = FormStatus.Submitted
        };
        db.Forms.Add(form);
        await db.SaveChangesAsync();
        formId = form.Id;
    }

    // Simulate a Manager request by adding a role header
    var request = new HttpRequestMessage(HttpMethod.Post, "/api/form/approve")
    {
        Content = JsonContent.Create(new
        {
            FormId          = formId,
            ManagerComments = "Approved — looks great"
        })
    };
    request.Headers.Add("X-User-Role", "Manager");

    // Act
    var response = await _client.SendAsync(request);

    // Assert HTTP
    Assert.Equal(HttpStatusCode.OK, response.StatusCode);

    // Assert DB
    using (var scope = _factory.Services.CreateScope())
    {
        var db   = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        var form = await db.Forms.FindAsync(formId);

        Assert.Equal(FormStatus.Approved, form!.Status);
        Assert.Equal("Approved — looks great", form.ManagerComments);
    }
}""",
        language="csharp",
    )

    subsection("Integration test: Status History popup data")
    paragraph(
        "The Status History popup loads a list of historical status changes for a form. "
        "This test seeds two history records and verifies the GET endpoint returns them "
        "in chronological order."
    )
    code_block(
        """[Fact]
public async Task GetStatusHistory_ReturnsAllRecordsInChronologicalOrder()
{
    // Arrange: seed a form with two history entries
    int formId;
    using (var scope = _factory.Services.CreateScope())
    {
        var db   = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        var form = new FormModel { AdminComments = "Done", Status = FormStatus.Submitted };
        db.Forms.Add(form);
        await db.SaveChangesAsync();
        formId = form.Id;

        db.StatusHistory.AddRange(
            new StatusHistory
            {
                FormId    = formId,
                Status    = FormStatus.Saved,
                ChangedBy = "alice@example.com",
                ChangedOn = DateTime.UtcNow.AddMinutes(-10)
            },
            new StatusHistory
            {
                FormId    = formId,
                Status    = FormStatus.Submitted,
                ChangedBy = "alice@example.com",
                ChangedOn = DateTime.UtcNow
            }
        );
        await db.SaveChangesAsync();
    }

    // Act
    var response = await _client.GetAsync($"/api/form/{formId}/status-history");

    // Assert HTTP
    Assert.Equal(HttpStatusCode.OK, response.StatusCode);

    // Assert body
    var history = await response.Content
        .ReadFromJsonAsync<List<StatusHistoryDto>>();

    Assert.NotNull(history);
    Assert.Equal(2, history.Count);
    Assert.Equal(FormStatus.Saved,     history[0].Status);   // oldest first
    Assert.Equal(FormStatus.Submitted, history[1].Status);
}""",
        language="csharp",
    )

    subsection("Integration test: Year dropdown Update")
    paragraph(
        "The landing page has a year dropdown (e.g. 2025-2026). Clicking Update "
        "filters the grid data to that year. This test posts an update-year request "
        "and verifies the grid returns only rows for the selected year."
    )
    code_block(
        """[Fact]
public async Task UpdateYear_FiltersGridDataToSelectedYear()
{
    // Arrange: seed two forms for different years
    using (var scope = _factory.Services.CreateScope())
    {
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        db.Forms.AddRange(
            new FormModel { AcademicYear = "2024-2025", AdminComments = "Old", Status = FormStatus.Saved },
            new FormModel { AcademicYear = "2025-2026", AdminComments = "New", Status = FormStatus.Draft }
        );
        await db.SaveChangesAsync();
    }

    // Act: request grid data for year 2025-2026
    var response = await _client.GetAsync("/api/form/grid?year=2025-2026");

    // Assert
    Assert.Equal(HttpStatusCode.OK, response.StatusCode);

    var rows = await response.Content.ReadFromJsonAsync<List<FormGridRowDto>>();
    Assert.NotNull(rows);
    Assert.All(rows, r => Assert.Equal("2025-2026", r.AcademicYear));
}""",
        language="csharp",
    )

    subsection("Running integration tests separately from unit tests")
    paragraph(
        "Integration tests are slower, so you typically run them only on pull requests "
        "rather than on every file save. Use a custom trait to separate them."
    )
    code_block(
        """// Mark every integration test class with this attribute
[Trait("Category", "Integration")]
public class FormSaveTests : IClassFixture<CustomWebApplicationFactory> { ... }""",
        language="csharp",
    )
    code_block(
        """# Run only unit tests (fast — on every file save)
dotnet test --filter "Category!=Integration"

# Run only integration tests (slower — on pull request)
dotnet test --filter "Category=Integration"

# Run everything
dotnet test""",
        language="bash",
    )

    subsection("Integration testing best practices")
    st.markdown(
        """
| # | Practice | Why it matters |
|---|---|---|
| 1 | Use a fresh in-memory DB per test class | Tests never interfere with each other |
| 2 | Seed data in the Arrange step — don't rely on leftover data | Tests are predictable and repeatable |
| 3 | Assert both the HTTP response AND the DB state | Catch bugs in the controller *and* the persistence layer |
| 4 | Keep integration tests in a separate project or folder | Easy to run them separately from fast unit tests |
| 5 | Use `IClassFixture` for the factory — not `IDisposable` per test | Reuses the web server across tests in the same class (faster) |
| 6 | Do NOT mock the database in integration tests | The whole point is to test with the real data layer |
| 7 | Mark them with `[Trait("Category","Integration")]` | Lets CI run unit and integration tests in separate steps |
| 8 | Integration tests should still be deterministic | Avoid `Thread.Sleep`, random data, or time-sensitive assertions |
"""
    )
