# AnimaLoom Project: Core Design Goals

This document outlines the fundamental principles and objectives guiding the development of the AnimaLoom engine. These goals are intended to ensure a cohesive, flexible, and robust system capable of generating rich, emergent narratives.

## 1. The "Tangled Web" - Deep Character Simulation

*   **Emergent Narrative:** The primary goal is to create a system where complex, unpredictable stories arise naturally from the interactions of deeply simulated characters, rather than being pre-scripted.
*   **Layered Metrics:** Implement a multi-tiered system of character attributes (Core, Personality, Dynamic States, History/Relationships) that interoperate to create nuanced and believable agent behavior.
*   **Contextual Actions:** Ensure that every action an agent takes is heavily influenced by their internal state (personality, emotions, needs) and their historical relationship with other agents and the world.
*   **Philosophical Depth:** Translate abstract concepts of ability, disposition, and intent into concrete, measurable game mechanics.

## 2. Everything is Data - Extreme Configurability

*   **TOML-Driven Logic:** All game elements, including core attributes, character definitions, card properties, and crucially, the *formulas* governing interactions, must be defined in human-readable TOML files.
*   **No Hardcoding:** Avoid hardcoding game logic or content wherever possible. The engine should be able to run entirely different game modules by simply loading different sets of TOML files.
*   **Hybrid Generation:** Support both statically defined (authored) content and procedurally generated content (e.g., characters, maps, items) through a flexible templating system.

## 3. Modular & Reusable Architecture

*   **Separation of Concerns:** Clearly separate the core simulation logic (`The Loom`) from the application layer (`The Loomwright`) and game-specific data (`The Hyle`).
*   **Portable Components:** Design individual components (e.g., `The Eidolon`, `The Moirai`, `The Alembic`) to be as self-contained and reusable as possible, minimizing dependencies.
*   **Abstract Design:** Use abstract concepts and thematic naming (The Mythos) to guide the design, making the system conceptually clear and extensible.
*   **UI Builder Abstraction:** The UI builder should be a generic tool capable of rendering any UI defined in TOML/JSON, and ideally reusable in other projects, independent of AnimaLoom's specific game logic.

## 4. Robust Development Practices

*   **Tandem Development:** Develop core logic, data definitions, and UI in parallel, ensuring continuous integration and validation of design choices.
*   **Continuous Testing:** Implement and regularly run automated tests (e.g., `run_all_tests.py`) to verify functionality and track project health at every stage.
*   **Version Control & Backups:** Utilize Git for version control and automate timestamped backups (`save.sh`) to ensure project history and data integrity.
*   **Clear Documentation:** Maintain up-to-date and accessible documentation (e.g., `README.md`, `THE_MYTHOS.md`, `design_goals.md`) to provide context for current and future developers.

These goals collectively aim to create not just a game engine, but a powerful, flexible platform for exploring emergent narratives and complex simulated worlds.