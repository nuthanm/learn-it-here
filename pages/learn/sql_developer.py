import streamlit as st


def render_sql_developer():
    # ── 1. What is SQL Developer? ─────────────────────────────────────────────
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🗄️ What is Oracle SQL Developer?</div>
  <div class="card-body">
<b>Oracle SQL Developer</b> is a <em>free graphical tool</em> made by Oracle Corporation that lets
you work with Oracle databases without needing to type complex commands in a terminal.
Think of it as a friendly window into your database — you can click through tables, write
and run SQL queries, view stored code, and manage database objects all from one place.
<br><br>
<b>Who is it for?</b><br>
<ul>
  <li><b>Beginners</b> — explore a database visually, no command-line knowledge required.</li>
  <li><b>Developers</b> — write, test, and debug SQL and PL/SQL code quickly.</li>
  <li><b>DBAs (Database Administrators)</b> — manage users, monitor sessions, and run scripts.</li>
</ul>
<br>
<b>In plain English:</b> If your data lives in an Oracle database, SQL Developer is the easiest
way to see it, query it, and change it — all for free.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── 2. Official Download ──────────────────────────────────────────────────
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">⬇️ Where to Download SQL Developer (Official Link)</div>
  <div class="card-body">
Always download SQL Developer directly from Oracle's official website to ensure you get the
latest, safe version.
<br><br>
<b>Official download page:</b><br>
<a href="https://www.oracle.com/database/sqldeveloper/technologies/download/" target="_blank">
  https://www.oracle.com/database/sqldeveloper/technologies/download/
</a>
<br><br>
<b>Which version should I pick?</b><br>
<ul>
  <li>Choose the <b>Windows 64-bit with JDK included</b> package if you are on Windows —
      it bundles Java so you don't need to install anything else first.</li>
  <li>Choose the platform-specific package (macOS or Linux) if you're on those systems.</li>
</ul>
<br>
<b>Note:</b> You may need to create a free Oracle account to download the file.
The sign-up is completely free and only takes a minute.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── 3. Oracle & Other Database Support ───────────────────────────────────
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🔌 Which Databases Does SQL Developer Support?</div>
  <div class="card-body">
