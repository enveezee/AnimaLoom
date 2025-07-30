import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING, Any, Dict

# Type checking for circular dependency
if TYPE_CHECKING:
    from .the_loomwright_ui_builder import TheLoomwrightUIBuilder
    from the_loom.the_alembic import TheAlembic
    from the_loom.the_moirai import TheMoirai
    from the_loom.the_nexus import TheNexus

class TheLoomwrightHandlers:
    def __init__(
        self,
        builder: "TheLoomwrightUIBuilder",
        alembic: "TheAlembic",
        moirai: "TheMoirai",
        nexus: "TheNexus",
        game_hyle: Dict[str, Any] # This will contain the loaded game_config, characters, cards, etc.
    ):
        self.builder = builder
        self.alembic = alembic
        self.moirai = moirai
        self.nexus = nexus
        self.game_hyle = game_hyle

    def _log(self, message):
        self.builder._log(f"[Handlers] {message}")

    def handle_button_click(self, event=None, widget_name=None):
        self._log(f"Button '{widget_name}' clicked!")

    def handle_key_press(self, event=None, widget_name=None):
        self._log(f"Key '{event.keysym}' pressed in widget '{widget_name}'.")

    def handle_randomize_attributes(self, event=None, widget_name=None):
        self._log("Randomizing attributes...")
        # This handler will need access to the specific Tkinter variables for attributes
        # which are managed by the builder. We need a way to pass these or access them.
        # For now, this is a placeholder.
        messagebox.showinfo("Randomize", "Attribute randomization logic needs to be implemented here, accessing builder.tk_vars.")

    def handle_attribute_change(self, attr_id: str, delta: int, event=None, widget_name=None):
        self._log(f"Changing attribute {attr_id} by {delta}")
        # This handler will also need access to the specific Tkinter variables for attributes.
        messagebox.showinfo("Attribute Change", f"Attribute {attr_id} change logic needs to be implemented here.")

    def handle_load_sample_card(self, event=None, widget_name=None):
        self._log("Loading sample card...")
        # This will load a sample card from the loaded game_hyle (cards.toml)
        # and populate the UI fields via builder.tk_vars.
        if "cards" in self.game_hyle and len(self.game_hyle["cards"]) > 0:
            # Assuming the first card in the Hyle is a sample
            sample_card_id = next(iter(self.game_hyle["cards"])) # Get the first card ID
            card_data = self.game_hyle["cards"][sample_card_id]
            self._log(f"Loaded sample card: {card_data.get('name', sample_card_id)}")
            messagebox.showinfo("Sample Card", f"Loaded sample card: {card_data.get('name', sample_card_id)}. Populate UI fields now.")
            # Logic to populate builder.tk_vars based on card_data goes here
        else:
            messagebox.showwarning("Sample Card", "No sample cards found in the loaded game module.")

    def handle_file_select(self, prop_id: str, event=None, widget_name=None):
        self._log(f"Opening file dialog for {prop_id}...")
        file_path = filedialog.askopenfilename()
        if file_path:
            # This will need to update a specific tk_var in the builder
            # self.builder.tk_vars[f"character_{prop_id}"].set(file_path)
            messagebox.showinfo("File Selected", f"Selected file for {prop_id}: {file_path}")

    def handle_save_card(self, event=None, widget_name=None):
        self._log("Attempting to save card...")
        # This will gather data from builder.tk_vars and use The Alembic to save it.
        messagebox.showinfo("Save Card", "Card saving logic needs to be implemented via The Alembic.")

    def handle_save_character(self, event=None, widget_name=None):
        self._log("Attempting to save character...")
        # This will gather data from builder.tk_vars and use The Alembic to save it.
        messagebox.showinfo("Save Character", "Character saving logic needs to be implemented via The Alembic.")

    # --- New Handlers for The Loomwright Application Flow ---

    def handle_load_module_button_click(self, event=None, widget_name=None):
        self._log("Load Module button clicked.")
        # This will trigger the module loading process in the main Loomwright application.
        # For now, it's a placeholder that would ideally open a dialog or prompt for module name.
        messagebox.showinfo("Load Module", "This button will trigger loading a game module.")

    def handle_create_eidolon_button_click(self, event=None, widget_name=None):
        self._log("Create Eidolon button clicked.")
        # This will trigger Eidolon creation logic in the main Loomwright application.
        messagebox.showinfo("Create Eidolon", "This button will trigger Eidolon creation.")

    def handle_simulate_interaction_button_click(self, event=None, widget_name=None):
        self._log("Simulate Interaction button clicked.")
        # This will trigger interaction simulation logic in the main Loomwright application.
        messagebox.showinfo("Simulate Interaction", "This button will trigger interaction simulation.")
