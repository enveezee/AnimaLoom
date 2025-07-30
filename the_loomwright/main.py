import os
import sys
import tkinter as tk
from tkinter import ttk
from typing import Optional

# Add the_loom to the Python path so we can import it
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from the_loom.the_alembic import TheAlembic
from the_loom.the_moirai import TheMoirai
from the_loom.the_nexus import TheNexus
from the_loom.the_eidolon import Eidolon

from ui_components.the_loomwright_ui_builder import TheLoomwrightUIBuilder
from ui_components.the_loomwright_handlers import TheLoomwrightHandlers

class TheLoomwrightApp:
    def __init__(self, master):
        self.master = master
        master.title("AnimaLoom: The Loomwright")
        master.geometry("800x600")

        self.alembic = TheAlembic()
        self.moirai = TheMoirai()
        self.nexus = TheNexus()
        self.game_hyle = {}

        self.ui_builder = TheLoomwrightUIBuilder(master)
        self.ui_builder.pack(fill="both", expand=True)

        self.event_handlers = TheLoomwrightHandlers(
            app=self, # Pass the app instance itself
            builder=self.ui_builder,
            alembic=self.alembic,
            moirai=self.moirai,
            nexus=self.nexus,
            game_hyle=self.game_hyle
        )
        self.ui_builder.set_event_handlers(self.event_handlers)

        # Register dynamic content builders
        # These functions will be called by TheLoomwrightUIBuilder when it encounters a DynamicContentPlaceholder
        # self.ui_builder.register_dynamic_builder("build_character_properties_section", self._build_character_properties_section)
        # self.ui_builder.register_dynamic_builder("build_character_attributes_section", self._build_character_attributes_section)
        # self.ui_builder.register_dynamic_builder("build_card_properties_section", self._build_card_properties_section)

        self.ui_builder.build_ui("main_window.tui")

    def load_game_module(self, module_name: str) -> bool:
        game_module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'game_modules', module_name))
        
        if not os.path.exists(game_module_path):
            print(f"Error: Game module '{module_name}' not found at {game_module_path}")
            return False

        print(f"Loading game module: {module_name} from {game_module_path}")

        # Load game_config.toml
        config_path = os.path.join(game_module_path, "game_config.toml")
        try:
            with open(config_path, 'rb') as f: # tomllib requires binary mode
                self.game_hyle["game_config"] = tomllib.load(f)
            print("game_config.toml loaded.")
        except FileNotFoundError:
            print(f"Warning: game_config.toml not found in {game_module_path}")
        except tomllib.TOMLDecodeError as e:
            print(f"Error decoding game_config.toml: {e}")
            return False

        # Load formulas (The Moirai's Hyle)
        formulas_path = os.path.join(game_module_path, "formulas.toml")
        self.moirai.load_formulas_from_hyle(formulas_path)
        print("formulas.toml loaded.")

        # Load characters (The Alembic's Hyle)
        characters_path = os.path.join(game_module_path, "characters.toml")
        self.alembic.load_hyle_file(characters_path, "characters")
        print("characters.toml loaded.")

        # Load cards (The Alembic's Hyle)
        cards_path = os.path.join(game_module_path, "cards.toml")
        self.alembic.load_hyle_file(cards_path, "cards")
        print("cards.toml loaded.")

        print(f"Module '{module_name}' loaded successfully.")
        return True


    # Placeholder for dynamic content builder functions (will be moved to a separate module later)
    # def _build_character_properties_section(self, parent_frame, properties_config, builder_instance):
    #     # Logic to build character properties UI dynamically
    #     pass

    # def _build_character_attributes_section(self, parent_frame, attributes_config, builder_instance):
    #     # Logic to build character attributes UI dynamically
    #     pass

    # def _build_card_properties_section(self, parent_frame, card_properties_config, builder_instance):
    #     # Logic to build card properties UI dynamically
    #     pass


if __name__ == "__main__":
    root = tk.Tk()
    app = TheLoomwrightApp(root)
    root.mainloop()