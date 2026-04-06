import streamlit as st


def render_unit_testing():
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🧪 What is Unit Testing? (For Complete Beginners)</div>
  <div class="card-body">
<b>Unit testing</b> means writing small, automated pieces of code that verify a tiny,
isolated piece (a "unit") of your application works correctly — <em>before a human ever
clicks a button</em>.<br><br>
<b>Think of it like this:</b> Imagine you built a calculator. A unit test would
automatically check: "Does 2 + 2 really return 4?" — and it checks that <em>every single
time</em> you change any code. If you accidentally break the addition logic later, the
test immediately shouts "FAILED!" and saves you from shipping a broken calculator.<br><br>
<b>Why should every developer write unit tests?</b><br>
✅ <b>Catch bugs early</b> — find problems in seconds, not in production<br>
✅ <b>Refactor confidently</b> — change code without fear; tests tell you if you broke something<br>
✅ <b>Living documentation</b> — tests show exactly how code is supposed to behave<br>
✅ <b>Faster debugging</b> — failing test pinpoints exactly which unit broke<br>
✅ <b>Required in most professional teams</b> — companies expect developers to write tests<br><br>
<b>The 3A Pattern (Arrange-Act-Assert)</b> — Every unit test follows this structure:<br>
🔵 <b>Arrange</b> — Set up the data and objects you need<br>
🟢 <b>Act</b> — Call the method/function you are testing<br>
🔴 <b>Assert</b> — Verify the result is what you expected
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">⚖️ xUnit vs NUnit vs MSTest — Complete Comparison</div>
  <div class="card-body">
There are three major unit testing frameworks for .NET. All three do the same job — the
differences are syntax, features, and community preference. Here's everything you need to know:<br><br>
<table class="shortcut-table">
  <tr><th>Feature</th><th>xUnit</th><th>NUnit</th><th>MSTest</th></tr>
  <tr><td>Created by</td><td>James Newkirk &amp; Brad Wilson (ex-NUnit creators)</td><td>Open-source community</td><td>Microsoft</td></tr>
  <tr><td>First released</td><td>2007</td><td>2000 (oldest!)</td><td>2005</td></tr>
  <tr><td>Current version</td><td>xUnit 2.x / 3.x</td><td>NUnit 3.x / 4.x</td><td>MSTest v2 / v3</td></tr>
  <tr><td>Preferred by</td><td>.NET Core / modern teams</td><td>Enterprise / Java-background devs</td><td>Visual Studio / Microsoft teams</td></tr>
  <tr><td>Test marker attribute</td><td>[Fact] / [Theory]</td><td>[Test] / [TestCase]</td><td>[TestMethod] / [DataTestMethod]</td></tr>
  <tr><td>Test class attribute</td><td>None needed</td><td>[TestFixture]</td><td>[TestClass]</td></tr>
  <tr><td>Setup method</td><td>Constructor</td><td>[SetUp]</td><td>[TestInitialize]</td></tr>
  <tr><td>Teardown method</td><td>IDisposable.Dispose()</td><td>[TearDown]</td><td>[TestCleanup]</td></tr>
  <tr><td>One-time setup</td><td>IClassFixture&lt;T&gt;</td><td>[OneTimeSetUp]</td><td>[ClassInitialize]</td></tr>
  <tr><td>Parameterised tests</td><td>[Theory] + [InlineData]</td><td>[TestCase(...)]</td><td>[DataTestMethod] + [DataRow]</td></tr>
  <tr><td>Assertion library</td><td>Assert.Equal / Throws etc.</td><td>Assert.That / Classic Assert</td><td>Assert.AreEqual / ThrowsException</td></tr>
  <tr><td>Parallel test execution</td><td>✅ By default (per class)</td><td>✅ Configurable</td><td>⚠️ Limited (opt-in)</td></tr>
  <tr><td>IDE integration</td><td>Excellent (VS, Rider, VS Code)</td><td>Excellent</td><td>Best in Visual Studio</td></tr>
  <tr><td>dotnet test support</td><td>✅ Native</td><td>✅ Native</td><td>✅ Native</td></tr>
  <tr><td>NuGet package</td><td>xunit, xunit.runner.visualstudio</td><td>NUnit, NUnit3TestAdapter</td><td>MSTest.TestFramework, MSTest.TestAdapter</td></tr>
  <tr><td>Install template</td><td>dotnet new xunit</td><td>dotnet new nunit</td><td>dotnet new mstest</td></tr>
  <tr><td>Community popularity (2024)</td><td>🥇 Most popular in .NET Core</td><td>🥈 Very popular (esp. legacy)</td><td>🥉 Common in MS-heavy shops</td></tr>
  <tr><td>Learning curve</td><td>Easy</td><td>Easy (familiar to JUnit devs)</td><td>Easy</td></tr>
  <tr><td>Best for</td><td>New .NET projects, open-source</td><td>Teams coming from Java/JUnit</td><td>Teams deep in Visual Studio ecosystem</td></tr>
