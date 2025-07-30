# AnimaLoom Project

## The Soul Weaver Engine

AnimaLoom is a highly flexible, data-driven engine designed for creating emergent narratives and complex character simulations. It allows game designers to define game logic, character attributes, and interactions through human-readable TOML files, enabling a unique blend of authored content and procedural generation.

### Core Concepts (The Mythos)

*   **AnimaLoom:** The overarching project, the "Soul Weaver" engine.
*   **The Loom:** The core engine library, containing the fundamental components.
*   **The Hyle:** Raw data definitions (TOML files) that provide the potential for game elements.
*   **The Alembic:** The component responsible for distilling The Hyle into living game objects.
*   **The Eidolon:** An instantiated character or agent within the simulation.
*   **The Moirai:** The formula engine that determines the outcomes of interactions.
*   **The Nexus:** The world state manager, holding all active Eidolons and their relationships.
*   **The Loomwright:** The editor and simulator application for interacting with the AnimaLoom engine.

### Getting Started

**Prerequisites:**

*   Python 3.11 or newer (due to reliance on `tomllib` from the standard library).

**Running The Loomwright (CLI Editor/Simulator):**

1.  Navigate to the `the_loomwright` directory:
    ```bash
    cd AnimaLoom/the_loomwright/
    ```
2.  Run the main application:
    ```bash
    python3 main.py
    ```
3.  Once the `Loomwright>` prompt appears, type `help` to see available commands.

**Example Usage:**

```
Loomwright> load kismet_social
Loomwright> create gregor_the_guard
Loomwright> create town_gossip
Loomwright> list eidolons
Loomwright> show gregor_the_guard
Loomwright> interact gregor_the_guard town_gossip offer_a_gift
```

### Project Structure

```
AnimaLoom/
├── game_modules/             # Contains The Hyle (game data definitions)
│   └── kismet_social/        # Example game module
│       ├── characters.toml
│       ├── cards.toml
│       ├── formulas.toml
│       └── game_config.toml
├── the_loom/                 # The Loom (core engine library)
│   ├── __init__.py
│   ├── the_alembic.py        # The Alembic (Hyle distiller)
│   ├── the_eidolon.py        # The Eidolon (Agent class)
│   ├── the_moirai.py         # The Moirai (Formula engine)
│   └── the_nexus.py          # The Nexus (World state manager)
├── the_loomwright/           # The Loomwright (editor/simulator application)
│   └── main.py
├── save.sh                   # Script to commit changes and create backups
├── run_all_tests.py          # Script to run internal tests and generate TEST_REPORT.md
├── TEST_REPORT.md            # Generated test report (tracked by Git)
└── THE_MYTHOS.md             # Documentation on the project's thematic architecture
└── README.md                 # This file
└── requirements.txt          # Project dependencies
```

### Development Workflow

To save your progress, commit changes to Git, and create a timestamped backup, run the `save.sh` script from the `AnimaLoom/` directory with a commit message:

```bash
./save.sh "Your descriptive commit message here"
```

This will also automatically run `run_all_tests.py` and update `TEST_REPORT.md` before committing.
