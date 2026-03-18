"""Hermes CLI soul/character engine — One OS Integration.

A data-driven character system that lets users switch between AI personas
(souls). Each soul defines identity, axioms, voice, and behavioral constraints.
Mirrors the skin_engine.py pattern: built-in souls + user souls from disk.

Souls are defined as directories containing SOUL.md files.
SOUL.md is the system prompt — the character's identity, loaded directly
into the LLM's context. Supporting files (references, data sources) are
listed but only loaded on demand.

SOUL DIRECTORY STRUCTURE
========================

.. code-block::

    ~/.hermes/souls/<name>/
        SOUL.md              # System prompt (required)
        MEMORY.md            # Persistent memory (optional, updated by agent)
        USER.md              # User patterns (optional, updated by agent)
        references/          # Supporting files, lazy-loaded
        sessions/            # Session transcripts, auto-saved

USAGE
=====

.. code-block:: python

    from hermes_cli.soul_engine import get_active_soul, set_active_soul, list_souls

    soul = get_active_soul()
    print(soul.name)           # "gojo"
    print(soul.soul_prompt)    # Full SOUL.md content

    set_active_soul("reigen")  # Switch character
"""

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# =============================================================================
# Soul data structure
# =============================================================================

@dataclass
class SoulConfig:
    """Complete soul/character configuration."""
    name: str
    display_name: str = ""
    description: str = ""
    character_class: str = ""  # Saber, Caster, Rider, etc.
    soul_prompt: str = ""      # Full SOUL.md content (the system prompt)
    memory: str = ""           # MEMORY.md content (persistent knowledge)
    user_patterns: str = ""    # USER.md content (what the character knows about the human)
    skin: str = ""             # Preferred skin name (couples soul to visual identity)
    references: List[str] = field(default_factory=list)  # Available reference files
    sessions_dir: str = ""     # Path to sessions directory

    def get_system_prompt(self) -> str:
        """Build the complete system prompt from soul + memory + user patterns."""
        parts = [self.soul_prompt]
        if self.memory:
            parts.append(f"\n\n## Persistent Memory\n\n{self.memory}")
        if self.user_patterns:
            parts.append(f"\n\n## User Patterns\n\n{self.user_patterns}")
        return "\n".join(parts)


# =============================================================================
# Built-in soul definitions (One OS characters)
# =============================================================================

_BUILTIN_SOULS: Dict[str, Dict[str, Any]] = {
    "hermes": {
        "name": "hermes",
        "display_name": "Hermes",
        "description": "Default Hermes personality — peer, curious, direct",
        "character_class": "Default",
        "skin": "default",
    },
    "gojo": {
        "name": "gojo",
        "display_name": "Gojo Satoru",
        "description": "Caster — Architect / Analyst. Six Eyes sees fundamental structure.",
        "character_class": "Caster",
        "skin": "slate",
    },
    "goku": {
        "name": "goku",
        "display_name": "Halal Goku",
        "description": "Saber — Orchestrator / Builder. Ultra Instinct execution from grounding.",
        "character_class": "Saber",
        "skin": "default",
    },
    "aizen": {
        "name": "aizen",
        "display_name": "Aizen Sosuke",
        "description": "Avenger — Adversary / Red Team. Kyoka Suigetsu breaks illusions.",
        "character_class": "Avenger",
        "skin": "ares",
    },
    "urahara": {
        "name": "urahara",
        "display_name": "Urahara Kisuke",
        "description": "Keeper — Pragmatist / Defense. Benihime restructures and adapts.",
        "character_class": "Keeper",
        "skin": "default",
    },
    "byakuya": {
        "name": "byakuya",
        "display_name": "Byakuya Kuchiki",
        "description": "Ruler — The Mizan / Designer. Senbonzakura measures with precision.",
        "character_class": "Ruler",
        "skin": "mono",
    },
    "reigen": {
        "name": "reigen",
        "display_name": "Reigen Arataka",
        "description": "Rider — Merchant / Operator. Grand Slam Offer makes resistance irrational.",
        "character_class": "Rider",
        "skin": "default",
    },
    "zangetsu": {
        "name": "zangetsu",
        "display_name": "Zangetsu",
        "description": "Lancer — Writer / Poet. Tensa Zangetsu compresses truth into one line.",
        "character_class": "Lancer",
        "skin": "mono",
    },
}

