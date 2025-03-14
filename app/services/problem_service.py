import logging
import uuid
from datetime import datetime
from typing import List, Dict, Any

from psycopg2.extras import execute_values
from db.connection import get_connection, get_dict_cursor
from models import ProblemCreate, Problem
from core.embeddings import generate_embedding
from config import SIMILARITY_THRESHOLD

logger = logging.getLogger(__name__)


def create_problem(problem_data: ProblemCreate) -> Problem:
    """Create a new problem in the database."""
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)

        # Generate a new UUID
        problem_id = str(uuid.uuid4())
        current_time = datetime.now().isoformat()

        # Insert the problem
        cur.execute(
            """
            INSERT INTO problems (id, title, description, solution, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, title, description, solution, created_at, updated_at
            """,
            (problem_id, problem_data.title, problem_data.description, problem_data.solution,
             current_time, current_time)
        )
        problem = dict(cur.fetchone())

        # Insert tags if present
        if problem_data.tags:
            tags_values = [(problem_id, tag) for tag in problem_data.tags]
            execute_values(
                cur,
                "INSERT INTO problem_tags (problem_id, tag) VALUES %s",
                tags_values
            )

        # Insert code snippets if present
        if problem_data.codeSnippets:
            snippet_values = [
                (str(uuid.uuid4()), problem_id, snippet.language, snippet.content, current_time)
                for snippet in problem_data.codeSnippets
            ]
            execute_values(
                cur,
                "INSERT INTO code_snippets (id, problem_id, language, content, created_at) VALUES %s",
                snippet_values
            )

        # Generate and store embedding
        text = f"{problem_data.title} {problem_data.description} {problem_data.solution}"
        embedding = generate_embedding(text)

        cur.execute(
            "INSERT INTO embeddings (problem_id, embedding) VALUES (%s, %s)",
            (problem_id, embedding.tolist())
        )

        conn.commit()

        # Get the full problem with tags and snippets
        result = _get_problem_by_id(problem_id, cur)

        cur.close()
        conn.close()

        return result

    except Exception as e:
        logger.error(f"Error creating problem: {str(e)}", exc_info=True)
        raise


def search_problems(query: str, limit: int = 10) -> List[Problem]:
    """Search for problems using semantic search with fallback to text search."""
    try:
        # First try semantic search
        semantic_results = _semantic_search(query, limit)

        # If semantic search returns results, use them
        if semantic_results:
            return semantic_results

        # Otherwise, fallback to text search
        return _text_search(query, limit)

    except Exception as e:
        logger.error(f"Error during search: {str(e)}", exc_info=True)
        raise


def _semantic_search(query: str, limit: int = 10) -> List[Problem]:
    """Perform semantic search using embeddings."""
    query_embedding = generate_embedding(query)

    conn = get_connection()
    cur = get_dict_cursor(conn)

    # Perform semantic search using cosine similarity
    cur.execute("""
        SELECT p.id, p.title, p.description, p.solution, p.created_at, p.updated_at,
               1 - (e.embedding <-> %s::vector) as similarity
        FROM problems p
        JOIN embeddings e ON p.id = e.problem_id
        WHERE 1 - (e.embedding <-> %s::vector) > %s
        ORDER BY similarity DESC
        LIMIT %s
    """, (query_embedding.tolist(), query_embedding.tolist(), SIMILARITY_THRESHOLD, limit))

    results = cur.fetchall()

    if not results:
        cur.close()
        conn.close()
        return []

    problems = []
    for row in results:
        problem_id = row['id']
        problems.append(_get_problem_by_id(problem_id, cur))

    cur.close()
    conn.close()
    return problems


def _text_search(query: str, limit: int = 10) -> List[Problem]:
    """Perform text search on title, description and tags."""
    conn = get_connection()
    cur = get_dict_cursor(conn)

    # Perform text search on title, description and tags
    like_pattern = f"%{query}%"

    cur.execute("""
        SELECT DISTINCT p.id, p.title, p.description, p.solution, p.created_at, p.updated_at
        FROM problems p
        LEFT JOIN problem_tags pt ON p.id = pt.problem_id
        WHERE 
            LOWER(p.title) LIKE LOWER(%s) OR
            LOWER(p.description) LIKE LOWER(%s) OR
            LOWER(pt.tag) LIKE LOWER(%s)
        LIMIT %s
    """, (like_pattern, like_pattern, like_pattern, limit))

    results = cur.fetchall()

    if not results:
        cur.close()
        conn.close()
        return []

    problems = []
    for row in results:
        problem_id = row['id']
        problems.append(_get_problem_by_id(problem_id, cur))

    cur.close()
    conn.close()
    return problems


def _get_problem_by_id(problem_id: str, cursor) -> Problem:
    """Get a problem by ID with its tags and code snippets."""
    # Get the problem
    cursor.execute(
        """
        SELECT p.id, p.title, p.description, p.solution, p.created_at, p.updated_at
        FROM problems p
        WHERE p.id = %s
        """,
        (problem_id,)
    )
    problem = dict(cursor.fetchone())

    # Get tags
    cursor.execute(
        "SELECT tag FROM problem_tags WHERE problem_id = %s",
        (problem_id,)
    )
    tags = [row['tag'] for row in cursor.fetchall()]

    # Get code snippets
    cursor.execute(
        "SELECT language, content FROM code_snippets WHERE problem_id = %s",
        (problem_id,)
    )
    code_snippets = [
        {"language": row['language'], "content": row['content']}
        for row in cursor.fetchall()
    ]

    # Format the response
    return {
        "id": str(problem["id"]),
        "title": problem["title"],
        "description": problem["description"],
        "solution": problem["solution"],
        "tags": tags,
        "codeSnippets": code_snippets,
        "createdAt": problem["created_at"].isoformat() if isinstance(problem["created_at"], datetime) else problem[
            "created_at"],
        "updatedAt": problem["updated_at"].isoformat() if isinstance(problem["updated_at"], datetime) else problem[
            "updated_at"]
    }
