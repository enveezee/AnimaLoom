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