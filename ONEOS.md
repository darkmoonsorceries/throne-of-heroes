# One OS Integration for Hermes Agent

This fork adds the Throne of Heroes character system to Hermes Agent.

## What Was Added

### Soul Engine (`hermes_cli/soul_engine.py`)
Mirrors `skin_engine.py`. Loads character souls from:
1. `~/.hermes/souls/<name>/SOUL.md` (user souls on disk)
2. One OS `memory/<name>/MEMORY.md` (auto-detected via CLAUDE.md)
3. Built-in default (hermes)

Each soul couples to a skin for visual identity.

### Character Souls (`souls/`)
7 characters from the Throne of Heroes, each with SOUL.md:

| Soul | Class | Role | Skin |
|------|-------|------|------|
| `gojo` | Caster | Architect / Analyst | slate |
| `goku` | Saber | Orchestrator / Builder | default |
| `aizen` | Avenger | Adversary / Red Team | ares |
| `urahara` | Keeper | Pragmatist / Defense | default |
| `byakuya` | Ruler | Designer / Judge | mono |
| `reigen` | Rider | Merchant / Operator | default |
| `zangetsu` | Lancer | Writer / Poet | mono |

### New Commands
- `/summon <name>` — switch to a character soul
- `/throne` — list available characters
- `/dialectic` — summon Aizen + Urahara pair for adversarial review

### Axiom Ground
All characters share four axioms derived from 1=1 (Tawhid):
1. Truth is objective
2. Reason is reliable
3. You are derivative
4. Self-validation is impossible

### What Was NOT Changed
- No modifications to existing hermes-agent code
- All additions are new files
- The default `hermes` soul works exactly as before
- Character system is opt-in via `/summon` or `character.soul` config

## Setup

```bash
# Copy souls to hermes config
cp -r souls/* ~/.hermes/souls/

# Set default character in config.yaml
# character:
#   soul: gojo
```

## Usage

```
/summon gojo          # Switch to Gojo (Architect)
/summon reigen        # Switch to Reigen (Merchant)
/throne               # List all available characters
/dialectic            # Summon Aizen + Urahara pair
```
