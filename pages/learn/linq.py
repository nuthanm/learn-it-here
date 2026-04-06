import streamlit as st


def render_linq():
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🔍 What is LINQ? (For Complete Beginners)</div>
  <div class="card-body">
<b>LINQ</b> stands for <b>Language Integrated Query</b>. It's a powerful C# feature that lets
you query and manipulate collections of data (lists, arrays, databases, XML, etc.) using
a clean, readable syntax — right inside your C# code, without switching to SQL or
another language.<br><br>
<b>Simple analogy:</b> Imagine you have a big box of coloured Lego bricks. LINQ is like
having a magic wand that lets you say:<br>
🪄 "Give me all the <b>red</b> bricks" → <code>.Where(b =&gt; b.Color == "Red")</code><br>
🪄 "Sort them by <b>size</b>" → <code>.OrderBy(b =&gt; b.Size)</code><br>
🪄 "Just tell me <b>how many</b> there are" → <code>.Count()</code><br><br>
<b>Why should you learn LINQ?</b><br>
✅ It's built into C# — no extra packages needed<br>
✅ Makes data manipulation code 5–10x shorter and more readable<br>
✅ Works on in-memory collections AND databases (via Entity Framework)<br>
✅ Helps you avoid messy for-loops for filtering/sorting<br>
✅ Essential knowledge for every C# developer<br><br>
<b>Where can you use LINQ?</b><br>
📦 <b>LINQ to Objects</b> — query any C# collection (List, Array, Dictionary)<br>
🗄️ <b>LINQ to SQL / LINQ to Entities</b> — query databases through EF Core<br>
📄 <b>LINQ to XML</b> — query and transform XML documents
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🏗️ Anatomy of a LINQ Query — Two Styles</div>
  <div class="card-body">
LINQ has two syntax styles — both do the same thing. Learn both because you'll see both
in the real world:
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<div class="cmd-block">
<span class="cmd-comment">// Our sample data — a list of students</span>
var students = new List&lt;Student&gt;
{
new Student { Name = "Alice", Age = 22, Grade = 90 },
new Student { Name = "Bob",   Age = 19, Grade = 72 },
new Student { Name = "Carol", Age = 25, Grade = 85 },
new Student { Name = "Dave",  Age = 21, Grade = 60 },
new Student { Name = "Eve",   Age = 23, Grade = 95 },
};
&#8203;
<span class="cmd-comment">// ── STYLE 1: Query Syntax (looks like SQL) ──────────────────────</span>
<span class="cmd-comment">//  from  [variable]  in  [source]         ← "look at each item in..."</span>
<span class="cmd-comment">//  where [condition]                       ← "only keep items where..."</span>
<span class="cmd-comment">//  orderby [property]                      ← "sort by..."</span>
<span class="cmd-comment">//  select [what to return]                 ← "return this..."</span>
&#8203;
var topStudentsQuery =
from s in students
where s.Grade &gt;= 80
orderby s.Grade descending
select s.Name;
&#8203;
<span class="cmd-comment">// ── STYLE 2: Method Syntax (most common in modern C#) ──────────</span>
<span class="cmd-comment">//  Uses chain of extension methods with lambda expressions (=&gt;)</span>
&#8203;
var topStudentsMethod = students
.Where(s =&gt; s.Grade &gt;= 80)         <span class="cmd-comment">// filter</span>
.OrderByDescending(s =&gt; s.Grade)   <span class="cmd-comment">// sort</span>
.Select(s =&gt; s.Name);              <span class="cmd-comment">// transform/project</span>
&#8203;
<span class="cmd-comment">// Both give: ["Eve", "Alice", "Carol"]</span>
foreach (var name in topStudentsMethod)
Console.WriteLine(name);
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">📚 Essential LINQ Methods — With Examples</div>
  <div class="card-body">
