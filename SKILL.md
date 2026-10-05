---
name: research-presentation-slides
description: Create, adapt, or review presentation slides for "showing your own work" (research reports, conference talks, group meetings, defenses, job talks, project/technical sharing). Tool-agnostic (PowerPoint, Keynote, Google Slides, Beamer, Marp, Slidev, reveal.js, python-pptx, etc. are all fine). Provides a step-by-step workflow (talk brief → storyline → slide spec → production → PDF auto-check → review checklist), templates, and check scripts. Use this skill whenever the user wants to make slides/PPT/deck/beamer/presentation/talk, generate report slides from a paper or code repo, or have you review/improve existing slides—even if the user only says "make a PPT" without mentioning quality requirements.
---

# Research Presentation Slides

This skill defines the **process and standards for making good work-showcasing slides**. It is tool-agnostic; tool-specific operations are delegated to the corresponding tool skill or documentation (e.g., the pptx skill, Beamer docs).

**One premise**: a talk is meant to be *heard*; slides are auxiliary. Slides are neither a script nor a compressed version of a paper. Every step below enforces this premise.

## Workflow

Proceed in order. Each step produces a file that serves as input for the next. Do not skip steps 1–3 and jump straight to building pages—this is the most common cause of bad slides.

| Step | Output | Template / Tool | Details |
|---|---|---|---|
| 1. Define objective | `talk-brief.md` | `assets/talk-brief-template.md` | `references/planning.md` |
| 2. Build storyline | `storyline.md` | `assets/storyline-template.md`, `scripts/lint_storyline.py` | `references/structure.md`, `references/talk-types.md` |
| 3. Write per-slide specs | `slide-specs.md` | `assets/slide-spec-template.md` | `references/slide-design.md`, `references/figures.md` |
| 4. Produce | Source files (.pptx / .tex / .md / …) | User-chosen tool | `references/visual-style.md` |
| 5. Export and check | `deck.pdf` + check report | `scripts/check_deck_pdf.py` | Step 5 below |
| 6. Review and contingency | Revised deck, backup slides, speaker notes | `references/review-checklist.md` | `references/delivery.md` |

### Step 1: Define Objective → `talk-brief.md`

Copy `assets/talk-brief-template.md` and fill in: purpose, audience, **one-sentence core message**, duration, venue constraints.

- If duration, audience, or venue is missing: **humans** fill it in themselves; **agents** ask the user first. If the user cannot be reached, write the assumptions explicitly into the brief and inform the user upon delivery.
- The core message must be a complete declarative sentence, not a topic. For example, "Method X" is a topic; "Method X cuts inference latency in half without sacrificing accuracy" is a core message.

### Step 2: Build Storyline → `storyline.md`

Copy `assets/storyline-template.md`. **Write each slide as a one-line conclusion title** and tag it with a role. Plan the order **working backward from the results**:

1. Group results by "which claim they support" into 2–4 groups, each yielding one major claim. Do not group by the order in which experiments were run.
2. Results that do not support these claims are deleted or moved to `[backup]`.
3. Describe the method only to the extent the audience needs to understand the results.
4. Finally, write the opening motivation: start from a problem everyone in the audience cares about and connect it to your specific objective.
5. End by returning to that big problem and restating the core message. The last main content slide must not be only "Thank you" or "Questions?".

Then run:

```bash
python scripts/lint_storyline.py storyline.md
```

Fix until there are no ERRORs. Finally, **read only the titles** from beginning to end: they should form a coherent story. If they do not, revise the storyline; do not proceed to the next step.

> Agent: show the user the core message and the list of titles first (or list them in the reply), and confirm the direction before generating pages.

### Step 3: Write Per-Slide Specs → `slide-specs.md`

For each slide in the storyline, write out per `assets/slide-spec-template.md`: title (conclusion sentence), visual center (which figure / diagram), minimal on-screen text, spoken words (speaker notes), source citation, estimated duration. Rules are in `references/slide-design.md` and `references/figures.md`.

### Step 4: Produce

Using the user's chosen tool, turn the specs into pages. Visual guidelines are in `references/visual-style.md`. Tool-specific operations refer to the corresponding tool skill or documentation.

### Step 5: Export PDF and Check

