# research-presentation-slides

A skill to help AI agents (and humans) make good presentation slides for "showing your own work": research reports, conference talks, group meetings, defenses, job talks, and project/technical sharing.

It defines the **process and standards**, independent of production tools: PowerPoint, Keynote, Google Slides, Beamer, Marp, Slidev, reveal.js, and python-pptx can all be used together with it.

## What It Does

The skill breaks slide-making into six steps; each step produces a file that serves as input for the next:

| Step | Output |
|---|---|
| 1. Define objective | `talk-brief.md`: purpose, audience, one-sentence core message, duration, venue |
| 2. Build storyline | `storyline.md`: one conclusion-title per page, checked with `scripts/lint_storyline.py` |
| 3. Write per-slide specs | `slide-specs.md`: visual center, on-screen text, speaker notes, sources |
| 4. Produce | Source files in the user's chosen tool |
| 5. Export and check | `deck.pdf` + check report and page-by-page PNGs from `scripts/check_deck_pdf.py` |
| 6. Review and contingency | Revise per numbered checklist, add backup slides and notes |

In addition, it can review and adapt existing slides: reverse-engineer the storyline from a PDF, and output a numbered list of issues sorted by severity.

The full workflow and non-negotiable rules are in [`SKILL.md`](SKILL.md).

## Installation

We recommend installing via the [`skills`](https://github.com/vercel-labs/skills) CLI. **Run this in the root of the repo where you need to make slides**:

```bash
npx skills add a-green-hand-jack/research-presentation-slides
```

To install for only one agent (e.g., Claude Code), add `--agent`:

```bash
npx skills add a-green-hand-jack/research-presentation-slides --agent claude-code
```

If you want to preview what skills are in the repo before installing, add `--list`; this lists them without installing.

### Recommendation: install only in repos that need it; do not install globally

`skills` installs to the current project by default (project-level), which is what we recommend. **Please do not add `-g` / `--global`** unless you truly need to make slides in almost every project. Reasons:

- **Avoid false triggers**: this skill's description is intentionally broad; it triggers on any mention of slides, PPT, deck, or talk. After global installation, it appears in every project's agent context and may be invoked even in repos unrelated to presentations.
- **Save context**: every installed skill's name and description enters the agent's context. Install only where needed so other projects do not pay this overhead.
- **Version control**: project-level installation generates `skills-lock.json`, recording the source and content hash. Different projects can stay on appropriate versions and upgrade independently.
- **Collaboration**: skill files and the lock file live in the repo; collaborators pull the same skill.

A good practice: install in the paper repo, the report materials repo, or a dedicated slides repo; remove it after the talk if it is no longer needed.

### What Gets Added After Installation

With `--agent claude-code`, the project gains:

```
.claude/skills/research-presentation-slides/   # skill contents
skills-lock.json                               # source and content hash
```

We recommend committing both to the repo so collaborators can use the skill directly. Other agents use different installation directories; follow the CLI output.

### Update and Remove

```bash
npx skills list                                   # list skills installed in current project
npx skills update -p                              # update skills for current project only
npx skills remove research-presentation-slides    # remove from current project
```

> Skills run with the agent's full permissions. Please browse `SKILL.md` and the contents of `scripts/` before installing.

## Usage

No special command is needed after installation; simply ask the agent to do the work, for example:

- "Here is my paper PDF. Help me make a 15-minute conference talk slides using Beamer."
- "Please review this group-meeting PPT (attached deck.pdf); I have 20 minutes next week."
- "We built an open-source tool and want a 5-minute lightning talk using Marp."

The agent will first produce a talk brief and a storyline, confirm the direction with you, and then generate the pages.

The two check scripts can also be run manually:

```bash
# Check storyline
python scripts/lint_storyline.py storyline.md

# Check exported PDF and render each page as PNG
pip install pdfplumber pypdfium2
python scripts/check_deck_pdf.py deck.pdf --duration 15 --backup-start 18 --render pages/
```

After installing into a project, prefix the script paths with the skill directory, e.g., `.claude/skills/research-presentation-slides/scripts/lint_storyline.py`.

## Repo Structure

```
research-presentation-slides/
├── SKILL.md                    # Workflow + index (agent entry point)
├── references/                 # Step-by-step details; read as needed
├── assets/                     # Templates for steps 1–3
├── scripts/
│   ├── lint_storyline.py       # Check storyline.md
│   └── check_deck_pdf.py       # Check exported PDF; can render page-by-page PNGs
└── evals/evals.json            # Test cases for regression after skill changes
```

## Contributing

Conventions for adding new occasions, rules, tool notes, or automated checks are in the "Extending This Skill" section of [`SKILL.md`](SKILL.md). Sources underlying the rules are listed in [`references/sources.md`](references/sources.md).

## License

[MIT](LICENSE)