Here are the most important LINQ methods every developer uses daily:
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<div class="cmd-block">
<span class="cmd-comment">// Sample data</span>
var numbers = new List&lt;int&gt; { 3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5 };
var products = new List&lt;Product&gt; {
new Product { Name = "Laptop",  Price = 999,  Category = "Electronics" },
new Product { Name = "Phone",   Price = 699,  Category = "Electronics" },
new Product { Name = "Desk",    Price = 249,  Category = "Furniture"   },
new Product { Name = "Chair",   Price = 199,  Category = "Furniture"   },
new Product { Name = "Monitor", Price = 399,  Category = "Electronics" },
};
&#8203;
<span class="cmd-comment">// ── FILTERING ──────────────────────────────────────────────────</span>
var evenNums  = numbers.Where(n =&gt; n % 2 == 0);          <span class="cmd-comment">// [4, 2, 6]</span>
var expensive = products.Where(p =&gt; p.Price &gt; 400);       <span class="cmd-comment">// Laptop, Phone</span>
&#8203;
<span class="cmd-comment">// ── SORTING ────────────────────────────────────────────────────</span>
var sorted    = numbers.OrderBy(n =&gt; n);                   <span class="cmd-comment">// ascending</span>
var desc      = numbers.OrderByDescending(n =&gt; n);         <span class="cmd-comment">// descending</span>
var multiSort = products.OrderBy(p =&gt; p.Category)
                    .ThenByDescending(p =&gt; p.Price);   <span class="cmd-comment">// category, then price</span>
&#8203;
<span class="cmd-comment">// ── PROJECTION (transform shape of data) ───────────────────────</span>
var names     = products.Select(p =&gt; p.Name);              <span class="cmd-comment">// just names</span>
var summaries = products.Select(p =&gt; new {                 <span class="cmd-comment">// anonymous type</span>
p.Name, Label = $"{p.Name} - ${p.Price}"
});
&#8203;
<span class="cmd-comment">// ── AGGREGATION ────────────────────────────────────────────────</span>
int total     = numbers.Sum();                             <span class="cmd-comment">// 44</span>
double avg    = numbers.Average();                         <span class="cmd-comment">// 4.0</span>
int max       = numbers.Max();                             <span class="cmd-comment">// 9</span>
int min       = numbers.Min();                             <span class="cmd-comment">// 1</span>
int count     = numbers.Count();                           <span class="cmd-comment">// 11</span>
decimal total2 = products.Sum(p =&gt; p.Price);               <span class="cmd-comment">// 2545</span>
&#8203;
<span class="cmd-comment">// ── GROUPING ───────────────────────────────────────────────────</span>
var byCategory = products.GroupBy(p =&gt; p.Category);
foreach (var group in byCategory) {
Console.WriteLine($"{group.Key}: {group.Count()} items");
}
<span class="cmd-comment">// Output: Electronics: 3 items  |  Furniture: 2 items</span>
&#8203;
<span class="cmd-comment">// ── ELEMENT OPERATIONS ─────────────────────────────────────────</span>
var first  = products.First(p =&gt; p.Price &gt; 300);           <span class="cmd-comment">// throws if none</span>
var firstN = products.FirstOrDefault(p =&gt; p.Price &gt; 9000); <span class="cmd-comment">// null if none — safer!</span>
var single = products.Single(p =&gt; p.Name == "Desk");       <span class="cmd-comment">// throws if 0 or 2+</span>
var last   = products.Last();
&#8203;
<span class="cmd-comment">// ── CHECKING ───────────────────────────────────────────────────</span>
bool anyExp  = products.Any(p =&gt; p.Price &gt; 900);           <span class="cmd-comment">// true</span>
bool allExp  = products.All(p =&gt; p.Price &gt; 100);           <span class="cmd-comment">// true</span>
bool hasDesk = products.Any(p =&gt; p.Name == "Desk");        <span class="cmd-comment">// true</span>
&#8203;
<span class="cmd-comment">// ── DISTINCT / SKIP / TAKE ─────────────────────────────────────</span>
var unique   = numbers.Distinct();                         <span class="cmd-comment">// [3,1,4,5,9,2,6]</span>
var page1    = products.Skip(0).Take(2);                   <span class="cmd-comment">// pagination: first 2</span>
var page2    = products.Skip(2).Take(2);                   <span class="cmd-comment">// pagination: next 2</span>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">⚡ Deferred vs Immediate Execution — Critical Concept!</div>
  <div class="card-body">
