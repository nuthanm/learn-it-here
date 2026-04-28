"""Unit Testing — minimal-layout page using shared content primitives."""

import streamlit as st

from components.content import (
    code_block,
    paragraph,
    section_intro,
    section_title,
    subsection,
)


def render_unit_testing():
    section_title(
        "Unit Testing",
        "Write small, automated checks that prove each unit of your code works.",
    )
    section_intro(
        "Unit tests verify a tiny, isolated piece of your application before a human "
        "ever clicks a button. They catch bugs early, enable confident refactoring, "
        "and act as living documentation."
    )

    subsection("What is unit testing?")
    paragraph(
        "Imagine you built a calculator. A unit test automatically checks that "
        "2 + 2 really returns 4 — and re-checks it every time you change any code. "
        "If you accidentally break the addition logic later, the test immediately "
        "fails and saves you from shipping a broken calculator."
    )
    paragraph("Why every developer should write unit tests:")
    paragraph("- Catch bugs early — find problems in seconds, not in production.")
    paragraph(
        "- Refactor confidently — change code without fear; tests tell you if you broke something."
    )
    paragraph("- Living documentation — tests show exactly how code is supposed to behave.")
    paragraph("- Faster debugging — a failing test pinpoints exactly which unit broke.")
    paragraph("- Required in most professional teams — companies expect developers to write tests.")

    subsection("The 3A pattern (Arrange-Act-Assert)")
    paragraph("Every unit test follows the same three-step structure:")
    paragraph("- Arrange — set up the data and objects you need.")
    paragraph("- Act — call the method or function you are testing.")
    paragraph("- Assert — verify the result is what you expected.")

    subsection("xUnit vs NUnit vs MSTest")
    paragraph(
        "There are three major unit testing frameworks for .NET. All three do the "
        "same job — the differences are syntax, features, and community preference."
    )
    st.markdown(
        """
| Feature | xUnit | NUnit | MSTest |
| --- | --- | --- | --- |
| Created by | James Newkirk & Brad Wilson (ex-NUnit creators) | Open-source community | Microsoft |
| First released | 2007 | 2000 (oldest) | 2005 |
| Current version | xUnit 2.x / 3.x | NUnit 3.x / 4.x | MSTest v2 / v3 |
| Preferred by | .NET Core / modern teams | Enterprise / Java-background devs | Visual Studio / Microsoft teams |
| Test marker attribute | `[Fact]` / `[Theory]` | `[Test]` / `[TestCase]` | `[TestMethod]` / `[DataTestMethod]` |
| Test class attribute | None needed | `[TestFixture]` | `[TestClass]` |
| Setup method | Constructor | `[SetUp]` | `[TestInitialize]` |
| Teardown method | `IDisposable.Dispose()` | `[TearDown]` | `[TestCleanup]` |
| One-time setup | `IClassFixture<T>` | `[OneTimeSetUp]` | `[ClassInitialize]` |
| Parameterised tests | `[Theory]` + `[InlineData]` | `[TestCase(...)]` | `[DataTestMethod]` + `[DataRow]` |
| Assertion library | `Assert.Equal` / `Throws` etc. | `Assert.That` / Classic Assert | `Assert.AreEqual` / `ThrowsException` |
| Parallel test execution | Yes, by default (per class) | Yes, configurable | Limited (opt-in) |
| IDE integration | Excellent (VS, Rider, VS Code) | Excellent | Best in Visual Studio |
| `dotnet test` support | Native | Native | Native |
| NuGet package | xunit, xunit.runner.visualstudio | NUnit, NUnit3TestAdapter | MSTest.TestFramework, MSTest.TestAdapter |
| Install template | `dotnet new xunit` | `dotnet new nunit` | `dotnet new mstest` |
| Community popularity (2024) | Most popular in .NET Core | Very popular (esp. legacy) | Common in MS-heavy shops |
| Learning curve | Easy | Easy (familiar to JUnit devs) | Easy |
| Best for | New .NET projects, open-source | Teams coming from Java/JUnit | Teams deep in Visual Studio ecosystem |
"""
    )
    paragraph(
        "Bottom line for beginners: pick xUnit for new projects — it is the de facto "
        "standard in modern .NET. Use NUnit if your team already uses it or if you "
        "are from a Java background. Use MSTest if you are in a pure Microsoft environment."
    )

    subsection("Same example in all three frameworks")
    paragraph(
        "We will test this simple Calculator class in xUnit, NUnit, and MSTest so you "
        "can see exactly how the same test looks in each framework. The business "
        "logic never changes — only the test attributes do."
    )
    code_block(
        """// The class we are testing (Calculator.cs) — same for all three frameworks
public class Calculator
{
    public int Add(int a, int b)      => a + b;
    public int Subtract(int a, int b) => a - b;
    public int Multiply(int a, int b) => a * b;

    public double Divide(int a, int b)
    {
        if (b == 0) throw new DivideByZeroException("Cannot divide by zero.");
        return (double)a / b;
    }
}""",
        language="csharp",
    )

    tabs_ut = st.tabs(["xUnit", "NUnit", "MSTest"])

    with tabs_ut[0]:
        code_block(
            """// XUNIT
// Install: dotnet new xunit -n MyApp.Tests
// Packages: xunit, xunit.runner.visualstudio, Microsoft.NET.Test.Sdk

using Xunit;

public class CalculatorTests
{
    // [Fact] = a single test with no parameters
    [Fact]
    public void Add_TwoPositiveNumbers_ReturnsCorrectSum()
    {
        // Arrange — set up what you need
        var calc = new Calculator();

        // Act — call the method
        int result = calc.Add(2, 3);

        // Assert — verify the result
        Assert.Equal(5, result);
    }

    [Fact]
    public void Subtract_LargerFromSmaller_ReturnsNegative()
    {
        var calc = new Calculator();
        int result = calc.Subtract(3, 10);
        Assert.Equal(-7, result);
    }

    // [Theory] + [InlineData] = parameterised test — runs once per InlineData row
    [Theory]
    [InlineData(2, 3,  6)]
    [InlineData(5, 4, 20)]
    [InlineData(0, 9,  0)]
    public void Multiply_ValidInputs_ReturnsProduct(int a, int b, int expected)
    {
        var calc = new Calculator();
        Assert.Equal(expected, calc.Multiply(a, b));
    }

    [Fact]
    public void Divide_ByZero_ThrowsDivideByZeroException()
    {
        var calc = new Calculator();

        // Assert.Throws verifies that an exception IS thrown
        Assert.Throws<DivideByZeroException>(() => calc.Divide(10, 0));
    }

    [Fact]
    public void Divide_TenByTwo_ReturnsFive()
    {
        var calc = new Calculator();
        double result = calc.Divide(10, 2);
        Assert.Equal(5.0, result);
    }
}""",
            language="csharp",
        )

    with tabs_ut[1]:
        code_block(
            """// NUNIT
// Install: dotnet new nunit -n MyApp.Tests
// Packages: NUnit, NUnit3TestAdapter, Microsoft.NET.Test.Sdk

using NUnit.Framework;

// [TestFixture] marks this class as containing tests (optional in NUnit 3+)
[TestFixture]
public class CalculatorTests
{
    private Calculator _calc;

    // [SetUp] runs BEFORE each test — like a constructor for setup
    [SetUp]
    public void SetUp()
    {
        _calc = new Calculator();
    }

    // [Test] marks a single test method
    [Test]
    public void Add_TwoPositiveNumbers_ReturnsCorrectSum()
    {
        // Arrange (done in SetUp), Act, Assert
        int result = _calc.Add(2, 3);

        // Assert.That is NUnit's modern assertion syntax
        Assert.That(result, Is.EqualTo(5));
    }

    [Test]
    public void Subtract_LargerFromSmaller_ReturnsNegative()
    {
        int result = _calc.Subtract(3, 10);
        Assert.That(result, Is.EqualTo(-7));
    }

    // [TestCase] = parameterised test — one attribute per set of inputs
    [TestCase(2, 3,  6)]
    [TestCase(5, 4, 20)]
    [TestCase(0, 9,  0)]
    public void Multiply_ValidInputs_ReturnsProduct(int a, int b, int expected)
    {
        Assert.That(_calc.Multiply(a, b), Is.EqualTo(expected));
    }

    [Test]
    public void Divide_ByZero_ThrowsDivideByZeroException()
    {
        // Assert.Throws in NUnit
        Assert.Throws<DivideByZeroException>(() => _calc.Divide(10, 0));
    }

    [Test]
    public void Divide_TenByTwo_ReturnsFive()
    {
        double result = _calc.Divide(10, 2);
        Assert.That(result, Is.EqualTo(5.0));
    }

    // [TearDown] runs AFTER each test — for cleanup
    [TearDown]
    public void TearDown()
    {
        // dispose resources if needed
    }
}""",
            language="csharp",
        )

    with tabs_ut[2]:
        code_block(
            """// MSTEST
// Install: dotnet new mstest -n MyApp.Tests
// Packages: MSTest.TestFramework, MSTest.TestAdapter, Microsoft.NET.Test.Sdk

using Microsoft.VisualStudio.TestTools.UnitTesting;

// [TestClass] marks this class as containing tests
[TestClass]
public class CalculatorTests
{
    private Calculator _calc;

    // [TestInitialize] runs BEFORE each test
    [TestInitialize]
    public void TestInitialize()
    {
        _calc = new Calculator();
    }

    // [TestMethod] marks a single test method
    [TestMethod]
    public void Add_TwoPositiveNumbers_ReturnsCorrectSum()
    {
        int result = _calc.Add(2, 3);

        // Assert.AreEqual(expected, actual) is MSTest's style
        Assert.AreEqual(5, result);
    }

    [TestMethod]
    public void Subtract_LargerFromSmaller_ReturnsNegative()
    {
        int result = _calc.Subtract(3, 10);
        Assert.AreEqual(-7, result);
    }

    // [DataTestMethod] + [DataRow] = parameterised test
    [DataTestMethod]
    [DataRow(2, 3,  6)]
    [DataRow(5, 4, 20)]
    [DataRow(0, 9,  0)]
    public void Multiply_ValidInputs_ReturnsProduct(int a, int b, int expected)
    {
        Assert.AreEqual(expected, _calc.Multiply(a, b));
    }

    [TestMethod]
    [ExpectedException(typeof(DivideByZeroException))]
    public void Divide_ByZero_ThrowsDivideByZeroException()
    {
        // [ExpectedException] tells MSTest: this test PASSES if this exception is thrown
        _calc.Divide(10, 0);
    }

    [TestMethod]
    public void Divide_TenByTwo_ReturnsFive()
    {
        double result = _calc.Divide(10, 2);
        Assert.AreEqual(5.0, result);
    }

    // [TestCleanup] runs AFTER each test
    [TestCleanup]
    public void TestCleanup()
    {
        // cleanup resources if needed
    }
}""",
            language="csharp",
        )

    subsection("How to run your tests")
    paragraph("All three frameworks work with the same CLI commands:")
    code_block(
        """# Run all tests in the project
dotnet test

# Run with verbose output to see each test name
dotnet test --verbosity normal

# Run only tests whose name contains a keyword
dotnet test --filter "Add"

# Run tests in a specific file/class
dotnet test --filter "FullyQualifiedName~CalculatorTests"

# Generate a test results report (TRX format)
dotnet test --logger "trx;LogFileName=TestResults.trx" """,
        language="bash",
    )

    subsection("Quick reference and best practices")
    st.markdown(
        """
| # | Practice | Why it matters |
| --- | --- | --- |
| 1 | Name tests as: `MethodName_Scenario_ExpectedResult` | Instantly clear what failed and why |
| 2 | One assertion per test (ideally) | Pinpoints exactly what broke |
| 3 | Never test framework code (`string.Length`, `DateTime.Now`) | You trust the framework; test YOUR logic |
| 4 | Use mocks for external dependencies (DB, API, file system) | Tests stay fast and isolated |
| 5 | Keep tests independent — no shared state between tests | Test order should never matter |
| 6 | Aim for 80%+ code coverage on business logic | Good safety net for refactoring |
| 7 | Run tests on every commit (CI/CD) | Catch breaks before they reach main branch |
| 8 | Tests should be FAST (milliseconds each) | Slow tests get skipped |
"""
    )
