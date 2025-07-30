"""
The Moirai: Determines the fate of interactions by evaluating configurable formulas.
This module is responsible for parsing and executing the game's core logic defined in The Hyle.
"""

import tomllib # Requires Python 3.11+
from typing import Dict, Any
from the_loom.the_eidolon import Eidolon

class TheMoirai:
    def __init__(self):
        self.formulas: Dict[str, str] = {}

    def load_formulas_from_hyle(self, hyle_path: str):
        """Loads formulas from a specified TOML file (The Hyle)."""
        try:
            with open(hyle_path, 'rb') as f: # tomllib requires binary mode
                hyle_data = tomllib.load(f)
            
            if 'formulas' in hyle_data:
                for formula_name, formula_data in hyle_data['formulas'].items():
                    if 'expression' in formula_data:
                        self.formulas[formula_name] = formula_data['expression']
                    else:
                        print(f"Warning: Formula '{formula_name}' in {hyle_path} is missing 'expression'.")
            else:
                print(f"Warning: No 'formulas' section found in {hyle_path}.")

        except FileNotFoundError:
            print(f"Error: Hyle file not found at {hyle_path}")
        except tomllib.TOMLDecodeError as e: # Updated exception name
            print(f"Error decoding TOML from {hyle_path}: {e}")

    def evaluate_formula(self, formula_name: str, actor: Eidolon, target: Eidolon = None) -> Any:
        """Evaluates a loaded formula using the provided Eidolon(s)."""
        if formula_name not in self.formulas:
            raise ValueError(f"Formula '{formula_name}' not found in The Moirai's repertoire.")

        expression = self.formulas[formula_name]

        # Create a safe execution environment for eval()
        # WARNING: Using eval() with untrusted input is a security risk.
        # For a production system, a custom, secure expression parser is highly recommended.
        # This is used for rapid prototyping based on the user's request for configurable formulas.
        
        # Provide access to Eidolon attributes via 'actor' and 'target' objects
        # This maps the dot notation in TOML (e.g., actor.core.strength) to Python object access
        local_vars = {
            'actor': actor,
            'target': target, # Target can be None for self-affecting formulas
            # Add any other global functions or constants needed in formulas here
        }

        try:
            # Replace dot notation with attribute access for eval
            # This is a very basic replacement and needs to be more robust for production
            # For example, 'actor.core.strength' becomes 'actor.core_attributes["strength"]'
            # This simple approach assumes a fixed structure for accessing attributes.
            # A more advanced parser would handle arbitrary depth and types.
            processed_expression = expression
            
            # Simple replacements for common access patterns based on Eidolon structure
            processed_expression = processed_expression.replace('actor.core.', 'actor.core_attributes["')
            processed_expression = processed_expression.replace('actor.personality.', 'actor.personality["')
            processed_expression = processed_expression.replace('actor.dynamic_states.', 'actor.dynamic_states["')
            processed_expression = processed_expression.replace('actor.ledger.', 'actor.ledger["')
            
            if target:
                processed_expression = processed_expression.replace('target.core.', 'target.core_attributes["')
                processed_expression = processed_expression.replace('target.personality.', 'target.personality["')
                processed_expression = processed_expression.replace('target.dynamic_states.', 'target.dynamic_states["')
                processed_expression = processed_expression.replace('target.ledger.', 'target.ledger["')
                
            # Close the bracket for the dictionary access
            processed_expression = processed_expression.replace('strength', 'strength"]')
            processed_expression = processed_expression.replace('agility', 'agility"]')
            processed_expression = processed_expression.replace('intellect', 'intellect"]')
            processed_expression = processed_expression.replace('charisma', 'charisma"]')
            processed_expression = processed_expression.replace('resilience', 'resilience"]')
            processed_expression = processed_expression.replace('passion', 'passion"]')
            processed_expression = processed_expression.replace('perception', 'perception"]')
            processed_expression = processed_expression.replace('composure', 'composure"]')
            
            processed_expression = processed_expression.replace('openness', 'openness"]')
            processed_expression = processed_expression.replace('conscientiousness', 'conscientiousness"]')
            processed_expression = processed_expression.replace('extraversion', 'extraversion"]')
            processed_expression = processed_expression.replace('agreeableness', 'agreeableness"]')
            processed_expression = processed_expression.replace('neuroticism', 'neuroticism"]')

            processed_expression = processed_expression.replace('health', 'health"]')
            processed_expression = processed_expression.replace('stamina', 'stamina"]')
            processed_expression = processed_expression.replace('social_battery', 'social_battery"]')
            processed_expression = processed_expression.replace('emotional_state', 'emotional_state"]')
            processed_expression = processed_expression.replace('sanity', 'sanity"]')

            processed_expression = processed_expression.replace('trauma', 'trauma"]')
            processed_expression = processed_expression.replace('secrets', 'secrets"]')
            processed_expression = processed_expression.replace('grievances', 'grievances"]')
            processed_expression = processed_expression.replace('reputation', 'reputation"]')

            # Handle affinity access: target.affinity.platonic_towards.actor
            # This is more complex and will require a more sophisticated parser for full implementation.
            # For now, we'll assume direct access to affinity values if they are stored as simple attributes
            # or require a specific function call like actor.get_affinity(target.name, 'platonic')
            # For this prototype, let's assume affinity is accessed via a method call for simplicity.
            # Example: actor.get_affinity(target.name, 'platonic')
            # This means formulas would need to be written like: actor.get_affinity(target.name, 'platonic')
            # instead of target.affinity.platonic_towards.actor
            # Let's add a placeholder for this in the local_vars for now.
            
            # For now, let's simplify and assume direct access to affinity values if they were stored as attributes
            # or that the formula explicitly calls a method like get_affinity.
            # If the formula uses 'target.affinity.platonic_towards.actor', it will fail with this simple eval.
            # A more robust solution would involve a custom parser or a more complex string replacement.
            
            # For the purpose of this prototype, let's assume formulas will use direct attribute access or simple arithmetic.
            # If affinity is needed, it would be something like: actor.get_affinity(target.name, 'platonic')
            # We need to make sure the Eidolon class has a get_affinity method that works with this.
            # (It does, from the_eidolon.py)

            result = eval(processed_expression, {"__builtins__": {}}, local_vars)
            return result
        except Exception as e:
            print(f"Error evaluating formula '{formula_name}': {e}")
            print(f"Expression: {expression}")
            print(f"Processed Expression: {processed_expression}")
            print(f"Local Vars: {local_vars}")
            raise

