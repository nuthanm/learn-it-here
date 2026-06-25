"use client";
import { useState } from "react";

interface CodeBlockProps {
  /** Reserved for future syntax highlighting (e.g. "bash", "csharp"). Currently unused. */
  language?: string;
  children: string;
}

export default function CodeBlock({ children }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(children).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className="cmd-block">
      <button
        className={`copy-btn${copied ? " copied" : ""}`}
        onClick={handleCopy}
        type="button"
        aria-label="Copy code">
        {copied ? "Copied!" : "Copy"}
      </button>
      {children}
    </div>
  );
}
