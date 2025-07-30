import tkinter as tk
from tkinter import ttk
from typing import Dict, Any

# Import widget_factory from the same package
from .the_loomwright_widgets import widget_factory

# This function will be registered with TheLoomwrightUIBuilder
def build_character_properties_section(parent_frame: tk.Frame, properties_config: Dict[str, Any], builder_instance: Any):
    builder_instance._log("Building dynamic character properties section...")
    
    # Create a frame to hold the properties, using grid for layout
    properties_frame = ttk.Frame(parent_frame)
    properties_frame.pack(fill="x", padx=5, pady=5)

    row = 0
    for prop_id, prop_data in properties_config.items():
        # Create a sub-frame for each property to manage layout easily
        prop_row_frame = ttk.Frame(properties_frame)
        prop_row_frame.grid(row=row, column=0, sticky="ew", pady=2)
        properties_frame.grid_columnconfigure(0, weight=1)

        label_text = prop_data.get("label", prop_id.replace("_", " ").title()) # Default label from ID
        label = widget_factory("ttk.Label", prop_row_frame, text=f"{label_text}:")
        label.pack(side="left", padx=5, pady=2)

        prop_type = prop_data.get("type", "string")
        prop_var_name = f"character_{prop_id}"
        prop_var = builder_instance._get_or_create_tk_var(prop_var_name, "StringVar", prop_data.get("default", ""))

        if prop_type == "enum":
            widget = widget_factory("ttk.Combobox", prop_row_frame, textvariable=prop_var, values=prop_data.get("options", []))
            widget.pack(side="left", expand=True, fill="x", padx=5, pady=2)
        elif prop_type == "integer":
            widget = widget_factory("ttk.Entry", prop_row_frame, textvariable=prop_var)
            widget.pack(side="left", expand=True, fill="x", padx=5, pady=2)
        elif prop_type == "file_selector":
            entry = widget_factory("ttk.Entry", prop_row_frame, textvariable=prop_var, state="readonly")
            entry.pack(side="left", expand=True, fill="x", padx=5, pady=2)
            # This button needs a handler from TheLoomwrightHandlers
            button = widget_factory("ttk.Button", prop_row_frame, text="Browse", 
                                  command=lambda p=prop_id: builder_instance.event_handlers.handle_file_select(p))
            button.pack(side="left", padx=5, pady=2)
        else:
            widget = widget_factory("ttk.Entry", prop_row_frame, textvariable=prop_var)
            widget.pack(side="left", expand=True, fill="x", padx=5, pady=2)
        
        row += 1

# This function will be registered with TheLoomwrightUIBuilder
def build_character_attributes_section(parent_frame: tk.Frame, attributes_config: Dict[str, Any], builder_instance: Any):
    builder_instance._log("Building dynamic character attributes section...")
    
    attributes_grid = ttk.Frame(parent_frame)
    attributes_grid.pack(fill="x", padx=5, pady=5)

    # Points remaining display (if applicable)
    # This assumes 'point_buy_total' is available in game_config, which needs to be passed via dynamic_data
    point_buy_total = builder_instance._current_dynamic_data.get("game_config", {}).get("character_creation", {}).get("point_buy_total", 40)
    points_remaining_var_name = "points_remaining"
    points_remaining_var = builder_instance._get_or_create_tk_var(points_remaining_var_name, "StringVar", f"Points Remaining: {point_buy_total}")
    
    points_label = widget_factory("ttk.Label", attributes_grid, textvariable=points_remaining_var)
    points_label.grid(row=0, column=0, columnspan=4, sticky="w", padx=5, pady=5)

    row = 1 # Start attributes from row 1
    for attr_id, attr_data in attributes_config.items():
        attr_var_name = f"attr_{attr_id}"
        attr_var = builder_instance._get_or_create_tk_var(attr_var_name, "IntVar", attr_data.get("default", 5))

        label_text = attr_data.get("name", attr_id.replace("_", " ").title()) # Default label from ID
        icon = attr_data.get("icon", "")
        label = widget_factory("ttk.Label", attributes_grid, text=f"{icon} {label_text}:")
        label.grid(row=row, column=0, sticky="w", padx=5, pady=2)

        entry = widget_factory("ttk.Entry", attributes_grid, textvariable=attr_var, width=5, state="readonly")
        entry.grid(row=row, column=1, padx=5, pady=2)

        # Buttons for increment/decrement
        decr_button = widget_factory("ttk.Button", attributes_grid, text="-", width=2,
                                   command=lambda a=attr_id: builder_instance.event_handlers.handle_attribute_change(a, -1))
        decr_button.grid(row=row, column=2, padx=(0, 2), pady=2)
        incr_button = widget_factory("ttk.Button", attributes_grid, text="+", width=2,
                                   command=lambda a=attr_id: builder_instance.event_handlers.handle_attribute_change(a, 1))
        incr_button.grid(row=row, column=3, padx=(2, 0), pady=2)

        row += 1

# This function will be registered with TheLoomwrightUIBuilder
def build_card_properties_section(parent_frame: tk.Frame, card_properties_config: Dict[str, Any], builder_instance: Any):
    builder_instance._log("Building dynamic card properties section...")
    properties_grid = ttk.Frame(parent_frame)
    properties_grid.pack(fill="x", padx=5, pady=5)

    row = 0
    for prop_id, prop_data in card_properties_config.items():
        builder_instance._log(f"Processing card property: {prop_id} (Type: {prop_data.get('type', 'string')})")
        label = widget_factory("ttk.Label", properties_grid, text=f"{prop_data.get('label', prop_id.replace("_", " ").title())}:")
        label.grid(row=row, column=0, sticky="w", padx=5, pady=2)

        prop_type = prop_data.get("type", "string")
        prop_var_name = f"card_{prop_id}"

        if prop_type == "string":
            prop_var = builder_instance._get_or_create_tk_var(prop_var_name, "StringVar")
            widget = widget_factory("ttk.Entry", properties_grid, textvariable=prop_var)
            builder_instance.tk_vars[prop_var_name] = prop_var # Store for direct access
        elif prop_type == "text":
            widget = widget_factory("Text", properties_grid, height=5, width=40)
            builder_instance.widgets[prop_var_name] = widget # Store the Text widget directly
        elif prop_type == "enum":
            prop_var = builder_instance._get_or_create_tk_var(prop_var_name, "StringVar")
            widget = widget_factory("ttk.Combobox", properties_grid, textvariable=prop_var, values=prop_data.get("options", []))
            builder_instance.tk_vars[prop_var_name] = prop_var
        elif prop_type == "list_enum":
            listbox_frame = widget_factory("ttk.Frame", properties_grid)
            listbox_frame.grid(row=row, column=1, sticky="ew", padx=5, pady=2)

            listbox = widget_factory("Listbox", listbox_frame, selectmode="multiple", height=5)
            listbox.pack(side="left", fill="both", expand=True)
            scrollbar = widget_factory("ttk.Scrollbar", listbox_frame, orient="vertical", command=listbox.yview)
            scrollbar.pack(side="right", fill="y")
            listbox.config(yscrollcommand=scrollbar.set)

            for value in prop_data.get("options", []): # Changed from 'values' to 'options' for consistency with enum
                listbox.insert(tk.END, value)

            builder_instance.widgets[prop_var_name] = listbox # Store the listbox widget directly
            widget = listbox_frame # The parent frame for grid placement

        widget.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
        row += 1