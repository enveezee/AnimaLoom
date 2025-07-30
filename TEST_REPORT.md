# AnimaLoom Test Report - 2025-07-30 02:48:28
This report details the output of basic functional tests for the AnimaLoom engine components.
Each test runs a specific module's `if __name__ == '__main__':` block.

## Test: The Eidolon (Agent Class)
```bash
python3 -m the_loom.the_eidolon
```
### Output
```
```
**Exit Code:** 0

---

## Test: The Nexus (World State Manager)
```bash
python3 -m the_loom.the_nexus
```
### Output
```
Initial Nexus time: 0
Eidolons in Nexus: ['Alice', 'Bob']
Alice's platonic affinity for Bob: 50
Bob's rivalrous affinity for Alice: 20
Time advanced to: 1
Time advanced to: 6
Nexus after reset: {}, Time: 0
```
**Exit Code:** 0

---

## Test: The Moirai (Formula Engine)
```bash
python3 -m the_loom.the_moirai
```
### Output
```
Alice's charisma: 15
Alice's extraversion: 70
Alice's joke success score: 57.5
Alice's intimidate power: 5.0
Bob's resistance: 60
```
**Exit Code:** 0

---

## Test: The Alembic (Hyle Distiller)
```bash
python3 -m the_loom.the_alembic
```
### Output
```
Successfully loaded 'characters' from dummy_characters.toml.
Created Eidolon: Gregor the Guard (Type: static)
Gregor Strength: 15
Gregor Openness: 20
Created Eidolon: Bandit (Type: template)
Bandit 1 Strength: 9
Bandit 1 Agility: 10
Bandit 1 Agreeableness: 0
Created Eidolon: Bandit (Type: template)
Bandit 2 Strength: 10
Bandit 2 Agility: 10
Bandit 2 Agreeableness: -3
```
**Exit Code:** 0

---

## Test: The Loomwright (GUI Application)
```bash
python3 -c "import tkinter as tk; from the_loomwright.main import TheLoomwrightApp; root = tk.Tk(); app = TheLoomwrightApp(root); root.destroy();"
```
> Note: This test attempts to initialize the Tkinter GUI application and immediately destroy it to confirm basic startup without errors.

### Output
```
[TheLoomwrightUIBuilder DEBUG] Registered dynamic builder: build_character_properties_section
[TheLoomwrightUIBuilder DEBUG] Registered dynamic builder: build_character_attributes_section
[TheLoomwrightUIBuilder DEBUG] Registered dynamic builder: build_card_properties_section
[TheLoomwrightUIBuilder DEBUG] Building UI from main_window.tui
[TheLoomwrightUIBuilder DEBUG] Loading UI definition: the_loomwright/ui_components/../ui_definitions/main_window.tui
[TheLoomwrightUIBuilder DEBUG] Processing widget: welcome_label (Type: ttk.Label)
[TheLoomwrightUIBuilder DEBUG] Processing widget: load_module_button (Type: ttk.Button)
[TheLoomwrightUIBuilder DEBUG] Processing widget: character_creator_button (Type: ttk.Button)
[TheLoomwrightUIBuilder DEBUG] Processing widget: card_creator_button (Type: ttk.Button)
[TheLoomwrightUIBuilder DEBUG] UI build complete.
```
**Exit Code:** 0

---

