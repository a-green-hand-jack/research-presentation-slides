#!/usr/bin/env python3
"""检查 storyline.md（格式：assets/storyline-template.md）。

检查项（编号对应 references/review-checklist.md）：
  M1  core_message 存在且为一句话
  S2  内容页标题是陈述句，不是话题
  T3  贡献/预告页出现在主线前 25% 内
  T6  最后一页主线不是「thank you / questions」
  T7  计划分钟数与 duration_min 匹配
  T9  存在备份页
  额外：重复标题、未知标签、标题过长

用法：
  python lint_storyline.py storyline.md [--json]
退出码：如有任何 ERROR 则为 1，否则为 0。
"""
import argparse
import json
import re
import sys

KNOWN_TAGS = {
    "hook", "motivation", "question", "contribution", "outline", "section",
    "method", "result", "discussion", "takeaway", "future", "ack", "backup",
}
# 标题可以合法为话题式的标签。
TOPIC_OK_TAGS = {"section", "outline", "ack", "backup"}
NON_TIMED_TAGS = {"backup"}

TOPIC_WORDS = {
    # 英文
    "introduction", "intro", "background", "motivation", "method", "methods",
    "methodology", "approach", "model", "results", "result", "experiments",
    "experiment", "evaluation", "discussion", "conclusion", "conclusions",
    "summary", "outline", "agenda", "overview", "related work", "future work",
    "limitations", "data", "setup", "experimental setup", "analysis",
    "contributions", "acknowledgments", "acknowledgements", "thanks",
    "q&a", "questions", "thank you", "the end",
    # 中文
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
    """粗略「词」长度：CJK 字符每个计 0.5 词。"""
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
    # 极短标题且没有动词特征的几乎总是话题。
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
            add("WARN", "FORMAT", f"无法解析的行（缺少 [标签]？）：{ln.strip()}")

    # M1
    cm = meta.get("core_message", "")
    if not cm:
        add("ERROR", "M1", "frontmatter 缺少 core_message（一句话核心信息）")
    else:
        if count_sentences(cm) > 1:
            add("WARN", "M1", "core_message 超过一句，请压缩成一个陈述句")
        if is_topic_title(cm):
            add("ERROR", "M1", f"core_message 看起来是话题而不是陈述句：「{cm}」")

    if not slides:
        add("ERROR", "FORMAT", "没有解析到任何页面。格式：`1. [tag] 标题 (1 min)`")
        return issues, slides, meta

    main = [s for s in slides if s["tag"] not in NON_TIMED_TAGS]
    backup = [s for s in slides if s["tag"] == "backup"]

    seen = {}
    for s in slides:
        if s["tag"] not in KNOWN_TAGS:
            add("WARN", "FORMAT", f"未知标签 [{s['tag']}]", s["n"])
        key = s["title"].lower()
        if key in seen:
            add("WARN", "S1", f"标题与第 {seen[key]} 页重复；若是逐步揭示请合并为一行，否则改写", s["n"])
        seen[key] = s["n"]
        # S2
        if s["tag"] not in TOPIC_OK_TAGS and is_topic_title(s["title"]):
            add("ERROR", "S2", f"话题式标题「{s['title']}」→ 改成这一页的结论句", s["n"])
        words, cjk, latin = title_len(s["title"])
        if words > 16 or cjk > 32:
            add("WARN", "S2", "标题过长，压缩到一行能读完", s["n"])

    # 备份页必须位于主线之后
    if backup and main and min(b["n"] for b in backup) < max(m["n"] for m in main):
        add("WARN", "T9", "备份页应放在全部主线页面之后")

    # T3
    k = max(1, round(len(main) * 0.25))
    if not any(s["tag"] == "contribution" for s in main[:k + 1]):
        add("WARN", "T3", f"前 {k + 1} 页没有 [contribution]（结果预告）。观众需要早点知道你要去哪")

    # T6
    tail = [s for s in main if s["tag"] != "ack"]
    last = main[-1]
    if tail and CLOSING_RE.match(tail[-1]["title"]):
        add("ERROR", "T6", f"最后一页主内容是「{tail[-1]['title']}」→ 用重申核心信息的结论页收尾", tail[-1]["n"])
    if last["tag"] == "ack":
        add("WARN", "T6", "主线以致谢页结束：Q&A 时屏幕会一直停在这页。考虑把署名并入结论页，或 Q&A 时切回结论页", last["n"])
    if tail and tail[-1]["tag"] not in {"takeaway", "future"}:
        add("WARN", "T6", "主线最后一页（致谢除外）不是 [takeaway] / [future]", tail[-1]["n"])
    if not any(s["tag"] == "takeaway" for s in main):
        add("ERROR", "T6", "没有 [takeaway] 结论页")

    # T7
    dur = meta.get("duration_min")
    try:
        dur = float(dur) if dur else None
    except ValueError:
        dur = None
        add("WARN", "T7", "duration_min 不是数字")
    if dur is None:
        add("ERROR", "T7", "frontmatter 缺少 duration_min（不含 Q&A 的分钟数）")
    else:
        timed = [s for s in main if s["min"] is not None]
        if len(timed) == len(main):
            total = sum(s["min"] for s in main)
            if total > dur * 1.05:
                add("ERROR", "T7", f"计划用时 {total:g} 分钟超过时长 {dur:g} 分钟 → 删减或移入备份")
            elif total < dur * 0.75:
                add("WARN", "T7", f"计划用时 {total:g} 分钟明显少于 {dur:g} 分钟；确认没有遗漏")
        else:
            if timed:
                add("WARN", "T7", f"{len(main) - len(timed)} 页没有标注分钟数，用页数估算")
            lo, hi = dur / 2.5, dur * 1.2
            if len(main) > hi:
                add("WARN", "T7", f"{len(main)} 页主线对 {dur:g} 分钟偏多（经验范围约 {lo:.0f}–{hi:.0f} 页）")
            elif len(main) < lo:
                add("WARN", "T7", f"{len(main)} 页主线对 {dur:g} 分钟偏少（经验范围约 {lo:.0f}–{hi:.0f} 页）")
        for s in main:
            if s["min"] is not None and s["min"] > 3:
                add("WARN", "S1", f"单页计划 {s['min']:g} 分钟，通常意味着一页装了多个观点", s["n"])

    # T9
    if not backup:
        add("WARN", "T9", "没有 [backup] 备份页：预判的问题、完整表格、细节放这里")

    results = [s for s in main if s["tag"] == "result"]
    if not results:
        add("WARN", "M3", "没有 [result] 页")
    return issues, slides, meta


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("storyline")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    a = ap.parse_args()
    issues, slides, meta = lint(a.storyline)
    n_err = sum(i["level"] == "ERROR" for i in issues)
    if a.json:
        print(json.dumps({"issues": issues, "n_slides": len(slides)}, ensure_ascii=False, indent=2))
    else:
        main_n = sum(s["tag"] not in NON_TIMED_TAGS for s in slides)
        print(f"storyline: {main_n} 页主线 + {len(slides) - main_n} 页备份；时长 {meta.get('duration_min', '?')} 分钟")
        print(f"核心信息：{meta.get('core_message', '(缺失)')}\n")
        for i in sorted(issues, key=lambda x: (x["level"] != "ERROR", x["slide"] or 0)):
            where = f"第 {i['slide']} 页 " if i["slide"] else ""
            print(f"{i['level']:5} [{i['check']}] {where}{i['msg']}")
        print(f"\n{n_err} 个错误, {len(issues) - n_err} 个警告")
        print("\n只读标题：")
        for s in slides:
            print(f"  {s['n']:>2}. {s['title']}")
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
