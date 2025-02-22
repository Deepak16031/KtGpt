package com.devknowledge.api.controller;

import com.devknowledge.api.model.Problem;
import com.devknowledge.api.service.ProblemService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

        import java.util.List;

@RestController
@RequestMapping("/api/problems")
@RequiredArgsConstructor
public class ProblemController {
    private final ProblemService problemService;

    @PostMapping
    public ResponseEntity<Problem> createProblem(@RequestBody Problem problem) {
        Problem createdProblem = problemService.createProblem(problem);
        return ResponseEntity.ok(createdProblem);
    }

    @GetMapping("/search")
    public ResponseEntity<List<Problem>> searchProblems(@RequestParam String query) {
        List<Problem> results = problemService.searchProblems(query);
        return ResponseEntity.ok(results);
    }
}
