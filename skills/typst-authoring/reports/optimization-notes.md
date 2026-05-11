# Optimization Notes

日期：2026-04-03

## 本轮判断

该 skill 入口已经足够轻，主要缺的是最小路由基线。

## 本轮动作

1. 新增 trigger cases
2. 记录当前状态，后续再决定是否补 execution eval

---

日期：2026-05-11

## 本轮判断

`references/report.md` 纯技术导向，缺乏实现层视觉护栏。当上游 skill 未指定具体视觉方向时，agent 容易自行发明不一致的品牌风格。

## 本轮优化动作

1. **`references/report.md`**：增加"实现层视觉护栏"章节
   - 排印层级保持：heading 与 body 字号比 ≥1.4×、间距梯度、全大写字距
   - 强调色纪律：accent 使用有限、语义色仅用于状态
   - 间距作为层级：章节间 > 节间 > 段间、标题"属于"后文
   - 不做的事：不发明品牌风格、不做叙事决策

## 参考来源

借鉴 nexu-io/open-design 的设计工艺规范，将 `craft/typography-hierarchy.md` 和 `craft/color.md` 的原则适配为 Typst 实现层护栏。

## 尚未解决的问题

1. 护栏规则尚无编译期或 lint 自动检查
2. 与 `report-building` skill 的 handoff 协议未形式化
