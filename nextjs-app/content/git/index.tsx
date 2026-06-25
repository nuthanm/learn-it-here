import CodeBlock from "@/components/CodeBlock";
import ContentTable from "@/components/ContentTable";

export function GitBasics() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>GIT — Basics</h2>
      <p className="text-sm mb-1" style={{ color: "var(--muted)" }}>Foundational commands you&apos;ll use every single day.</p>
      <p className="text-sm mb-5" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Git is a distributed version control system. These commands cover the everyday loop:
        get the code, see what changed, save your work, share it.
      </p>

      <h3 className="font-semibold text-sm mb-2" style={{ color: "var(--ink)" }}>Get the code</h3>
      <p className="text-sm mb-2" style={{ color: "var(--body)" }}>Clone a remote repository onto your machine:</p>
      <CodeBlock language="bash">{`git clone https://github.com/example/repo.git`}</CodeBlock>

      <h3 className="font-semibold text-sm mb-2 mt-4" style={{ color: "var(--ink)" }}>See what changed</h3>
      <p className="text-sm mb-2" style={{ color: "var(--body)" }}>Inspect the working tree and view a compact log of recent commits:</p>
      <CodeBlock language="bash">{`git status\ngit log --oneline -n 10`}</CodeBlock>

      <h3 className="font-semibold text-sm mb-2 mt-4" style={{ color: "var(--ink)" }}>Save your progress</h3>
      <p className="text-sm mb-2" style={{ color: "var(--body)" }}>Stage files and record a commit with a meaningful message:</p>
      <CodeBlock language="bash">{`git add .\ngit commit -m "feat: add forgot password flow"`}</CodeBlock>

      <h3 className="font-semibold text-sm mb-2 mt-4" style={{ color: "var(--ink)" }}>Share your work</h3>
      <p className="text-sm mb-2" style={{ color: "var(--body)" }}>Push your branch to the remote so others can review it:</p>
      <CodeBlock language="bash">{`git push origin feature/forgot-password`}</CodeBlock>

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Quick-reference cheat sheet</h3>
      <ContentTable headers={["Command", "What it does"]} rows={[
        ["`git clone <url>`", "Copy a remote repository to your local machine"],
        ["`git status`", "Show which files are modified, staged, or untracked"],
        ["`git diff`", "Show line-by-line changes not yet staged"],
        ["`git add .`", "Stage all changed files for the next commit"],
        ["`git add <file>`", "Stage a single file"],
        ["`git commit -m \"message\"`", "Save staged changes as a new commit"],
        ["`git push origin <branch>`", "Upload your local commits to the remote branch"],
        ["`git pull`", "Fetch remote changes and merge them into your current branch"],
        ["`git log --oneline`", "Compact one-line history of recent commits"],
        ["`git log --oneline --graph`", "Visual branch/merge history in the terminal"],
        ["`git show <sha>`", "Show the changes introduced by a specific commit"],
        ["`git stash`", "Temporarily shelve uncommitted changes"],
        ["`git stash pop`", "Re-apply the most recently stashed changes"],
      ]} />

      <p className="text-sm mt-4" style={{ color: "var(--muted)" }}>Further reading: {" "}
        <a href="https://git-scm.com/book" target="_blank" rel="noopener noreferrer" className="font-semibold no-underline hover:underline" style={{ color: "var(--accent)" }}>Pro Git book (free)</a>
        {" · "}
        <a href="https://education.github.com/git-cheat-sheet-education.pdf" target="_blank" rel="noopener noreferrer" className="font-semibold no-underline hover:underline" style={{ color: "var(--accent)" }}>Git cheatsheet (GitHub)</a>
      </p>
    </div>
  );
}

export function GitBranching() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>GIT — Branching</h2>
      <p className="text-sm mb-1" style={{ color: "var(--muted)" }}>Work in isolation, then merge cleanly.</p>
      <p className="text-sm mb-5" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Branches let you develop features without disturbing the main codebase.
        Create one, switch to it, push it, and open a pull request when ready.
      </p>

      <h3 className="font-semibold text-sm mb-2" style={{ color: "var(--ink)" }}>Create and switch to a branch</h3>
      <CodeBlock language="bash">{`git checkout -b feature/forgot-password`}</CodeBlock>

      <h3 className="font-semibold text-sm mb-2 mt-4" style={{ color: "var(--ink)" }}>List branches</h3>
      <CodeBlock language="bash">{`git branch        # local\ngit branch -a     # local + remote`}</CodeBlock>

      <h3 className="font-semibold text-sm mb-2 mt-4" style={{ color: "var(--ink)" }}>Merge a branch</h3>
      <p className="text-sm mb-2" style={{ color: "var(--body)" }}>Bring another branch&apos;s history into your current branch:</p>
      <CodeBlock language="bash">{`git checkout main\ngit pull\ngit merge feature/forgot-password`}</CodeBlock>

      <h3 className="font-semibold text-sm mb-2 mt-4" style={{ color: "var(--ink)" }}>Delete a finished branch</h3>
      <CodeBlock language="bash">{`git branch -d feature/forgot-password`}</CodeBlock>

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Quick-reference cheat sheet</h3>
      <ContentTable headers={["Command", "What it does"]} rows={[
        ["`git branch`", "List all local branches"],
        ["`git branch -a`", "List local and remote branches"],
        ["`git checkout -b <name>`", "Create a new branch and switch to it"],
        ["`git switch <name>`", "Switch to an existing branch (modern syntax)"],
        ["`git switch -c <name>`", "Create and switch to a new branch (modern syntax)"],
        ["`git push -u origin <name>`", "Push new branch to remote and set tracking"],
        ["`git merge <branch>`", "Merge the named branch into your current branch"],
        ["`git rebase <branch>`", "Replay your commits on top of the named branch"],
        ["`git branch -d <name>`", "Delete a local branch (safe — won't delete unmerged)"],
        ["`git branch -D <name>`", "Force-delete a local branch (even if unmerged)"],
        ["`git push origin --delete <name>`", "Delete the branch on the remote"],
        ["`git fetch --prune`", "Remove local references to deleted remote branches"],
        ["`git cherry-pick <sha>`", "Apply a single commit from another branch"],
      ]} />
    </div>
  );
}

export function GitOverview() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>GIT</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Select a sub-topic from the sidebar to explore Git Basics or Branching.
      </p>
      <ul className="text-sm list-disc pl-5" style={{ color: "var(--body)" }}>
        <li className="mb-1"><strong>Basics</strong> — everyday commands: clone, status, add, commit, push, pull</li>
        <li className="mb-1"><strong>Branching</strong> — create, merge, rebase, delete branches</li>
      </ul>
    </div>
  );
}