</table>
<br>
<b>🏆 Bottom line for beginners:</b> Pick <b>xUnit</b> for new projects — it's the de facto
standard in modern .NET. Use NUnit if your team already uses it or if you're from a Java
background. Use MSTest if you're in a pure Microsoft environment.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🧮 Same Example in All Three Frameworks — Calculator Tests</div>
  <div class="card-body">
We'll test this simple <b>Calculator</b> class in xUnit, NUnit, and MSTest — so you can see exactly
how the same test looks in each framework. The business logic never changes, only the test attributes do.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<div class="cmd-block">
<span class="cmd-comment">// ── The class we are testing (Calculator.cs) — same for all three frameworks</span>
public class Calculator
{
public int Add(int a, int b)      =&gt; a + b;
public int Subtract(int a, int b) =&gt; a - b;
public int Multiply(int a, int b) =&gt; a * b;
public double Divide(int a, int b)
{
    if (b == 0) throw new DivideByZeroException("Cannot divide by zero.");
    return (double)a / b;
}
}
</div>
""",
        unsafe_allow_html=True,
    )

    tabs_ut = st.tabs(["xUnit", "NUnit", "MSTest"])

    with tabs_ut[0]:
        st.markdown(
            """
<div class="cmd-block">
<span class="cmd-comment">// ── XUNIT ────────────────────────────────────────────────────────</span>
<span class="cmd-comment">// Install: dotnet new xunit -n MyApp.Tests</span>
<span class="cmd-comment">// Packages: xunit, xunit.runner.visualstudio, Microsoft.NET.Test.Sdk</span>
&#8203;
using Xunit;
&#8203;
public class CalculatorTests
{
<span class="cmd-comment">// [Fact] = a single test with no parameters</span>
[Fact]
public void Add_TwoPositiveNumbers_ReturnsCorrectSum()
{
    <span class="cmd-comment">// Arrange — set up what you need</span>
    var calc = new Calculator();
&#8203;
    <span class="cmd-comment">// Act — call the method</span>
    int result = calc.Add(2, 3);
&#8203;
    <span class="cmd-comment">// Assert — verify the result</span>
    Assert.Equal(5, result);
}
&#8203;
[Fact]
public void Subtract_LargerFromSmaller_ReturnsNegative()
{
    var calc = new Calculator();
    int result = calc.Subtract(3, 10);
    Assert.Equal(-7, result);
}
&#8203;
<span class="cmd-comment">// [Theory] + [InlineData] = parameterised test — runs once per InlineData row</span>
[Theory]
[InlineData(2, 3,  6)]
[InlineData(5, 4, 20)]
[InlineData(0, 9,  0)]
public void Multiply_ValidInputs_ReturnsProduct(int a, int b, int expected)
{
    var calc = new Calculator();
    Assert.Equal(expected, calc.Multiply(a, b));
}
&#8203;
[Fact]
public void Divide_ByZero_ThrowsDivideByZeroException()
{
    var calc = new Calculator();
&#8203;
    <span class="cmd-comment">// Assert.Throws verifies that an exception IS thrown</span>
    Assert.Throws&lt;DivideByZeroException&gt;(() =&gt; calc.Divide(10, 0));
}
&#8203;
[Fact]
public void Divide_TenByTwo_ReturnsFive()
{
    var calc = new Calculator();
    double result = calc.Divide(10, 2);
    Assert.Equal(5.0, result);
}
}
</div>
""",
            unsafe_allow_html=True,
        )

    with tabs_ut[1]:
        st.markdown(
            """
