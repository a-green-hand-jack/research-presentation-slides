# Structure: Building the Storyline

Details for Step 2.

## Table of Contents
1. Hourglass Structure
2. Planning Backward from Results
3. General Skeleton
4. Newspaper-Style Argument
5. Nested Layers (Adapting to Different Durations)
6. Opening
7. Where to Put the Literature Review
8. Ending
9. Navigation and Transitions
10. Duration and Slide Count

## 1. Hourglass Structure

When presenting: start from the big question everyone cares about (wide) → narrow down to your specific question, method, and results (narrow) → expand again to significance and impact, returning to the big question (wide).

## 2. Planning Backward from Results

The planning order differs from the presentation order. Plan starting from the narrowest point of the hourglass:

1. **Interpret results**: What point does each result support?
2. **Group**: Group by "which point it supports," not by experimental order. Form 2–4 groups, each with one main point.
3. **Filter**: Results that do not support these points: delete them or move them to backup slides.
4. **Check the argument**: Do the results really support the points? Do the points really support the core message? Fix any gaps, or revise the core message.
5. **Methods**: Cover only enough for the audience to understand the results.
6. **Motivation**: Start from what the whole audience cares about, and step by step connect to your specific goal.
7. **Impact**: What did your work directly achieve? What is the next step? How does it connect back to that big question?

## 3. General Skeleton

Pick and choose as needed; do not copy blindly:

| Section | Questions it answers | Tags |
|---|---|---|
| Opening | What is the problem? Why is it worth caring about? | Intro, motivation, problem |
| Contribution preview | What is new? What was discovered? (One sentence, no elaboration) | Contribution |
| Evidence (optional) | State the fact first, then show the figure | Results |
| Methods / model | How it was done (just enough to understand the results) | Methods |
| Results | One conclusion per slide | Results |
| Discussion | What is new compared to the 2–3 most related works; limitations; significance | Discussion |
| Conclusion | What to take away; return to the big question | Takeaways, future work |
| Backup | Answers to anticipated questions, full tables, detailed references, robustness checks | Backup |

When previewing results, state only the conclusion, not details or intuitions: the audience hasn't seen the methods yet, so they won't understand.

Get to the point early. There is a saying in economics talks: get to your model within ten minutes.

## 4. Newspaper-Style Argument

State the conclusion first, then the main steps, and finally the details. Do not save the answer for the end like a mystery novel. The benefits are:
- The audience always knows where you are going.
- When time runs short, you can cut details from the end backward without affecting the main thread.

Apply this order to every section and every slide: give the point first, then the evidence.

## 5. Nested Layers

Assign a level to every piece of content:
- **Outer layer** (must present): core message, main points, key evidence.
- **Middle layer**: full methods, secondary results.
- **Inner layer**: details, extensions, robustness checks.

Short talks present only the outer layer; medium-length talks add the middle layer; long talks cover all. The same work can therefore adapt to different durations. If you run out of time on stage, skip the inner layer; if you get lost, fall back to the previous layer's main thread.

In `storyline.md`, you can mark skippable slides with the comment: `<!-- skippable -->`.

## 6. Opening

- State the problem or point directly. Do not begin with the history of the field or a long list of references.
- Write down or memorize the first one or two sentences of the opening to ensure a smooth start.
- Start from what the audience cares about: for experts, this can be a specific problem; for non-specialists, start from a broader goal.

## 7. Where to Put the Literature Review

Do not pile up a literature review at the beginning. The audience does not yet know your work and cannot see how you differ from others; most are also unfamiliar with the literature details.
- In the discussion section, compare with the **2–3 most relevant works**: say what is new and better about your work, not what is bad about others.
- Put the detailed review on backup slides, and bring it out only when an expert asks.

## 8. Ending

- Reiterate the core message and connect back to the big question from the opening.
- Discuss the direct impact and next steps.
- The main content of the last slide should be the conclusion. During Q&A, this is usually the slide that stays on screen the longest, so it should show what you most want people to remember, not just "Thank you" or "Questions?". Acknowledgments can be on a separate slide, or attribution can be placed in the corner of the conclusion slide.

## 9. Navigation and Transitions

- At the start and end of each section, give a brief review and preview: where we came from, why we are here, and where we are going next.
- Periodically "reclaim" audience members who may have gotten lost: summarize what has been established so far.
- The end of every slide should naturally lead to the next. If you cannot write a transition sentence, the order is wrong.
- Short talks do not need a separate outline slide; long talks can have one, and repeat it on section divider slides with the current position marked.

## 10. Duration and Slide Count

- Plan by **time**, not by slide count. Rule of thumb: about 1 minute per slide; information-dense long academic talks may take 2–3 minutes per slide.
- Progressive-reveal slides increase the slide count; this is fine.
- If a slide takes a long time to explain, it contains too much: split it up or delete it.
- Backup slides do not count toward the duration.
- Do not run overtime. Finishing early is never a problem.
