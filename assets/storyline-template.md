---
core_message: Training-free sparse caching can halve long-context inference latency with almost no accuracy loss
duration_min: 15
audience: peer experts
---

# Storyline

<!-- Below is a complete example. Replace frontmatter and all pages when using. -->

<!--
Format (scripts/lint_storyline.py depends on this format):
  <number>. [<tag>] <conclusion-sentence title> (<minutes> min)
Minutes are optional. Explanatory text that should not be linted goes in HTML comments.

Tags:
  hook          Opening: grab the audience with a problem or phenomenon
  motivation    Why it matters
  question      The specific question this work answers
  contribution  What we did / found (one-sentence preview of results)
  outline       Roadmap (may be omitted for short talks)
  section       Section divider (only this page type may use a topic-style title)
  method        Method / model / system
  result        Result (one conclusion per page)
  discussion    Comparison with 2–3 most related works, limitations, significance
  takeaway      Conclusion: restate core message, return to the big question
  future        Future work
  ack           Acknowledgments / credits
  backup        Backup pages (placed after the main line, not counted in duration)

Reading only the titles should tell a coherent story.
-->

1. [hook] Long-context inference cost grows quadratically with length, becoming a deployment bottleneck (1 min)
2. [question] Can attention overhead be reduced to linear without retraining? (1 min)
3. [contribution] Our sparse caching halves latency at 64k length with <0.5% accuracy loss (1 min)
4. [method] Most attention concentrates on a small number of "anchor" tokens (1.5 min)
5. [method] Caching anchors + sliding window approximates full attention (2 min)
6. [result] Accuracy matches full attention on 4 benchmarks (2 min)
7. [result] Latency grows linearly with length, 2.1× faster at 64k (2 min)
8. [result] Gains mainly come from anchor selection, not window size (1.5 min)
9. [discussion] Compared with A and B, we require no fine-tuning and support any model (1.5 min)
10. [takeaway] Training-free sparse caching reduces long-context deployment cost by half (1.5 min)

<!-- Backup pages below -->
11. [backup] Full results table for all 12 benchmarks
12. [backup] Ablation study on anchor count
13. [backup] Detailed comparison with related work
