import CodeBlock from "@/components/CodeBlock";
import ContentTable from "@/components/ContentTable";

export default function UnitTestingOverview() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>Unit Testing</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Automated testing practices for .NET projects — covering TDD methodology,
        unit tests, and integration tests.
      </p>
      <ul className="text-sm list-disc pl-5" style={{ color: "var(--body)" }}>
        <li className="mb-1"><strong>TDD</strong> — Test-Driven Development: Red → Green → Refactor</li>
        <li className="mb-1"><strong>Unit Test</strong> — Isolated tests using xUnit / NUnit / MSTest</li>
        <li className="mb-1"><strong>Integration Test</strong> — Tests that verify multiple components together</li>
      </ul>
    </div>
  );
}

export function TDD() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>TDD — Test-Driven Development</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Write the failing test first, make it pass with minimal code, then refactor. Repeat.
      </p>
      <h3 className="font-semibold text-sm mb-2" style={{ color: "var(--ink)" }}>The cycle</h3>
      <ol className="text-sm list-decimal pl-5 mb-4" style={{ color: "var(--body)" }}>
        <li className="mb-1"><strong>Red</strong> — write a test that fails (the feature doesn&apos;t exist yet)</li>
        <li className="mb-1"><strong>Green</strong> — write the simplest code to make the test pass</li>
        <li className="mb-1"><strong>Refactor</strong> — clean up the code without breaking the test</li>
      </ol>
      <h3 className="font-semibold text-sm mb-2 mt-4" style={{ color: "var(--ink)" }}>Example (xUnit + C#)</h3>
      <CodeBlock language="csharp">{`[Fact]
public void Add_TwoIntegers_ReturnsSum()
{
    var calc = new Calculator();
    int result = calc.Add(2, 3);
    Assert.Equal(5, result);
}`}</CodeBlock>
    </div>
  );
}

export function UnitTestContent() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>Unit Test</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Unit tests verify a single unit of code (class / method) in complete isolation
        — no database, no network, no file system.
      </p>
      <h3 className="font-semibold text-sm mb-2" style={{ color: "var(--ink)" }}>Arrange — Act — Assert</h3>
      <CodeBlock language="csharp">{`[Fact]
public void GetUser_ExistingId_ReturnsUser()
{
    // Arrange
    var mockRepo = new Mock<IUserRepository>();
    mockRepo.Setup(r => r.GetById(1)).Returns(new User { Id = 1, Name = "Alice" });
    var sut = new UserService(mockRepo.Object);

    // Act
    var user = sut.GetUser(1);

    // Assert
    Assert.NotNull(user);
    Assert.Equal("Alice", user.Name);
}`}</CodeBlock>
      <ContentTable headers={["Framework", "NuGet package", "Assertion style"]} rows={[
        ["xUnit", "xunit", "Assert.Equal / Assert.True"],
        ["NUnit", "NUnit", "Assert.That(…, Is.EqualTo(…))"],
        ["MSTest", "MSTest.TestFramework", "[TestMethod] + Assert.AreEqual"],
      ]} />
    </div>
  );
}

export function IntegrationTest() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>Integration Test</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Integration tests verify that multiple components work together — typically including
        the database layer, HTTP pipeline, or external services.
      </p>
      <h3 className="font-semibold text-sm mb-2" style={{ color: "var(--ink)" }}>WebApplicationFactory (ASP.NET Core)</h3>
      <CodeBlock language="csharp">{`public class OrdersControllerTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public OrdersControllerTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task GetOrders_ReturnsOk()
    {
        var response = await _client.GetAsync("/api/orders");
        response.EnsureSuccessStatusCode();
    }
}`}</CodeBlock>
    </div>
  );
}
