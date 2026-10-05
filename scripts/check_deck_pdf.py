#!/usr/bin/env python3
"""Check exported slide PDFs (any tool: PowerPoint, Keynote, Beamer, Marp, etc.).

Checks (numbers correspond to references/review-checklist.md):
  T7  Slide count matches duration (consecutive identical titles count as one slide,
      so Beamer overlays / stepwise reveals are not double-counted)
  V1  Font size, normalized to a 7.5-inch (540 pt) tall slide; tiny text anywhere,
      small text in body areas
  S6  Words per slide
  S7  Text-only pages (no images and almost no vector graphics)
  V5  Content overflowing page boundaries
  V3  Number of distinct font families
  V7  Page numbers present
  S2  Content pages using topic-style titles (e.g. "Results", "Method")
  T6  Slides end with a "Thank you / Questions" page

Requires: pdfplumber (pip install pdfplumber). --render also needs pypdfium2.

Usage:
  python check_deck_pdf.py deck.pdf --duration 15 [--backup-start 18]
                           [--render pages/] [--json]
Exit code: 1 if any ERROR, otherwise 0.
"""
import argparse
import json
import os
import re
import sys
from collections import Counter

try:
    import pdfplumber
except ImportError:
    sys.exit("Requires pdfplumber: pip install pdfplumber")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lint_storyline import is_topic_title, CLOSING_RE  # noqa: E402

REF_HEIGHT = 540.0          # 7.5-inch slide height in pt
TINY_PT = 12.0              # Text smaller than this is unreadable when projected
BODY_MIN_PT = 18.0          # Body text smaller than this triggers a warning
FOOTER_FRAC = 0.10          # Top/bottom 10% are header/footer zones
MAX_WORDS = 50              # Per-slide word limit (CJK chars count as 0.5 words); warn if exceeded
HARD_MAX_WORDS = 90         # Hard per-slide word limit
CJK_RE = re.compile(r"[\u3400-\u9fff\uf900-\ufaff\u3040-\u30ff\uac00-\ud7af]")


def word_count(text):
    cjk = len(CJK_RE.findall(text))
    latin = len(re.findall(r"[A-Za-z0-9]+", CJK_RE.sub(" ", text)))
    return latin + cjk / 2.0


def font_family(name):
    name = name.split("+")[-1]                 # Strip subset prefix ABCDEF+
    name = re.split(r"[-,]", name)[0]
    return re.sub(r"(Bold|Italic|Oblique|Regular|Medium|Light|Semibold|MT|PS)+$", "", name) or name


def page_title(page, scale):
    """Largest text line in the top 30% of the page."""
    h = page.height
    try:
        words = page.extract_words(extra_attrs=["size"], keep_blank_chars=False)
    except TypeError:
        words = page.extract_words()
    words = [w for w in words if w["top"] < h * 0.30 and w["text"].strip()]
    if not words:
        return ""
    biggest = max(w.get("size", 0) for w in words)
    line = [w for w in words if w.get("size", 0) >= biggest * 0.9]
    line.sort(key=lambda w: (round(w["top"] / 4), w["x0"]))
    out = ""
    for w in line:
        t = w["text"]
        if out and not (CJK_RE.search(out[-1]) or CJK_RE.search(t[0])):
            out += " "
        out += t
    return out.strip()


