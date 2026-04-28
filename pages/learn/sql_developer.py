"""Oracle SQL Developer: minimal-layout page using shared content primitives."""

import streamlit as st

from components.content import (
    code_block,
    link_list,
    paragraph,
    section_intro,
    section_title,
    subsection,
)


def render_sql_developer():
    section_title(
        "Oracle SQL Developer",
        "A friendly, free graphical tool for working with Oracle databases.",
    )
    section_intro(
        "Download, install, connect, browse, and query Oracle databases — plus "
        "the everyday tips and shortcuts that make SQL Developer pleasant to use."
    )

    # ── What is SQL Developer? ────────────────────────────────────────────────
    subsection("What is Oracle SQL Developer?")
    paragraph(
        "Oracle SQL Developer is a free graphical tool made by Oracle Corporation "
        "that lets you work with Oracle databases without needing to type complex "
        "commands in a terminal. Think of it as a friendly window into your "
        "database — you can click through tables, write and run SQL queries, "
        "view stored code, and manage database objects all from one place."
    )
    paragraph("Who is it for?")
    link_list(
        [
            "Beginners — explore a database visually, no command-line knowledge required.",
            "Developers — write, test, and debug SQL and PL/SQL code quickly.",
            "DBAs (Database Administrators) — manage users, monitor sessions, and run scripts.",
        ]
    )
    paragraph(
        "In plain English: if your data lives in an Oracle database, SQL Developer "
        "is the easiest way to see it, query it, and change it — all for free."
    )

    # ── Official Download ────────────────────────────────────────────────────
    subsection("Where to download SQL Developer (official link)")
    paragraph(
        "Always download SQL Developer directly from Oracle's official website to "
        "ensure you get the latest, safe version."
    )
    link_list(
        [
            (
                "Official download page",
                "https://www.oracle.com/database/sqldeveloper/technologies/download/",
                "Oracle SQL Developer downloads",
            ),
        ]
    )
    paragraph("Which version should I pick?")
    link_list(
        [
            "Choose the Windows 64-bit with JDK included package if you are on Windows — it bundles Java so you don't need to install anything else first.",
            "Choose the platform-specific package (macOS or Linux) if you're on those systems.",
        ]
    )
    paragraph(
        "Note: you may need to create a free Oracle account to download the file. "
        "The sign-up is completely free and only takes a minute."
    )

    # ── Database Support ─────────────────────────────────────────────────────
    subsection("Which databases does SQL Developer support?")
    paragraph("Primary support — Oracle Database:")
    paragraph(
        "SQL Developer is built specifically for Oracle databases and provides the "
        "deepest support for them:"
    )
    link_list(
        [
            "Connect to any Oracle database (on your computer, on a server, or in the cloud).",
            "Browse and edit every type of Oracle object — tables, views, packages, procedures, triggers, sequences, and more.",
            "Write, run, and debug PL/SQL (Oracle's built-in programming language).",
            "Works with Oracle Database 11g, 12c, 18c, 19c, 21c and the latest versions.",
        ]
    )
    paragraph("Other databases — limited support via third-party JDBC drivers:")
    paragraph(
        "SQL Developer can also connect to non-Oracle databases, but the experience "
        "is more basic compared to dedicated tools for those databases."
    )
    st.markdown(
        """
| Database | Supported? | What You Need |
| --- | --- | --- |
| Oracle | Full support | Built-in — nothing extra needed |
| MySQL | Partial | Download MySQL JDBC driver (.jar file) and add it in SQL Developer preferences |
| SQL Server | Partial | Download Microsoft JDBC driver for SQL Server and configure it |
| PostgreSQL | Partial | Download PostgreSQL JDBC driver (postgresql-xx.jar) and configure it |
| IBM DB2 | Partial | Requires IBM JDBC driver |
"""
    )
    paragraph(
        "Recommendation: for SQL Server, use SQL Server Management Studio (SSMS). "
        "For PostgreSQL, use pgAdmin. These are free tools purpose-built for those "
        "databases and will give you a much better experience. Use SQL Developer "
        "when you are primarily working with Oracle."
    )

    # ── Installation Steps ───────────────────────────────────────────────────
    subsection("Installation steps (Windows)")
    paragraph(
        "SQL Developer is very easy to install on Windows because it comes as a "
        "simple ZIP file — there is no complex installer wizard."
    )

    paragraph(
        "Step 1 — Download the ZIP. Go to the official download page, choose "
        '"Windows 64-bit with JDK included", and save the ZIP file to your '
        "computer (e.g. your Desktop or Downloads folder)."
    )
    paragraph(
        "Screenshot tip: you'll see a table of download options — look for the row "
        'that says "Windows 64-bit with JDK" and click the download link on the right.'
    )

    paragraph(
        "Step 2 — Extract the ZIP. Right-click the downloaded ZIP file → "
        "Extract All… → choose a destination folder (for example C:\\sqldeveloper)."
    )
    paragraph(
        'Screenshot tip: Windows will show an "Extract Compressed Folders" dialog '
        '— just click "Extract" and wait for it to finish.'
    )

    paragraph(
        "Step 3 — Run SQL Developer. Open the extracted folder and double-click "
        "sqldeveloper.exe to launch the tool."
    )
    paragraph(
        "Screenshot tip: you'll see the SQL Developer icon — an orange circle with "
        "a white plug symbol."
    )

    paragraph(
        "Step 4 — First-time setup (optional). On the very first launch, SQL "
        "Developer may ask if you want to import settings from a previous version. "
        'If this is your first time, click "No".'
    )

    paragraph("Step 5 — You're in! The SQL Developer window opens. You'll see:")
    link_list(
        [
            "A left panel (Connections & Navigator) — for browsing database connections and objects.",
            "A main area (Worksheet) — where you write and run SQL.",
            "A bottom panel — where query results appear.",
        ]
    )
    paragraph(
        "No installation on macOS/Linux? On macOS, download the .dmg file, "
        "double-click it, and drag SQL Developer to your Applications folder. On "
        "Linux, download the .rpm or .tar.gz and follow the instructions in the "
        "README file inside the package."
    )

    # ── Connecting to a Database ─────────────────────────────────────────────
    subsection("How to connect to an Oracle database")
    paragraph(
        "Connecting SQL Developer to an Oracle database is like giving it the "
        "address and password to the front door. Here is exactly how to do it."
    )

    paragraph(
        "Step 1 — Open the New Connection dialog. In the left panel, click the "
        'green + icon next to "Connections", or go to File → New → Database '
        "Connection."
    )

    paragraph(
        "Step 2 — Fill in the connection details. A dialog box appears with "
        "several fields. Here's what each one means:"
    )
    st.markdown(
        """
| Field | What to enter | Example |
| --- | --- | --- |
| Connection Name | A friendly label you choose — just for you | MyLocalDB |
| Username | Your Oracle database username | hr |
| Password | Your Oracle database password | •••••••• |
| Hostname | The server address (IP or machine name) | localhost or 192.168.1.10 |
| Port | The port Oracle listens on (default is 1521) | 1521 |
| SID / Service Name | The name of the Oracle database instance | ORCL or XEPDB1 |
"""
    )
    paragraph("SID vs Service Name — which one?")
    link_list(
        [
            "SID — older style, used for single databases (e.g. ORCL).",
            "Service Name — modern style, recommended for most setups (e.g. XEPDB1 for Oracle XE, or orclpdb1 for container databases).",
        ]
    )
    paragraph(
        "If you're not sure, ask the person who set up the database, or try "
        "XEPDB1 for a local Oracle XE installation."
    )

    paragraph(
        'Step 3 — Test the connection. Click the "Test" button at the bottom of '
        'the dialog. You should see "Status: Success" in the bottom-left corner. '
        "If it shows an error, double-check your hostname, port, and credentials."
    )

    paragraph(
        'Step 4 — Save and Connect. Click "Save" to remember this connection for '
        'next time, then click "Connect". Your new connection appears in the left '
        'panel under "Connections". Click the triangle/arrow next to it to expand '
        "the database objects."
    )

    paragraph("Common connection errors and fixes:")
    st.markdown(
        """
| Error message | Likely cause | Fix |
| --- | --- | --- |
| IO Error: The Network Adapter could not establish the connection | Wrong hostname or port, or Oracle listener is not running | Check hostname/port; start the Oracle listener service |
| ORA-01017: invalid username/password | Wrong credentials | Double-check username and password (case-sensitive) |
| ORA-12514: TNS:listener does not currently know of service | Wrong Service Name or SID | Try the other option (switch from SID to Service Name or vice versa) |
"""
    )

    # ── Viewing Database Objects ─────────────────────────────────────────────
    subsection("How to view database objects")
    paragraph(
        "Once connected, you can browse everything in the database from the "
        "left-side panel called the Database Navigator. Think of it like Windows "
        "Explorer but for your database."
    )
    paragraph(
        'Expand your connection name → expand "Other Users" to browse other '
        "schemas, or browse your own schema directly. You'll see folders for "
        "every type of object."
    )
    link_list(
        [
            "Tables — expand Tables to see all tables in the schema. Click any table name to open a detail window showing its Columns, Data, Constraints, Indexes, and Grants in separate tabs.",
            "Views — expand Views to see virtual tables (queries saved as named views). Click a view to see its definition (the SQL behind it) and its data.",
            "Packages — expand Packages to see PL/SQL packages — bundles of related procedures and functions. Click a package to see its Spec (the public interface) and Body (the actual code).",
            "Procedures — expand Procedures to see standalone stored procedures. Double-click one to open its code in the editor, where you can read, edit, and recompile it.",
            "Triggers — expand Triggers to see all triggers. A trigger is code that runs automatically when a row is inserted, updated, or deleted. Click one to view its code and the table it fires on.",
            "Functions — expand Functions for standalone PL/SQL functions — similar to procedures but they return a value. Double-click to open the source code.",
            "Sequences — expand Sequences to see auto-number generators (like an identity column in other databases). Used to generate unique IDs for primary keys.",
            "Indexes — expand Indexes to see all indexes — these speed up queries. Click an index to see which table and columns it covers.",
        ]
    )
    paragraph(
        "Quick tip — filter objects by name: if a schema has hundreds of tables, "
        "right-click the Tables folder → Apply Filter → type part of the table "
        "name → click OK. Only matching tables are shown."
    )
    paragraph(
        "Quick tip — jump straight to an object: use View → Find DB Object to "
        "search for any object by name across all schemas at once."
    )

    # ── Query Window ─────────────────────────────────────────────────────────
    subsection("How to open a query window and run SQL")
    paragraph(
        "The SQL Worksheet is where you type and run SQL queries. Here's how to "
        "use it."
    )

    paragraph("Open a new Worksheet (query window):")
    link_list(
        [
            "Press Alt+F10 (fastest way), or",
            "Click Tools → SQL Worksheet from the menu, or",
            "Right-click your connection in the Navigator → Open SQL Worksheet.",
        ]
    )
    paragraph(
        "A blank worksheet opens. Make sure the correct connection is selected "
        "in the drop-down at the top of the worksheet."
    )

    paragraph("Write and run a query. Type your SQL in the worksheet area:")
    code_block(
        "SELECT * FROM employees WHERE department_id = 10;",
        language="sql",
    )
    paragraph("Then run it using one of these methods:")
    st.markdown(
        """
| Action | Keyboard shortcut | Toolbar button |
| --- | --- | --- |
| Run the statement your cursor is in | F9 or Ctrl+Enter | Green play button |
| Run the entire script (all statements) | F5 | Script run button |
"""
    )
    paragraph("F9 vs F5 — what's the difference?")
    link_list(
        [
            "F9 (Run Statement) — runs only the single SQL statement your cursor is sitting in. Results appear in the Query Result tab at the bottom. Use this for SELECT queries.",
            "F5 (Run Script) — runs every SQL statement in the worksheet top to bottom, as if they were in a script file. Output appears in the Script Output tab. Use this when you have multiple statements like INSERTs or DDL.",
        ]
    )

    paragraph(
        "View results: after running a SELECT, click the Query Result tab at the "
        "bottom to see the data in a grid. You can:"
    )
    link_list(
        [
            "Click any column header to sort the results.",
            "Right-click the grid → Export to save results as CSV, Excel, or JSON.",
            "Double-click a cell to edit its value directly (if you have permission).",
        ]
    )

    paragraph(
        "View and edit stored code: double-click any Procedure, Function, "
        "Package, or Trigger in the Navigator — its source code opens directly "
        "in an editor tab. Make changes, then press F10 (or click the Compile "
        "button) to save and compile."
    )

    paragraph(
        "Open multiple worksheets: you can have as many worksheet tabs open as "
        "you need. Each one can be connected to a different database if "
        "required. Use Alt+F10 again to open another one, or click the + tab icon."
    )

    # ── Tips & Tricks ────────────────────────────────────────────────────────
    subsection("Tips and tricks for SQL Developer")
    link_list(
        [
            "Change the theme to dark mode — Tools → Preferences → Environment → Appearance → Theme. Choose Dark or Darcula for easier reading on long sessions.",
            "Pin your most-used connections — right-click a connection → Add to Favorites. It appears at the top of the Connections panel so you don't have to scroll every time.",
            "Auto-complete SQL keywords — press Ctrl+Space anywhere in the worksheet to trigger IntelliSense-style code completion (suggests table names, column names, and SQL keywords).",
            "Quick data preview without writing SQL — in the Navigator, right-click any table → Open → click the Data tab. You see the first 500 rows instantly.",
            "Format (pretty-print) your SQL — paste messy SQL into the worksheet, select it all (Ctrl+A), then press Ctrl+F7 to auto-format it into clean, readable indented SQL.",
            "Save and reuse your SQL scripts — press Ctrl+S to save the current worksheet as a .sql file. Press Ctrl+O to open a saved file later. Great for scripts you run regularly.",
            "Re-run previous queries — press the Up Arrow key in the worksheet to cycle through your query history, or open View → History to search all previously executed statements.",
            "Use snippets for repetitive code — open View → Snippets to access a library of ready-made SQL and PL/SQL code templates. Drag any snippet into your worksheet to insert it.",
            "Explain Plan — understand why queries are slow. Write a SELECT query, then press F6 (or click Explain Plan in the toolbar). SQL Developer shows a diagram of how Oracle will execute the query — helping you spot missing indexes or inefficient operations.",
            "Avoid accidentally changing data — before running UPDATE or DELETE statements on a live database, always use a SELECT with the same WHERE clause first to confirm exactly which rows will be affected. Only then switch to UPDATE/DELETE.",
            "Export table data easily — right-click any table in the Navigator → Export Data. Choose from CSV, Excel, JSON, XML, or SQL INSERT statements. Handy for sharing data or backups.",
            "Increase font size in the editor — Tools → Preferences → Code Editor → Fonts. Or hold Ctrl and scroll the mouse wheel in the editor to zoom in/out.",
        ]
    )

    # ── Keyboard Shortcuts ───────────────────────────────────────────────────
    subsection("Essential keyboard shortcuts")
    st.markdown(
        """
| Shortcut | Action |
| --- | --- |
| F9 / Ctrl+Enter | Run the current SQL statement |
| F5 | Run all statements in the worksheet as a script |
| F6 | Explain Plan — see the query execution plan |
| F10 | Compile PL/SQL (procedure / function / package) |
| Ctrl+Space | Auto-complete — suggest table/column/keyword names |
| Alt+F10 | Open a new SQL Worksheet |
| Ctrl+F7 | Format / pretty-print selected SQL |
| Ctrl+/ | Comment / uncomment selected lines |
| Ctrl+S | Save current worksheet to a .sql file |
| Ctrl+O | Open a saved .sql file |
| Ctrl+A | Select all text in the worksheet |
| Up / Down (in editor) | Cycle through SQL statement history |
| Ctrl+Z | Undo last change |
| Ctrl+Shift+Z | Redo |
"""
    )
