from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CodeSnippet(BaseModel):
    language: str
    content: str

class ProblemCreate(BaseModel):
    title: str
    description: str
    solution: str
    tags: List[str] = []
    codeSnippets: List[CodeSnippet] = []

class Problem(ProblemCreate):
    id: str
    createdAt: str
    updatedAt: str