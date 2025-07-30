import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.frame = ttk.Frame(self.canvas)

        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.grid(row=0, column=1, sticky="ns")

        self.hsb = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.hsb.set)
        self.hsb.grid(row=1, column=0, sticky="ew")

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.window = self.canvas.create_window(0,0, window=self.frame, anchor="nw", tags="self.frame")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_frame_configure(self, event=None):
        #Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event=None):
        #Resize the inner frame to match the canvas
        minWidth = self.frame.winfo_reqwidth()
        minHeight = self.frame.winfo_reqheight()

        if self.winfo_width() >= minWidth:
            newWidth = self.winfo_width()
            #Hide the scrollbar when not needed
            self.hsb.grid_remove()
        else:
            newWidth = minWidth
            #Show the scrollbar when needed
            self.hsb.grid()

        if self.winfo_height() >= minHeight:
            newHeight = self.winfo_height()
            #Hide the scrollbar when not needed
            self.vsb.grid_remove()
        else:
            newHeight = minHeight
            #Show the scrollbar when needed
            self.vsb.grid()

        self.canvas.itemconfig(self.window, width = newWidth, height = newHeight)

    @property
    def content_frame(self):
        return self.frame

def widget_factory(widget_type, parent, **config):
    """Creates and returns a Tkinter widget based on the given type and configuration."""
    widget_classes = {
        "Frame": tk.Frame,
        "Label": tk.Label,
        "Button": tk.Button,
        "Entry": tk.Entry,
        "Text": tk.Text,
        "Checkbutton": tk.Checkbutton,
        "Radiobutton": tk.Radiobutton,
        "Scale": tk.Scale,
        "Canvas": tk.Canvas,
        "Listbox": tk.Listbox,
        "Scrollbar": tk.Scrollbar,
        "Spinbox": tk.Spinbox,
        "Menubutton": tk.Menubutton,
        "Menu": tk.Menu,
        "ttk.Button": ttk.Button,
        "ttk.Entry": ttk.Entry,
        "ttk.Label": ttk.Label,
        "ttk.Frame": ttk.Frame,
        "ttk.Checkbutton": ttk.Checkbutton,
        "ttk.Radiobutton": ttk.Radiobutton,
        "ttk.Scale": ttk.Scale,
        "ttk.Spinbox": ttk.Spinbox,
        "ttk.Combobox": ttk.Combobox,
        "ttk.Notebook": ttk.Notebook,
        "ttk.Progressbar": ttk.Progressbar,
        "ttk.Separator": ttk.Separator,
        "ttk.Sizegrip": ttk.Sizegrip,
        "ttk.Treeview": ttk.Treeview,
        "ttk.Scrollbar": ttk.Scrollbar,
        "ScrollableFrame": ScrollableFrame, # Reference the local ScrollableFrame
    }
    
    widget_class = widget_classes.get(widget_type)
    if widget_class:
        return widget_class(parent, **config)
    else:
        raise ValueError(f"Unknown widget type: {widget_type}")
