# Oracle Reader Review - Delegation Guide

委托 Oracle 扮演目标读者进行批判性审视。

## 核心价值

自己很难完全带入读者视角批判性审视。Oracle 扮演目标读者，提供「局外人」反馈。

| 自己审视 | Oracle 审视 |
|---------|------------|
| 已知所有背景，难以「假装不知道」 | 真正从零开始理解 |
| 倾向于认为自己的逻辑清晰 | 会指出跳跃/假设过多 |
| 容易忽略「专家盲区」 | 会问「这个术语什么意思」 |
| 情感上抗拒否定 | 客观批评，不留情面 |

**关键心态**：Oracle 的批评 = 真实读者可能的反应。不是「AI 不理解」，而是「如果读者也不理解怎么办」。

---

## Prompt Template

```markdown
## Task: Reader-Perspective Review

**Role**: 你是这个报告的目标读者 [{reader_description}]。

**Context**:
- 报告目标: {goal}
- 读者背景: {reader_background}
- 预期用途: {intended_use}

**Material**:
{outline_or_content}

**Review Focus**:
1. **Opening**: 开头是否抓住我的注意力？我为什么要继续读？
2. **Problem Definition**: 这个问题真的是我关心的吗？还是作者自己关心的？
3. **Logic Chain**: 论证链条清晰吗？我能用一句话复述核心结论吗？
4. **So What**: 每个章节结束后，我知道该想什么/做什么吗？
5. **Evidence**: 数据/引用有说服力吗？还是「听起来不错但缺乏证据」？
6. **Actionability**: 读完后，我能带走什么可行动的东西？

**Output Format**:
1. **Overall Impression** (1-2 sentences): 作为读者的第一反应
2. **Strengths**: 什么地方真正有价值
3. **Weaknesses**: 哪里让我困惑/不买账/觉得冗余
4. **Specific Suggestions**: 针对具体 section 的改进建议
5. **Missing Angles**: 我作为读者想知道但没讲到的
```

---

## 使用方法

1. **准备材料**：
   - 文本内容：大纲或内容（Markdown、Typst 或其他文本格式）
   - 或截图：用 `look_at` 工具查看 PDF 截图，提取内容后传给 Oracle
2. **填充模板**：替换 `{reader_description}`, `{goal}` 等占位符
3. **委托 Oracle**：`@oracle` + 完整 prompt
4. **处理反馈**：
   - 采纳合理建议
   - 对于不采纳的，记录原因（可能是读者理解有误，或约束条件不同）
5. **迭代验证**：重大修改后可再次审视

---

## Review Focus 详解

| Focus | 检查什么 | 常见问题 |
|-------|---------|---------|
| **Opening** | 开头能否吸引继续阅读 | Executive Summary 过于笼统、缺乏 hook |
| **Problem Definition** | 问题定义是否与读者共鸣 | 讲「我研究的」而非「他们关心的」 |
| **Logic Chain** | 论证链条是否清晰连贯 | 跳跃假设、MECE 不满足 |
| **So What** | 每章节结论是否明确 | 只陈述发现，不给出 implication |
| **Evidence** | 数据/引用是否有说服力 | 来源不权威、数据过时、cherry-picking |
| **Actionability** | 读者能带走什么 | 「有意思」但不知道 next step |

---

## 典型应用场景

| 场景 | Material | 重点关注 |
|------|----------|---------|
| 大纲审视（Phase 2.5） | Outline markdown | Opening, Problem Definition, Logic Chain |
| 内容审视（Phase 4.5） | 完整章节内容 | Evidence, So What, Actionability |
| 迭代困境 | 当前版本 + 改进困境说明 | Missing Angles, Specific Suggestions |

---

## Report vs Slide 的审视差异

| 维度 | Slide 审视 | Report 审视 |
|------|-----------|-------------|
| 受众模式 | 听众（被动接收、时间有限） | 读者（主动阅读、可回看） |
| 关注点 | Hook, Story Arc, Takeaway | Logic Chain, Evidence, Actionability |
| 信息密度 | 低（每页一个 point） | 高（需要完整论证） |
| 反馈侧重 | 「哪里让我走神」 | 「哪里让我困惑/不买账」 |
