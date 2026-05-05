"""Unit Testing — overview landing page for the sub-menu section."""

from components.content import (
    paragraph,
    section_intro,
    section_title,
    subsection,
)


def render_unit_testing():
    section_title(
        "Unit Testing",
        "Write automated checks that prove every layer of your code works.",
    )
    section_intro(
        "Automated testing is one of the most valuable skills a developer can build. "
        "It catches bugs early, lets you refactor without fear, and acts as living "
        "documentation. This section is split into three focused sub-pages — choose "
        "the one that matches where you are right now."
    )

    subsection("What you will learn in this section")
    paragraph(
        "The three sub-pages below build on each other in a natural progression. "
        "Start with TDD to understand the philosophy, then move to Unit Test for the "
        "mechanics of writing great tests, and finish with Integration Test to see how "
        "all the pieces work together."
    )

    subsection("TDD — Test-Driven Development")
    paragraph(
        "TDD flips the usual approach: you write the test before you write the code. "
        "The famous **Red → Green → Refactor** cycle gives you a clear rhythm and "
        "prevents over-engineering. You will see TDD applied to a real form-submission "
        "workflow — validating comments, triggering status changes, and enforcing "
        "business rules — step by step."
    )

    subsection("Unit Test")
    paragraph(
        "A unit test checks one small piece of logic in complete isolation. "
        "This sub-page covers the **Arrange-Act-Assert** pattern, the three major "
        ".NET testing frameworks (xUnit, NUnit, MSTest), mocking with Moq, and "
        "practical examples drawn from the same form-based application: testing that "
        "Save is blocked when comments are empty, that status transitions are correct, "
        "and that the Manager approval logic behaves as expected."
    )

    subsection("Integration Test")
    paragraph(
        "Integration tests verify that multiple components — services, repositories, "
        "the database, the HTTP layer — work correctly together. This sub-page shows "
        "how to use **WebApplicationFactory** to spin up a real in-memory ASP.NET "
        "server, seed test data, and assert on end-to-end behaviour: submitting the "
        "form, checking the status history popup, and exercising the full "
        "Save → Submit → Approve flow."
    )

    subsection("The application we test throughout")
    paragraph(
        "All three sub-pages use the same sample application so examples connect "
        "across them. The application is a **form submission system** with:"
    )
    paragraph("- A **status bar** showing Current Status, Last Updated By, Last Updated On, and a Status History button that opens a popup.")
    paragraph("- A **year dropdown** (e.g. 2025-2026) with an Update button on the landing page.")
    paragraph("- A **data grid** where rows contain a Textbox, a Date picker, and read-only fields.")
    paragraph("- **Save**, **Cancel**, and **Send for Approval** buttons.")
    paragraph("- **Admin Comments** and **Manager Comments** text areas.")
    paragraph("- Validation: Save and Send for Approval are **blocked when comments are empty**.")
    paragraph("- A **Manager role** that can Approve or Return a Saved/Submitted form.")
