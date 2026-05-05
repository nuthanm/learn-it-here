"""Unit Testing → Unit Test sub-page: frameworks, patterns, and practical examples."""

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
        "Unit Test",
        "Test one piece of logic in isolation — fast, focused, and repeatable.",
    )
    section_intro(
        "A unit test exercises a single method or class with all external dependencies "
        "replaced by fakes. Each test runs in milliseconds, gives you an exact failure "
        "message, and can be run thousands of times a day without touching a database "
        "or a network."
    )

    subsection("What is a unit?")
    paragraph(
        "A 'unit' is the smallest piece of code that makes sense to test on its own — "
        "usually a single public method. The key constraint is **isolation**: if the "
        "method calls a database, an API, or the file system, those are replaced with "
        "controlled fakes (mocks/stubs) so the test only verifies the logic inside "
        "the method itself."
    )

    subsection("The Arrange-Act-Assert (AAA) pattern")
    paragraph("Every unit test has exactly three parts:")
    paragraph("**Arrange** — create the objects and data the test needs.")
    paragraph("**Act** — call the single method you are testing.")
    paragraph("**Assert** — verify the result is what you expected.")
    code_block(
        """[Fact]
public void Save_WithAdminComments_SetsStatusToSaved()
{
    // Arrange
    var service = new FormService();
    var form = new FormModel { AdminComments = "All checked", Status = FormStatus.Draft };

    // Act
    service.Save(form, updatedBy: "alice@example.com");

    // Assert
    Assert.Equal(FormStatus.Saved, form.Status);
    Assert.Equal("alice@example.com", form.LastUpdatedBy);
}""",
        language="csharp",
    )

    subsection("xUnit vs NUnit vs MSTest at a glance")
    st.markdown(
        """
| Feature | xUnit | NUnit | MSTest |
|---|---|---|---|
| Test marker | `[Fact]` / `[Theory]` | `[Test]` / `[TestCase]` | `[TestMethod]` / `[DataTestMethod]` |
| Class marker | *(none needed)* | `[TestFixture]` | `[TestClass]` |
| Setup | Constructor | `[SetUp]` | `[TestInitialize]` |
| Teardown | `IDisposable.Dispose()` | `[TearDown]` | `[TestCleanup]` |
| Parameterised | `[InlineData]` | `[TestCase]` | `[DataRow]` |
| Assertion style | `Assert.Equal(expected, actual)` | `Assert.That(actual, Is.EqualTo(expected))` | `Assert.AreEqual(expected, actual)` |
| Install | `dotnet new xunit` | `dotnet new nunit` | `dotnet new mstest` |
| Best for | Modern .NET / new projects | Teams from Java/JUnit background | Pure Microsoft / Visual Studio shops |
"""
    )
    paragraph(
        "**Recommendation for beginners:** use xUnit — it is the de-facto standard "
        "for .NET Core and has the simplest setup."
    )

    subsection("The form application model")
    paragraph(
        "All examples below test the same `FormService` class used throughout this "
        "section. Here is the domain model for reference."
    )
    code_block(
        """public enum FormStatus { Draft, Saved, Submitted, Approved, Returned }

public class FormModel
{
    public string AdminComments   { get; set; } = string.Empty;
    public string ManagerComments { get; set; } = string.Empty;
    public FormStatus Status      { get; set; } = FormStatus.Draft;
    public string LastUpdatedBy   { get; set; } = string.Empty;
    public DateTime LastUpdatedOn { get; set; }
}""",
        language="csharp",
    )

    subsection("Testing validation: comments are required")
    paragraph(
        "The business rule: Save and Send for Approval must throw when "
        "Admin Comments are empty. A parameterised test covers both actions at once."
    )
    tabs_validation = st.tabs(["xUnit", "NUnit", "MSTest"])

    with tabs_validation[0]:
        code_block(
            """// xUnit — [Theory] runs the test once per [InlineData] row
[Theory]
[InlineData("")]
[InlineData("   ")]  // whitespace only should also fail
public void Save_WithEmptyOrWhitespaceComments_ThrowsInvalidOperationException(string comments)
{
    var service = new FormService();
    var form = new FormModel { AdminComments = comments, Status = FormStatus.Draft };

    Assert.Throws<InvalidOperationException>(() => service.Save(form));
}

[Theory]
[InlineData("")]
[InlineData("   ")]
public void SendForApproval_WithEmptyOrWhitespaceComments_ThrowsInvalidOperationException(
    string comments)
{
    var service = new FormService();
    var form = new FormModel { AdminComments = comments };

    Assert.Throws<InvalidOperationException>(() =>
        service.SendForApproval(form, submittedBy: "alice@example.com"));
}""",
            language="csharp",
        )

    with tabs_validation[1]:
        code_block(
            """// NUnit — [TestCase] attribute
[TestCase("")]
[TestCase("   ")]
public void Save_WithEmptyOrWhitespaceComments_ThrowsInvalidOperationException(string comments)
{
    var service = new FormService();
    var form = new FormModel { AdminComments = comments, Status = FormStatus.Draft };

    Assert.Throws<InvalidOperationException>(() => service.Save(form));
}

[TestCase("")]
[TestCase("   ")]
public void SendForApproval_WithEmptyComments_ThrowsInvalidOperationException(string comments)
{
    var service = new FormService();
    var form = new FormModel { AdminComments = comments };

    Assert.Throws<InvalidOperationException>(() =>
        service.SendForApproval(form, submittedBy: "alice@example.com"));
}""",
            language="csharp",
        )

    with tabs_validation[2]:
        code_block(
            """// MSTest — [DataTestMethod] + [DataRow]
[DataTestMethod]
[DataRow("")]
[DataRow("   ")]
public void Save_WithEmptyOrWhitespaceComments_ThrowsInvalidOperationException(string comments)
{
    var service = new FormService();
    var form = new FormModel { AdminComments = comments, Status = FormStatus.Draft };

    Assert.ThrowsException<InvalidOperationException>(() => service.Save(form));
}

[DataTestMethod]
[DataRow("")]
[DataRow("   ")]
public void SendForApproval_WithEmptyComments_ThrowsInvalidOperationException(string comments)
{
    var service = new FormService();
    var form = new FormModel { AdminComments = comments };

    Assert.ThrowsException<InvalidOperationException>(() =>
        service.SendForApproval(form, submittedBy: "alice@example.com"));
}""",
            language="csharp",
        )

    subsection("Testing status transitions")
    paragraph(
        "Each action must move the form to the correct status. These tests confirm "
        "the happy-path transitions."
    )
    code_block(
        """// xUnit examples — same logic applies in NUnit/MSTest with different attributes

[Fact]
public void Save_WithComments_SetsStatusToSaved()
{
    var service = new FormService();
    var form = new FormModel { AdminComments = "Reviewed", Status = FormStatus.Draft };

    service.Save(form, updatedBy: "alice@example.com");

    Assert.Equal(FormStatus.Saved, form.Status);
    Assert.Equal("alice@example.com", form.LastUpdatedBy);
}

[Fact]
public void SendForApproval_WithComments_SetsStatusToSubmitted()
{
    var service = new FormService();
    var form = new FormModel { AdminComments = "Ready to submit", Status = FormStatus.Saved };

    service.SendForApproval(form, submittedBy: "alice@example.com");

    Assert.Equal(FormStatus.Submitted, form.Status);
}""",
        language="csharp",
    )

    subsection("Testing Manager actions: Approve and Return")
    paragraph(
        "A Manager can Approve or Return a form only if its status is Saved or Submitted. "
        "A `[Theory]` lets us cover both statuses without duplicating the test body."
    )
    code_block(
        """// Approve happy path — both Saved and Submitted are valid starting statuses
[Theory]
[InlineData(FormStatus.Saved)]
[InlineData(FormStatus.Submitted)]
public void Approve_WhenSavedOrSubmitted_SetsStatusToApproved(FormStatus initial)
{
    var service = new FormService();
    var form = new FormModel
    {
        AdminComments   = "Done",
        ManagerComments = "Looks great",
        Status = initial
    };

    service.Approve(form, managerName: "bob@example.com");

    Assert.Equal(FormStatus.Approved, form.Status);
    Assert.Equal("bob@example.com", form.LastUpdatedBy);
}

// Return happy path
[Theory]
[InlineData(FormStatus.Saved)]
[InlineData(FormStatus.Submitted)]
public void Return_WhenSavedOrSubmitted_SetsStatusToReturned(FormStatus initial)
{
    var service = new FormService();
    var form = new FormModel
    {
        AdminComments   = "Done",
        ManagerComments = "Needs more detail",
        Status = initial
    };

    service.Return(form, managerName: "bob@example.com");

    Assert.Equal(FormStatus.Returned, form.Status);
}

// Guard: draft forms cannot be approved
[Fact]
public void Approve_WhenStatusIsDraft_ThrowsInvalidOperationException()
{
    var service = new FormService();
    var form = new FormModel { AdminComments = "Done", Status = FormStatus.Draft };

    Assert.Throws<InvalidOperationException>(() =>
        service.Approve(form, managerName: "bob@example.com"));
}""",
        language="csharp",
    )

    subsection("Mocking external dependencies with Moq")
    paragraph(
        "When `FormService` needs to save to a database or call an audit log service, "
        "you **mock** those dependencies so the test stays fast and isolated. "
        "Moq is the most popular mocking library for .NET."
    )
    code_block(
        """# Add Moq to the test project
dotnet add package Moq""",
        language="bash",
    )
    code_block(
        """// Suppose FormService depends on IFormRepository to persist the form
public interface IFormRepository
{
    void Save(FormModel form);
}

public class FormService
{
    private readonly IFormRepository _repo;

    public FormService(IFormRepository repo)
    {
        _repo = repo;
    }

    public void Save(FormModel form, string updatedBy = "")
    {
        if (string.IsNullOrWhiteSpace(form.AdminComments))
            throw new InvalidOperationException("Admin Comments are required.");

        form.Status = FormStatus.Saved;
        form.LastUpdatedBy = updatedBy;
        form.LastUpdatedOn = DateTime.UtcNow;

        _repo.Save(form);   // persist
    }
}""",
        language="csharp",
    )
    code_block(
        """using Moq;
using Xunit;

public class FormServiceTests
{
    [Fact]
    public void Save_WithComments_CallsRepositorySaveOnce()
    {
        // Arrange: create a mock that does nothing but records calls
        var mockRepo = new Mock<IFormRepository>();
        var service  = new FormService(mockRepo.Object);
        var form     = new FormModel { AdminComments = "OK", Status = FormStatus.Draft };

        // Act
        service.Save(form, updatedBy: "alice@example.com");

        // Assert: repository.Save was called exactly once with our form
        mockRepo.Verify(r => r.Save(form), Times.Once);
    }

    [Fact]
    public void Save_WithNoComments_NeverCallsRepository()
    {
        // Arrange
        var mockRepo = new Mock<IFormRepository>();
        var service  = new FormService(mockRepo.Object);
        var form     = new FormModel { AdminComments = "", Status = FormStatus.Draft };

        // Act
        Assert.Throws<InvalidOperationException>(() => service.Save(form));

        // Assert: repository should never have been called
        mockRepo.Verify(r => r.Save(It.IsAny<FormModel>()), Times.Never);
    }
}""",
        language="csharp",
    )

    subsection("How to run unit tests")
    code_block(
        """# Run all tests
dotnet test

# Verbose output — shows each test name
dotnet test --verbosity normal

# Filter to a specific class
dotnet test --filter "FullyQualifiedName~FormServiceTests"

# Filter to tests whose name contains a keyword
dotnet test --filter "Save"

# Run tests and generate a code-coverage report
dotnet test --collect:"XPlat Code Coverage"
reportgenerator -reports:"TestResults/**/coverage.cobertura.xml" -targetdir:"coverage-html" """,
        language="bash",
    )

    subsection("Unit test quick-reference and best practices")
    st.markdown(
        """
| # | Practice | Why it matters |
|---|---|---|
| 1 | Name tests: `Method_Scenario_ExpectedResult` | Instantly clear what failed and why |
| 2 | One assertion per test (ideally) | Pinpoints exactly what broke |
| 3 | Never test framework/library code | Trust the framework; test YOUR logic |
| 4 | Use mocks for DB, API, file system | Tests stay fast and isolated |
| 5 | Keep tests independent — no shared mutable state | Order should never matter |
| 6 | Aim for 80%+ coverage on business logic | Good safety net for refactoring |
| 7 | Run tests on every commit (CI/CD) | Catch breaks before they reach main |
| 8 | Each test should run in < 100 ms | Slow tests get skipped |
| 9 | Test edge cases: empty string, null, boundary values | Bugs hide at the edges |
| 10 | If a test is hard to write, the code is probably too complex | Refactor the production code |
"""
    )
