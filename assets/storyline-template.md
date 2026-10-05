---
core_message: 免训练的稀疏缓存能把长上下文推理延迟减半而几乎不损失精度
duration_min: 15
audience: 同行专家
---

# Storyline

<!-- 下面是一个完整示例。使用时替换 frontmatter 和所有页面。 -->

<!--
格式（scripts/lint_storyline.py 依赖此格式）：
  <序号>. [<标签>] <结论句标题> (<分钟> min)
分钟可省略。不想被检查的说明文字写在 HTML 注释里。

标签：
  hook          开场：抓住观众的问题或现象
  motivation    为什么重要
  question      本工作要回答的具体问题
  contribution  我们做了什么、发现了什么（结果预告一句）
  outline       路线图（短报告可省略）
  section       章节分隔页（只有这类页面允许用话题式标题）
  method        方法 / 模型 / 系统
  result        结果（每页一个结论）
  discussion    与 2–3 篇最相关工作的对比、局限、意义
  takeaway      结论：重申核心信息、回到大问题
  future        未来工作
  ack           致谢 / 署名
  backup        备份页（放在主线之后，不计入时长）

只读标题时，应该能读成一个连贯的故事。
-->

1. [hook] 长上下文推理的成本随长度平方增长，已成为部署瓶颈 (1 min)
2. [question] 能否在不重新训练的情况下把注意力开销降到线性？ (1 min)
3. [contribution] 我们的稀疏缓存把 64k 长度下的延迟减半，精度损失 <0.5% (1 min)
4. [method] 大部分注意力集中在少量「锚点」token 上 (1.5 min)
5. [method] 只缓存锚点 + 滑动窗口即可近似完整注意力 (2 min)
6. [result] 在 4 个基准上精度与全注意力持平 (2 min)
7. [result] 延迟随长度线性增长，64k 时快 2.1 倍 (2 min)
8. [result] 收益主要来自锚点选择，而不是窗口大小 (1.5 min)
9. [discussion] 与 A、B 相比，我们无需微调且支持任意模型 (1.5 min)
10. [takeaway] 免训练的稀疏缓存让长上下文部署成本降低一半 (1.5 min)

<!-- 以下为备份页 -->
11. [backup] 全部 12 个基准的完整结果表
12. [backup] 锚点数量的消融实验
13. [backup] 与相关工作的详细比较
