import os
import tkinter as tk
import json
import tomllib # Requires Python 3.11+
from functools import partial
from typing import Dict, Any, Callable, Optional

from .the_loomwright_widgets import widget_factory

class TheLoomwrightUIBuilder(tk.Frame):
    def __init__(self, master, definitions_path="ui_definitions", debug=True, **kwargs):
        super().__init__(master, **kwargs)
        # The definitions_path will now be relative to the main.py of The Loomwright
        self.definitions_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", definitions_path)
        self.widgets = {}
        self.tk_vars = {}
        self.event_handlers: Optional[Any] = None # Will be set by TheLoomwright application
        self.dynamic_builders: Dict[str, Callable] = {} # To register dynamic content builders
        self.debug = debug

    def set_event_handlers(self, handlers_instance: Any):
        self.event_handlers = handlers_instance

    def register_dynamic_builder(self, name: str, builder_func: Callable):
        self.dynamic_builders[name] = builder_func
        self._log(f"Registered dynamic builder: {name}")

    def _log(self, message):
        if self.debug:
            print(f"[TheLoomwrightUIBuilder DEBUG] {message}")

    def _load_definition(self, filename: str) -> Optional[Dict[str, Any]]:
        filepath = os.path.join(self.definitions_path, filename)
        self._log(f"Loading UI definition: {filepath}")
        try:
            if filename.endswith(".jui"): # JSON UI definition
                with open(filepath, 'r') as f:
                    return json.load(f)
            elif filename.endswith(".tui"): # TOML UI definition
                with open(filepath, 'rb') as f: # tomllib requires binary mode
                    return tomllib.load(f)
            else:
                raise ValueError("Unsupported UI definition file extension. Use .jui or .tui")
        except FileNotFoundError:
            self._log(f"Error: UI definition file not found: {filepath}")
            return None
        except (json.JSONDecodeError, tomllib.TOMLDecodeError) as e:
            self._log(f"Error decoding UI definition file {filepath}: {e}")
            return None

    def _create_tk_var(self, var_name: str, var_type: str = "StringVar", initial_value: Any = "") -> tk.Variable:
        self._log(f"Creating Tk var: {var_name} (Type: {var_type}, Initial: {initial_value})")
        if var_name in self.tk_vars:
            self._log(f"Warning: Tk var '{var_name}' already exists. Overwriting.")
        
        var_class = getattr(tk, var_type, None)
        if var_class:
            self.tk_vars[var_name] = var_class(value=initial_value)
            return self.tk_vars[var_name]
        else:
            raise ValueError(f"Unsupported Tkinter variable type: {var_type}")

    def _get_or_create_tk_var(self, var_name: str, var_type: str = "StringVar", initial_value: Any = "") -> tk.Variable:
        if var_name in self.tk_vars:
            return self.tk_vars[var_name]
        return self._create_tk_var(var_name, var_type, initial_value)

    def _process_widget(self, parent: tk.Widget, widget_def: Dict[str, Any]):
        widget_type = widget_def.get("type")
        widget_name = widget_def.get("name")
        
        if not widget_type or not widget_name:
            self._log("Warning: Skipping widget with missing type or name.")
            return

        self._log(f"Processing widget: {widget_name} (Type: {widget_type})")

        config = widget_def.get("config", {})
        layout = widget_def.get("layout", {})
        children = widget_def.get("children", [])
        bindings = widget_def.get("bindings", {})

        # Handle Tkinter variables
        for prop, value in list(config.items()):
            if isinstance(value, str) and value.startswith("tkvar:"):
                var_name = value[len("tkvar:"):]
                var_type = config.pop(f"{prop}_type", "StringVar")
                initial_value = config.pop(f"{prop}_initial", "")
                config[prop] = self._get_or_create_tk_var(var_name, var_type, initial_value)

        # Create the widget
        try:
            if widget_type == "DynamicContentPlaceholder":
                self._process_dynamic_placeholder(parent, widget_def)
                return # Dynamic placeholders don't create a direct Tkinter widget to store
            else:
                widget = widget_factory(widget_type, parent, **config)
                self.widgets[widget_name] = widget
        except (ValueError, tk.TclError) as e:
            self._log(f"Error creating widget '{widget_name}': {e}")
            return

        # Apply layout
        layout_method = next((key for key in ["pack", "grid", "place"] if key in layout), None)
        if layout_method:
            getattr(widget, layout_method)(**layout[layout_method])
        else:
            widget.pack() # Default to pack if no layout specified

        # Apply bindings
        for event_sequence, handler_name in bindings.items():
            if self.event_handlers and hasattr(self.event_handlers, handler_name):
                handler = getattr(self.event_handlers, handler_name)
                if callable(handler):
                    # Use partial to pass widget_name to the handler
                    widget.bind(event_sequence, partial(handler, widget_name=widget_name))
                else:
                    self._log(f"Warning: Event handler '{handler_name}' is not callable.")
            else:
                self._log(f"Warning: Event handler '{handler_name}' not found in registered handlers.")

        # Process children
        for child_def in children:
            self._process_widget(widget, child_def)

    def build_ui(self, filename: str, dynamic_data: Dict[str, Any] = {}):
        self._log(f"Building UI from {filename}")
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        self.widgets.clear()
        self.tk_vars.clear()

        ui_definition = self._load_definition(filename)
        if ui_definition:
            # Pass dynamic_data to the dynamic content builders
            self._current_dynamic_data = dynamic_data # Store for access by dynamic builders
            for widget_def in ui_definition.get("widgets", []):
                self._process_widget(self, widget_def)
        self.master.update_idletasks()
        self._log("UI build complete.")

    def _process_dynamic_placeholder(self, parent: tk.Widget, widget_def: Dict[str, Any]):
        self._log(f"Processing dynamic placeholder: {widget_def.get('name')}")
        config = widget_def.get("config", {})
        builder_function_name = config.get("builder_function")
        data_key = config.get("data_key") # Key to retrieve data from _current_dynamic_data

        if not builder_function_name:
            self._log(f"Warning: DynamicContentPlaceholder '{widget_def.get('name')}' missing builder_function.")
            return

        builder_function = self.dynamic_builders.get(builder_function_name)
        if builder_function and callable(builder_function):
            # Pass the relevant dynamic data to the builder function
            data_for_builder = self._current_dynamic_data.get(data_key, {}) if data_key else self._current_dynamic_data
            
            # If the parent has a content_frame (like ScrollableFrame), use it
            if hasattr(parent, 'content_frame'):
                builder_function(parent.content_frame, data_for_builder, self)
            else:
                builder_function(parent, data_for_builder, self)
        else:
            self._log(f"Warning: Dynamic builder function '{builder_function_name}' not found or not callable.")

    # Removed hardcoded build_character_properties_section, build_character_attributes_section, etc.
    # These will now be external functions registered via register_dynamic_builder