<b>Primary support — Oracle Database:</b><br>
SQL Developer is built specifically for Oracle databases and provides the deepest support for them:
<ul>
  <li>Connect to any Oracle database (on your computer, on a server, or in the cloud).</li>
  <li>Browse and edit every type of Oracle object — tables, views, packages, procedures, triggers, sequences, and more.</li>
  <li>Write, run, and debug PL/SQL (Oracle's built-in programming language).</li>
  <li>Works with <b>Oracle Database 11g, 12c, 18c, 19c, 21c</b> and the latest versions.</li>
</ul>
<br>
<b>Other databases — limited support via third-party JDBC drivers:</b><br>
SQL Developer can also connect to non-Oracle databases, but the experience is more basic
compared to dedicated tools for those databases:
<br><br>
<table class="shortcut-table">
  <tr><th>Database</th><th>Supported?</th><th>What You Need</th></tr>
  <tr><td>Oracle</td><td>✅ Full support</td><td>Built-in — nothing extra needed</td></tr>
  <tr><td>MySQL</td><td>⚠️ Partial</td><td>Download MySQL JDBC driver (.jar file) and add it in SQL Developer preferences</td></tr>
  <tr><td>SQL Server</td><td>⚠️ Partial</td><td>Download Microsoft JDBC driver for SQL Server and configure it</td></tr>
  <tr><td>PostgreSQL</td><td>⚠️ Partial</td><td>Download PostgreSQL JDBC driver (postgresql-xx.jar) and configure it</td></tr>
  <tr><td>IBM DB2</td><td>⚠️ Partial</td><td>Requires IBM JDBC driver</td></tr>
</table>
<br>
<b>Recommendation:</b> For SQL Server, use <em>SQL Server Management Studio (SSMS)</em>.
For PostgreSQL, use <em>pgAdmin</em>. These are free tools purpose-built for those databases
and will give you a much better experience. Use SQL Developer when you are primarily working
with Oracle.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── 4. Installation Steps ─────────────────────────────────────────────────
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🛠️ Installation Steps (Windows)</div>
  <div class="card-body">
SQL Developer is very easy to install on Windows because it comes as a simple ZIP file —
there is no complex installer wizard.
<br><br>

<b>Step 1 — Download the ZIP</b><br>
Go to the official download page, choose <b>"Windows 64-bit with JDK included"</b>,
and save the ZIP file to your computer (e.g. your Desktop or Downloads folder).
<br>
📸 <em>Screenshot tip: You'll see a table of download options — look for the row that says
"Windows 64-bit with JDK" and click the download link on the right.</em>
<br><br>

<b>Step 2 — Extract the ZIP</b><br>
Right-click the downloaded ZIP file → <b>Extract All…</b> → choose a destination folder
(for example <code>C:\\sqldeveloper</code>).
<br>
📸 <em>Screenshot tip: Windows will show an "Extract Compressed Folders" dialog — just click
"Extract" and wait for it to finish.</em>
<br><br>

<b>Step 3 — Run SQL Developer</b><br>
Open the extracted folder and double-click <code>sqldeveloper.exe</code> to launch the tool.
<br>
📸 <em>Screenshot tip: You'll see the SQL Developer icon — an orange circle with a white plug symbol.</em>
<br><br>

<b>Step 4 — First-time setup (optional)</b><br>
On the very first launch, SQL Developer may ask if you want to import settings from a previous
version. If this is your first time, click <b>"No"</b>.
<br><br>

<b>Step 5 — You're in!</b><br>
The SQL Developer window opens. You'll see:<br>
<ul>
  <li>A <b>left panel</b> (Connections &amp; Navigator) — for browsing database connections and objects.</li>
  <li>A <b>main area</b> (Worksheet) — where you write and run SQL.</li>
  <li>A <b>bottom panel</b> — where query results appear.</li>
</ul>
<br>
<b>No installation on macOS/Linux?</b><br>
On macOS, download the <em>.dmg</em> file, double-click it, and drag SQL Developer to your
Applications folder. On Linux, download the <em>.rpm</em> or <em>.tar.gz</em> and follow
the instructions in the README file inside the package.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── 5. How to Connect to a Database ──────────────────────────────────────
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🔗 How to Connect to an Oracle Database</div>
  <div class="card-body">
Connecting SQL Developer to an Oracle database is like giving it the address and password
to the front door. Here is exactly how to do it:
<br><br>

<b>Step 1 — Open the New Connection dialog</b><br>
In the left panel, click the green <b>+</b> icon next to "Connections", or go to
<b>File → New → Database Connection</b>.
<br><br>

<b>Step 2 — Fill in the connection details</b><br>
A dialog box appears with several fields. Here's what each one means:
<br><br>
<table class="shortcut-table">
  <tr><th>Field</th><th>What to enter</th><th>Example</th></tr>
  <tr><td>Connection Name</td><td>A friendly label you choose — just for you</td><td>MyLocalDB</td></tr>
  <tr><td>Username</td><td>Your Oracle database username</td><td>hr</td></tr>
  <tr><td>Password</td><td>Your Oracle database password</td><td>••••••••</td></tr>
  <tr><td>Hostname</td><td>The server address (IP or machine name)</td><td>localhost or 192.168.1.10</td></tr>
  <tr><td>Port</td><td>The port Oracle listens on (default is 1521)</td><td>1521</td></tr>
  <tr><td>SID / Service Name</td><td>The name of the Oracle database instance</td><td>ORCL or XEPDB1</td></tr>
</table>
<br>
<b>SID vs Service Name — which one?</b><br>
<ul>
  <li><b>SID</b> — older style, used for single databases (e.g. <code>ORCL</code>).</li>
  <li><b>Service Name</b> — modern style, recommended for most setups (e.g. <code>XEPDB1</code>
      for Oracle XE, or <code>orclpdb1</code> for container databases).</li>
</ul>
If you're not sure, ask the person who set up the database, or try <code>XEPDB1</code> for
a local Oracle XE installation.
<br><br>

<b>Step 3 — Test the connection</b><br>
Click the <b>"Test"</b> button at the bottom of the dialog. You should see
<span style="color:#40916C"><b>"Status: Success"</b></span> in the bottom-left corner.
If it shows an error, double-check your hostname, port, and credentials.
<br><br>

<b>Step 4 — Save and Connect</b><br>
Click <b>"Save"</b> to remember this connection for next time, then click <b>"Connect"</b>.
Your new connection appears in the left panel under "Connections". Click the triangle/arrow
next to it to expand the database objects.
<br><br>

<b>Common connection errors and fixes:</b><br>
<table class="shortcut-table">
  <tr><th>Error message</th><th>Likely cause</th><th>Fix</th></tr>
  <tr><td>IO Error: The Network Adapter could not establish the connection</td><td>Wrong hostname or port, or Oracle listener is not running</td><td>Check hostname/port; start the Oracle listener service</td></tr>
  <tr><td>ORA-01017: invalid username/password</td><td>Wrong credentials</td><td>Double-check username and password (case-sensitive)</td></tr>
  <tr><td>ORA-12514: TNS:listener does not currently know of service</td><td>Wrong Service Name or SID</td><td>Try the other option (switch from SID to Service Name or vice versa)</td></tr>
</table>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── 6. Viewing Database Objects ───────────────────────────────────────────
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">🔍 How to View Database Objects</div>
  <div class="card-body">
Once connected, you can browse everything in the database from the left-side panel called
the <b>Database Navigator</b>. Think of it like Windows Explorer but for your database.
<br><br>
Expand your connection name → expand <b>"Other Users"</b> to browse other schemas,
or browse your own schema directly. You'll see folders for every type of object.
<br><br>

<div class="feature-grid">
  <div class="feature-pill">
    <strong>📋 Tables</strong>
    <p>Expand <b>Tables</b> to see all tables in the schema. Click any table name to open
    a detail window showing its <b>Columns</b>, <b>Data</b>, <b>Constraints</b>,
    <b>Indexes</b>, and <b>Grants</b> in separate tabs.</p>
  </div>
  <div class="feature-pill">
    <strong>👁️ Views</strong>
    <p>Expand <b>Views</b> to see virtual tables (queries saved as named views). Click a view
    to see its definition (the SQL behind it) and its data.</p>
  </div>
  <div class="feature-pill">
    <strong>📦 Packages</strong>
    <p>Expand <b>Packages</b> to see PL/SQL packages — bundles of related procedures and
    functions. Click a package to see its <b>Spec</b> (the public interface) and
    <b>Body</b> (the actual code).</p>
  </div>
  <div class="feature-pill">
    <strong>⚙️ Procedures</strong>
    <p>Expand <b>Procedures</b> to see standalone stored procedures. Double-click one to open
    its code in the editor, where you can read, edit, and recompile it.</p>
  </div>
  <div class="feature-pill">
    <strong>⚡ Triggers</strong>
    <p>Expand <b>Triggers</b> to see all triggers. A trigger is code that runs automatically
    when a row is inserted, updated, or deleted. Click one to view its code and the table
    it fires on.</p>
  </div>
  <div class="feature-pill">
    <strong>🔧 Functions</strong>
    <p>Expand <b>Functions</b> for standalone PL/SQL functions — similar to procedures but
    they return a value. Double-click to open the source code.</p>
  </div>
  <div class="feature-pill">
    <strong>🔢 Sequences</strong>
    <p>Expand <b>Sequences</b> to see auto-number generators (like an identity column in
    other databases). Used to generate unique IDs for primary keys.</p>
  </div>
  <div class="feature-pill">
    <strong>🗂️ Indexes</strong>
    <p>Expand <b>Indexes</b> to see all indexes — these speed up queries. Click an index to
    see which table and columns it covers.</p>
  </div>
</div>
<br>
<b>Quick Tip — Filter objects by name:</b><br>
If a schema has hundreds of tables, right-click the <b>Tables</b> folder → <b>Apply Filter</b>
→ type part of the table name → click OK. Only matching tables are shown.
<br><br>
<b>Quick Tip — Jump straight to an object:</b><br>
Use <b>View → Find DB Object</b> to search for any object by name
across all schemas at once.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── 7. How to Open a Query Window ─────────────────────────────────────────
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">📝 How to Open a Query Window and Run SQL</div>
  <div class="card-body">
The <b>SQL Worksheet</b> is where you type and run SQL queries. Here's how to use it:
<br><br>

<b>Open a new Worksheet (query window):</b><br>
<ul>
  <li>Press <b>Alt+F10</b> (fastest way), <b>or</b></li>
  <li>Click <b>Tools → SQL Worksheet</b> from the menu, <b>or</b></li>
  <li>Right-click your connection in the Navigator → <b>Open SQL Worksheet</b>.</li>
</ul>
A blank worksheet opens. Make sure the correct connection is selected in the
drop-down at the top of the worksheet.
<br><br>

<b>Write and run a query:</b><br>
Type your SQL in the worksheet area:
<div class="cmd-block">SELECT * FROM employees WHERE department_id = 10;</div>
Then run it using one of these methods:
<br><br>
<table class="shortcut-table">
  <tr><th>Action</th><th>Keyboard shortcut</th><th>Toolbar button</th></tr>
  <tr><td>Run the statement your cursor is in</td><td><b>F9</b> or <b>Ctrl+Enter</b></td><td>▶ (green play button)</td></tr>
  <tr><td>Run the entire script (all statements)</td><td><b>F5</b></td><td>▶▶ (script run button)</td></tr>
</table>
<br>
<b>F9 vs F5 — what's the difference?</b><br>
<ul>
  <li><b>F9 (Run Statement)</b> — runs only the single SQL statement your cursor is sitting in.
      Results appear in the <b>Query Result</b> tab at the bottom. Use this for SELECT queries.</li>
  <li><b>F5 (Run Script)</b> — runs every SQL statement in the worksheet top to bottom,
      as if they were in a script file. Output appears in the <b>Script Output</b> tab.
      Use this when you have multiple statements like INSERTs or DDL.</li>
</ul>
<br>

<b>View results:</b><br>
After running a SELECT, click the <b>Query Result</b> tab at the bottom to see the data in
a grid. You can:<br>
<ul>
  <li>Click any column header to sort the results.</li>
  <li>Right-click the grid → <b>Export</b> to save results as CSV, Excel, or JSON.</li>
  <li>Double-click a cell to edit its value directly (if you have permission).</li>
</ul>
<br>

<b>View and edit stored code:</b><br>
Double-click any Procedure, Function, Package, or Trigger in the Navigator — its source code
opens directly in an editor tab. Make changes, then press <b>F10</b> (or click the
<b>Compile</b> button) to save and compile.
<br><br>

<b>Open multiple worksheets:</b><br>
You can have as many worksheet tabs open as you need. Each one can be connected to a
different database if required. Use <b>Alt+F10</b> again to open another one, or click
the <b>+</b> tab icon.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── 8. Tips & Tricks ──────────────────────────────────────────────────────
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">💡 Tips &amp; Tricks for SQL Developer</div>
  <div class="feature-grid">
    <div class="feature-pill">
      <strong>🎨 Change the Theme to Dark Mode</strong>
      <p>Go to <b>Tools → Preferences → Environment → Appearance → Theme</b>.
      Choose <em>Dark</em> or <em>Darcula</em> for easier reading on long sessions.</p>
    </div>
    <div class="feature-pill">
      <strong>📌 Pin Your Most-Used Connections</strong>
      <p>Right-click a connection → <b>Add to Favorites</b>. It appears at the top of the
      Connections panel so you don't have to scroll every time.</p>
    </div>
    <div class="feature-pill">
      <strong>⚡ Auto-Complete SQL Keywords</strong>
      <p>Press <b>Ctrl+Space</b> anywhere in the worksheet to trigger IntelliSense-style
      code completion — it suggests table names, column names, and SQL keywords.</p>
    </div>
    <div class="feature-pill">
      <strong>📊 Quick Data Preview Without Writing SQL</strong>
      <p>In the Navigator, right-click any table → <b>Open</b> → click the <b>Data</b> tab.
      You see the first 500 rows instantly — no SQL needed.</p>
    </div>
    <div class="feature-pill">
      <strong>🔎 Format (Pretty-Print) Your SQL</strong>
      <p>Paste messy SQL into the worksheet, select it all (<b>Ctrl+A</b>), then press
      <b>Ctrl+F7</b> to auto-format it into clean, readable indented SQL.</p>
    </div>
    <div class="feature-pill">
      <strong>📂 Save &amp; Reuse Your SQL Scripts</strong>
      <p>Press <b>Ctrl+S</b> to save the current worksheet as a <code>.sql</code> file.
      Press <b>Ctrl+O</b> to open a saved file later. Great for scripts you run regularly.</p>
    </div>
    <div class="feature-pill">
      <strong>🔄 Re-run Previous Queries</strong>
      <p>Press the <b>↑ Up Arrow</b> key in the worksheet to cycle through your query history,
      or open <b>View → History</b> to search all previously executed statements.</p>
    </div>
    <div class="feature-pill">
      <strong>🧩 Use Snippets for Repetitive Code</strong>
      <p>Open <b>View → Snippets</b> to access a library of ready-made SQL and PL/SQL
      code templates. Drag any snippet into your worksheet to insert it.</p>
    </div>
    <div class="feature-pill">
      <strong>📋 Explain Plan — Understand Why Queries Are Slow</strong>
      <p>Write a SELECT query, then press <b>F6</b> (or click <b>Explain Plan</b> in the
      toolbar). SQL Developer shows a diagram of how Oracle will execute the query —
      helping you spot missing indexes or inefficient operations.</p>
    </div>
    <div class="feature-pill">
      <strong>🔐 Avoid Accidentally Changing Data</strong>
      <p>Before running UPDATE or DELETE statements on a live database, always use a
      <b>SELECT</b> with the same WHERE clause first to confirm exactly which rows
      will be affected. Only then switch to UPDATE/DELETE.</p>
    </div>
    <div class="feature-pill">
      <strong>📤 Export Table Data Easily</strong>
      <p>Right-click any table in the Navigator → <b>Export Data</b>. Choose from CSV,
      Excel, JSON, XML, or SQL INSERT statements. Handy for sharing data or backups.</p>
    </div>
    <div class="feature-pill">
      <strong>🔧 Increase Font Size in the Editor</strong>
      <p>Go to <b>Tools → Preferences → Code Editor → Fonts</b> and increase the font size.
      Or hold <b>Ctrl</b> and scroll the mouse wheel in the editor to zoom in/out.</p>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── Keyboard Shortcuts ────────────────────────────────────────────────────
    st.markdown(
        """
<div class="content-card">
  <div class="card-title">⌨️ Essential Keyboard Shortcuts</div>
  <table class="shortcut-table">
    <tr><th>Shortcut</th><th>Action</th></tr>
    <tr><td>F9 / Ctrl+Enter</td><td>Run the current SQL statement</td></tr>
    <tr><td>F5</td><td>Run all statements in the worksheet as a script</td></tr>
    <tr><td>F6</td><td>Explain Plan — see the query execution plan</td></tr>
    <tr><td>F10</td><td>Compile PL/SQL (procedure / function / package)</td></tr>
    <tr><td>Ctrl+Space</td><td>Auto-complete — suggest table/column/keyword names</td></tr>
    <tr><td>Alt+F10</td><td>Open a new SQL Worksheet</td></tr>
    <tr><td>Ctrl+F7</td><td>Format / pretty-print selected SQL</td></tr>
    <tr><td>Ctrl+/</td><td>Comment / uncomment selected lines</td></tr>
    <tr><td>Ctrl+S</td><td>Save current worksheet to a .sql file</td></tr>
    <tr><td>Ctrl+O</td><td>Open a saved .sql file</td></tr>
    <tr><td>Ctrl+A</td><td>Select all text in the worksheet</td></tr>
    <tr><td>↑ / ↓ (in editor)</td><td>Cycle through SQL statement history</td></tr>
    <tr><td>Ctrl+Z</td><td>Undo last change</td></tr>
    <tr><td>Ctrl+Shift+Z</td><td>Redo</td></tr>
  </table>
</div>
""",
        unsafe_allow_html=True,
    )
