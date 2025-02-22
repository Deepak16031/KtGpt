export interface Problem {
  id: string;
  title: string;
  description: string;
  solution: string;
  tags: string[];
  codeSnippets: CodeSnippet[];
  createdAt: string;
  updatedAt: string;
}

export interface CodeSnippet {
  language: string;
  code: string;
}

export type SearchResult = Problem;