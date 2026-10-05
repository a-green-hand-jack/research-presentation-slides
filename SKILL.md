---
name: research-presentation-slides
description: 制作、改写或评审「展示自己工作」的演示幻灯片（研究报告、会议 talk、组会汇报、答辩、求职 talk、项目/技术分享），与工具无关（PowerPoint、Keynote、Google Slides、Beamer、Marp、Slidev、reveal.js、python-pptx 等均可）。提供分步工作流（talk brief → storyline → slide spec → 制作 → PDF 自动检查 → 评审清单）、模板和检查脚本。只要用户要做 slides/PPT/deck/beamer/presentation/talk、从论文或代码仓库生成报告幻灯片、或让你评审/改进一份已有的 slides，就使用本 skill，即使用户只说「做个 PPT」而没提质量要求。
---

# Research Presentation Slides

本 skill 规定**做一份好的工作展示 slides 的流程和标准**。它不管用什么工具做；工具层面的操作交给对应工具的 skill 或文档（例如 pptx skill、Beamer 文档）。

**一个前提**：演讲是给人「听」的，slides 是辅助。slides 不是讲稿，也不是论文的压缩版。下面每一步都在执行这个前提。

## 工作流

按顺序做。每一步都产出一个文件，下一步以它为输入。不要跳过第 1–3 步直接做页面，这是做坏 slides 最常见的原因。

| 步骤 | 产出 | 模板 / 工具 | 细则 |
|---|---|---|---|
| 1. 定目标 | `talk-brief.md` | `assets/talk-brief-template.md` | `references/planning.md` |
| 2. 搭故事线 | `storyline.md` | `assets/storyline-template.md`，`scripts/lint_storyline.py` | `references/structure.md`，`references/talk-types.md` |
| 3. 写逐页规格 | `slide-specs.md` | `assets/slide-spec-template.md` | `references/slide-design.md`，`references/figures.md` |
| 4. 制作 | 源文件（.pptx / .tex / .md / …） | 用户选定的工具 | `references/visual-style.md` |
| 5. 导出并检查 | `deck.pdf` + 检查报告 | `scripts/check_deck_pdf.py` | 本文「第 5 步」 |
| 6. 评审与保底 | 修改后的 deck，备份页，演讲者备注 | `references/review-checklist.md` | `references/delivery.md` |

### 第 1 步：定目标 → `talk-brief.md`

复制 `assets/talk-brief-template.md` 并填写：目的、听众、**一句话核心信息**、时长、场合约束。

- 缺少时长、听众、场合中的任何一项时：**人类**自己补上；**agent** 先问用户，问不到就把假设明确写进 brief，并在交付时告诉用户。
- 核心信息必须是一个完整的陈述句，不能是一个话题。例如「X 方法」是话题；「X 把推理延迟降低一半且不损失精度」是核心信息。

### 第 2 步：搭故事线 → `storyline.md`

复制 `assets/storyline-template.md`。**每一页写成一行结论句标题**，并打上角色标签。规划顺序是**从结果倒推**：

1. 把结果按「它支持哪个观点」分组，分成 2–4 组，每组得出一个主要观点。不要按实验做的先后分组。
2. 不支持这些观点的结果，删掉或移到 `[backup]`。
3. 方法只写到观众能看懂结果为止。
4. 最后写开场动机：从全体观众都关心的问题出发，连接到你的具体目标。
5. 结尾回到那个大问题并重申核心信息。最后一页主内容不能只有「Thank you」或「Questions?」。

然后运行：

```bash
python scripts/lint_storyline.py storyline.md
```

修到没有 ERROR 为止。最后**只读标题**，从头到尾读一遍：读下来应该是一个连贯的故事。读不通就改故事线，不要进入下一步。

> agent：把核心信息和标题清单先给用户过目（或在回复里列出），确认方向后再生成页面。

### 第 3 步：写逐页规格 → `slide-specs.md`

对故事线中的每一页，按 `assets/slide-spec-template.md` 写清楚：标题（结论句）、视觉中心（哪张图/哪个示意图）、屏幕上的少量文字、要讲的话（演讲者备注）、来源引用、预计时长。规则见 `references/slide-design.md` 和 `references/figures.md`。

### 第 4 步：制作

用用户选定的工具，把规格变成页面。视觉规范见 `references/visual-style.md`。工具相关的操作看对应工具的 skill 或文档。

