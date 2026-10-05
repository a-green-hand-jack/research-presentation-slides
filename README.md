# research-presentation-slides

一个帮助 AI agent（以及人）做好「展示自己工作」的演示幻灯片的 skill：研究报告、会议 talk、组会汇报、答辩、求职 talk、项目/技术分享都适用。

它规定的是**流程和标准**，与制作工具无关：PowerPoint、Keynote、Google Slides、Beamer、Marp、Slidev、reveal.js、python-pptx 都可以配合使用。

## 它做什么

skill 把做 slides 拆成六步，每一步产出一个文件，作为下一步的输入：

| 步骤 | 产出 |
|---|---|
| 1. 定目标 | `talk-brief.md`：目的、听众、一句话核心信息、时长、场合 |
| 2. 搭故事线 | `storyline.md`：每页一行结论句标题，用 `scripts/lint_storyline.py` 检查 |
| 3. 写逐页规格 | `slide-specs.md`：视觉中心、屏幕文字、演讲者备注、来源 |
| 4. 制作 | 用户选定工具的源文件 |
| 5. 导出并检查 | `deck.pdf` + `scripts/check_deck_pdf.py` 的检查报告和逐页 PNG |
| 6. 评审与保底 | 按带编号的评审清单修改，补备份页和备注 |

除此之外，它还可以评审和改写已有的 slides：从 PDF 反推故事线，输出带清单编号、按严重程度排序的问题列表。

完整工作流和不可违反的规则见 [`SKILL.md`](SKILL.md)。

## 安装

推荐用 [`skills`](https://github.com/vercel-labs/skills) CLI 安装。**在需要做 slides 的那个仓库的根目录下**运行：

```bash
npx skills add a-green-hand-jack/research-presentation-slides
```

只想装给某一个 agent（例如 Claude Code）时，加上 `--agent`：

```bash
npx skills add a-green-hand-jack/research-presentation-slides --agent claude-code
```

安装前想先看看仓库里有哪些 skill，可以加 `--list`，这样只列出、不安装。

### 建议：只在需要的仓库里安装，不要全局安装

`skills` 默认安装到当前项目（project-level），这也是我们推荐的方式。**请不要加 `-g` / `--global`**，除非你确实在几乎所有项目里都要做 slides。理由：

- **避免误触发**：这个 skill 的描述有意写得很宽，只要提到 slides、PPT、deck、talk 就会触发。全局安装后，它会出现在每个项目的 agent 上下文里，在和演讲无关的仓库中也可能被调用。
- **少占上下文**：每个已安装 skill 的名称和描述都会进入 agent 的上下文。只在需要的地方装，其他项目就不必为它付出这部分开销。
- **版本可控**：项目级安装会生成 `skills-lock.json`，记录来源和内容哈希。不同项目可以各自停留在合适的版本，升级时互不影响。
- **方便协作**：skill 文件和锁文件都在仓库里，合作者拉取后用的是同一份 skill。

一个合适的做法是：在论文仓库、报告材料仓库或专门放 slides 的仓库里安装；做完报告后如果不再需要，就移除。

### 安装后会多出什么

以 `--agent claude-code` 为例，项目里会多出：

```
.claude/skills/research-presentation-slides/   # skill 本体
skills-lock.json                               # 来源与内容哈希
```

建议把这两项都提交到仓库，方便合作者直接使用。其他 agent 的安装目录不同，以 CLI 输出为准。

### 更新与移除

```bash
npx skills list                                   # 查看当前项目已安装的 skill
npx skills update -p                              # 只更新当前项目的 skill
npx skills remove research-presentation-slides    # 从当前项目移除
```

> skill 会以 agent 的完整权限运行。安装前请先浏览一遍 `SKILL.md` 和 `scripts/` 里的内容。

## 使用

安装后不需要特别的命令，直接让 agent 做事即可，例如：

- 「这是我的论文 PDF，帮我做一个 15 分钟的会议报告 slides，用 Beamer。」
- 「帮我看看这份组会 PPT 哪里不好（附 deck.pdf），下周要讲 20 分钟。」
- 「我们做了一个开源工具，想做一个 5 分钟的 lightning talk，用 Marp。」

agent 会先产出 talk brief 和故事线，确认方向后再做页面。

两个检查脚本也可以手动运行：

```bash
# 检查故事线
python scripts/lint_storyline.py storyline.md

# 检查导出的 PDF，并把每页渲染成 PNG
pip install pdfplumber pypdfium2
python scripts/check_deck_pdf.py deck.pdf --duration 15 --backup-start 18 --render pages/
```

安装到项目后，脚本路径要加上 skill 所在目录，例如 `.claude/skills/research-presentation-slides/scripts/lint_storyline.py`。

## 仓库结构

```
research-presentation-slides/
├── SKILL.md                    # 工作流 + 索引（agent 的入口）
├── references/                 # 各步骤细则，按需读取
├── assets/                     # 第 1–3 步的模板
├── scripts/
│   ├── lint_storyline.py       # 检查 storyline.md
│   └── check_deck_pdf.py       # 检查导出的 PDF，可渲染逐页 PNG
└── evals/evals.json            # 测试用例，修改 skill 后用来回归
```

## 参与改进

新增场合、规则、工具说明或自动检查的约定，见 [`SKILL.md`](SKILL.md) 的「扩展本 skill」一节。规则所依据的资料列在 [`references/sources.md`](references/sources.md)。

## 许可证

[MIT](LICENSE)
