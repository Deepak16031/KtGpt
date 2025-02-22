package com.devknowledge.api.service;

import com.devknowledge.api.model.Problem;
import com.devknowledge.api.repository.ProblemRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.Data;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpStatusCode;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.ResponseEntity;
import org.springframework.beans.factory.annotation.Value;
import java.util.*;

@Service
@Slf4j
public class LlmService {
  private final RestClient restClient;
  private final ProblemRepository problemRepository;
  private static final ObjectMapper objectMapper = new ObjectMapper();

  public LlmService(RestClient restClient, ProblemRepository problemRepository) {
    this.restClient = restClient;
    this.problemRepository = problemRepository;
  }

  public void generateEmbeddings(Problem problem) {
    EmbeddingRequestDTO request =
        new EmbeddingRequestDTO(
            problem.getId(),
            problem.getTitle(),
            problem.getDescription(),
            problem.getSolution(),
            problem.getCodeSnippets().stream()
                .map(s -> new CodeSnippetDTO(s.getLanguage(), s.getCode()))
                .toList(),
            new ArrayList<>(problem.getTags()));
  }

  public List<Problem> semanticSearch(String query) {
    try {
      ResponseEntity<List<Map<String, Object>>> response = restClient
              .get()
              .uri(uriBuilder -> uriBuilder.path("/search")
                      .queryParam("query", query)
                      .build())
              .retrieve()
              .toEntity(new ParameterizedTypeReference<List<Map<String, Object>>>() {});

      if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
        List<UUID> problemIds = response.getBody().stream()
                .map(map -> UUID.fromString((String) map.get("id")))
                .toList();
        return problemRepository.findAllById(problemIds);
      }
      return Collections.emptyList();
    } catch (Exception e) {
      log.error("Error during semantic search", e);
      return Collections.emptyList();
    }
  }

  // DTO Classes
  @Data
  @AllArgsConstructor
  private static class EmbeddingRequestDTO {
    private UUID problemId;
    private String title;
    private String description;
    private String solution;
    private List<CodeSnippetDTO> codeSnippets;
    private List<String> tags;
  }

  @Data
  @AllArgsConstructor
  private static class CodeSnippetDTO {
    private String language;
    private String content;
  }

  @Data
  @AllArgsConstructor
  private static class SearchRequestDTO {
    private String query;
  }

  @Data
  private static class SearchResultDTO {
    private List<UUID> problemIds;
  }
}
