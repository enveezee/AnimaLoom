
# Kismet Engine: Architectural Vision

This document outlines the high-level architecture for the Kismet Engine, incorporating a data-driven formula system, a dual-application structure, and a hybrid model for content generation.

## 1. The Core Principle: Everything is Data

Our guiding principle is that **game logic, as much as possible, should be defined as data** in human-readable TOML files, not as hard-coded Python statements. This includes not only characters and items, but the very formulas that govern their interactions.

## 2. The Configurable Formula Engine

To avoid hard-coding game mechanics, we will create a system for defining mathematical and logical formulas within TOML files. The engine will parse these formulas at runtime.

### 2.1. Formula Definition (`formulas.toml`)

We will create a `formulas.toml` file within each game module. It will contain definitions like this:

```toml
# formulas.toml

[tell_joke_success]
description = "Calculates the success chance of telling a joke."
# This expression uses a simple, defined syntax.
# 'actor' and 'target' are keywords for the agents involved.
expression = """
    (actor.core.charisma * 1.5) + 
    (actor.personality.extraversion * 0.5) - 
    (target.affinity.antagonistic_towards.actor * 2.0) + 
    (actor.state.emotion_modifier.joy * 5)
"""

[intimidate_power]
description = "Calculates the power of an intimidation attempt."
expression = "(actor.core.strength + actor.core.composure) / 2"
```

### 2.2. The Python Formula Parser (`core/formula_parser.py`)

A Python module will be responsible for:
1.  Reading a formula `expression` from the TOML file.
2.  Identifying the required stats (e.g., `actor.core.charisma`).
3.  Fetching the corresponding values from the `Agent` objects involved in the interaction.
4.  Safely executing the mathematical operations.
5.  Returning the final value.

This makes game balance and mechanic design something that can be done entirely by editing a text file.

## 3. The Dual-Application Architecture

The project will be structured to separate the core logic from the presentation layer.

```
/kismet_project/
├── game_modules/
│   └── kismet_social/        # The default game module
│       ├── formulas.toml
│       ├── characters.toml
│       ├── cards.toml
│       └── maps.toml
│
├── kismet_core/                # The Headless Engine Library
│   ├── __init__.py
│   ├── agent.py              # The Agent class definition
│   ├── formula_parser.py     # The formula engine
│   ├── encounter_manager.py  # Logic for handling interactions
│   └── world_state.py        # Manages all agents and the environment
│
└── kismet_editor/              # The Editor/Simulator Application
    ├── main.py                 # Starts the editor application
    ├── ui_components.py        # Tkinter widgets for displaying agents, maps
    └── simulator.py            # Runs the live, nethack-style simulation
```

-   **`kismet_core`** can be installed as a package in other projects.
-   **`kismet_editor`** imports `kismet_core` to do its work.
-   A future, more advanced graphical client would also import `kismet_core`.

## 4. The Hybrid Generation System

To allow for both authored stories and emergent gameplay, every object definition will support two modes: `static` and `template`.

### 4.1. Static vs. Template Objects

This is defined by a `generation_type` flag in the object's TOML definition.

**Static Object Example (`characters.toml`):**
```toml
[gregor_the_guard]
generation_type = "static" # This is a specific, unique NPC.
name = "Gregor the Guard"
core.strength = 15
# ... other stats are fixed values
```

**Template Object Example (`characters.toml`):**
```toml
[generic_bandit]
generation_type = "template" # This is a template for creating random bandits.
name = "Bandit"
core.strength = { type = "range", min = 8, max = 12 }
core.agility = { type = "range", min = 10, max = 14 }
personality.agreeableness = { type = "range", min = -20, max = 0 }
# ... other stats are defined as ranges or weighted lists
```

### 4.2. The Spawning System

The engine will have a "Spawner" that:
-   When the story requires "Gregor the Guard," it loads the `static` definition directly.
-   When the game needs a random encounter in the forest, it uses the `generic_bandit` `template` to generate a new, randomized Agent instance.

This same logic applies to items, maps, quests, and any other game element.

---

This architectural plan provides a clear roadmap for building the highly flexible, data-driven, and emergent narrative engine we have envisioned.