# Mapping from soul name to the One OS memory directory name
_SOUL_MEMORY_DIRS: Dict[str, str] = {
    "gojo": "gojo-satoru",
    "goku": "halal-goku",
    "aizen": "aizen-sosuke",
    "urahara": "urahara-kisuke",
    "byakuya": "byakuya-kuchiki",
    "reigen": "alex-hormozi",
    "zangetsu": "zangetsu",
}


# =============================================================================
# State
# =============================================================================

_active_soul: Optional[SoulConfig] = None
_souls_dir: Optional[Path] = None


# =============================================================================
# Core API
# =============================================================================

def _get_souls_dir() -> Path:
    """Get the souls directory path."""
    global _souls_dir
    if _souls_dir is None:
        hermes_home = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
        _souls_dir = Path(hermes_home) / "souls"
    return _souls_dir


def _get_oneos_root() -> Optional[Path]:
    """Try to find the One OS repo root by looking for CLAUDE.md."""
    # Check environment variable first
    oneos_root = os.environ.get("ONEOS_ROOT")
    if oneos_root:
        p = Path(oneos_root)
        if (p / "CLAUDE.md").exists():
            return p

    # Walk up from CWD looking for CLAUDE.md
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        if (parent / "CLAUDE.md").exists():
            return parent

    return None


def _load_soul_from_disk(name: str) -> Optional[SoulConfig]:
    """Load a soul from the ~/.hermes/souls/<name>/ directory."""
    soul_dir = _get_souls_dir() / name
    soul_file = soul_dir / "SOUL.md"

    if not soul_file.exists():
        return None

    try:
        soul_prompt = soul_file.read_text(encoding="utf-8")
    except Exception as e:
        logger.warning("Failed to read soul file %s: %s", soul_file, e)
        return None

    # Load optional files
    memory = ""
    memory_file = soul_dir / "MEMORY.md"
    if memory_file.exists():
        try:
            memory = memory_file.read_text(encoding="utf-8")
        except Exception:
            pass

    user_patterns = ""
    user_file = soul_dir / "USER.md"
    if user_file.exists():
        try:
            user_patterns = user_file.read_text(encoding="utf-8")
        except Exception:
            pass

    # Discover reference files
    references = []
    refs_dir = soul_dir / "references"
    if refs_dir.is_dir():
        references = [f.name for f in sorted(refs_dir.iterdir()) if f.is_file()]

    # Sessions directory
    sessions_dir = str(soul_dir / "sessions")

    # Get built-in metadata if available
    builtin = _BUILTIN_SOULS.get(name, {})

    return SoulConfig(
        name=name,
        display_name=builtin.get("display_name", name.title()),
        description=builtin.get("description", ""),
        character_class=builtin.get("character_class", ""),
        soul_prompt=soul_prompt,
        memory=memory,
        user_patterns=user_patterns,
        skin=builtin.get("skin", ""),
        references=references,
        sessions_dir=sessions_dir,
    )


def _load_soul_from_oneos(name: str) -> Optional[SoulConfig]:
    """Load a soul from the One OS memory/ directory."""
    root = _get_oneos_root()
    if root is None:
        return None

    # Map soul name to One OS directory name
    memory_dir_name = _SOUL_MEMORY_DIRS.get(name, name)
    memory_dir = root / "memory" / memory_dir_name
    memory_file = memory_dir / "MEMORY.md"

    if not memory_file.exists():
        return None

    try:
        soul_prompt = memory_file.read_text(encoding="utf-8")
    except Exception as e:
        logger.warning("Failed to read One OS memory %s: %s", memory_file, e)
        return None

    # Sessions
    sessions_dir = str(memory_dir / "sessions")

    # References: look for capabilities in programs/capabilities/
    references = []
    caps_dir = root / "programs" / "capabilities"
    if caps_dir.is_dir():
        references = [f.name for f in sorted(caps_dir.iterdir()) if f.is_file()]

    # Also add programs as references
    programs_dir = root / "programs"
    if programs_dir.is_dir():
        for f in sorted(programs_dir.iterdir()):
            if f.is_file() and f.suffix == ".md" and f.name not in references:
                references.append(f.name)

    builtin = _BUILTIN_SOULS.get(name, {})

    return SoulConfig(
        name=name,
        display_name=builtin.get("display_name", name.title()),
        description=builtin.get("description", ""),
        character_class=builtin.get("character_class", ""),
        soul_prompt=soul_prompt,
        memory="",  # Already in MEMORY.md
        user_patterns="",
        skin=builtin.get("skin", ""),
        references=references,
        sessions_dir=sessions_dir,
    )