<div class="cmd-block">
<span class="cmd-comment">// ── NUNIT ────────────────────────────────────────────────────────</span>
<span class="cmd-comment">// Install: dotnet new nunit -n MyApp.Tests</span>
<span class="cmd-comment">// Packages: NUnit, NUnit3TestAdapter, Microsoft.NET.Test.Sdk</span>
&#8203;
using NUnit.Framework;
&#8203;
<span class="cmd-comment">// [TestFixture] marks this class as containing tests (optional in NUnit 3+)</span>
[TestFixture]
public class CalculatorTests
{
private Calculator _calc;
&#8203;
<span class="cmd-comment">// [SetUp] runs BEFORE each test — like a constructor for setup</span>
[SetUp]
public void SetUp()
{
    _calc = new Calculator();
}
&#8203;
<span class="cmd-comment">// [Test] marks a single test method</span>
[Test]
public void Add_TwoPositiveNumbers_ReturnsCorrectSum()
{
    <span class="cmd-comment">// Arrange (done in SetUp), Act, Assert</span>
    int result = _calc.Add(2, 3);
&#8203;
    <span class="cmd-comment">// Assert.That is NUnit's modern assertion syntax</span>
    Assert.That(result, Is.EqualTo(5));
}
&#8203;
[Test]
public void Subtract_LargerFromSmaller_ReturnsNegative()
{
    int result = _calc.Subtract(3, 10);
    Assert.That(result, Is.EqualTo(-7));
}
&#8203;
<span class="cmd-comment">// [TestCase] = parameterised test — one attribute per set of inputs</span>
[TestCase(2, 3,  6)]
[TestCase(5, 4, 20)]
[TestCase(0, 9,  0)]
public void Multiply_ValidInputs_ReturnsProduct(int a, int b, int expected)
{
    Assert.That(_calc.Multiply(a, b), Is.EqualTo(expected));
}
&#8203;
[Test]
public void Divide_ByZero_ThrowsDivideByZeroException()
{
    <span class="cmd-comment">// Assert.Throws in NUnit</span>
    Assert.Throws&lt;DivideByZeroException&gt;(() =&gt; _calc.Divide(10, 0));
}
&#8203;
[Test]
public void Divide_TenByTwo_ReturnsFive()
{
    double result = _calc.Divide(10, 2);
    Assert.That(result, Is.EqualTo(5.0));
}
&#8203;
<span class="cmd-comment">// [TearDown] runs AFTER each test — for cleanup</span>
[TearDown]
public void TearDown()
{
    <span class="cmd-comment">// dispose resources if needed</span>
}
}
</div>
""",
            unsafe_allow_html=True,
        )

    with tabs_ut[2]:
        st.markdown(
            """
