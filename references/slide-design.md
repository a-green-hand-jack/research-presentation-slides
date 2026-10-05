# Slide Design: Single-Page Rules

Details for Step 3. Corresponds to the `S*` items in the review checklist.

## Rules

### S1 One Point Per Slide
Each slide has only one core goal. Break complex content into multiple slides and explain it step by step. For complex flowcharts or architecture diagrams, build them across several slides: add one block per slide, and only show the full picture on the last slide. By the time the audience sees the full picture, they already understand each component.

### S2 Titles State Conclusions
Titles on content slides should be a conclusion; everything else on the slide serves that sentence. Only section divider slides may use topic-style titles.

| Topic-style (bad) | Conclusion-style (good) |
|---|---|
| Results | Removing pre-training drops accuracy by 12 points |
| Experiment 2 | False-positive rate depends heavily on samples |
| Method | Two-stage retrieval reduces latency to 40 ms |
| Related Work | Existing methods all assume stationary data |
| Background | Phosphorylation sites far outnumber what we can measure |

### S3 Only Include What You Will Discuss
When you speak, the audience's eyes wander across the screen. Every detail on the screen must be something you plan to discuss; if you won't discuss it, don't include it. Experienced listeners will question any detail that appears on screen, so only include what you want them to focus on.

### S4 Say More Than What's on the Screen
First say what is on the screen, then explain it, rephrase it, and extend it. Do not read the text on the screen verbatim.

### S5 Limit the Number of Elements
A slide's visual elements (title, each figure, each text block, icon, logo) should generally not exceed 6. Beyond that, the effort required to understand the slide rises sharply. Note that decorative elements built into the template also count.

### S6 Text Is a Signpost, Not a Script
- Reading and listening use the same cognitive channel. The audience can either read or listen; doing both at once leads to poor performance in both.
- Use phrases, not complete long sentences. Each bullet should ideally fit on one line; limit the number per slide.
- Short text that carries the same meaning as the spoken content (redundant phrases) aids memory and can be kept.

### S7 Visual-Centric
Avoid purely text-based slides. Build each slide around one visual element: a data plot, a diagram, a photo, a screenshot, an enlarged key number, or a before/after comparison. When no ready-made figure exists, draw a simple diagram yourself or enlarge the key number rather than writing another paragraph.

### S8 Glance Test
Ask of every slide: can someone who hasn't been listening look up and get the point? At the same time, check the abstraction level: are there so many details that they drown out the conclusion?

### S9 Demote Formulas
If a conclusion can be stated in one sentence, do not put the derivation on the main slide.
- Bad: a full fractional expression
- Good: "The rate of technological progress decreases with the labor share," with the derivation on a backup slide

When a formula must be shown, include only one, and use color or annotation to explain the meaning of each term.

### S10 Cite Sources on the Spot
When using someone else's figure, data, or method, cite the source on that slide. Use a consistent format and position throughout (e.g., small text in the lower-right corner). Add it when creating the slide—"I'll fill it in later" always gets forgotten. Attribution must also clearly state who did which part.

### S11 Progressive Reveal, Not Decorative Animation
When you need to control the order of information, use progressive reveal (duplicate the slide and show elements step by step, or use the tool's built-in build/overlay features). Do not use decorative animations such as fly-ins, spins, or flashes.

## Revision Examples

### Example 1: Wall of Text → One Figure, One Point

**Before**
> Title: Background
> - Protein-protein interactions are mediated by multiple domains, among which SH2 domains recognize phosphorylated tyrosine
> - The human proteome contains a large number of phosphorylation sites, and current experimental techniques can only measure a small fraction
> - Therefore, a large number of potential interactions remain uncharacterized, limiting our understanding of signaling networks
> - This study proposes a computational method…

Problem: topic-style title; four complete sentences; no visual anchor; two points crammed into one slide (mechanism + scale).

**After revision (split into 2 slides)**
> Slide 1 Title: SH2 domains mediate interactions by recognizing phosphorylated tyrosine
> Visual: a specific binding diagram (a particular SH2 domain and a phosphorylation site)
> Text: none, or one label
>
> Slide 2 Title: Possible interactions far outnumber what we can measure
> Visual: generalize the same diagram to a "many-to-many" view, marking the ratio of measured vs. unmeasured
> Text: one redundant phrase, e.g., "Most remain unknown"

### Example 2: Paper Results Table → Conclusion + Simplified Figure

**Before**: title "Results," an 8-column × 12-row comparison table, 10 pt font.
**After**: title "Our method matches or outperforms on all 4 benchmarks"; bar chart keeping only our method and the top 2 baselines; our method in the accent color, the rest in gray; full table on a backup slide with a link from this slide.

### Example 3: Long Sentences Compressed into Signposts

| Original sentence | On-screen text |
|---|---|
| The purpose of this talk is to introduce the positive and negative effects of social media on adolescent mental health | How social media affects adolescent mental health |
| The new marketing strategy will focus on expanding social media influence to reach younger audiences through social platforms | Use social media to reach young users |
| Photosynthesis is the process by which plants convert sunlight into energy, and it is essential for plant growth | Plants grow through photosynthesis |

## Common Agent Failure Modes

| Failure mode | Countermeasure |
|---|---|
| Compressing each paper section into bullet points | Write the brief and storyline first; organize by point, not by section |
| Titles use Introduction / Method / Results | All content slides must use conclusion sentences (S2); only `[section]` slides may use topic-style titles |
| 5–8 bullet points per slide | Count elements (S5); replace with one visual anchor (S7) |
| Pasting multi-panel figures directly from the paper | Split panels, enlarge fonts, highlight key points; see `figures.md` |
| Fabricating numbers or citations to fill gaps | Leave a `[TODO: …]` placeholder and tell the user |
| Delivering without checking the rendered output | Step 5: review every slide after `--render` |
