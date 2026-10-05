# Review Checklist

Review checklist for Step 6 and the final check before delivery.

- When writing review comments, cite item IDs, e.g., "Page 7 violates S2, F3."
- **Do not modify or reuse existing IDs.** Add new items under the corresponding prefix with the next available number; mark deprecated items as "(deprecated)"—do not delete them.
- The "Auto" column indicates which checks can be performed by scripts: `L` = `lint_storyline.py`, `P` = `check_deck_pdf.py`, blank means it requires human or agent visual inspection.
- Severity: **High** = must fix; **Medium** = should fix; **Low** = recommended to fix.

## M — Objective (Message)

| ID | Check Item | Severity | Auto |
|---|---|---|---|
| M1 | Core message is a complete declarative sentence | High | L |
| M2 | Core message appears in the opening (preview) and closing (restatement) | High | |
| M3 | 2–4 key points, each supported by results, and all support the core message | High | |
| M4 | Content depth matches audience background | Medium | |

## T — Structure

| ID | Check Item | Severity | Auto |
|---|---|---|---|
| T1 | Reading titles alone forms a coherent story from start to finish | High | |
| T2 | Results are grouped by point, not by experimental order | Medium | |
| T3 | Results preview appears within the first 25% of slides | Medium | L |
| T4 | Opening dives straight into the problem; no field history or long literature review | Medium | |
| T5 | Comparison with the 2–3 most relevant works is placed in the discussion | Low | |
| T6 | The last main slide is a conclusion, not "Thank you / Questions" | High | L |
| T7 | Slide count matches duration | High | L P |
| T8 | There is a plan for skippable slides | Low | |
| T9 | Backup slides exist | Medium | L |

## S — Single Slide

| ID | Check Item | Severity | Auto |
|---|---|---|---|
| S1 | One point per slide | High | |
| S2 | Content slide titles are conclusion sentences, not topics | High | L |
| S3 | Every item on screen is discussed | Medium | |
| S5 | Visual elements roughly ≤ 6 | Medium | |
| S6 | No long complete sentences; few words per slide | High | P |
| S7 | Has a visual center; not a text-only slide | Medium | P |
| S8 | Passes the distraction test | Medium | |
| S9 | No unnecessary derivations on the main slide | Medium | |
| S10 | Citations annotated on the same slide, consistent format; attribution clear | Medium | |
| S11 | No decorative animations | Low | |

(S4 "Say more than what is on screen" belongs to the delivery phase; see D1.)

## F — Figures

| ID | Check Item | Severity | Auto |
|---|---|---|---|
| F1 | One figure, one message; the message is in the title | High | |
| F2 | Multi-panel figures have been split | Medium | |
| F3 | Text in figures is readable when projected | High | |
| F4 | Few series, highlight emphasized | Medium | |
| F5 | Annotated directly rather than relying on a legend | Low | |
| F6 | Axes have labels and units | High | |
| F7 | Tables keep only the numbers to be discussed | Medium | |
| F10 | Colorblind-friendly | Medium | |

## V — Visual (Visual Style)

| ID | Check Item | Severity | Auto |
|---|---|---|---|
| V1 | Body text large enough (approx. 24 pt equivalent or above), no text smaller than approx. 12 pt | High | P |
| V2 | Sufficient contrast, simple background | High | |
| V3 | Fonts ≤ 2–3 kinds; no emphasis via italics, underline, or all caps | Low | P |
| V4 | Restrained palette, color meanings consistent throughout | Medium | |
| V5 | Alignment consistent, no overlapping or off-page elements | High | P |
| V7 | Terminology and symbols consistent throughout; page numbers present | Medium | P |

## D — Delivery

| ID | Check Item | Severity | Auto |
|---|---|---|---|
| D1 | Every slide has speaker notes and a transition sentence | Medium | |
| D2 | Full timed rehearsal completed (human) / Per-slide render check completed (agent) | High | |
| D3 | Backup slides cover anticipated questions | Medium | |
| D4 | PDF fallback available; videos have screenshots; online content has offline version | Medium | |

## X — Accuracy

| ID | Check Item | Severity | Auto |
|---|---|---|---|
| X1 | All numbers, results, and citations are traceable to user materials or verifiable sources | High | |
| X2 | Missing information is marked with obvious placeholders and the user has been informed | High | |

## Review Output Format

```
## Review Result: <Presentation Name>
Scripts: check_deck_pdf.py → N ERROR / M WARN; lint_storyline.py → ...

### High
- [T6] Page 22: Last main slide only says "Thank you" → Change to a conclusion slide that restates the core message
- [S2] Pages 5, 9, 14: Title "Results" → Change to...
### Medium
- …
### Low
- …
```
