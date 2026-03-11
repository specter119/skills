# Craft Skills

Craft your insights into content with marketplace-managed research, writing, slides, and Typst authoring skills.

A collection of Agent Skills for Claude Code that help you research, write, and create professional documents.

## Installation

### Install as Plugin

This installs the `skills` plugin, which bundles all skills in this repository.

```bash
# Add marketplace
/plugin marketplace add specter119/craft-skills

# Install plugin
/plugin install skills@craft-skills
```

### Local Development

For local iteration, clone the repo and validate the manifests before publishing updates:

```bash
git clone https://github.com/specter119/craft-skills.git /tmp/craft-skills
cd /tmp/craft-skills
claude plugins validate .
./scripts/validate-skills.sh
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
| **onenote-wiki** | Sync and convert OneNote wiki pages | "拉取 onenote", "同步 wiki" |

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