# Example Usage (for testing purposes)
if __name__ == "__main__":
    from the_loom.the_eidolon import Eidolon

    moirai = TheMoirai()

    # Create a dummy formulas.toml file for testing
    dummy_hyle_content = """
    [formulas.tell_joke_success]
    description = "Calculates the success chance of telling a joke."
    expression = "(actor.core.charisma * 1.5) + (actor.personality.extraversion * 0.5)"

    [formulas.intimidate_power]
    description = "Calculates the power of an intimidation attempt."
    expression = "(actor.core.strength + actor.core.composure) / 2"

    [formulas.target_resistance]
    description = "Calculates target's resistance to social actions."
    expression = "target.core.resilience + target.personality.agreeableness"
    """

    with open("dummy_formulas.toml", "w") as f:
        f.write(dummy_hyle_content)

    moirai.load_formulas_from_hyle("dummy_formulas.toml")

    # Create some Eidolons
    alice = Eidolon("Alice", strength=10, charisma=15, openness=80, extraversion=70, resilience=5, agreeableness=10)
    bob = Eidolon("Bob", strength=8, intellect=12, neuroticism=60, resilience=10, agreeableness=50)

    print(f"Alice's charisma: {alice.core_attributes['charisma']}")
    print(f"Alice's extraversion: {alice.personality['extraversion']}")

    try:
        joke_success_score = moirai.evaluate_formula("tell_joke_success", actor=alice)
        print(f"Alice's joke success score: {joke_success_score}")

        intimidate_score = moirai.evaluate_formula("intimidate_power", actor=alice)
        print(f"Alice's intimidate power: {intimidate_score}")

        bob_resistance = moirai.evaluate_formula("target_resistance", actor=alice, target=bob)
        print(f"Bob's resistance: {bob_resistance}")

    except ValueError as e:
        print(e)

    import os
    os.remove("dummy_formulas.toml")
