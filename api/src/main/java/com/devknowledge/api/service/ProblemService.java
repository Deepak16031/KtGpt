package com.devknowledge.api.service;

import com.devknowledge.api.model.Problem;
import com.devknowledge.api.repository.ProblemRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class ProblemService {
  private final ProblemRepository problemRepository;
  private final LlmService llmService;

  @Transactional
  public Problem createProblem(Problem problem) {
    Problem savedProblem = problemRepository.save(problem);
    llmService.generateEmbeddings(savedProblem);
    return savedProblem;
  }

  @Transactional(readOnly = true)
  public List<Problem> searchProblems(String query) {
    // First try semantic search via LLM service
    List<Problem> semanticResults = llmService.semanticSearch(query);
    if (!semanticResults.isEmpty()) {
      return semanticResults;
    }

    // Fallback to basic text search
    return problemRepository.searchByQuery(query);
  }
}
