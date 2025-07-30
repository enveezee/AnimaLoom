# AnimaLoom Project

## The Soul Weaver Engine

AnimaLoom is a highly flexible, data-driven engine designed for creating emergent narratives and complex character simulations. It allows game designers to define game logic, character attributes, and interactions through human-readable TOML files, enabling a unique blend of authored content and procedural generation.

### Core Concepts (The Mythos)

For a deeper dive into the philosophical and thematic underpinnings of AnimaLoom, including the meaning behind its unique naming conventions, please refer to [THE_MYTHOS.md](docs/THE_MYTHOS.md).

### Getting Started

**Prerequisites:**

*   Python 3.11 or newer (due to reliance on `tomllib` from the standard library).

**Running The Loomwright (GUI Editor/Simulator):**

1.  Navigate to the `the_loomwright` directory:
    ```bash
    cd AnimaLoom/the_loomwright/
    ```
2.  Run the main application:
    ```bash
    python3 main.py
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
│   ├── main.py
│   ├── ui_components/        # UI-specific modules
│   │   ├── __init__.py
│   │   ├── the_loomwright_ui_builder.py
│   │   ├── the_loomwright_widgets.py
│   │   └── the_loomwright_handlers.py
│   └── ui_definitions/       # UI definition files (e.g., .tui, .jui)
│       └── main_window.tui
├── docs/                     # Project documentation
│   ├── design/               # Design documents
│   │   ├── character_metrics_deep_dive.md
│   │   ├── engine_architecture.md
│   │   └── game_engine_outline.md
│   └── THE_MYTHOS.md         # Documentation on the project's thematic architecture
├── tools/                    # Utility scripts
│   ├── save.sh               # Script to commit changes and create backups
│   └── run_all_tests.py      # Script to run internal tests and generate TEST_REPORT.md
├── TEST_REPORT.md            # Generated test report (tracked by Git)
└── requirements.txt          # Project dependencies
```

### Development Workflow

To save your progress, commit changes to Git, and create a timestamped backup, run the `save.sh` script from the `AnimaLoom/` directory with a commit message:

```bash
./tools/save.sh "Your descriptive commit message here"
```

This will also automatically run `run_all_tests.py` and update `TEST_REPORT.md` before committing.
