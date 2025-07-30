"""
The Alembic: Distills The Hyle (TOML data) into living Eidolons and other game objects.
This module handles the loading and instantiation of game entities based on their definitions.
"""

import tomllib # Requires Python 3.11+
import random
from typing import Dict, Any, List, Optional
from the_loom.the_eidolon import Eidolon

class TheAlembic:
    def __init__(self):
        self.loaded_hyle: Dict[str, Any] = {}

    def load_hyle_file(self, hyle_path: str, section_name: str):
        """Loads a specific section (e.g., 'characters') from a TOML file into The Alembic's memory."""
        try:
            with open(hyle_path, 'rb') as f: # tomllib requires binary mode
                data = tomllib.load(f)
            if section_name in data:
                self.loaded_hyle[section_name] = data[section_name]
                print(f"Successfully loaded '{section_name}' from {hyle_path}.")
            else:
                print(f"Warning: Section '{section_name}' not found in {hyle_path}.")
        except FileNotFoundError:
            print(f"Error: Hyle file not found at {hyle_path}")
        except tomllib.TOMLDecodeError as e: # Updated exception name
            print(f"Error decoding TOML from {hyle_path}: {e}")

    def create_eidolon(self, eidolon_id: str) -> Optional[Eidolon]:
        """Creates an Eidolon instance based on a static or template definition from loaded Hyle."""
        if "characters" not in self.loaded_hyle:
            print("Error: No character Hyle loaded. Please load a characters TOML file first.")
            return None

        char_data = self.loaded_hyle["characters"].get(eidolon_id)
        if not char_data:
            print(f"Error: Eidolon definition for '{eidolon_id}' not found in loaded Hyle.")
            return None

        name = char_data.get("name", eidolon_id) # Use ID as name if not specified
        generation_type = char_data.get("generation_type", "static")

        eidolon_kwargs = {"name": name}

        # Process attributes based on generation type
        for tier_name, tier_data in char_data.items():
            if tier_name in ["core", "personality", "dynamic_states", "ledger"]:
                for attr_name, attr_value_def in tier_data.items():
                    if isinstance(attr_value_def, dict) and "type" in attr_value_def:
                        # This is a procedural definition (e.g., range)
                        if attr_value_def["type"] == "range":
                            min_val = attr_value_def.get("min", 0)
                            max_val = attr_value_def.get("max", 100)
                            eidolon_kwargs[attr_name] = random.randint(min_val, max_val)
                        # Add other procedural types here (e.g., weighted_list, formula)
                    else:
                        # This is a static value
                        eidolon_kwargs[attr_name] = attr_value_def

        # Instantiate Eidolon
        eidolon = Eidolon(**eidolon_kwargs)
        print(f"Created Eidolon: {eidolon.name} (Type: {generation_type})")
        return eidolon

# Example Usage (for testing purposes)
if __name__ == "__main__":
    alembic = TheAlembic()

    # Create a dummy characters.toml file for testing
    dummy_characters_hyle_content = """
    [characters.gregor_the_guard]
    name = "Gregor the Guard"
    generation_type = "static"
    core.strength = 15
    core.agility = 8
    personality.openness = 20

    [characters.generic_bandit]
    name = "Bandit"
    generation_type = "template"
    core.strength = { type = "range", min = 8, max = 12 }
    core.agility = { type = "range", min = 10, max = 14 }
    personality.agreeableness = { type = "range", min = -20, max = 0 }
    """

    with open("dummy_characters.toml", "w") as f:
        f.write(dummy_characters_hyle_content)

    # Load the Hyle
    alembic.load_hyle_file("dummy_characters.toml", "characters")

    # Create a static Eidolon
    gregor = alembic.create_eidolon("gregor_the_guard")
    if gregor:
        print(f"Gregor Strength: {gregor.core_attributes['strength']}")
        print(f"Gregor Openness: {gregor.personality['openness']}")

    # Create a template-based Eidolon
    bandit1 = alembic.create_eidolon("generic_bandit")
    if bandit1:
        print(f"Bandit 1 Strength: {bandit1.core_attributes['strength']}")
        print(f"Bandit 1 Agility: {bandit1.core_attributes['agility']}")
        print(f"Bandit 1 Agreeableness: {bandit1.personality['agreeableness']}")

    bandit2 = alembic.create_eidolon("generic_bandit")
    if bandit2:
        print(f"Bandit 2 Strength: {bandit2.core_attributes['strength']}")
        print(f"Bandit 2 Agility: {bandit2.core_attributes['agility']}")
        print(f"Bandit 2 Agreeableness: {bandit2.personality['agreeableness']}")

    import os
    os.remove("dummy_characters.toml")