<div class="cmd-block">
<span class="cmd-comment">// ── MSTEST ───────────────────────────────────────────────────────</span>
<span class="cmd-comment">// Install: dotnet new mstest -n MyApp.Tests</span>
<span class="cmd-comment">// Packages: MSTest.TestFramework, MSTest.TestAdapter, Microsoft.NET.Test.Sdk</span>
&#8203;
using Microsoft.VisualStudio.TestTools.UnitTesting;
&#8203;
<span class="cmd-comment">// [TestClass] marks this class as containing tests</span>
[TestClass]
public class CalculatorTests
{
private Calculator _calc;
&#8203;
<span class="cmd-comment">// [TestInitialize] runs BEFORE each test</span>
[TestInitialize]
public void TestInitialize()
{
    _calc = new Calculator();
}
&#8203;
<span class="cmd-comment">// [TestMethod] marks a single test method</span>
[TestMethod]
public void Add_TwoPositiveNumbers_ReturnsCorrectSum()
{
    int result = _calc.Add(2, 3);
&#8203;
    <span class="cmd-comment">// Assert.AreEqual(expected, actual) is MSTest's style</span>
    Assert.AreEqual(5, result);
}
&#8203;
[TestMethod]
public void Subtract_LargerFromSmaller_ReturnsNegative()
{
    int result = _calc.Subtract(3, 10);
    Assert.AreEqual(-7, result);
}
&#8203;
<span class="cmd-comment">// [DataTestMethod] + [DataRow] = parameterised test</span>
[DataTestMethod]
[DataRow(2, 3,  6)]
[DataRow(5, 4, 20)]
[DataRow(0, 9,  0)]
public void Multiply_ValidInputs_ReturnsProduct(int a, int b, int expected)
{
    Assert.AreEqual(expected, _calc.Multiply(a, b));
}
&#8203;
[TestMethod]
[ExpectedException(typeof(DivideByZeroException))]
public void Divide_ByZero_ThrowsDivideByZeroException()
{
    <span class="cmd-comment">// [ExpectedException] tells MSTest: this test PASSES if this exception is thrown</span>
    _calc.Divide(10, 0);
}
&#8203;
[TestMethod]
public void Divide_TenByTwo_ReturnsFive()
{
    double result = _calc.Divide(10, 2);
    Assert.AreEqual(5.0, result);
}
&#8203;
<span class="cmd-comment">// [TestCleanup] runs AFTER each test</span>
[TestCleanup]
public void TestCleanup()
{
    <span class="cmd-comment">// cleanup resources if needed</span>
}
}
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">▶️ How to Run Your Tests</div>
  <div class="card-body">
All three frameworks work with the same CLI commands:
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<div class="cmd-block">
<span class="cmd-comment"># Run all tests in the project</span>
dotnet test
&#8203;
<span class="cmd-comment"># Run with verbose output to see each test name</span>
dotnet test --verbosity normal
&#8203;
<span class="cmd-comment"># Run only tests whose name contains a keyword</span>
dotnet test --filter "Add"
&#8203;
<span class="cmd-comment"># Run tests in a specific file/class</span>
dotnet test --filter "FullyQualifiedName~CalculatorTests"
&#8203;
<span class="cmd-comment"># Generate a test results report (TRX format)</span>
dotnet test --logger "trx;LogFileName=TestResults.trx"
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">📋 Unit Testing Quick Reference &amp; Best Practices</div>
  <div class="card-body">
<table class="shortcut-table">
  <tr><th>#</th><th>Practice</th><th>Why It Matters</th></tr>
  <tr><td>1</td><td>Name tests as: MethodName_Scenario_ExpectedResult</td><td>Instantly clear what failed and why</td></tr>
  <tr><td>2</td><td>One assertion per test (ideally)</td><td>Pinpoints exactly what broke</td></tr>
  <tr><td>3</td><td>Never test framework code (string.Length, DateTime.Now)</td><td>You trust the framework; test YOUR logic</td></tr>
  <tr><td>4</td><td>Use mocks for external dependencies (DB, API, file system)</td><td>Tests stay fast and isolated</td></tr>
  <tr><td>5</td><td>Keep tests independent — no shared state between tests</td><td>Test order should never matter</td></tr>
  <tr><td>6</td><td>Aim for 80%+ code coverage on business logic</td><td>Good safety net for refactoring</td></tr>
  <tr><td>7</td><td>Run tests on every commit (CI/CD)</td><td>Catch breaks before they reach main branch</td></tr>
  <tr><td>8</td><td>Tests should be FAST (milliseconds each)</td><td>Slow tests get skipped</td></tr>
</table>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