def analyze(path, duration, backup_start):
    issues = []
    pages_info = []

    def add(level, code, msg, page=None):
        issues.append({"level": level, "check": code, "page": page, "msg": msg})

    with pdfplumber.open(path) as pdf:
        n = len(pdf.pages)
        fonts = Counter()
        for i, page in enumerate(pdf.pages, start=1):
            w, h = page.width, page.height
            scale = REF_HEIGHT / h
            chars = [c for c in page.chars if c["text"].strip()]
            text = page.extract_text() or ""
            info = {"page": i, "title": page_title(page, scale), "words": word_count(text)}
            pages_info.append(info)
            is_backup = backup_start is not None and i >= backup_start

            for c in chars:
                fonts[font_family(c.get("fontname", "?"))] += 1

            # V5 overflow detection
            out = [c for c in chars if c["x1"] > w + 1 or c["x0"] < -1 or c["bottom"] > h + 1 or c["top"] < -1]
            if out:
                add("ERROR", "V5", f"{len(out)} characters overflow page boundary: {''.join(c['text'] for c in out[:20])}", i)

            # V1 font size check
            if chars:
                sizes = [c["size"] * scale for c in chars]
                tiny = [c for c, s in zip(chars, sizes) if s < TINY_PT - 0.5]
                body = [c for c, s in zip(chars, sizes)
                        if s < BODY_MIN_PT - 0.5 and h * FOOTER_FRAC < c["top"] < h * (1 - FOOTER_FRAC)]
                info["min_pt"] = round(min(sizes), 1)
                if tiny and len(tiny) > 3:
                    sample = "".join(c["text"] for c in tiny[:25])
                    add("WARN" if is_backup else "ERROR", "V1",
                        f"{len(tiny)} characters smaller than {TINY_PT:g}pt equivalent (min {min(sizes):.1f}pt), unreadable when projected: {sample}", i)
                frac = len(body) / len(chars)
                if frac > 0.25 and not is_backup:
                    add("WARN", "V1", f"{frac:.0%} of body-area text is smaller than {BODY_MIN_PT:g}pt equivalent (text inside figures also counts)", i)

            # S2 topic-style title (heuristic: largest text in top 30%)
            if (not is_backup and i > 1 and info["title"] and is_topic_title(info["title"])
                    and not CLOSING_RE.match(info["title"])):
                add("WARN", "S2", f"Title \"{info['title']}\" looks like a topic; content pages should use conclusion sentences (section dividers may be ignored)", i)

            # S6 word count
            if not is_backup:
                if info["words"] > HARD_MAX_WORDS:
                    add("ERROR", "S6", f"~{info['words']:.0f} words, wall of text -> split page or move text to speaker notes", i)
                elif info["words"] > MAX_WORDS:
                    add("WARN", "S6", f"~{info['words']:.0f} words, on the high side", i)

            # S7 text-only page
            graphics = len(page.images) + len(page.curves) + len([r for r in page.rects
                         if (r["x1"] - r["x0"]) < w * 0.95 or (r["bottom"] - r["top"]) < h * 0.95])
            info["graphics"] = graphics
            if not is_backup and i > 1 and graphics < 3 and info["words"] > 15:
                add("WARN", "S7", "Suspected text-only page: no images or graphics -> consider adding a visual center", i)

        # V7 page numbers
        numbered = 0
        for i, page in enumerate(pdf.pages, start=1):
            h = page.height
            zone = [c for c in page.chars if c["top"] > h * 0.85 or c["bottom"] < h * 0.12]
            txt = "".join(c["text"] for c in sorted(zone, key=lambda c: (round(c["top"]), c["x0"])))
            if re.search(rf"(?<!\d){i}(?!\d)", txt):
                numbered += 1
        if n >= 5 and numbered < n * 0.5:
            add("WARN", "V7", f"Only {numbered}/{n} pages detected with page numbers; add page numbers for easier Q&A referencing")

    # V3 font families
    fam = [f for f, k in fonts.items() if k > 20]
    if len(fam) > 4:
        add("WARN", "V3", f"Used {len(fam)} font families ({', '.join(fam[:8])}), recommend <= 3")

    # T7 page count, merging stepwise reveals (consecutive identical titles)
    main = [p for p in pages_info if backup_start is None or p["page"] < backup_start]
    logical = 0
    prev = None
    for p in main:
        if not p["title"] or p["title"] != prev:
            logical += 1
        prev = p["title"]
    if main and main[-1]["title"] and CLOSING_RE.match(main[-1]["title"]):
        add("WARN", "T6", f"Last main page is \"{main[-1]['title']}\"; screen will stop here during Q&A -> end with a conclusion page",
            main[-1]["page"])
    summary = {"pages": len(pages_info), "main_pages": len(main), "logical_slides": logical,
               "backup_pages": len(pages_info) - len(main)}
    if duration:
        lo, hi = duration / 3.0, duration * 1.2
        if logical > hi:
            add("ERROR" if logical > duration * 1.6 else "WARN", "T7",
                f"{logical} logical slides (stepwise reveals merged) for {duration:g} min is high; empirical range ~{lo:.0f}-{hi:.0f}")
        elif logical < lo:
            add("WARN", "T7", f"{logical} logical slides for {duration:g} min is low; confirm each page isn't overloaded")
    if backup_start is None:
        add("INFO", "T9", "--backup-start not specified; if there are backup pages, please specify, otherwise they will be counted in duration and word checks")
    return issues, pages_info, summary


def render(path, outdir, scale=1.0):
    try:
        import pypdfium2 as pdfium
    except ImportError:
        print("Skipping render: requires pypdfium2 (pip install pypdfium2)", file=sys.stderr)
        return []
    os.makedirs(outdir, exist_ok=True)
    doc = pdfium.PdfDocument(path)
    out = []
    for i in range(len(doc)):
        page = doc[i]
        s = scale * 1280.0 / page.get_width()
        img = page.render(scale=s).to_pil()
        fp = os.path.join(outdir, f"page-{i + 1:03d}.png")
        img.save(fp)
        out.append(fp)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--duration", type=float, help="Duration in minutes (excluding Q&A)")
    ap.add_argument("--backup-start", type=int, help="Page number of the first backup page (pages after this are excluded from duration checks and relaxed)")
    ap.add_argument("--render", metavar="DIR", help="Render each page as PNG for visual page-by-page inspection")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    issues, pages, summary = analyze(a.pdf, a.duration, a.backup_start)
    rendered = render(a.pdf, a.render) if a.render else []
    n_err = sum(i["level"] == "ERROR" for i in issues)

    if a.json:
        print(json.dumps({"summary": summary, "issues": issues, "pages": pages,
                          "rendered": rendered}, ensure_ascii=False, indent=2))
    else:
        print(f"{a.pdf}: {summary['pages']} pages ({summary['main_pages']} main, "
              f"{summary['logical_slides']} logical after merging stepwise reveals; {summary['backup_pages']} backup)\n")
        order = {"ERROR": 0, "WARN": 1, "INFO": 2}
        for i in sorted(issues, key=lambda x: (order[x["level"]], x["page"] or 0)):
            where = f"page {i['page']} " if i["page"] else ""
            print(f"{i['level']:5} [{i['check']}] {where}{i['msg']}")
        print(f"\n{n_err} errors, {sum(i['level'] == 'WARN' for i in issues)} warnings")
        if rendered:
            print(f"\nRendered {len(rendered)} pages to {a.render}/ -- inspect page-by-page for overlap, clipping, blur, contrast, and alignment.")
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
