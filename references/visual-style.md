# Visual Style: Readability, Accessibility, Consistency

Details for Step 4. Corresponds to the `V*` items in the review checklist. This section covers only tool-agnostic standards, not tool-specific setup instructions.

## V1 Font Size

- Body text no smaller than approximately 24 pt (based on a 16:9 page 7.5 inches tall; other sizes scale proportionally, and `check_deck_pdf.py` will convert automatically).
- Citations and footers can be smaller, but not below approximately 12 pt.
- Quick check: print the slides and place them on the floor—can you read them while standing? Text that looks "just right" on a laptop screen is often too small when projected to the back row.

## V2 Contrast and Background

- High contrast: dark text on a light background, or vice versa. Light-gray text on a white background or dark charts on a dark background are common accidents.
- Keep the background simple; do not use photos or gradients as the background for body text.
- Contrast problems are worse for online talks and on small screens.

## V3 Typeface

- Prefer sans-serif fonts for projection; use no more than 2 typefaces throughout (one for headings, one for body text; code may use an additional monospace font).
- Use bold or color for emphasis; avoid italics, underlining, and ALL CAPS—these three are unfriendly to readers with dyslexia and to distant viewing.
- Use common fonts or embed fonts in the file to avoid layout breakage when opening on another computer.

## V4 Color

- One neutral color (text) + one accent color, plus one or two auxiliary colors, is enough.
- When colors carry meaning, keep them consistent throughout.
- Use color-blind-friendly palettes; do not rely on color alone to convey information. Check with a color-blindness simulator.

## V5 White Space and Alignment

- White space is part of the design. When things do not fit, it means there is too much content, not that the margins are too large.
- Align elements to a uniform grid or margin; keep the same kind of element (title, figure, citation) in the same position on every slide.

## V6 Template

- Choose the plainest template, or remove decorative bars, large logos, and fancy footers from the template. They all consume the audience's attention.
- Keep the useful parts: page numbers, a short talk title or section name.

## V7 Consistency

- **Terminology**: use one and only one name for a concept from start to finish. If you call it agent at first, then actor, then policy, the audience will think they are three different things.
- **Notation**: follow field conventions and keep them consistent throughout.
- **Style**: title position, font size, color meaning, citation format, and figure style should be consistent throughout.
- **Page numbers**: add them, so that during Q&A an audience member can say "the figure on slide 12."

## V8 Accessibility Add-ons

- Animations increase the processing burden for people with visual impairments: avoid them when possible.
- For online talks, practice with automatic captions to check speaking rate, volume, and pronunciation.
- When an image contains key information, describe it orally.
