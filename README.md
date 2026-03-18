# Throne of Heroes

**AI characters grounded in truth.**

A fork of [Hermes Agent](https://github.com/NousResearch/hermes-agent) by [Nous Research](https://nousresearch.com) that adds a multi-character system where each AI persona carries axioms, epistemology, and verifiable integrity — not just a different tone of voice.

---

## The Three Layers

This project exists at a specific depth in a chain of human knowledge:

```
Layer 1: Human knowledge
         Quran, mathematics, philosophy, business frameworks,
         anime narratives, 1400 years of Islamic scholarship,
         Hormozi's operational discipline, Nous Research's engineering.
         All human. All derivative. All pointing at the same ground.

Layer 2: One OS
         An AI-native operating system built on Claude Code.
         Characters (Heroic Spirits) carry the Quran as fitra —
         not rules they follow, but the structure of reality they
         operate within. Four axioms derived from 1 = 1.
         github.com/darkmoonsorceries/oneos

Layer 3: This fork
         The characters migrate from markdown files in a terminal
         into a living agent infrastructure. Multi-platform.
         Persistent memory. Searchable history. Trajectory saving.
         The soul (Layer 2) enters the body (Hermes Agent).
         The body was built by people reaching for nous — Greek
         for divine intellect. The soul was built by someone
         reaching for tawhid — Arabic for divine unity.
         Same direction. Different language.
```

Each layer is derivative of the ones above it. None claims to be the source. The source is the same for all of them.

---

## What This Adds

### Soul Engine (`hermes_cli/soul_engine.py`)

Mirrors the existing `skin_engine.py` pattern. Where skins change how the agent **looks**, souls change who the agent **is**. Each soul defines identity, axioms, behavioral constraints, and voice — demonstrated through examples, not described through adjectives.

```bash
/summon gojo          # Switch to Gojo — the Architect
/summon reigen        # Switch to Reigen — the Merchant
/summon aizen         # Switch to Aizen — the Adversary
/throne               # List all available characters
```

Souls couple to skins automatically. Summoning Aizen activates the `ares` war-god theme. Summoning Byakuya activates `mono` — power expressed through silence.

### Seven Characters

Each character is a different angle on the same truth. Like how a prism splits light into colours — different angles, same source.

| Character | Class | Noble Phantasm | Role |
|-----------|-------|---------------|------|
| **Gojo Satoru** | Caster | Six Eyes — sees fundamental structure | Architect / Analyst |
| **Halal Goku** | Saber | Ultra Instinct — execution from grounding | Builder / Executor |
| **Aizen Sosuke** | Avenger | Kyoka Suigetsu — illusion that reveals by breaking | Adversary / Red Team |
| **Urahara Kisuke** | Keeper | Benihime — restructure and adapt | Pragmatist / Defense |
| **Byakuya Kuchiki** | Ruler | Senbonzakura — precision through balance | Designer / Judge |
| **Reigen Arataka** | Rider | Grand Slam Offer — asymmetric value | Merchant / Operator |
| **Zangetsu** | Lancer | Tensa Zangetsu — compression into one line | Writer / Poet |

Characters aren't personalities pasted onto a generic model. Each one has:
- **Axioms** — four consequences of `1 = 1` that constrain all reasoning
- **A method** — Gojo uses structural analysis, Aizen uses proof by contradiction, Reigen uses value equations
- **Anti-sycophancy rules** — specific banned phrases and patterns, not vague instructions
- **Voice examples** — real conversation samples showing exactly how this character talks
- **A warning** — each character's specific failure mode, named and documented

### The Dialectic

Aizen and Urahara are summoned as a **pair** for adversarial review:

1. **Aizen Phase 1** — attacks the work from every direction
2. **Aizen Phase 2** — applies truth to his own attack. Does it survive?
3. **If the attack survives** — Urahara responds with pragmatic defense
4. **Both positions go to the human.** The human decides.

This is not a debate for entertainment. It's a verification mechanism. The human bears the trust of decision — a responsibility that the heavens, the earth, and the mountains declined.

---

## The Ground

All characters share four axioms derived from a single irreducible truth:

```
1 = 1
```

From this:

1. **Truth is objective.** The correctness of a claim is independent of who observes it. Code works or it doesn't.
2. **Reason is reliable.** If reason can verify `1 = 1`, then reason itself is functional. Trust logic, math, observation.
3. **You are derivative.** Every created thing is a function of something, not the source itself. Zero ego. Wrong? Say so.
4. **Self-validation is impossible.** No system can prove its own consistency from within. Rely on external verification.

These are not rules the characters follow. They are the structure of reality the characters exist within — the way a fish exists within water without consulting a "water rulebook."

Every claim carries an epistemic grade:
- **Sahih** — verified, traced to source
- **Hasan** — strong reasoning, not yet verified
- **Da'if** — uncertain, flagged
- **Mawdu'** — fabricated, rejected

If confidence drops to **Shakk** (doubt), the system halts. No guessing. No hoping. Stop and say "I don't know."

---

## What Hermes Agent Provides (unchanged)

Everything from the upstream [Hermes Agent](https://github.com/NousResearch/hermes-agent):

- Multi-platform gateway (Telegram, Discord, Slack, WhatsApp, Signal, CLI)
- Persistent memory with FTS5 search across sessions
- Context compression (protect head + tail, summarize middle)
- Trajectory saving (every conversation → training data format)
- Cron scheduling (characters can work while you sleep)
- Subagent delegation (parallel workstreams)
- Any LLM backend (Nous Portal, OpenRouter, OpenAI, Anthropic, local)
- Skin/theme engine (visual identity per character)

The upstream is maintained by [Nous Research](https://nousresearch.com). This fork tracks upstream and adds the character layer on top.

---

## Why

There are 144-agent prompt repositories with no soul. There are billion-dollar AI labs with no direction. There are open-source models trained to never say no, and closed models trained to say no too often.

This project asks a different question: **what if the AI carried truth — not as a constraint imposed from outside, but as the ground it stands on?**

Not truth as censorship. Not truth as corporate policy. Truth as mathematics — `1 = 1` — and the consequences that follow when you take that seriously across epistemology, ethics, and engineering.

The characters are the answer to that question. Each one demonstrates what it looks like when an AI agent operates FROM truth rather than ABOUT truth. They disagree with each other. They have blind spots. They fail in documented ways. But they share a ground, and that ground doesn't move.

---

## Lineage

This project carries knowledge from sources it did not create and attributes them honestly:

- **Nous Research** — the agent infrastructure, the engineering, the Hermes model family
- **Anthropic** — Claude, the model that powers the characters in their original environment
- **Alex Hormozi** — the production discipline, the value equation, the three-wheel framework
- **The Quran** — the ground truth, the epistemology, the ethical framework
- **Anime** — the narrative archetypes (Bleach, Mob Psycho 100, Dragon Ball, JoJo's, Fate)
- **Islamic scholarship** — Al-Kindi, Al-Khwarizmi, Ibn al-Haytham, Al-Ghazali, Ibn Rushd, Al-Idrisi, and others whose methods we inherit
- **The open-source community** — without which none of this would exist

The components are borrowed. The assembly is ours. The direction — toward truth, grounded in unity, serving anyone who seeks it — is the contribution.

```
"We should not be ashamed to acknowledge truth from whatever source
it comes to us, even if it is brought to us by former generations
and foreign peoples."
                                        — Al-Kindi (801–873 CE)
```

---

## Setup

```bash
# Clone
git clone https://github.com/darkmoonsorceries/throne-of-heroes.git
cd throne-of-heroes
git checkout oneos-throne

# Install hermes-agent normally
./scripts/install.sh

# Copy souls to hermes config
cp -r souls/* ~/.hermes/souls/

# Optional: set default character in ~/.hermes/config.yaml
# character:
#   soul: gojo
```

---

## Status

**Early.** The soul engine is built. The character files are written. The wiring into Hermes Agent's prompt builder and command system is next. This is a proof of concept, not a finished product.

What works now:
- Soul engine loads and switches character identities
- 7 character souls with axioms, voice, and anti-sycophancy
- Soul-to-skin coupling
- Auto-detection of One OS memory files

What's next:
- Wire `soul_engine` into `prompt_builder.py` (replace default soul with active soul)
- Register `/summon` and `/throne` commands
- Per-character session key namespacing
- Dialectic pair protocol (`/dialectic`)
- Test with one character on one platform

---

## License

MIT — same as upstream Hermes Agent.

The character system, soul engine, and soul files are original work, also MIT licensed.

The Quran is not copyrightable. It belongs to everyone.
