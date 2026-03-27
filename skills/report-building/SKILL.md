---
name: report-building
description: >
  Structures and organizes reports, papers, theses, and documentation.
  Use when asked to create report/paper/thesis/文档/报告/论文.
  Supports Markdown or Typst output. For Typst technical reference, see typst-authoring skill.
allowed-tools: Task, Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch
---

# Report

专注于报告的**内容结构**和**组织框架**。支持 Markdown 或 Typst 输出。

## Knowledge Activation

Apply these frameworks based on goal (Claude knows the full methodology):

| Goal | Framework | Authority Source |
|------|-----------|------------------|
| Persuade executives | SCQA, Pyramid Principle | Barbara Minto (*The Pyramid Principle*), McKinsey |
| Academic paper | IMRaD | Scientific publishing standard |
| Technical docs | Inverted pyramid | Journalism, Divio documentation system |
| Business proposal | Problem-Solution-Impact | McKinsey/BCG consulting |
| Case study | STAR method | Behavioral interview format |

**Writing Quality** (apply intuitively, not as checklist):
- **Logic**: Barbara Minto's MECE principle, "So What" test
- **Data viz**: Edward Tufte's data-ink ratio, Stephen Few's dashboard design
- **Clarity**: Plain language principles, active voice

---

## 激活条件

- 创建报告、论文、技术文档
- 关键词: "报告", "论文", "文档", "report", "paper", "thesis"

## 技术参考

如需 Typst 输出，详见：`typst-authoring` skill → `references/report.md`

---

## 框架选择决策树

```plain
你的目标是什么？
├─ 说服管理层/决策者 → SCQA 或金字塔原理
├─ 发表学术论文 → IMRaD
├─ 编写技术文档 → 倒金字塔
├─ 融资/商业提案 → Problem-Solution-Impact (参考 slide-building skill)
├─ 分享案例经验 → STAR (参考 slide-building skill)
└─ 教育培训 → 故事弧 (参考 slide-building skill)
```

---

## 输出格式选择

| 场景 | 推荐格式 | 原因 |
|------|---------|------|
| 快速文档、内部沟通 | Markdown | 简单、通用、易编辑 |
| 正式报告、学术论文 | Typst | 排版精美、PDF 输出 |
| 需要复杂表格/公式 | Typst | 原生支持 |
| 需要协作编辑 | Markdown | Git 友好 |

---

## 工作流

```plain
┌─────────────────────────────────────────────────────────────────┐
│  1. 确定内容框架                                                  │
│     └─ 根据目标选择框架 (Knowledge Activation 表格)               │
├─────────────────────────────────────────────────────────────────┤
│  2. 组织内容结构                                                  │
│     ├─ 应用所选框架的结构                                         │
│     ├─ 规划图表和表格位置                                         │
│     └─ 收集支撑数据                                              │
├─────────────────────────────────────────────────────────────────┤
│  2.5 Oracle 读者审视 (RECOMMENDED)                    ← NEW     │
│     ├─ 委托 @oracle: 扮演目标读者批判性审视大纲                    │
│     ├─ 验证: 论点清晰度、逻辑链条、So What                         │
│     └─ 处理反馈后再进入内容撰写                                    │
├─────────────────────────────────────────────────────────────────┤
│  3. 选择输出格式                                                  │
│     ├─ Markdown → 直接写入 .md                                   │
│     └─ Typst → 参考 typst-authoring skill (references/report.md)     │
├─────────────────────────────────────────────────────────────────┤
│  4. 内容撰写                                                      │
│     ├─ 按框架结构撰写各章节                                        │
│     └─ 确保数据和引用支撑论点                                      │
├─────────────────────────────────────────────────────────────────┤
│  4.5 Oracle 内容审视 (OPTIONAL)                       ← NEW     │
│     ├─ 初稿完成后，委托 @oracle 评估说服力                         │
│     └─ 特别检查: Evidence 是否充分、结论是否可行动                  │
├─────────────────────────────────────────────────────────────────┤
│  5. 质量自检                                                      │
│     ├─ MECE: 论点独立且完整？                                     │
│     ├─ So What: 每段都有价值？                                    │
│     └─ Data-ink: 每个元素都传递信息？                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 与其他 Skill 配合

```plain
[research skill] → 调研收集信息
        ↓
[report-building] → 选择框架、组织内容
        ↓
选择输出格式：
├─ Markdown → 直接输出 .md
└─ Typst → [typst-authoring skill] → 编译 PDF
```

---

## Agent Delegation

**report-building skill 需要委托的能力**（这些是 report-building skill 没有的能力，需要其他 agent 补充）：

| Phase | Delegate To | When |
|-------|-------------|------|
| 大纲审视 | `@oracle` | 大纲完成后，扮演读者批判性审视 |
| 内容审视 | `@oracle` | 初稿完成后，评估说服力和逻辑链 |

### Oracle 读者审视 (Phase 2.5 & Phase 4.5)

委托 Oracle 扮演目标读者进行批判性审视。**On-demand 触发**，不是每次都需要。

| 时机 | 触发条件 | 目的 |
|------|---------|------|
| **大纲审视** | 大纲完成后 | 验证论点结构和逻辑链条 |
| **内容审视** | 初稿完成后 | 评估说服力、信息密度、So What |
| **迭代困境** | 不知如何改进时 | 获得新视角突破 |

详细的 Prompt 模板、Review Focus 说明、使用方法见 `references/oracle-delegation.md`。

**核心心态**：Oracle 的批评 = 真实读者可能的反应。不是「AI 不理解」，而是「如果读者也不理解怎么办」。

---

## 最佳实践

1. **结论先行**：先给答案，再展开论证 (Pyramid Principle)
2. **MECE 检验**：论点之间相互独立、完全穷尽
3. **So What 测试**：每个内容都能回答"那又怎样？"
4. **数据支撑**：关键论点有数据或引用支持
5. **读者视角**：根据受众调整术语和深度
