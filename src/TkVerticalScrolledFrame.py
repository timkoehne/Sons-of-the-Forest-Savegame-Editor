import tkinter as tk

class TkVerticalScrolledFrame(tk.Frame):
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)
 
        # Create a canvas object and a vertical scrollbar for scrolling it.
        scrollBar = tk.Scrollbar(self, orient="vertical")
        scrollBar.pack(fill="y", side="right", expand=False)
        self.canvas = tk.Canvas(self, highlightthickness=0,
                                yscrollcommand=scrollBar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollBar.config(command = self.canvas.yview)
 
        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = tk.Frame(self.canvas)
        self.interior.bind('<Configure>', self._configureInterior)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor="nw")
        self.canvas.bind('<Configure>', self._configureCanvas)
        self.canvas.bind_all("<MouseWheel>", self._onMousewheel)
        
    def _configureInterior(self, event):
        # Update the scrollbars to match the size of the inner frame.
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width = self.interior.winfo_reqwidth())
        
    def _configureCanvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())
            
    def _onMousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")