<b>This is the #1 thing beginners misunderstand about LINQ.</b><br><br>
Most LINQ queries are <b>deferred</b> — they don't actually run until you iterate the results
(with <code>foreach</code>, <code>.ToList()</code>, <code>.ToArray()</code> etc.).<br><br>
Think of a LINQ query as a <em>recipe</em>, not a cooked meal. The query describes WHAT to
do — but the cooking (execution) only happens when you actually ask for the food.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<div class="cmd-block">
<span class="cmd-comment">// DEFERRED execution — query defined but NOT run yet</span>
var query = students.Where(s =&gt; s.Grade &gt;= 80);  <span class="cmd-comment">// ← no DB/loop hit here</span>
&#8203;
students.Add(new Student { Name = "Frank", Age = 20, Grade = 92 });  <span class="cmd-comment">// add after query</span>
&#8203;
<span class="cmd-comment">// Query runs HERE — Frank IS included because execution is now</span>
foreach (var s in query)
Console.WriteLine(s.Name);   <span class="cmd-comment">// Alice, Carol, Eve, Frank ← Frank appears!</span>
&#8203;
<span class="cmd-comment">// IMMEDIATE execution — use ToList(), ToArray(), Count(), First() etc.</span>
var snapshot = students.Where(s =&gt; s.Grade &gt;= 80).ToList(); <span class="cmd-comment">// runs NOW, Frank included</span>
&#8203;
<span class="cmd-comment">// Rule of thumb:</span>
<span class="cmd-comment">// • Add .ToList() when you want a fixed snapshot of results</span>
<span class="cmd-comment">// • Add .ToList() to avoid running the query multiple times</span>
<span class="cmd-comment">// • In EF Core: always .ToListAsync() to execute DB queries</span>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="content-card">
  <div class="card-title">📋 LINQ Quick-Reference Cheat Sheet</div>
  <div class="card-body">
<table class="shortcut-table">
  <tr><th>Method</th><th>What it does</th><th>Example</th></tr>
  <tr><td>Where</td><td>Filter items</td><td>.Where(x =&gt; x.Age &gt; 18)</td></tr>
  <tr><td>Select</td><td>Transform/project items</td><td>.Select(x =&gt; x.Name)</td></tr>
  <tr><td>OrderBy / OrderByDescending</td><td>Sort ascending / descending</td><td>.OrderBy(x =&gt; x.Name)</td></tr>
  <tr><td>GroupBy</td><td>Group items by key</td><td>.GroupBy(x =&gt; x.Category)</td></tr>
  <tr><td>First / FirstOrDefault</td><td>Get first match (or null)</td><td>.FirstOrDefault(x =&gt; x.Id == 1)</td></tr>
  <tr><td>Single / SingleOrDefault</td><td>Exactly one match expected</td><td>.Single(x =&gt; x.Email == email)</td></tr>
  <tr><td>Any</td><td>Does any item match?</td><td>.Any(x =&gt; x.IsActive)</td></tr>
  <tr><td>All</td><td>Do ALL items match?</td><td>.All(x =&gt; x.Age &gt;= 18)</td></tr>
  <tr><td>Count</td><td>How many items?</td><td>.Count(x =&gt; x.IsActive)</td></tr>
  <tr><td>Sum / Average / Min / Max</td><td>Math aggregates</td><td>.Sum(x =&gt; x.Price)</td></tr>
  <tr><td>Distinct</td><td>Remove duplicates</td><td>.Distinct()</td></tr>
  <tr><td>Skip / Take</td><td>Pagination</td><td>.Skip(10).Take(5)</td></tr>
  <tr><td>ToList / ToArray</td><td>Execute immediately</td><td>.ToList()</td></tr>
  <tr><td>SelectMany</td><td>Flatten nested collections</td><td>.SelectMany(x =&gt; x.Tags)</td></tr>
  <tr><td>Join</td><td>Join two collections</td><td>.Join(other, x =&gt; x.Id, y =&gt; y.Id, ...)</td></tr>
</table>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