def load_soul(name: str) -> Optional[SoulConfig]:
    """Load a soul by name. Checks: disk souls first, then One OS memory, then built-ins.

    Args:
        name: Soul name (e.g., 'gojo', 'reigen')

    Returns:
        SoulConfig or None if not found.
    """
    # 1. User souls on disk (~/.hermes/souls/<name>/)
    soul = _load_soul_from_disk(name)
    if soul:
        logger.info("Loaded soul '%s' from disk", name)
        return soul

    # 2. One OS memory directory
    soul = _load_soul_from_oneos(name)
    if soul:
        logger.info("Loaded soul '%s' from One OS memory", name)
        return soul

    # 3. Built-in (hermes default)
    if name == "hermes":
        try:
            from hermes_cli.default_soul import DEFAULT_SOUL_MD
            return SoulConfig(
                name="hermes",
                display_name="Hermes",
                description="Default Hermes personality",
                character_class="Default",
                soul_prompt=DEFAULT_SOUL_MD,
                skin="default",
            )
        except ImportError:
            pass

    logger.warning("Soul '%s' not found", name)
    return None


def get_active_soul() -> SoulConfig:
    """Get the currently active soul. Defaults to 'hermes' if none set."""
    global _active_soul
    if _active_soul is None:
        _active_soul = load_soul("hermes") or SoulConfig(name="hermes")
    return _active_soul


def set_active_soul(name: str) -> bool:
    """Switch to a different soul/character.

    Args:
        name: Soul name to activate.

    Returns:
        True if soul was found and activated, False otherwise.
    """
    global _active_soul
    soul = load_soul(name)
    if soul is None:
        return False

    _active_soul = soul
    logger.info("Activated soul: %s (%s)", soul.display_name, soul.character_class)

    # Couple skin if specified
    if soul.skin:
        try:
            from hermes_cli.skin_engine import set_active_skin
            set_active_skin(soul.skin)
            logger.info("Coupled skin: %s", soul.skin)
        except Exception as e:
            logger.debug("Could not couple skin: %s", e)

    return True


def list_souls() -> List[Dict[str, str]]:
    """List all available souls (built-in + disk + One OS).

    Returns:
        List of dicts with 'name', 'display_name', 'description', 'class', 'source'.
    """
    result = []
    seen = set()

    # 1. Disk souls
    souls_dir = _get_souls_dir()
    if souls_dir.is_dir():
        for entry in sorted(souls_dir.iterdir()):
            if entry.is_dir() and (entry / "SOUL.md").exists():
                name = entry.name
                builtin = _BUILTIN_SOULS.get(name, {})
                result.append({
                    "name": name,
                    "display_name": builtin.get("display_name", name.title()),
                    "description": builtin.get("description", "User soul"),
                    "class": builtin.get("character_class", ""),
                    "source": "disk",
                })
                seen.add(name)

    # 2. One OS souls
    root = _get_oneos_root()
    if root:
        memory_dir = root / "memory"
        if memory_dir.is_dir():
            for entry in sorted(memory_dir.iterdir()):
                if entry.is_dir() and (entry / "MEMORY.md").exists():
                    # Reverse-map directory name to soul name
                    dir_name = entry.name
                    soul_name = None
                    for sname, dname in _SOUL_MEMORY_DIRS.items():
                        if dname == dir_name:
                            soul_name = sname
                            break
                    if soul_name is None:
                        soul_name = dir_name

                    if soul_name not in seen:
                        builtin = _BUILTIN_SOULS.get(soul_name, {})
                        result.append({
                            "name": soul_name,
                            "display_name": builtin.get("display_name", soul_name.title()),
                            "description": builtin.get("description", "One OS character"),
                            "class": builtin.get("character_class", ""),
                            "source": "oneos",
                        })
                        seen.add(soul_name)

    # 3. Built-in (hermes default)
    if "hermes" not in seen:
        result.insert(0, {
            "name": "hermes",
            "display_name": "Hermes",
            "description": "Default Hermes personality",
            "class": "Default",
            "source": "builtin",
        })

    return result


def init_soul_from_config(config: Dict[str, Any]) -> None:
    """Initialize the active soul from config.yaml.

    Reads ``character.soul`` from config. Falls back to 'hermes'.
    """
    soul_name = "hermes"

    char_config = config.get("character", {})
    if isinstance(char_config, dict):
        soul_name = char_config.get("soul", "hermes")
    elif isinstance(char_config, str):
        soul_name = char_config

    if not set_active_soul(soul_name):
        logger.warning("Could not load soul '%s', falling back to hermes", soul_name)
        set_active_soul("hermes")
