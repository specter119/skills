# Skills

A small collection of AI agent skills. Skills follow the [agentskills.io](https://agentskills.io) specification and can be used with any compatible agent host.

## Installation

### Claude Code (via Marketplace)

```bash
# Add marketplace
/plugin marketplace add specter119/skills

# Install plugin
/plugin install skills@specter119-skills
```

## Active Skills

| Skill            | Description                                                                                           |
| ---------------- | ----------------------------------------------------------------------------------------------------- |
| **marimo-style** | Notebook style for marimo: discovery-first EDA and conclusion-first report with its own control rules |
| **jj**           | jj (Jujutsu) version control with pre-push hook integration                                           |

`marimo-style` covers the purpose-driven shape of a notebook only. It is meant to sit beside two official skills: [marimo-pair](https://github.com/marimo-team/marimo-pair) for driving a live kernel (running code, editing cells, setting widgets, packages) and [marimo-notebook](https://github.com/marimo-team/skills/tree/main/skills/marimo-notebook) for the file format and API. Install them alongside:

```bash
npx skills add marimo-team/skills
npx skills add marimo-team/marimo-pair
```

## Archived Skills

Low-frequency skills live in [`.archived/`](.archived), outside `skills/`, so they are not listed in the marketplace, not picked up by [skm](https://github.com/specter119/skm), not validated by the repo scripts, and not actively maintained. To revive one, move it into `skills/` and register it in `.claude-plugin/marketplace.json`.

| Skill               | Description                                                                     |
| ------------------- | ------------------------------------------------------------------------------- |
| **deep-research**   | Deep research with multi-source synthesis                                       |
| **thorough-digest** | Exhaustive batch processing for local materials                                 |
| **report-building** | Generate and structure professional reports                                     |
| **slide-building**  | Create presentation slides with Typst                                           |
| **typst-authoring** | Typst authoring foundation layer (used by slide-building / report-building)     |
| **genimg**          | Generate images for content (needs API key, see `genimg/.env.example`)          |
| **msgraph-explore** | Search, fetch, and sync Microsoft Graph content (SharePoint, OneDrive, OneNote) |
| **skill-craft**     | Create, refactor, evaluate, and package agent skills                            |

## Usage

Skills are **model-invoked**: the agent activates them based on your request. Just describe what you need:

```text
Turn this analysis into a marimo report notebook for stakeholders.
```

## Acknowledgments

- **jj** is based on [onevcat-jj](https://github.com/nicepkg/skills/tree/main/skills/onevcat-jj) by onevcat, modified to use `jj push` (jj-pre-push alias) instead of `jj git push`.
- **marimo-style** builds on [marimo-pair](https://github.com/marimo-team/marimo-pair) by the marimo team for live-kernel interaction.
- Archived **skill-craft** is based on [yao-meta-skill](https://github.com/nicepkg/skills/tree/main/skills/yao-meta-skill) by Yao Team, adapted for waza spec compliance. Structure influenced by [microsoft/waza](https://github.com/microsoft/waza/tree/main/skills).

## License

MIT License -- see [LICENSE](LICENSE) for details.
