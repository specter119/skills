# 提示增强指南

## 原理
Gemini 图像模型更擅长理解富叙述性的描述，简单关键词往往达不到最佳效果。因此要用 50~150 字的段落，把主体、动作、场景、光线、构图与风格串成一个小故事。

## 关键元素
| 元素 | 说明 | 示例 |
|------|------|------|
| 主体 | 明确主角是谁 | "带着蓝色光学器的机器人咖啡师" |
| 动作 | 主体在干什么 | "在未来咖啡馆里冲咖啡" |
| 场景 | 环绕环境 | "未来主义咖啡馆" |
| 光线 | 光源性质与方向 | "上方霓虹管投下柔和环境光" |
| 技术 | 镜头/质量/景深等 | "浅景深，4K 质感" |
| 风格 | 与 `-s` 对应的整体调性 | "现代科技美学" |

## 自动补充规则
- 未显式请求文字则补 `-n "text, words, letters, labels"`。
- 根据 `-s` 风格参数，加入对应描述。
- 根据场景类型补充适当光影与构图建议。

## 示例
用户输入：
```plain
画一个 A2A 协议的概念图，要有科技感
```

增强后：
```plain
An isometric 3D illustration depicting the A2A protocol concept. Multiple AI agents represented as glowing geometric nodes connected by flowing data streams. Clean, modern tech aesthetic with blue accent lighting. Soft diffused top-down lighting creates depth. Professional, corporate style suitable for technical presentation. Sharp focus, high quality rendering.
```

## 编辑模式提示
修改已有图像时，把用户修改指令扩展为：
```plain
Adjust the lighting to warmer tones. Add golden hour warmth with soft orange highlights. Maintain the original composition and subject placement. Keep all other elements unchanged.
```

## 执行建议
- 先用 Flash 模型快速探索，再用 Pro 模型精修。
- 需要对比时用 `--variants` + `--grid` 自动生成多图格。详细 CLI 操作参见 `references/cli-workflow.md`。

## 视觉反默认值

AI 图像模型有自己的"默认审美"。以下模式不是禁止使用，而是不应无意识地默认产出：

### 避免默认产出

- **蓝紫科技渐变背景**——模型偏爱 indigo→cyan、purple→blue 的"信任感"渐变。如果用户没有要求渐变，默认用纯色或自然光照。
- **悬浮抽象几何体**——发光的立方体、球体、六边形网格没有语义内容。如果概念图需要形状，让形状承载含义。
- **假 UI / 假仪表盘**——模型生成的界面元素通常文字不可读且布局不合理。需要 UI 截图时用真实截图或代码生成。
- **过度发光和光晕**——lens flare、neon glow、光线粒子。适量用于科幻风格，但不应成为每张图的默认效果。

### 参考负向提示

当检测到上述默认倾向时，可追加负向提示：

```plain
-n "generic gradient background, floating abstract shapes, fake UI elements, lens flare, glowing particles"
```

注意：如果用户明确要求某种风格（如"科幻风格的发光节点"），则尊重用户意图，不添加该类型的负向提示。

### 判断标准

问自己：去掉这个视觉元素后，图片的核心信息是否改变？如果不变，这个元素大概率是模型的默认填充而非设计选择。
