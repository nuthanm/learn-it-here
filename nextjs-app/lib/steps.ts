/**
 * Project requirements questionnaire definition.
 * Mirrors the STEPS list in the Streamlit pages/requirements.py.
 */

export type QuestionKind = "select" | "multi" | "text";

export interface Step {
  key: string;
  title: string;
  help: string;
  kind: QuestionKind;
  options?: string[];
  section: string;
  placeholder?: string;
}

export const VC_OPTIONS = [
  "Git",
  "SVN (Subversion)",
  "TFS (Team Foundation)",
  "Mercurial",
  "Perforce",
  "None",
  "Other",
];

export const CODE_PUSH_OPTIONS = [
  "GIT CLI (Command Line)",
  "GitHub Desktop",
  "Visual Studio Built-in Git",
  "VS Code Built-in Git",
  "SourceTree",
  "GitKraken",
  "TortoiseGit",
  "Azure DevOps (Web Push)",
  "Fork (Git Client)",
  "Other",
];

export const IDE_OPTIONS = [
  "Visual Studio (Full IDE)",
  "Visual Studio Code",
  "IntelliJ IDEA",
  "Eclipse",
  "Rider (JetBrains)",
  "PyCharm",
  "WebStorm",
  "Sublime Text",
  "Atom",
  "Notepad++",
  "Vim / Neovim",
  "Other",
];

export const DEPLOYMENT_OPTIONS = [
  "Azure DevOps Pipelines (CI/CD)",
  "GitHub Actions",
  "Jenkins",
  "AWS CodePipeline",
  "Docker / Containers",
  "Kubernetes (K8s)",
  "Manual / FTP Deploy",
  "Azure App Service",
  "IIS Direct Deploy",
  "Other",
];

export const ARCHITECTURE_OPTIONS = [
  "Clean Architecture",
  "Microservices",
  "Monolithic",
  "Layered (N-Tier)",
  "Event-Driven",
  "Serverless",
  "CQRS",
  "DDD (Domain-Driven Design)",
  "Hexagonal (Ports & Adapters)",
  "MVC",
  "Other",
];

export const DESIGN_PATTERN_OPTIONS = [
  "Repository Pattern",
  "Unit of Work",
  "Singleton",
  "Factory",
  "Strategy",
  "Observer",
  "Mediator (MediatR)",
  "Dependency Injection",
  "SOLID Principles",
  "Builder",
  "Decorator",
  "Other",
];

export const ORM_OPTIONS = [
  "Entity Framework Core",
  "Entity Framework 6",
  "Dapper",
  "NHibernate",
  "ADO.NET (Raw)",
  "Hibernate (Java)",
  "SQLAlchemy (Python)",
  "Django ORM (Python)",
  "Sequelize (Node.js)",
  "Prisma (Node.js)",
  "None / Not applicable",
  "Other",
];

export const STEPS: Step[] = [
  {
    key: "version_control",
    title: "Version control",
    help: "Which version control system does your team use?",
    kind: "select",
    options: VC_OPTIONS,
    section: "Version Management",
  },
  {
    key: "code_push",
    title: "How do you push the code?",
    help: "Which tool or method do you use to push code to the remote repository?",
    kind: "select",
    options: CODE_PUSH_OPTIONS,
    section: "Version Management",
  },
  {
    key: "ide",
    title: "IDE or editor",
    help: "Select the IDE / editor your team primarily uses.",
    kind: "select",
    options: IDE_OPTIONS,
    section: "Development Environment",
  },
  {
    key: "deployment",
    title: "Deployment approaches",
    help: "Select all deployment strategies that apply to your project.",
    kind: "multi",
    options: DEPLOYMENT_OPTIONS,
    section: "Development Environment",
  },
  {
    key: "architecture",
    title: "Architecture patterns",
    help: "Select the architecture patterns followed in your project.",
    kind: "multi",
    options: ARCHITECTURE_OPTIONS,
    section: "Architecture",
  },
  {
    key: "design_patterns",
    title: "Design patterns",
    help: "Select the design patterns commonly used in your codebase.",
    kind: "multi",
    options: DESIGN_PATTERN_OPTIONS,
    section: "Architecture",
  },
  {
    key: "orm",
    title: "ORM",
    help: "Which ORM framework does your project use?",
    kind: "select",
    options: ORM_OPTIONS,
    section: "Architecture",
  },
  {
    key: "additional_requirements",
    title: "Additional notes",
    help: "Any other tools, frameworks, or notes you'd like to mention?",
    kind: "text",
    section: "Other",
    placeholder:
      "e.g. We use Docker for containerization, Redis for caching, CI/CD with GitHub Actions…",
  },
];
