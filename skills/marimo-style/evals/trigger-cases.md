# Trigger Cases

## Should Trigger

1. Help me write a marimo notebook for exploratory data analysis.

1. I want to turn this analysis into a lightweight interactive notebook without it becoming a complex app.

1. Optimize this marimo notebook's cell boundaries and UI density.

1. Refactor this EDA notebook so feature-selection plots show the evidence before manual exclusions.

1. Fix my marimo EDA notebook: `marimo check` reports duplicate definitions and a cyclic dependency.

1. Refactor this exploratory marimo notebook so cell outputs and exported names follow marimo graph rules.

1. 这个 marimo notebook 一个 cell 好像输出不对，帮我看下。

1. 帮我理一下这个 EDA notebook 的变量作用域和 cell 依赖。

1. 这个 EDA 太像 presentation/demo 了，帮我改回探索逻辑。

1. `mo.vstack` / `mo.ui` 是不是在这个 EDA 里用过了？

1. My marimo notebook errors because `slider.value` is read in the same cell where the slider is created.

1. Turn this finished EDA into a marimo report notebook for stakeholders.

1. 帮我写一个 marimo 报告 notebook，结论放前面，代码默认隐藏。

1. Should this be an EDA notebook or a report notebook? I need to share findings with my manager.

1. This report notebook walks the reader through every exploratory chart before the conclusion. Reorder it.

1. The report's summary at the top changes when a reader moves the threshold slider. Fix it.

1. 报告里这个筛选控件改的是下面很远的一张图，读者看不出来它影响了什么，帮我调整一下。

1. I want a report with a date filter that applies to the whole document. Where should it go?

1. Prepare this marimo report for sharing as HTML with working controls.

## Should Not Trigger

1. Help me build a complete frontend application.
1. Fix a pandas bug in an ordinary Python script.
1. Write a Jupyter tutorial.
1. Teach me the full marimo API.
1. Explain Python LEGB scoping in a script.
1. Turn this completed analysis into a polished multi-page dashboard for end users.
1. Connect to my running marimo session and add a cell that plots `df`. (Expected: marimo-pair)
1. Set this slider to 5 and rerun the dependent cells in the live notebook. (Expected: marimo-pair)
1. Format my notebook code with ruff and fix PEP 8 issues. (Expected: not this skill)
1. What is the right PEP 723 header for a marimo notebook, and how do I run it in script mode? (Expected: marimo-notebook)

## Near Neighbors

1. I have already decided to refactor the notebook into a formal module.
   Expected: no longer primarily depends on `marimo-style`
1. Add a new cell to my live notebook and make the EDA story order clean.
   Expected: marimo-pair for the mechanics, `marimo-style` for the story order
