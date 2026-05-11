# Optimization Notes

日期：2026-04-03

## 本轮判断

`slide-building` 原始入口文件信息量很大，但存在 3 个主要问题：

1. 路由描述过泛，容易与 `report-building`、`typst-authoring`、`deep-research` 混淆
2. `SKILL.md` 过长，把路由、流程、知识库、代码样例混在一起
3. 缺少最小 eval，后续很难稳定迭代

## 本轮优化动作

1. 将入口改成“边界 + 执行骨架 + 输出契约 + 参考地图”
2. 把长文内容迁移到独立 `references/`
3. 新增 `evals/trigger-cases.md` 作为无 ground truth 场景下的最小基线
4. 对齐 `agents/openai.yaml` 的显示说明

## 参考来源

外部参考主要借鉴了 MiniMax `pptx-generator` 的三类做法：

1. 明确的 skill 边界与 quick reference
2. 把细节拆到 `references/` 而不是堆在入口
3. 先定义 slide/page type，再决定页面实现

## 尚未解决的问题

1. 还没有真实用户 prompt 回放，无法验证路由精度
2. 视觉参考仍偏“原则型”，后续可补更多真实案例
3. 还没有 execution eval，暂时只做 trigger 级别防回退

## 下一轮可选方向

1. 补真实 prompt 集，做一次 trigger 回放
2. 为不同 deck 类型补更多页面模式样例
3. 增加一个“implementation handoff 模板”，方便直接交给 `typst-authoring`

---

日期：2026-05-11

## 本轮判断

`design-system.md` 和 `review-and-qa.md` 的设计工艺指导偏基础，缺乏排印层级、色彩纪律和反 AI 默认值方面的结构化规则。

## 本轮优化动作

1. **`references/design-system.md`**：
   - 将"字体层级"升级为"排印层级"，增加层级行为（入口点、节奏、信息流）、五向量模型、三级工作模型和排印反模式
   - 将"语义色板"升级为"色彩纪律"，增加四层色板结构、强调色纪律（≤2 处/屏）、对比度门限、深色主题规则、反 AI 默认色
   - 增加"反 AI 默认值"章节（P0/P1/P2 分级）
   - 增加视觉节奏规则
   - 扩展常见失误列表

2. **`references/review-and-qa.md`**：增加 P0 交付门限（6 项可判定检查），在主观评审之前运行

## 参考来源

借鉴 nexu-io/open-design 的设计工艺规范，主要参考：
- `craft/typography-hierarchy.md`：排印层级行为与反模式
- `craft/color.md`：色板结构与强调色纪律
- `craft/anti-ai-slop.md`：P0/P1/P2 分级的反 AI 默认值规则

所有内容均为原则适配，未直接搬用 CSS/HTML 细节。

## 尚未解决的问题

1. P0 门限尚无自动化检查机制
2. 排印层级规则缺乏 Typst 代码示例
3. 反 AI 默认值规则的判定在部分边界情况下仍需人工判断
