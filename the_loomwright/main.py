
"""
The Loomwright: The editor and simulator application for the AnimaLoom engine.
This module provides a basic interface for loading game modules, creating Eidolons, and simulating interactions.
"""

import os
import sys
import tomllib # Requires Python 3.11+
from typing import Optional # Import Optional

# Add the_loom to the Python path so we can import it
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from the_loom.the_alembic import TheAlembic
from the_loom.the_moirai import TheMoirai
from the_loom.the_nexus import TheNexus
from the_loom.the_eidolon import Eidolon

class TheLoomwright:
    def __init__(self):
        self.alembic = TheAlembic()
        self.moirai = TheMoirai()
        self.nexus = TheNexus()
        self.game_module_path = ""
        self.loaded_game_config = {}

    def load_game_module(self, module_name: str):
        self.game_module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'game_modules', module_name))
        
        if not os.path.exists(self.game_module_path):
            print(f"Error: Game module '{module_name}' not found at {self.game_module_path}")
            return False

        print(f"Loading game module: {module_name} from {self.game_module_path}")

        # Load game_config.toml
        config_path = os.path.join(self.game_module_path, "game_config.toml")
        try:
            with open(config_path, 'rb') as f: # tomllib requires binary mode
                self.loaded_game_config = tomllib.load(f)
            print("game_config.toml loaded.")
        except FileNotFoundError:
            print(f"Warning: game_config.toml not found in {self.game_module_path}")
        except tomllib.TOMLDecodeError as e: # Updated exception name
            print(f"Error decoding game_config.toml: {e}")
            return False

        # Load formulas (The Moirai's Hyle)
        formulas_path = os.path.join(self.game_module_path, "formulas.toml")
        self.moirai.load_formulas_from_hyle(formulas_path)
        print("formulas.toml loaded.")

        # Load characters (The Alembic's Hyle)
        characters_path = os.path.join(self.game_module_path, "characters.toml")
        self.alembic.load_hyle_file(characters_path, "characters")
        print("characters.toml loaded.")

        # Load cards (The Alembic's Hyle)
        cards_path = os.path.join(self.game_module_path, "cards.toml")
        self.alembic.load_hyle_file(cards_path, "cards")
        print("cards.toml loaded.")

        print(f"Module '{module_name}' loaded successfully.")
        return True

    def create_and_add_eidolon(self, eidolon_id: str) -> Optional[Eidolon]:
        eidolon = self.alembic.create_eidolon(eidolon_id)
        if eidolon:
            self.nexus.add_eidolon(eidolon)
            print(f"Eidolon '{eidolon.name}' added to The Nexus.")
        return eidolon

    def simulate_interaction(self, actor_name: str, target_name: str, card_id: str):
        actor = self.nexus.get_eidolon(actor_name)
        target = self.nexus.get_eidolon(target_name)
        card_data = self.alembic.loaded_hyle.get("cards", {}).get(card_id)

        if not actor: print(f"Error: Actor '{actor_name}' not found."); return
        if not target: print(f"Error: Target '{target_name}' not found."); return
        if not card_data: print(f"Error: Card '{card_id}' not found."); return

        print(f"\n--- Simulating Interaction: {actor.name} plays '{card_data['name']}' on {target.name} ---")

        # 1. Calculate Challenge Score
        challenge_formula_name = card_data.get("effects", {}).get("success", {}).get("formula")
        if not challenge_formula_name:
            print(f"Warning: Card '{card_id}' has no success formula defined.")
            return

        try:
            actor_challenge_score = self.moirai.evaluate_formula(challenge_formula_name, actor=actor, target=target)
            print(f"{actor.name}'s Challenge Score: {actor_challenge_score}")
        except Exception as e:
            print(f"Error calculating actor challenge score: {e}"); return

        # 2. Calculate Resistance Score (using a generic social resistance formula for now)
        resistance_formula_name = "social_action_resistance" # Or a specific one from card_data
        try:
            target_resistance_score = self.moirai.evaluate_formula(resistance_formula_name, actor=target) # Target is actor for resistance
            print(f"{target.name}'s Resistance Score: {target_resistance_score}")
        except Exception as e:
            print(f"Error calculating target resistance score: {e}"); return

        # 3. Determine Outcome (Simplified for now)
        if actor_challenge_score > target_resistance_score:
            print(f"Outcome: SUCCESS! {actor.name}'s action is effective.")
            # Apply success effects (e.g., update affinity, emotional state)
            # This would involve more complex logic, potentially calling other formulas
            # For now, let's just update a platonic affinity as an example
            try:
                affinity_change = self.moirai.evaluate_formula("affinity_change_platonic_success", actor=actor, target=target)
                current_affinity = target.get_affinity(actor.name, "platonic")
                target.update_affinity(actor.name, "platonic", current_affinity + affinity_change)
                print(f"{target.name}'s Platonic affinity towards {actor.name} increased by {affinity_change} to {target.get_affinity(actor.name, 'platonic')}.")
            except Exception as e:
                print(f"Error applying success effect: {e}")

        else:
            print(f"Outcome: FAILURE! {actor.name}'s action was resisted.")
            # Apply failure effects
            try:
                affinity_change = self.moirai.evaluate_formula("affinity_change_platonic_fail", actor=actor, target=target)
                current_affinity = target.get_affinity(actor.name, "platonic")
                target.update_affinity(actor.name, "platonic", current_affinity + affinity_change)
                print(f"{target.name}'s Platonic affinity towards {actor.name} changed by {affinity_change} to {target.get_affinity(actor.name, 'platonic')}.")
            except Exception as e:
                print(f"Error applying failure effect: {e}")

        # Apply costs (e.g., social battery drain)
        cost_formula_name = card_data.get("costs", {}).get("social_battery")
        if cost_formula_name:
            try:
                drain_amount = self.moirai.evaluate_formula(cost_formula_name, actor=actor)
                actor.update_dynamic_state("social_battery", actor.dynamic_states["social_battery"] - drain_amount)
                print(f"{actor.name}'s Social Battery drained by {drain_amount} to {actor.dynamic_states['social_battery']}.")
            except Exception as e:
                print(f"Error applying cost: {e}")


    def run_cli(self):
        print("\n--- Welcome to The Loomwright ---")
        print("Type 'help' for commands.")

        while True:
            command = input("\nLoomwright> ").strip().lower()

            if command == "exit":
                print("Exiting The Loomwright. Goodbye!")
                break
            elif command == "help":
                print("  load <module_name> - Load a game module (e.g., 'kismet_social')")
                print("  create <eidolon_id> - Create and add an Eidolon to The Nexus")
                print("  list eidolons - List all Eidolons currently in The Nexus")
                print("  show <eidolon_name> - Show details of a specific Eidolon")
                print("  interact <actor_name> <target_name> <card_id> - Simulate an interaction")
                print("  reset - Reset The Nexus (clear all Eidolons)")
                print("  exit - Exit the application")
            elif command.startswith("load "):
                module_name = command.split(" ", 1)[1]
                self.load_game_module(module_name)
            elif command.startswith("create "):
                eidolon_id = command.split(" ", 1)[1]
                self.create_and_add_eidolon(eidolon_id)
            elif command == "list eidolons":
                if not self.nexus.eidolons:
                    print("No Eidolons in The Nexus.")
                else:
                    print("Eidolons in The Nexus:")
                    for name, eidolon in self.nexus.get_all_eidolons().items():
                        print(f"  - {name}")
            elif command.startswith("show "):
                eidolon_name = command.split(" ", 1)[1]
                eidolon = self.nexus.get_eidolon(eidolon_name)
                if eidolon:
                    print(f"\n--- Eidolon: {eidolon.name} ---")
                    print(f"  Core Attributes: {eidolon.core_attributes}")
                    print(f"  Personality: {eidolon.personality}")
                    print(f"  Dynamic States: {eidolon.dynamic_states}")
                    print(f"  Affinities: {eidolon.affinities}")
                    print(f"  Ledger: {eidolon.ledger}")
                else:
                    print(f"Eidolon '{eidolon_name}' not found in The Nexus.")
            elif command.startswith("interact "):
                parts = command.split(" ")
                if len(parts) == 4:
                    actor_name, target_name, card_id = parts[1], parts[2], parts[3]
                    self.simulate_interaction(actor_name, target_name, card_id)
                else:
                    print("Usage: interact <actor_name> <target_name> <card_id>")
            elif command == "reset":
                self.nexus.reset()
                print("The Nexus has been reset. All Eidolons cleared.")
            else:
                print("Unknown command. Type 'help' for commands.")

if __name__ == "__main__":
    loomwright = TheLoomwright()
    loomwright.run_cli()
