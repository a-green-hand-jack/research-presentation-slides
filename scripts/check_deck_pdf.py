#!/usr/bin/env python3
"""Check an exported slide deck PDF (any tool: PowerPoint, Keynote, Beamer, Marp, ...).

Checks (ids refer to references/review-checklist.md):
  T7  slide count vs duration (consecutive pages with the same title count as one
      slide, so Beamer overlays / step-by-step builds are not double counted)
  V1  font size, normalized to a 7.5in(540pt)-tall slide; tiny text anywhere,
      small text in the body area
  S6  word count per page
  S7  text-only pages (no images and almost no vector graphics)
  V5  content outside the page box
  V3  number of distinct font families
  V7  page numbers present
  S2  topic-style titles ('Results', 'Method') on content pages
  T6  deck ends on a 'Thank you / Questions' page

Needs: pdfplumber (pip install pdfplumber). --render also needs pypdfium2.

Usage:
  python check_deck_pdf.py deck.pdf --duration 15 [--backup-start 18]
                           [--render pages/] [--json]
Exit code: 1 if any ERROR, else 0.
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
    sys.exit("需要 pdfplumber：pip install pdfplumber")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lint_storyline import is_topic_title, CLOSING_RE  # noqa: E402

REF_HEIGHT = 540.0          # 7.5in slide height in pt
TINY_PT = 12.0              # anything smaller is unreadable when projected
BODY_MIN_PT = 18.0          # body text smaller than this is a warning
FOOTER_FRAC = 0.10          # bottom/top 10% is footer/header zone
MAX_WORDS = 50              # words (CJK char = 0.5 word) per page before warning
HARD_MAX_WORDS = 90
CJK_RE = re.compile(r"[\u3400-\u9fff\uf900-\ufaff\u3040-\u30ff\uac00-\ud7af]")


def word_count(text):
    cjk = len(CJK_RE.findall(text))
    latin = len(re.findall(r"[A-Za-z0-9]+", CJK_RE.sub(" ", text)))
    return latin + cjk / 2.0


def font_family(name):
    name = name.split("+")[-1]                 # drop subset prefix ABCDEF+
    name = re.split(r"[-,]", name)[0]
    return re.sub(r"(Bold|Italic|Oblique|Regular|Medium|Light|Semibold|MT|PS)+$", "", name) or name


def page_title(page, scale):
    """Text of the largest-font line in the top 30% of the page."""
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

            # V5 overflow
            out = [c for c in chars if c["x1"] > w + 1 or c["x0"] < -1 or c["bottom"] > h + 1 or c["top"] < -1]
            if out:
                add("ERROR", "V5", f"{len(out)} 个字符超出页面边界：「{''.join(c['text'] for c in out[:20])}」", i)

            # V1 font size
            if chars:
                sizes = [c["size"] * scale for c in chars]
                tiny = [c for c, s in zip(chars, sizes) if s < TINY_PT - 0.5]
                body = [c for c, s in zip(chars, sizes)
                        if s < BODY_MIN_PT - 0.5 and h * FOOTER_FRAC < c["top"] < h * (1 - FOOTER_FRAC)]
                info["min_pt"] = round(min(sizes), 1)
                if tiny and len(tiny) > 3:
                    sample = "".join(c["text"] for c in tiny[:25])
                    add("WARN" if is_backup else "ERROR", "V1",
                        f"{len(tiny)} 个字符小于 {TINY_PT:g}pt 等效（最小 {min(sizes):.1f}pt），投影不可读：「{sample}」", i)
                frac = len(body) / len(chars)
                if frac > 0.25 and not is_backup:
                    add("WARN", "V1", f"{frac:.0%} 的正文区文字小于 {BODY_MIN_PT:g}pt 等效（图中文字也算）", i)

            # S2 topic titles (heuristic: largest text in top 30%)
            if (not is_backup and i > 1 and info["title"] and is_topic_title(info["title"])
                    and not CLOSING_RE.match(info["title"])):
                add("WARN", "S2", f"标题「{info['title']}」像话题；内容页请用结论句（章节分隔页可忽略）", i)

            # S6 words
            if not is_backup:
                if info["words"] > HARD_MAX_WORDS:
                    add("ERROR", "S6", f"约 {info['words']:.0f} 词，文字墙 → 拆页或把文字移到演讲者备注", i)
                elif info["words"] > MAX_WORDS:
                    add("WARN", "S6", f"约 {info['words']:.0f} 词，偏多", i)

            # S7 text-only
            graphics = len(page.images) + len(page.curves) + len([r for r in page.rects
                         if (r["x1"] - r["x0"]) < w * 0.95 or (r["bottom"] - r["top"]) < h * 0.95])
            info["graphics"] = graphics
            if not is_backup and i > 1 and graphics < 3 and info["words"] > 15:
                add("WARN", "S7", "疑似纯文字页：没有图片或图形 → 考虑加一个视觉中心", i)

        # V7 page numbers
        numbered = 0
        for i, page in enumerate(pdf.pages, start=1):
            h = page.height
            zone = [c for c in page.chars if c["top"] > h * 0.85 or c["bottom"] < h * 0.12]
            txt = "".join(c["text"] for c in sorted(zone, key=lambda c: (round(c["top"]), c["x0"])))
            if re.search(rf"(?<!\d){i}(?!\d)", txt):
                numbered += 1
        if n >= 5 and numbered < n * 0.5:
            add("WARN", "V7", f"只有 {numbered}/{n} 页检测到页码；加上页码方便 Q&A 时引用")

    # V3 fonts
    fam = [f for f, k in fonts.items() if k > 20]
    if len(fam) > 4:
        add("WARN", "V3", f"使用了 {len(fam)} 种字体族（{', '.join(fam[:8])}），建议 ≤ 3")

    # T7 count, merging builds (consecutive identical titles)
    main = [p for p in pages_info if backup_start is None or p["page"] < backup_start]
    logical = 0
    prev = None
    for p in main:
        if not p["title"] or p["title"] != prev:
            logical += 1
        prev = p["title"]
    if main and main[-1]["title"] and CLOSING_RE.match(main[-1]["title"]):
        add("WARN", "T6", f"主线最后一页是「{main[-1]['title']}」；Q&A 时屏幕会停在这页 → 以结论页收尾",
            main[-1]["page"])
    summary = {"pages": len(pages_info), "main_pages": len(main), "logical_slides": logical,
               "backup_pages": len(pages_info) - len(main)}
    if duration:
        lo, hi = duration / 3.0, duration * 1.2
        if logical > hi:
            add("ERROR" if logical > duration * 1.6 else "WARN", "T7",
                f"{logical} 张逻辑页（已合并逐步揭示）对 {duration:g} 分钟偏多；经验范围约 {lo:.0f}–{hi:.0f}")
        elif logical < lo:
            add("WARN", "T7", f"{logical} 张逻辑页对 {duration:g} 分钟偏少；确认每页不是太满")
    if backup_start is None:
        add("INFO", "T9", "未指定 --backup-start；如果有备份页，请指定，否则会被计入时长和字数检查")
    return issues, pages_info, summary


def render(path, outdir, scale=1.0):
    try:
        import pypdfium2 as pdfium
    except ImportError:
        print("跳过渲染：需要 pypdfium2（pip install pypdfium2）", file=sys.stderr)
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
    ap.add_argument("--duration", type=float, help="时长（分钟，不含 Q&A）")
    ap.add_argument("--backup-start", type=int, help="第一页备份页的页码（之后的页不计入时长，检查放宽）")
    ap.add_argument("--render", metavar="DIR", help="把每页渲染成 PNG 以便逐页看图")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    issues, pages, summary = analyze(a.pdf, a.duration, a.backup_start)
    rendered = render(a.pdf, a.render) if a.render else []
    n_err = sum(i["level"] == "ERROR" for i in issues)

    if a.json:
        print(json.dumps({"summary": summary, "issues": issues, "pages": pages,
                          "rendered": rendered}, ensure_ascii=False, indent=2))
    else:
        print(f"{a.pdf}: {summary['pages']} 页（主线 {summary['main_pages']}，"
              f"合并逐步揭示后 {summary['logical_slides']} 张逻辑页；备份 {summary['backup_pages']}）\n")
        order = {"ERROR": 0, "WARN": 1, "INFO": 2}
        for i in sorted(issues, key=lambda x: (order[x["level"]], x["page"] or 0)):
            where = f"第 {i['page']} 页 " if i["page"] else ""
            print(f"{i['level']:5} [{i['check']}] {where}{i['msg']}")
        print(f"\n{n_err} ERROR, {sum(i['level'] == 'WARN' for i in issues)} WARN")
        if rendered:
            print(f"\n已渲染 {len(rendered)} 页到 {a.render}/ ——逐页看图，检查重叠、截断、模糊、对比度和对齐。")
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
