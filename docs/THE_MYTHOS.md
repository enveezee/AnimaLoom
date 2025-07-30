# The AnimaLoom Project: A Thematic Architecture

This document outlines the thematic naming scheme and architectural mythology for the AnimaLoom project.

*   **Overall Project Name: `AnimaLoom`**
    *   *Meaning:* The "Soul Weaver." The entire collection of tools and libraries for weaving narrative tapestries from simulated souls.

*   **The Core Engine Library: `The Loom`**
    *   *Meaning:* This is the heart of the machine, the engine itself. It's a fittingly simple yet powerful name for the core library.
    *   *Corresponds to:* The `kismet_core` directory.

    *   **Component: Raw Data Definitions (`.toml` files): `The Hyle`**
        *   *Meaning:* From the Greek for "primordial matter." This perfectly describes the raw, formless potential contained in the TOML files before the engine gives it structure.
        *   *Corresponds to:* The `game_modules` directory and its contents (e.g., `kismet_social/formulas.toml`, `characters.toml`, etc.).

    *   **Component: Object Creation System (The Spawner): `The Alembic`**
        *   *Meaning:* The alchemical still. This component takes the raw `Hyle` (data) and *distills* it into living game objects (`Eidolons`).
        *   *Corresponds to:* A module within `The Loom` responsible for parsing `The Hyle` and instantiating game objects.

    *   **Component: The Agent Class (`agent.py`): `The Eidolon`**
        *   *Meaning:* A Greek term for a phantom or idealized image. This beautifully represents a specific, instantiated character—a "spirit" given form by the `Alembic`.
        *   *Corresponds to:* The `agent.py` module within `The Loom`.

    *   **Component: Interaction & Formula Engine (`formula_parser.py`): `The Moirai`**
        *   *Meaning:* The Fates of Greek myth who spin, measure, and cut the threads of life. This module is responsible for executing the formulas that decide the outcome of events—it literally determines the fate of an interaction.
        *   *Corresponds to:* The `formula_parser.py` module within `The Loom`.

    *   **Component: World State Manager (`world_state.py`): `The Nexus`**
        *   *Meaning:* The central point of connection. This component holds all the `Eidolons` and the web of their relationships, acting as the central hub of the simulation.
        *   *Corresponds to:* The `world_state.py` module within `The Loom`.

*   **The Editor/Simulator Application: `The Loomwright`**
    *   *Meaning:* An archaic term for a person who builds or operates a loom. This is a perfect name for the creative tool used by a game designer to work with the `AnimaLoom` engine.
    *   *Corresponds to:* The `kismet_editor` directory.

---

**In Summary:**

A game designer, the **Loomwright**, uses the editor to define the **Hyle** (data). When the simulation runs, the **Alembic** distills this data into living **Eidolons**. These Eidolons interact within the **Nexus**, and the outcome of their actions is determined by the **Moirai**. The entire system, the **Loom**, is what makes up the **AnimaLoom** engine.
