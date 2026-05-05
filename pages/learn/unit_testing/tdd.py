"""Unit Testing → TDD sub-page: beginner-friendly introduction to Test-Driven Development."""

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
        "TDD — Test-Driven Development",
        "Write the test first, then write just enough code to make it pass.",
    )
    section_intro(
        "TDD sounds backwards at first — why write a test before the code exists? "
        "But the discipline of describing *what the code should do* before you write it "
        "leads to cleaner design, fewer bugs, and tests that actually prove your code works "
        "rather than tests written to make passing numbers look good."
    )

    subsection("The Red → Green → Refactor cycle")
    paragraph("Every TDD session follows three short steps, repeated over and over:")
    paragraph(
        "**Red** — Write a test that describes the behaviour you want. Run it. "
        "It fails (red) because the code doesn't exist yet. That red bar is good — "
        "it proves your test is actually checking something."
    )
    paragraph(
        "**Green** — Write the *minimum* code needed to make the test pass. Don't "
        "worry about elegance yet. The goal is a green bar."
    )
    paragraph(
        "**Refactor** — Clean up the code (and the test) without changing behaviour. "
        "The green test suite tells you immediately if you accidentally broke something."
    )

    subsection("Why TDD leads to better code")
    paragraph("- You only write code that is needed — no speculative features.")
    paragraph("- Each class/method stays small because you design around testability.")
    paragraph("- You get instant feedback every few minutes instead of debugging later.")
    paragraph("- The tests double as living documentation of every business rule.")

    subsection("The application we will TDD")
    paragraph(
        "We will build the core business logic for a **form submission system**. "
        "The rules are:"
    )
    paragraph("1. A form can be Saved only if Admin Comments are not empty.")
    paragraph("2. A form can be Sent for Approval only if Admin Comments are not empty.")
    paragraph("3. A Manager can Approve or Return a form that is in Saved or Submitted status.")
    paragraph("4. Approve transitions the status to Approved; Return transitions it to Returned.")
    paragraph(
        "We will TDD these rules one failing test at a time, building up the "
        "`FormService` class from nothing."
    )

    subsection("Step 0 — Project setup")
    code_block(
        """# Create the main project
dotnet new classlib -n FormApp.Core

# Create the test project
dotnet new xunit -n FormApp.Tests

# Add a reference from the test project to the main project
cd FormApp.Tests
dotnet add reference ../FormApp.Core/FormApp.Core.csproj

# Run tests (all pass — zero tests yet)
dotnet test""",
        language="bash",
    )

    subsection("Step 1 — RED: write the first failing test")
    paragraph(
        "The first rule: Save must fail when Admin Comments are empty. "
        "Write a test that calls `FormService.Save()` with no comments and "
        "expects an `InvalidOperationException`."
    )
    code_block(
        """// FormApp.Tests/FormServiceTests.cs
using Xunit;
using FormApp.Core;

public class FormServiceTests
{
    // RED: FormService doesn't exist yet — this will not even compile.
    [Fact]
    public void Save_WithNoAdminComments_ThrowsInvalidOperationException()
    {
        // Arrange
        var service = new FormService();
        var form = new FormModel
        {
            AdminComments = "",   // empty — should block Save
            Status = FormStatus.Draft
        };

        // Act & Assert
        Assert.Throws<InvalidOperationException>(() => service.Save(form));
    }
}""",
        language="csharp",
    )
    paragraph(
        "Run `dotnet test`. The build fails because `FormService`, `FormModel`, and "
        "`FormStatus` do not exist. That is the **Red** step."
    )

    subsection("Step 2 — GREEN: write the minimum code to pass")
    paragraph(
        "Add only what is needed to make the test compile and pass. No extra logic yet."
    )
    code_block(
        """// FormApp.Core/FormStatus.cs
namespace FormApp.Core;

public enum FormStatus
{
    Draft,
    Saved,
    Submitted,
    Approved,
    Returned,
}""",
        language="csharp",
    )
    code_block(
        """// FormApp.Core/FormModel.cs
namespace FormApp.Core;

public class FormModel
{
    public string AdminComments { get; set; } = string.Empty;
    public string ManagerComments { get; set; } = string.Empty;
    public FormStatus Status { get; set; } = FormStatus.Draft;
    public string LastUpdatedBy { get; set; } = string.Empty;
    public DateTime LastUpdatedOn { get; set; }
}""",
        language="csharp",
    )
    code_block(
        """// FormApp.Core/FormService.cs
namespace FormApp.Core;

public class FormService
{
    public void Save(FormModel form)
    {
        if (string.IsNullOrWhiteSpace(form.AdminComments))
            throw new InvalidOperationException("Admin Comments are required before saving.");
    }
}""",
        language="csharp",
    )
    paragraph(
        "Run `dotnet test`. The test is **Green**. We wrote the absolute minimum "
        "— nothing more."
    )

    subsection("Step 3 — REFACTOR")
    paragraph(
        "The code is already simple, but let's extract the validation message to a "
        "constant so it is easy to assert in multiple tests."
    )
    code_block(
        """// FormApp.Core/FormService.cs  (refactored)
namespace FormApp.Core;

public class FormService
{
    public const string MissingAdminCommentsError =
        "Admin Comments are required before saving.";

    public void Save(FormModel form)
    {
        if (string.IsNullOrWhiteSpace(form.AdminComments))
            throw new InvalidOperationException(MissingAdminCommentsError);
    }
}""",
        language="csharp",
    )
    paragraph("Run `dotnet test` again — still green. The refactor did not break anything.")

    subsection("Step 4 — RED again: add the Save happy-path test")
    paragraph(
        "We need to verify that Save *succeeds* when comments are present and updates "
        "the status and metadata."
    )
    code_block(
        """// Add to FormServiceTests.cs
[Fact]
public void Save_WithAdminComments_SetsStatusToSavedAndRecordsUpdater()
{
    // Arrange
    var service = new FormService();
    var form = new FormModel
    {
        AdminComments = "Looks good",
        Status = FormStatus.Draft
    };

    // Act
    service.Save(form, updatedBy: "alice@example.com");

    // Assert
    Assert.Equal(FormStatus.Saved, form.Status);
    Assert.Equal("alice@example.com", form.LastUpdatedBy);
}""",
        language="csharp",
    )
    paragraph("Run — Red (Save doesn't accept `updatedBy` yet).")

    subsection("Step 5 — GREEN: update Save to accept the updater")
    code_block(
        """// FormApp.Core/FormService.cs
public void Save(FormModel form, string updatedBy = "")
{
    if (string.IsNullOrWhiteSpace(form.AdminComments))
        throw new InvalidOperationException(MissingAdminCommentsError);

    form.Status = FormStatus.Saved;
    form.LastUpdatedBy = updatedBy;
    form.LastUpdatedOn = DateTime.UtcNow;
}""",
        language="csharp",
    )
    paragraph("Run — Green. Both tests pass.")

    subsection("Step 6 — TDD the Send for Approval rule")
    code_block(
        """// Add to FormServiceTests.cs

[Fact]
public void SendForApproval_WithNoAdminComments_ThrowsInvalidOperationException()
{
    var service = new FormService();
    var form = new FormModel { AdminComments = "", Status = FormStatus.Draft };

    Assert.Throws<InvalidOperationException>(() =>
        service.SendForApproval(form, submittedBy: "alice@example.com"));
}

[Fact]
public void SendForApproval_WithAdminComments_SetsStatusToSubmitted()
{
    var service = new FormService();
    var form = new FormModel { AdminComments = "Ready", Status = FormStatus.Saved };

    service.SendForApproval(form, submittedBy: "alice@example.com");

    Assert.Equal(FormStatus.Submitted, form.Status);
    Assert.Equal("alice@example.com", form.LastUpdatedBy);
}""",
        language="csharp",
    )
    paragraph("Run — Red. Add `SendForApproval` to `FormService`:")
    code_block(
        """public const string MissingSendCommentsError =
    "Admin Comments are required before sending for approval.";

public void SendForApproval(FormModel form, string submittedBy = "")
{
    if (string.IsNullOrWhiteSpace(form.AdminComments))
        throw new InvalidOperationException(MissingSendCommentsError);

    form.Status = FormStatus.Submitted;
    form.LastUpdatedBy = submittedBy;
    form.LastUpdatedOn = DateTime.UtcNow;
}""",
        language="csharp",
    )
    paragraph("Run — Green.")

    subsection("Step 7 — TDD the Manager Approve / Return rules")
    code_block(
        """// Add to FormServiceTests.cs

[Theory]
[InlineData(FormStatus.Saved)]
[InlineData(FormStatus.Submitted)]
public void Approve_WhenStatusIsSavedOrSubmitted_SetsStatusToApproved(FormStatus initial)
{
    var service = new FormService();
    var form = new FormModel
    {
        AdminComments = "Done",
        ManagerComments = "Approved",
        Status = initial
    };

    service.Approve(form, managerName: "bob@example.com");

    Assert.Equal(FormStatus.Approved, form.Status);
}

[Theory]
[InlineData(FormStatus.Saved)]
[InlineData(FormStatus.Submitted)]
public void Return_WhenStatusIsSavedOrSubmitted_SetsStatusToReturned(FormStatus initial)
{
    var service = new FormService();
    var form = new FormModel
    {
        AdminComments = "Done",
        ManagerComments = "Needs rework",
        Status = initial
    };

    service.Return(form, managerName: "bob@example.com");

    Assert.Equal(FormStatus.Returned, form.Status);
}

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
    paragraph("Run — Red. Add `Approve` and `Return` to `FormService`:")
    code_block(
        """public void Approve(FormModel form, string managerName = "")
{
    if (form.Status != FormStatus.Saved && form.Status != FormStatus.Submitted)
        throw new InvalidOperationException("Only Saved or Submitted forms can be approved.");

    form.Status = FormStatus.Approved;
    form.LastUpdatedBy = managerName;
    form.LastUpdatedOn = DateTime.UtcNow;
}

public void Return(FormModel form, string managerName = "")
{
    if (form.Status != FormStatus.Saved && form.Status != FormStatus.Submitted)
        throw new InvalidOperationException("Only Saved or Submitted forms can be returned.");

    form.Status = FormStatus.Returned;
    form.LastUpdatedBy = managerName;
    form.LastUpdatedOn = DateTime.UtcNow;
}""",
        language="csharp",
    )
    paragraph("Run — all tests Green.")

    subsection("Final test suite at a glance")
    st.markdown(
        """
| Test | Covers |
|---|---|
| `Save_WithNoAdminComments_Throws` | Validation blocks save when comments empty |
| `Save_WithAdminComments_SetsStatusToSaved` | Happy path saves and records updater |
| `SendForApproval_WithNoAdminComments_Throws` | Validation blocks submit when comments empty |
| `SendForApproval_WithAdminComments_SetsStatusToSubmitted` | Happy path submits correctly |
| `Approve_WhenSavedOrSubmitted_SetsApproved` (×2 via Theory) | Manager can approve |
| `Return_WhenSavedOrSubmitted_SetsReturned` (×2 via Theory) | Manager can return |
| `Approve_WhenDraft_Throws` | Manager cannot approve a Draft form |
"""
    )

    subsection("TDD golden rules")
    paragraph("- Write **one failing test** at a time — never two.")
    paragraph("- Write the **minimum code** to pass — resist the urge to add more.")
    paragraph("- Keep the **refactor step short** — do it while the tests are green.")
    paragraph("- **Never skip the Red step** — if the test passes before you write code, it is testing nothing.")
    paragraph("- Tests name business rules: `Save_WithNoAdminComments_Throws` is a specification.")
