import type { Problem } from './types';

const API_URL = 'http://localhost:8080';

export async function searchProblems(query: string): Promise<Problem[]> {
  const response = await fetch(`${API_URL}/api/problems/search?query=${encodeURIComponent(query)}`);
  if (!response.ok) {
    throw new Error('Failed to search problems');
  }
  return response.json();
}

export async function createProblem(problem: Omit<Problem, 'id' | 'createdAt' | 'updatedAt'>): Promise<Problem> {
  const response = await fetch(`${API_URL}/api/problems`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(problem),
  });
  if (!response.ok) {
    throw new Error('Failed to create problem');
  }
  return response.json();
}