### 第 5 步：导出 PDF 并检查

几乎所有工具都能导出 PDF，所以检查统一在 PDF 上做：

```bash
python scripts/check_deck_pdf.py deck.pdf --duration 15 --backup-start 18 --render pages/
```

- 依赖：`pip install pdfplumber pypdfium2`（`--render` 需要后者）。
- 脚本检查：页数与时长是否匹配、字号是否过小、每页字数、纯文字页、内容是否超出页面、字体数量、页码。参数说明见 `--help`。
- `--render` 把每页导出成 PNG。**逐页看图**，检查脚本查不出的问题：重叠、截断、图片模糊、对比度不足、对齐。agent 必须做这一步：代码编译通过不等于版面正确。
- 修复所有 ERROR。WARN 逐条判断：要么修，要么能说出不修的理由。

### 第 6 步：评审与保底

- 逐条过 `references/review-checklist.md`，条目带编号（例如 `S3`、`F2`）。写评审意见时引用编号。
- 按 `references/delivery.md` 补全：备份页、演讲者备注、PDF 保底版本、视频截图、超时时的跳过方案。
- 人类：计时完整练一遍，回到第 2–3 步修改讲超时或讲不顺的页。

## 不可违反的规则

这些规则在任何场合都成立。其余规则见 references，可以根据场合取舍。

1. 一页只讲一个观点；内容页标题写结论，不写话题。
2. 屏幕上的东西你都会讲到；不讲的不放。
3. 每页有视觉中心；不写大段完整句子。
4. 字要大到在投影下可读；图表的字也一样。
5. 数据、结果、引用只能来自用户提供的材料或可核实的来源。缺了就留明显的占位符（例如 `【待补：xx 实验数字】`）并告知用户。绝不编造。
6. 先有核心信息和故事线，再做页面。

## 改写或评审已有 slides

1. 导出或拿到 PDF，运行 `scripts/check_deck_pdf.py`。
2. 从现有页面反推出 `storyline.md`（把每页标题改写成结论句），运行 `lint_storyline.py`。
3. 用 `references/review-checklist.md` 输出带条目编号的问题清单，按影响从大到小排序：结构问题 > 单页问题 > 视觉问题。
4. 修改时先改故事线，再改页面。

## 目录结构

```
research-presentation-slides/
├── SKILL.md                    # 本文件：工作流 + 索引
├── references/                 # 各步骤细则，按需读取
├── assets/                     # 第 1–3 步的模板（复制后填写）
├── scripts/
│   ├── lint_storyline.py       # 检查 storyline.md
│   └── check_deck_pdf.py       # 检查导出的 PDF，可渲染逐页 PNG
└── evals/evals.json            # 测试用例，修改 skill 后用来回归
```

## References 索引

需要时再读，不必一次全读：

- `references/planning.md`：目的、听众、核心信息怎么定；常见错误目标。
- `references/structure.md`：沙漏结构、从结果倒推、报纸式论证、套娃分层、开场与结尾、文献综述放哪。
- `references/talk-types.md`：不同场合（会议短报告、组会、答辩、求职 talk、lightning talk、非专业听众）的取舍和时长配比。
- `references/slide-design.md`：单页规则，附改写前后对比示例。
- `references/figures.md`：图和表怎么从论文版改成 slides 版。
- `references/visual-style.md`：字号、配色、字体、可访问性、一致性。
- `references/delivery.md`：演讲者备注、练习、备份页、技术故障预案。
- `references/review-checklist.md`：带编号的评审清单，也是交付前的最终检查。
- `references/sources.md`：本 skill 依据的资料。

## 扩展本 skill

- **新增一种场合**（例如 grant pitch、产品评审）：在 `references/talk-types.md` 里加一节，格式与已有各节一致（目的 / 时长配比 / 必有页 / 常见错误）。
- **新增一条规则**：放进对应主题的 reference 文件，同时在 `references/review-checklist.md` 加一个新编号条目。已有编号不要改动，以免破坏旧的评审记录。
- **新增工具相关说明**（例如 Beamer 主题建议）：新建 `references/tools/<tool>.md`，在上面的索引里加一行。本文件保持与工具无关。
- **新增自动检查**：在 `scripts/` 中扩展。检查对象尽量是 PDF 或 `storyline.md` 这类与工具无关的产物，并在 `evals/evals.json` 加对应测试用例。
