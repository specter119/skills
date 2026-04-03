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
