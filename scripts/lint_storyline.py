#!/usr/bin/env python3
"""Lint storyline.md (format: assets/storyline-template.md).

Checks (numbers correspond to references/review-checklist.md):
  M1  core_message exists and is one sentence
  S2  Content page titles are declarative sentences, not topics
  T3  Contribution / preview page appears within first 25% of main line
  T6  Last main page is not "thank you / questions"
  T7  Planned minutes match duration_min
  T9  Backup pages exist
  Extra: duplicate titles, unknown tags, titles too long

Usage:
  python lint_storyline.py storyline.md [--json]
Exit code: 1 if any ERROR, otherwise 0.
"""
import argparse
import json
import re
import sys

KNOWN_TAGS = {
    "hook", "motivation", "question", "contribution", "outline", "section",
    "method", "result", "discussion", "takeaway", "future", "ack", "backup",
}
# Tags that may legitimately have topic-style titles.
TOPIC_OK_TAGS = {"section", "outline", "ack", "backup"}
NON_TIMED_TAGS = {"backup"}

TOPIC_WORDS = {
    # English
    "introduction", "intro", "background", "motivation", "method", "methods",
    "methodology", "approach", "model", "results", "result", "experiments",
    "experiment", "evaluation", "discussion", "conclusion", "conclusions",
    "summary", "outline", "agenda", "overview", "related work", "future work",
    "limitations", "data", "setup", "experimental setup", "analysis",
    "contributions", "acknowledgments", "acknowledgements", "thanks",
    "q&a", "questions", "thank you", "the end",
    # Chinese
    "引言", "介绍", "背景", "研究背景", "动机", "方法", "研究方法", "模型", "结果",
    "实验", "实验结果", "评估", "讨论", "结论", "总结", "大纲", "目录", "概述",
    "相关工作", "未来工作", "局限", "数据", "实验设置", "分析", "贡献", "致谢",
    "谢谢", "问答", "提问", "感谢聆听", "谢谢观看",
}
CLOSING_RE = re.compile(
    r"^(thank(s| you)|questions?\??|q\s*&\s*a|the end|谢谢|感谢|欢迎提问|问答|提问)",
    re.I,
)
LINE_RE = re.compile(
    r"^\s*(\d+)\.\s*\[([\w-]+)\]\s*(.+?)\s*(?:\((\d+(?:\.\d+)?)\s*min\))?\s*$"
)
CJK_RE = re.compile(r"[\u3400-\u9fff\uf900-\ufaff]")


def strip_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def parse_frontmatter(text):
    meta = {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.S)
    if not m:
        return meta, text
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, text[m.end():]


def title_len(title):
    """Rough "word" length: CJK chars count as 0.5 words."""
    cjk = len(CJK_RE.findall(title))
    latin = len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", CJK_RE.sub(" ", title)))
    return latin + cjk / 2.0, cjk, latin


def is_topic_title(title):
    t = title.strip().rstrip(":：.。").lower()
    if t in TOPIC_WORDS:
        return True
    # "Results (cont.)", "Method 2", "Experiment II", "实验一"
    base = re.sub(r"[\s\-–—:：]*(\(.*\)|（.*）|\d+|[ivx]+|[一二三四五六七八九十]+|cont\.?|续)$", "", t).strip()
    if base in TOPIC_WORDS:
        return True
    words, cjk, latin = title_len(title)
    # Very short titles with no verb characteristics are almost always topics.
    if cjk == 0 and latin <= 2:
        return True
    if latin == 0 and cjk <= 5:
        return True
    return False


def count_sentences(s):
    parts = [p for p in re.split(r"[.!?。！？；;]+", s) if p.strip()]
    return len(parts)


