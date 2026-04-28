"""LINQ learning page using the minimal content primitives."""

import streamlit as st

from components.content import (
    code_block,
    paragraph,
    section_intro,
    section_title,
    subsection,
)


def render_linq():
    section_title(
        "LINQ",
        "Language Integrated Query — filter, sort, and transform data the C# way.",
    )

    section_intro(
        "LINQ (Language Integrated Query) is a powerful C# feature that lets you "
        "query and manipulate collections of data — lists, arrays, databases, XML "
        "and more — using a clean, readable syntax right inside your C# code, "
        "without switching to SQL or another language."
    )

    subsection("What is LINQ? (For complete beginners)")
    paragraph(
        'Simple analogy: imagine you have a big box of coloured Lego bricks. LINQ '
        'is like having a magic wand that lets you say things like "give me all '
        'the red bricks", "sort them by size", or "just tell me how many there are".'
    )
    code_block(
        '// "Give me all the red bricks"\n'
        '.Where(b => b.Color == "Red")\n'
        '\n'
        '// "Sort them by size"\n'
        '.OrderBy(b => b.Size)\n'
        '\n'
        '// "Just tell me how many there are"\n'
        '.Count()',
        language="csharp",
    )

    subsection("Why should you learn LINQ?")
    paragraph(
        "LINQ is built into C# — no extra packages needed. It makes data "
        "manipulation code 5–10x shorter and more readable, works on in-memory "
        "collections AND databases (via Entity Framework), helps you avoid messy "
        "for-loops for filtering and sorting, and is essential knowledge for "
        "every C# developer."
    )

    subsection("Where can you use LINQ?")
    paragraph(
        "LINQ to Objects — query any C# collection (List, Array, Dictionary). "
        "LINQ to SQL / LINQ to Entities — query databases through EF Core. "
        "LINQ to XML — query and transform XML documents."
    )

    subsection("Anatomy of a LINQ query — two styles")
    paragraph(
        "LINQ has two syntax styles — both do the same thing. Learn both because "
        "you'll see both in the real world."
    )
    code_block(
        '// Our sample data — a list of students\n'
        'var students = new List<Student>\n'
        '{\n'
        '    new Student { Name = "Alice", Age = 22, Grade = 90 },\n'
        '    new Student { Name = "Bob",   Age = 19, Grade = 72 },\n'
        '    new Student { Name = "Carol", Age = 25, Grade = 85 },\n'
        '    new Student { Name = "Dave",  Age = 21, Grade = 60 },\n'
        '    new Student { Name = "Eve",   Age = 23, Grade = 95 },\n'
        '};\n'
        '\n'
        '// ── STYLE 1: Query Syntax (looks like SQL) ──────────────────────\n'
        '//  from  [variable]  in  [source]         ← "look at each item in..."\n'
        '//  where [condition]                       ← "only keep items where..."\n'
        '//  orderby [property]                      ← "sort by..."\n'
        '//  select [what to return]                 ← "return this..."\n'
        '\n'
        'var topStudentsQuery =\n'
        '    from s in students\n'
        '    where s.Grade >= 80\n'
        '    orderby s.Grade descending\n'
        '    select s.Name;\n'
        '\n'
        '// ── STYLE 2: Method Syntax (most common in modern C#) ──────────\n'
        '//  Uses a chain of extension methods with lambda expressions (=>)\n'
        '\n'
        'var topStudentsMethod = students\n'
        '    .Where(s => s.Grade >= 80)         // filter\n'
        '    .OrderByDescending(s => s.Grade)   // sort\n'
        '    .Select(s => s.Name);              // transform/project\n'
        '\n'
        '// Both give: ["Eve", "Alice", "Carol"]\n'
        'foreach (var name in topStudentsMethod)\n'
        '    Console.WriteLine(name);',
        language="csharp",
    )

    subsection("Essential LINQ methods — with examples")
    paragraph(
        "Here are the most important LINQ methods every developer uses daily — "
        "filtering, sorting, projection, aggregation, grouping, element selection, "
        "checking, and pagination."
    )
    code_block(
        '// Sample data\n'
        'var numbers = new List<int> { 3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5 };\n'
        'var products = new List<Product> {\n'
        '    new Product { Name = "Laptop",  Price = 999, Category = "Electronics" },\n'
        '    new Product { Name = "Phone",   Price = 699, Category = "Electronics" },\n'
        '    new Product { Name = "Desk",    Price = 249, Category = "Furniture"   },\n'
        '    new Product { Name = "Chair",   Price = 199, Category = "Furniture"   },\n'
        '    new Product { Name = "Monitor", Price = 399, Category = "Electronics" },\n'
        '};\n'
        '\n'
        '// ── FILTERING ──────────────────────────────────────────────────\n'
        'var evenNums  = numbers.Where(n => n % 2 == 0);          // [4, 2, 6]\n'
        'var expensive = products.Where(p => p.Price > 400);      // Laptop, Phone\n'
        '\n'
        '// ── SORTING ────────────────────────────────────────────────────\n'
        'var sorted    = numbers.OrderBy(n => n);                 // ascending\n'
        'var desc      = numbers.OrderByDescending(n => n);       // descending\n'
        'var multiSort = products.OrderBy(p => p.Category)\n'
        '                        .ThenByDescending(p => p.Price); // category, then price\n'
        '\n'
        '// ── PROJECTION (transform shape of data) ───────────────────────\n'
        'var names     = products.Select(p => p.Name);            // just names\n'
        'var summaries = products.Select(p => new {               // anonymous type\n'
        '    p.Name, Label = $"{p.Name} - ${p.Price}"\n'
        '});\n'
        '\n'
        '// ── AGGREGATION ────────────────────────────────────────────────\n'
        'int total      = numbers.Sum();                          // 44\n'
        'double avg     = numbers.Average();                      // 4.0\n'
        'int max        = numbers.Max();                          // 9\n'
        'int min        = numbers.Min();                          // 1\n'
        'int count      = numbers.Count();                        // 11\n'
        'decimal total2 = products.Sum(p => p.Price);             // 2545\n'
        '\n'
        '// ── GROUPING ───────────────────────────────────────────────────\n'
        'var byCategory = products.GroupBy(p => p.Category);\n'
        'foreach (var group in byCategory) {\n'
        '    Console.WriteLine($"{group.Key}: {group.Count()} items");\n'
        '}\n'
        '// Output: Electronics: 3 items  |  Furniture: 2 items\n'
        '\n'
        '// ── ELEMENT OPERATIONS ─────────────────────────────────────────\n'
        'var first  = products.First(p => p.Price > 300);           // throws if none\n'
        'var firstN = products.FirstOrDefault(p => p.Price > 9000); // null if none — safer\n'
        'var single = products.Single(p => p.Name == "Desk");       // throws if 0 or 2+\n'
        'var last   = products.Last();\n'
        '\n'
        '// ── CHECKING ───────────────────────────────────────────────────\n'
        'bool anyExp  = products.Any(p => p.Price > 900);           // true\n'
        'bool allExp  = products.All(p => p.Price > 100);           // true\n'
        'bool hasDesk = products.Any(p => p.Name == "Desk");        // true\n'
        '\n'
        '// ── DISTINCT / SKIP / TAKE ─────────────────────────────────────\n'
        'var unique = numbers.Distinct();                           // [3,1,4,5,9,2,6]\n'
        'var page1  = products.Skip(0).Take(2);                     // pagination: first 2\n'
        'var page2  = products.Skip(2).Take(2);                     // pagination: next 2',
        language="csharp",
    )

    subsection("Deferred vs immediate execution — critical concept")
    paragraph(
        "This is the number-one thing beginners misunderstand about LINQ. Most "
        "LINQ queries are deferred — they don't actually run until you iterate "
        "the results (with foreach, .ToList(), .ToArray() etc.)."
    )
    paragraph(
        "Think of a LINQ query as a recipe, not a cooked meal. The query "
        "describes WHAT to do — but the cooking (execution) only happens when "
        "you actually ask for the food."
    )
    code_block(
        '// DEFERRED execution — query defined but NOT run yet\n'
        'var query = students.Where(s => s.Grade >= 80);  // ← no DB/loop hit here\n'
        '\n'
        'students.Add(new Student { Name = "Frank", Age = 20, Grade = 92 }); // add after query\n'
        '\n'
        '// Query runs HERE — Frank IS included because execution is now\n'
        'foreach (var s in query)\n'
        '    Console.WriteLine(s.Name);   // Alice, Carol, Eve, Frank ← Frank appears\n'
        '\n'
        '// IMMEDIATE execution — use ToList(), ToArray(), Count(), First() etc.\n'
        'var snapshot = students.Where(s => s.Grade >= 80).ToList(); // runs NOW, Frank included\n'
        '\n'
        '// Rule of thumb:\n'
        '// • Add .ToList() when you want a fixed snapshot of results\n'
        '// • Add .ToList() to avoid running the query multiple times\n'
        '// • In EF Core: always .ToListAsync() to execute DB queries',
        language="csharp",
    )

    subsection("LINQ quick-reference cheat sheet")
    st.markdown(
        "| Method | What it does | Example |\n"
        "| --- | --- | --- |\n"
        "| Where | Filter items | `.Where(x => x.Age > 18)` |\n"
        "| Select | Transform/project items | `.Select(x => x.Name)` |\n"
        "| OrderBy / OrderByDescending | Sort ascending / descending | `.OrderBy(x => x.Name)` |\n"
        "| GroupBy | Group items by key | `.GroupBy(x => x.Category)` |\n"
        "| First / FirstOrDefault | Get first match (or null) | `.FirstOrDefault(x => x.Id == 1)` |\n"
        "| Single / SingleOrDefault | Exactly one match expected | `.Single(x => x.Email == email)` |\n"
        "| Any | Does any item match? | `.Any(x => x.IsActive)` |\n"
        "| All | Do ALL items match? | `.All(x => x.Age >= 18)` |\n"
        "| Count | How many items? | `.Count(x => x.IsActive)` |\n"
        "| Sum / Average / Min / Max | Math aggregates | `.Sum(x => x.Price)` |\n"
        "| Distinct | Remove duplicates | `.Distinct()` |\n"
        "| Skip / Take | Pagination | `.Skip(10).Take(5)` |\n"
        "| ToList / ToArray | Execute immediately | `.ToList()` |\n"
        "| SelectMany | Flatten nested collections | `.SelectMany(x => x.Tags)` |\n"
        "| Join | Join two collections | `.Join(other, x => x.Id, y => y.Id, ...)` |\n"
    )
