# Slide Spec

<!-- Step 3 output. Each page in storyline.md corresponds to one block. Follow these specs when building; do not improvise content. -->

## Page <N> — [<Tag>]

- **Title (conclusion sentence)**:
- **Single message this page must convey**: <!-- usually same as the title; if you can't write it, this page needs to be split -->
- **Visual center**: <!-- which figure / diagram / key number enlargement / comparison; source file path -->
  - Does the original figure need editing: <!-- split panels, enlarge fonts, highlight a line, remove extra series -->
- **On-screen text** (≤ 3 phrases, one per line):
  -
- **Element count** (title + figure + text blocks + icons…, target ≤ 6):
- **Build** (reveal all at once / reveal in k steps (content of each step)):
- **Speaker notes** (what to say, 2–5 sentences; first describe what's on screen, then explain, then extend):
- **Transition** (how to lead to the next page):
- **Source / citation**:
- **Estimated duration**:
- **Distraction test**: <!-- what can someone who zoned out grasp at a glance? -->

---

<!-- Example -->

## Page 7 — [result]

- **Title (conclusion sentence)**: Latency grows linearly with length; 2.1× faster at 64k
- **Single message this page must convey**: Our method's latency advantage increases with context length
- **Visual center**: Line chart, x = context length, y = latency; two lines (full-attention gray, our method orange); label "2.1×" at 64k
  - Does the original figure need editing: Paper Fig.4 has 5 baselines → keep only full attention; enlarge axis labels to projection-readable; remove legend, label directly at curve ends
- **On-screen text**:
  - 64k: 2.1× faster
- **Element count**: title, figure, one annotation = 3
- **Build**: show gray line first ("this is full attention"), then add orange line
- **Speaker notes**: The horizontal axis is context length, vertical axis is per-request latency. The gray line is full attention, roughly quadratic growth. The orange line is our method, basically linear. At 64k the gap reaches 2.1×, and the longer the sequence, the larger the gap.
- **Transition**: Where does this speedup come from? Let's break it down on the next page.
- **Source / citation**: This work; experimental setup see backup page 12
- **Estimated duration**: 2 minutes
- **Distraction test**: see an orange line clearly below a gray line, plus "2.1× faster"
