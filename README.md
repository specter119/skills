# Skills

A collection of AI agent skills for research, writing, presentations, notebook prototyping, and related content workflows. Skills follow the [agentskills.io](https://agentskills.io) specification and can be used with any compatible agent host.

## Installation

### Claude Code (via Marketplace)

```bash
# Add marketplace
/plugin marketplace add specter119/skills

# Install plugin
/plugin install skills@specter119-skills
```

## Available Skills

| Skill                    | Description                                                                         |
| ------------------------ | ----------------------------------------------------------------------------------- |
| **deep-research**        | Deep research with multi-source synthesis                                           |
| **thorough-digest**      | Exhaustive batch processing for local materials                                     |
| **report-building**      | Generate and structure professional reports                                         |
| **slide-building**       | Create presentation slides with Typst                                               |
| **typst-authoring**      | Typst authoring foundation layer (used by slide-building / report-building)         |
| **genimg**               | Generate images for content                                                         |
| **marimo-eda-prototype** | Write EDA-first marimo notebooks with restrained UI and clear extraction boundaries |
| **msgraph-explore**      | Search, fetch, and sync Microsoft Graph content (SharePoint, OneDrive, OneNote)     |
| **skill-craft**          | Create, refactor, evaluate, and package agent skills                                |
| **jj**                   | jj (Jujutsu) version control with pre-push hook integration                         |

## Usage

Skills are **model-invoked** -- the agent automatically activates them based on your request. Just describe what you need:

```text
Research the commercial adoption of the A2A protocol.
```

## Requirements

- For `genimg`: Requires API key configuration (see `genimg/.env.example`)

## Acknowledgments

- **jj** is based on [onevcat-jj](https://github.com/nicepkg/skills/tree/main/skills/onevcat-jj) by onevcat, modified to use `jj push` (jj-pre-push alias) instead of `jj git push`.
- **skill-craft** is based on [yao-meta-skill](https://github.com/nicepkg/skills/tree/main/skills/yao-meta-skill) by Yao Team, adapted for waza spec compliance. Structure influenced by [microsoft/waza](https://github.com/microsoft/waza/tree/main/skills).

## License

MIT License -- see [LICENSE](LICENSE) for details.
