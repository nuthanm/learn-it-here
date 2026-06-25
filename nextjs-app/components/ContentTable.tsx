interface ContentTableProps {
  headers: string[];
  rows: string[][];
}

/** Render an HTML table with the shared `content-table` CSS class. */
export default function ContentTable({ headers, rows }: ContentTableProps) {
  // Render `code` for content wrapped in backticks
  function renderCell(cell: string) {
    const parts = cell.split(/(`[^`]+`)/g);
    return parts.map((part, i) => {
      if (part.startsWith("`") && part.endsWith("`")) {
        return <code key={i}>{part.slice(1, -1)}</code>;
      }
      // Allow basic HTML entities (already safe — no user input here)
      return <span key={i} dangerouslySetInnerHTML={{ __html: part }} />;
    });
  }

  return (
    <div className="overflow-x-auto">
      <table className="content-table">
        <thead>
          <tr>
            {headers.map((h) => (
              <th key={h}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, ri) => (
            <tr key={ri}>
              {row.map((cell, ci) => (
                <td key={ci}>{renderCell(cell)}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
