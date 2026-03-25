# Skills

Marketplace-managed skills for research, writing, slides, Typst authoring, and notebook prototyping.

A collection of Agent Skills for Claude Code that help you research, write, prototype exploratory notebooks, and create professional documents.

## Installation

### Install as Plugin

This installs the `skills` plugin from the `specter119-skills` marketplace, which bundles all skills in this repository.

```bash
# Add marketplace
/plugin marketplace add specter119/skills

# Install plugin
/plugin install skills@specter119-skills
```

### Local Development

For local iteration, clone the repo and validate the manifests before publishing updates:

```bash
git clone https://github.com/specter119/skills.git /tmp/skills
cd /tmp/skills
claude plugins validate .
./scripts/validate-skills.sh
```

如果你本地用 `jj` 管理变更，推荐在 clone 后启用 colocated 模式；远端仍然保持普通 Git 工作流：

```bash
git clone https://github.com/specter119/skills.git /tmp/skills
cd /tmp/skills
jj git init --colocate
jj bookmark track master --remote=origin
jj log
jj status
```

## Available Skills

| Skill | Description | Trigger Keywords |
|-------|-------------|------------------|
| **deep-research** | Deep research with multi-source synthesis | "调研", "研究", "深入了解" |
| **thorough-digest** | Exhaustive batch processing for local materials | "批量分析", "整理材料", "汇总这些" |
| **report-building** | Generate and structure professional reports | "报告", "report" |
| **slide-building** | Create presentation slides with Typst | "幻灯片", "slide", "演示" |
| **typst-authoring** | Typst authoring foundation layer | Used by slide-building/report-building |
| **genimg** | Generate images for content | "生成图片", "配图" |
| **marimo-eda-prototype** | Write EDA-first marimo notebooks with restrained UI and clear extraction boundaries | "marimo", "EDA notebook", "prototype-first" |
| **msgraph-fetch** | Unified Microsoft Graph fetch for SharePoint, OneDrive, and OneNote | "拉 SharePoint 文件", "同步 OneDrive", "拉取 onenote" |

## Usage

Skills are **model-invoked** - Claude automatically uses them based on your request. Just describe what you need:

```plain
帮我调研一下 A2A 协议的商业落地案例
```

Claude will automatically activate the `deep-research` skill.

## Requirements

- Claude Code >= 1.0.33
- For `genimg`: Requires API key configuration (see `genimg/.env.example`)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

[specter119](https://github.com/specter119)
