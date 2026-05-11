# Optimization Notes

日期：2026-04-03

## 本轮判断

原 `genimg` 入口把 prompt 方法论、CLI 手册、slides 集成、模型选择全堆在一起，入口过重且边界不够清晰。

## 本轮动作

1. 将 `SKILL.md` 收缩为边界、执行骨架和参考地图
2. 保留已有的 prompt 增强说明，迁移 CLI 细节到 `references/cli-workflow.md`
3. 新增最小 trigger cases，给后续路由回归提供基线

## 后续可补

1. 增加 execution eval，例如单图生成、编辑模式、variants 三类场景
2. 为常见风格沉淀更多 prompt recipe

---

日期：2026-05-11

## 本轮判断

`prompt-enhancement.md` 缺乏对 AI 图像模型默认审美倾向的引导，容易产出"通用 AI 风格"的图片。

## 本轮优化动作

1. **`references/prompt-enhancement.md`**：增加"视觉反默认值"章节
   - 列出 4 类常见 AI 图像默认模式（蓝紫渐变、悬浮几何体、假 UI、过度发光）
   - 提供参考负向提示模板
   - 明确区分"用户要求 = 尊重"vs"模型默认 = 避免"
   - 增加判断标准（去掉视觉元素后核心信息是否改变）

## 参考来源

借鉴 nexu-io/open-design `craft/anti-ai-slop.md` 的反 AI 默认值思路，适配到图像生成场景。

## 尚未解决的问题

1. 缺乏真实 prompt + 输出样本的对比案例
2. 不同风格参数下的反默认规则可能需要差异化
