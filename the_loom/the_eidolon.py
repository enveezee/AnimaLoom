"""
The Eidolon: Represents an Agent within the AnimaLoom engine.
This module defines the core structure for any character or entity that can act and be acted upon.
"""

class Eidolon:
    def __init__(self, name: str, **kwargs):
        self.name = name

        # Tier 1: Core Attributes (The Foundation)
        self.core_attributes = {
            "strength": kwargs.get("strength", 0),
            "agility": kwargs.get("agility", 0),
            "intellect": kwargs.get("intellect", 0),
            "charisma": kwargs.get("charisma", 0),
            "resilience": kwargs.get("resilience", 0),
            "passion": kwargs.get("passion", 0),
            "perception": kwargs.get("perception", 0),
            "composure": kwargs.get("composure", 0),
        }

        # Tier 2: Personality & Disposition (The Psyche)
        # Using OCEAN model as a base, values can be -100 to 100 or similar range
        self.personality = {
            "openness": kwargs.get("openness", 0),
            "conscientiousness": kwargs.get("conscientiousness", 0),
            "extraversion": kwargs.get("extraversion", 0),
            "agreeableness": kwargs.get("agreeableness", 0),
            "neuroticism": kwargs.get("neuroticism", 0),
        }

        # Tier 3: Dynamic States & Resources (The Moment)
        self.dynamic_states = {
            "health": kwargs.get("health", 100),
            "stamina": kwargs.get("stamina", 100),
            "social_battery": kwargs.get("social_battery", 100),
            "emotional_state": kwargs.get("emotional_state", "neutral"), # e.g., "joyful", "sad", "angry"
            "sanity": kwargs.get("sanity", 100), # Derived, but can be directly set for testing
        }

        # Tier 4: History & Relationships (The Ledger)
        # Affinity will be a dictionary of dictionaries: {target_eidolon_id: {affinity_type: value}}
        self.affinities = {}
        # Hidden ledger stats
        self.ledger = {
            "trauma": kwargs.get("trauma", 0),
            "secrets": kwargs.get("secrets", []), # List of secret IDs or descriptions
            "grievances": kwargs.get("grievances", {}), # {target_eidolon_id: grievance_score}
            "reputation": kwargs.get("reputation", 0), # Derived, but can be directly set for testing
        }

    def __repr__(self):
        return f"<Eidolon: {self.name}>"

    def update_core_attribute(self, attribute: str, value: int):
        if attribute in self.core_attributes:
            self.core_attributes[attribute] = value
        else:
            raise ValueError(f"Core attribute '{attribute}' not found.")

    def update_dynamic_state(self, state: str, value):
        if state in self.dynamic_states:
            self.dynamic_states[state] = value
        else:
            raise ValueError(f"Dynamic state '{state}' not found.")

    def update_affinity(self, target_eidolon_id: str, affinity_type: str, value: int):
        if target_eidolon_id not in self.affinities:
            self.affinities[target_eidolon_id] = {}
        self.affinities[target_eidolon_id][affinity_type] = value

    def get_affinity(self, target_eidolon_id: str, affinity_type: str):
        return self.affinities.get(target_eidolon_id, {}).get(affinity_type, 0)

    # Placeholder for derived stat calculation (e.g., Sanity, Reputation)
    def calculate_derived_stats(self):
        # Example: Sanity calculation
        self.dynamic_states["sanity"] = (self.core_attributes["resilience"] + self.core_attributes["composure"]) / 2
        # Example: Reputation calculation (simplified)
        self.ledger["reputation"] = self.core_attributes["charisma"] + self.personality["extraversion"] - sum(self.ledger["grievances"].values())

    # More methods will be added here for actions, interactions, etc.
