# AnimaLoom Test Report - 2025-07-30 02:37:48
This report details the output of basic functional tests for the AnimaLoom engine components.
Each test runs a specific module's `if __name__ == '__main__':` block.

## Test: The Eidolon (Agent Class)
```bash
python3 the_loom/the_eidolon.py
```
### Output
```
```
### Errors (Stderr)
```
python3: can't open file '/home/nvz/Documents/gemini-cli/kismet/AnimaLoom/the_loom/the_loom/the_eidolon.py': [Errno 2] No such file or directory
```
**Exit Code:** 2

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
Bandit 1 Strength: 8
Bandit 1 Agility: 11
Bandit 1 Agreeableness: -7
Created Eidolon: Bandit (Type: template)
Bandit 2 Strength: 10
Bandit 2 Agility: 10
Bandit 2 Agreeableness: -9
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
```
### Errors (Stderr)
```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import tkinter as tk; from the_loomwright.main import TheLoomwrightApp; root = tk.Tk(); app = TheLoomwrightApp(root); root.destroy();
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/nvz/Documents/gemini-cli/kismet/AnimaLoom/the_loomwright/main.py", line 15, in <module>
    from ui_components.the_loomwright_ui_builder import TheLoomwrightUIBuilder
ModuleNotFoundError: No module named 'ui_components'
```
**Exit Code:** 1

---

