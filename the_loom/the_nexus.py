"""
The Nexus: Manages the world state and all active Eidolons within the AnimaLoom engine.
This module acts as the central hub for the simulation, holding all instantiated agents and their relationships.
"""

from typing import Dict, Optional
from the_loom.the_eidolon import Eidolon

class TheNexus:
    _instance: Optional["TheNexus"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TheNexus, cls).__new__(cls)
            cls._instance.eidolons: Dict[str, Eidolon] = {}
            cls._instance.time = 0 # Simple time counter
            # Add other global world state variables here
        return cls._instance

    def add_eidolon(self, eidolon: Eidolon):
        if eidolon.name in self.eidolons:
            raise ValueError(f"Eidolon with name {eidolon.name} already exists in The Nexus.")
        self.eidolons[eidolon.name] = eidolon

    def get_eidolon(self, name: str) -> Optional[Eidolon]:
        return self.eidolons.get(name)

    def remove_eidolon(self, name: str):
        if name in self.eidolons:
            del self.eidolons[name]

    def advance_time(self, steps: int = 1):
        self.time += steps
        print(f"Time advanced to: {self.time}")
        # In a real game, this would trigger updates for all eidolons, world events, etc.

    def get_all_eidolons(self) -> Dict[str, Eidolon]:
        return self.eidolons

    def reset(self):
        """Resets the Nexus to its initial state. Useful for starting new simulations."""
        self.eidolons = {}
        self.time = 0

# Example Usage (for testing purposes)
if __name__ == "__main__":
    nexus = TheNexus()
    print(f"Initial Nexus time: {nexus.time}")

    # Create some Eidolons
    alice = Eidolon("Alice", strength=10, charisma=15, openness=80)
    bob = Eidolon("Bob", strength=8, intellect=12, neuroticism=60)

    # Add them to The Nexus
    nexus.add_eidolon(alice)
    nexus.add_eidolon(bob)

    print(f"Eidolons in Nexus: {[e.name for e in nexus.get_all_eidolons().values()]}")

    # Update affinity
    alice.update_affinity(bob.name, "platonic", 50)
    bob.update_affinity(alice.name, "rivalrous", 20)

    print(f"Alice's platonic affinity for Bob: {alice.get_affinity(bob.name, 'platonic')}")
    print(f"Bob's rivalrous affinity for Alice: {bob.get_affinity(alice.name, 'rivalrous')}")

    # Advance time
    nexus.advance_time()
    nexus.advance_time(5)

    # Reset Nexus
    nexus.reset()
    print(f"Nexus after reset: {nexus.get_all_eidolons()}, Time: {nexus.time}")
