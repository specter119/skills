# Workflow

## 核心循环

```plain
1. Write or inspect Typst code
2. Run tinymist diagnostics
3. Fix errors with hover / definition as needed
4. Compile to PDF / PNG
5. Verify page count and rendered output
```

## 常用命令

```bash
typst compile input.typ output.pdf
typst watch input.typ output.pdf
typst init @preview/package-name name
typst compile --format png input.typ output-{0p}.png
```

## 输出检查

- `pdfinfo`：检查页数
- `pdftoppm`：导出截图做视觉检查

## 版本管理

Typst package 需要固定版本。

建议：

- 优先查最新文档或 Universe 信息
- 不确定时不要直接沿用旧版本号

## 图形方案选择

- 简单 flowchart：优先 `diagraph`
- nested containers：考虑 `D2`
- sequence / gantt / pie：考虑 `oxdraw`