Almost every tool can export to PDF, so checks are unified on the PDF:

```bash
python scripts/check_deck_pdf.py deck.pdf --duration 15 --backup-start 18 --render pages/
```

- Dependencies: `pip install pdfplumber pypdfium2` (the latter is needed for `--render`).
- Script checks: page count vs. duration match, font size too small, word count per page, text-only pages, content overflowing the page, font variety, page numbers. See `--help` for parameter descriptions.
- `--render` exports each page as a PNG. **Inspect page by page** to catch problems the script cannot detect: overlap, truncation, blurry images, insufficient contrast, misalignment. Agents must perform this step: clean compilation does not guarantee correct layout.
- Fix all ERRORs. For each WARN, either fix it or be able to explain why it does not need fixing.

### Step 6: Review and Contingency

- Go through `references/review-checklist.md` item by item; items are numbered (e.g., `S3`, `F2`). Reference the numbers when writing review comments.
- Complete per `references/delivery.md`: backup slides, speaker notes, PDF fallback version, video screenshots, skip plan for when time runs out.
- Humans: time a full run-through, then return to steps 2–3 to revise pages that run over time or do not flow well.

## Non-Negotiable Rules

These rules hold in all situations. Other rules are in the references and may be adapted to the occasion.

1. One claim per page; content slide titles state conclusions, not topics.
2. Everything on screen will be discussed; do not put up what you will not mention.
3. Every page has a visual center; no long complete sentences.
4. Text must be large enough to read when projected; the same applies to text in figures.
5. Data, results, and citations may only come from materials provided by the user or from verifiable sources. If missing, leave an obvious placeholder (e.g., `【TBD: xx experiment number】`) and inform the user. Never fabricate.
6. Establish the core message and storyline before making pages.

## Adapting or Reviewing Existing Slides

1. Export or obtain the PDF, and run `scripts/check_deck_pdf.py`.
2. Reverse-engineer `storyline.md` from the existing pages (rewrite each page title as a conclusion sentence), and run `lint_storyline.py`.
3. Use `references/review-checklist.md` to output a numbered list of issues sorted by impact: structural problems > single-page problems > visual problems.
4. When revising, fix the storyline first, then the pages.

## Directory Structure

```
research-presentation-slides/
├── SKILL.md                    # This file: workflow + index
├── references/                 # Step-by-step details; read as needed
├── assets/                     # Templates for steps 1–3 (copy and fill in)
├── scripts/
│   ├── lint_storyline.py       # Check storyline.md
│   └── check_deck_pdf.py       # Check exported PDF; can render page-by-page PNGs
└── evals/evals.json            # Test cases for regression after skill changes
```

## References Index

Read when needed; no need to read everything at once:

- `references/planning.md`: how to set purpose, audience, and core message; common misguided objectives.
- `references/structure.md`: hourglass structure, working backward from results, newspaper-style argument, nested layering, opening and closing, where to place the literature review.
- `references/talk-types.md`: trade-offs and time budgets for different occasions (conference short talk, group meeting, defense, job talk, lightning talk, non-specialist audience).
- `references/slide-design.md`: single-page rules, with before/after examples.
- `references/figures.md`: how to adapt figures and tables from paper format to slide format.
- `references/visual-style.md`: font size, color, typeface, accessibility, consistency.
- `references/delivery.md`: speaker notes, practice, backup slides, technical failure contingency.
- `references/review-checklist.md`: numbered review checklist; also the final pre-delivery check.
- `references/sources.md`: sources this skill is based on.

## Extending This Skill

- **Add a new occasion** (e.g., grant pitch, product review): add a section in `references/talk-types.md`, following the existing format (purpose / time budget / must-have slides / common mistakes).
- **Add a new rule**: place it in the appropriate reference file, and simultaneously add a new numbered item in `references/review-checklist.md`. Do not change existing numbers, to avoid breaking past review records.
- **Add tool-specific notes** (e.g., Beamer theme recommendations): create `references/tools/<tool>.md`, and add a line in the index above. Keep this file tool-agnostic.
- **Add automated checks**: extend in `scripts/`. Prefer checking tool-agnostic artifacts such as PDF or `storyline.md`, and add corresponding test cases in `evals/evals.json`.
