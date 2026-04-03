# Review And QA

slide 的质量必须看渲染结果，不能只看源码。

## 1. 先做结构检查

Typst / Touying 文字溢出常常不会报错，但会静默多出一页。

建议先检查：

```bash
grep -c "^==+ " slide.typ
pdfinfo slide.pdf | grep Pages
pdftotext slide.pdf - | head -200
```

如果预期页数和实际页数不一致，先修结构问题，再谈美学。

## 2. 再做渲染审阅

```bash
pdftoppm -png -r 150 slide.pdf /tmp/review/page
```

逐页检查：

- 视觉重心是否稳定
- 留白是否有意义
- 连续翻 5 页是否有节奏变化
- 投影时是否一眼知道最重要的信息

## 3. 四个核心测试

### Squint Test

眯眼后还能先看到最重要的信息吗？

### Whitespace Test

留白是为了强调，还是只是内容太空？

### Rhythm Test

连续页面是否有结构变化，还是每页都像复制粘贴？

### So What Test

读完这页，听众是否知道该怎么理解或采取什么行动？

## 4. 评分框架

每项 1-10 分：

| 维度 | 问题 |
| --- | --- |
| Narrative Structure | 主线是否清晰，part 之间是否有因果关系 |
| Information Density | 是否有数字、对比、场景，而不是泛泛描述 |
| Visual Rhythm | 连续页面是否有变化 |
| So What | 每页是否有明确 takeaway |
| Domain-Specific Value | 是否真正服务于该主题的判断或决策 |

建议目标：

- 每轮至少提升 3 分
- 总分达到 42/50 后再视作可交付版本

## 5. 经验分享类的特别检查

必须回答：

1. 遇到了什么问题
2. 怎么解决
3. 效果如何
4. 听众如何复用

如果整套 deck 只有“功能介绍”，那通常更像文档，不像分享。

## 6. 何时请外部评审

- 大纲冻结前，请 `@oracle` 审主线和痛点
- 内容初稿后，请 `@oracle` 审证据和说服力
- 视觉评分停滞时，请 `@frontend-ui-ux-engineer` 审投影效果
