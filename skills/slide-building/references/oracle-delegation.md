# Oracle Audience Review - Delegation Guide

委托 Oracle 扮演目标听众进行批判性审视。

## 核心价值

自己很难完全带入听众视角批判性审视。Oracle 扮演目标听众，提供「局外人」反馈。

| 自己审视 | Oracle 审视 |
|---------|------------|
| 已知所有背景，难以「假装不知道」 | 真正从零开始理解 |
| 倾向于认为自己的逻辑清晰 | 会指出跳跃/假设过多 |
| 容易忽略「专家盲区」 | 会问「这个术语什么意思」 |
| 情感上抗拒否定 | 客观批评，不留情面 |

**关键心态**：Oracle 的批评 = 真实听众可能的反应。不是「AI 不理解」，而是「如果听众也不理解怎么办」。

---

## Prompt Template

```markdown
## Task: Audience-Perspective Review

**Role**: 你是这个 slide 的目标听众 [{audience_description}]。

**Context**:
- 演讲目标: {goal}
- 时长: {duration}
- 听众背景: {audience_background}

**Material**:
{outline_or_content}

**Review Focus**:
1. **Hook**: 开头是否抓住我的注意力？我为什么要继续听？
2. **Pain Point**: 这个问题真的是我关心的吗？还是演讲者自己关心的？
3. **Story Arc**: 叙事主线清晰吗？我能用一句话复述核心信息吗？
4. **So What**: 每个部分结束后，我知道该想什么/做什么吗？
5. **Evidence**: 数据/案例有说服力吗？还是「听起来不错但缺乏证据」？
6. **Takeaway**: 听完后，我能带走什么可行动的东西？

**Output Format**:
1. **Overall Impression** (1-2 sentences): 作为听众的第一反应
2. **Strengths**: 什么地方真正吸引我
3. **Weaknesses**: 哪里让我走神/困惑/不买账
4. **Specific Suggestions**: 针对具体 page/section 的改进建议
5. **Missing Angles**: 我作为听众想知道但没讲到的
```

---

## 使用方法

1. **准备材料**：
   - 文本内容：大纲或内容（Markdown、Typst 或其他文本格式）
   - 或截图：用 `look_at` 工具查看 PDF 截图，提取内容后传给 Oracle
2. **填充模板**：替换 `{audience_description}`, `{goal}` 等占位符
3. **委托 Oracle**：`@oracle` + 完整 prompt
4. **处理反馈**：
   - 采纳合理建议
   - 对于不采纳的，记录原因（可能是听众理解有误，或约束条件不同）
5. **迭代验证**：重大修改后可再次审视

---

## Review Focus 详解

| Focus | 检查什么 | 常见问题 |
|-------|---------|---------|
| **Hook** | 开头 30 秒能否抓住注意力 | 背景铺垫过长、直接进技术细节 |
| **Pain Point** | 问题定义是否与听众共鸣 | 讲「我想讲的」而非「他们想听的」 |
| **Story Arc** | 叙事主线是否清晰连贯 | 功能罗列、各部分无因果关系 |
| **So What** | 每部分结论是否明确 | 只陈述事实，不引导思考 |
| **Evidence** | 数据/案例是否有说服力 | 空洞口号、缺乏具体数字 |
| **Takeaway** | 听众能带走什么 | 「很有意思」但不知道下一步 |

---

## 典型应用场景

| 场景 | Material | 重点关注 |
|------|----------|---------|
| 大纲审视（Phase 2.5） | Outline markdown | Hook, Pain Point, Story Arc |
| 内容审视（Phase 4.5） | 完整 slide 内容或 PDF 截图 | Evidence, So What, Takeaway |
| 迭代困境 | 当前版本 + 评分停滞说明 | Missing Angles, Specific Suggestions |