def lint(path):
    raw = open(path, encoding="utf-8").read()
    meta, body = parse_frontmatter(raw)
    body = strip_comments(body)
    issues = []

    def add(level, code, msg, slide=None):
        issues.append({"level": level, "check": code, "slide": slide, "msg": msg})

    slides = []
    for ln in body.splitlines():
        m = LINE_RE.match(ln)
        if m:
            slides.append({
                "n": int(m.group(1)), "tag": m.group(2).lower(),
                "title": m.group(3).strip(),
                "min": float(m.group(4)) if m.group(4) else None,
            })
        elif re.match(r"^\s*\d+\.\s+", ln):
            add("WARN", "FORMAT", f"Unparseable line (missing [tag]?): {ln.strip()}")

    # M1
    cm = meta.get("core_message", "")
    if not cm:
        add("ERROR", "M1", "frontmatter missing core_message (one-sentence core message)")
    else:
        if count_sentences(cm) > 1:
            add("WARN", "M1", "core_message is more than one sentence, please compress into a single declarative sentence")
        if is_topic_title(cm):
            add("ERROR", "M1", f"core_message looks like a topic rather than a declarative sentence: \"{cm}\"")

    if not slides:
        add("ERROR", "FORMAT", "No pages parsed. Format: `1. [tag] Title (1 min)`")
        return issues, slides, meta

    main = [s for s in slides if s["tag"] not in NON_TIMED_TAGS]
    backup = [s for s in slides if s["tag"] == "backup"]

    seen = {}
    for s in slides:
        if s["tag"] not in KNOWN_TAGS:
            add("WARN", "FORMAT", f"Unknown tag [{s['tag']}]", s["n"])
        key = s["title"].lower()
        if key in seen:
            add("WARN", "S1", f"Title duplicates page {seen[key]}; if stepwise reveal please merge into one line, otherwise rewrite", s["n"])
        seen[key] = s["n"]
        # S2
        if s["tag"] not in TOPIC_OK_TAGS and is_topic_title(s["title"]):
            add("ERROR", "S2", f"Topic-style title \"{s['title']}\" -> change to a conclusion sentence for this page", s["n"])
        words, cjk, latin = title_len(s["title"])
        if words > 16 or cjk > 32:
            add("WARN", "S2", "Title too long, compress to one line readable at a glance", s["n"])

    # Backup pages must be after all main pages
    if backup and main and min(b["n"] for b in backup) < max(m["n"] for m in main):
        add("WARN", "T9", "Backup pages should be placed after all main pages")

    # T3
    k = max(1, round(len(main) * 0.25))
    if not any(s["tag"] == "contribution" for s in main[:k + 1]):
        add("WARN", "T3", f"No [contribution] (result preview) in first {k + 1} pages. The audience needs to know where you're headed early")

    # T6
    tail = [s for s in main if s["tag"] != "ack"]
    last = main[-1]
    if tail and CLOSING_RE.match(tail[-1]["title"]):
        add("ERROR", "T6", f"Last main content page is \"{tail[-1]['title']}\" -> end with a conclusion page that restates the core message", tail[-1]["n"])
    if last["tag"] == "ack":
        add("WARN", "T6", "Main line ends with an acknowledgments page: screen will stay on this during Q&A. Consider merging credits into the conclusion page, or switch back to the conclusion page during Q&A", last["n"])
    if tail and tail[-1]["tag"] not in {"takeaway", "future"}:
        add("WARN", "T6", "Last main page (excluding acknowledgments) is not [takeaway] / [future]", tail[-1]["n"])
    if not any(s["tag"] == "takeaway" for s in main):
        add("ERROR", "T6", "No [takeaway] conclusion page")

    # T7
    dur = meta.get("duration_min")
    try:
        dur = float(dur) if dur else None
    except ValueError:
        dur = None
        add("WARN", "T7", "duration_min is not a number")
    if dur is None:
        add("ERROR", "T7", "frontmatter missing duration_min (minutes excluding Q&A)")
    else:
        timed = [s for s in main if s["min"] is not None]
        if len(timed) == len(main):
            total = sum(s["min"] for s in main)
            if total > dur * 1.05:
                add("ERROR", "T7", f"Planned time {total:g} min exceeds duration {dur:g} min -> cut or move to backup")
            elif total < dur * 0.75:
                add("WARN", "T7", f"Planned time {total:g} min is significantly less than {dur:g} min; confirm nothing is missing")
        else:
            if timed:
                add("WARN", "T7", f"{len(main) - len(timed)} pages have no minute labels, estimating by page count")
            lo, hi = dur / 2.5, dur * 1.2
            if len(main) > hi:
                add("WARN", "T7", f"{len(main)} main pages for {dur:g} min is high (empirical range ~{lo:.0f}-{hi:.0f} pages)")
            elif len(main) < lo:
                add("WARN", "T7", f"{len(main)} main pages for {dur:g} min is low (empirical range ~{lo:.0f}-{hi:.0f} pages)")
        for s in main:
            if s["min"] is not None and s["min"] > 3:
                add("WARN", "S1", f"Single page planned {s['min']:g} min, usually means multiple points crammed into one page", s["n"])

    # T9
    if not backup:
        add("WARN", "T9", "No [backup] pages: anticipated questions, full tables, details go here")

    results = [s for s in main if s["tag"] == "result"]
    if not results:
        add("WARN", "M3", "No [result] pages")
    return issues, slides, meta


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("storyline")
    ap.add_argument("--json", action="store_true", help="Output JSON")
    a = ap.parse_args()
    issues, slides, meta = lint(a.storyline)
    n_err = sum(i["level"] == "ERROR" for i in issues)
    if a.json:
        print(json.dumps({"issues": issues, "n_slides": len(slides)}, ensure_ascii=False, indent=2))
    else:
        main_n = sum(s["tag"] not in NON_TIMED_TAGS for s in slides)
        print(f"storyline: {main_n} main pages + {len(slides) - main_n} backup pages; duration {meta.get('duration_min', '?')} min")
        print(f"Core message: {meta.get('core_message', '(missing')}\n")
        for i in sorted(issues, key=lambda x: (x["level"] != "ERROR", x["slide"] or 0)):
            where = f"page {i['slide']} " if i["slide"] else ""
            print(f"{i['level']:5} [{i['check']}] {where}{i['msg']}")
        print(f"\n{n_err} errors, {len(issues) - n_err} warnings")
        print("\nTitles only:")
        for s in slides:
            print(f"  {s['n']:>2}. {s['title']}")
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
