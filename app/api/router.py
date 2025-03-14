from fastapi import APIRouter, HTTPException, Depends
from typing import List

from models import ProblemCreate, Problem
from services.problem_service import create_problem, search_problems

router = APIRouter()

@router.post("/api/problems", response_model=Problem)
async def create_problem_endpoint(problem: ProblemCreate):
    """Create a new problem."""
    return create_problem(problem)

@router.get("/api/problems/search", response_model=List[Problem])
async def search_problems_endpoint(query: str, limit: int = 10):
    """Search for problems by query."""
    return search_problems(query, limit)