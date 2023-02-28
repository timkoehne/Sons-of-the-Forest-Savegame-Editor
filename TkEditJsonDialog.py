import tkinter as tk

class TkEditJsonDialog(tk.Toplevel):

    root = None
    
    def on_save(self):
        self.origialText = self.jsonText.get("1.0", tk.END)
        self.destroy()
        
    def on_cancel(self):
        self.destroy()
    
    def show(self):
        self.wm_deiconify()
        self.jsonText.focus_force()
        self.wait_window()
        
        return self.origialText

    def __init__(self, parent, title, text):

        tk.Toplevel.__init__(self, parent)
        
        self.origialText = text
        self.title = title
        
        self.mainFrame = tk.Frame(self, borderwidth=4, relief='ridge')
        self.mainFrame.pack(fill='both', expand=True)

        self.textFrame = tk.Frame(self.mainFrame)
        self.textFrame.pack()
        self.jsonScrollbar = tk.Scrollbar(self.textFrame)
        self.jsonScrollbar.pack(side="right", fill="y")
        self.textVar = tk.StringVar(self)
        self.jsonText = tk.Text(self.textFrame, yscrollcommand=self.jsonScrollbar.set)
        self.jsonText.pack(side="left", expand=True, fill="both")
        self.jsonScrollbar.config(command=self.jsonText.yview)
        self.jsonText.delete("1.0", tk.END)
        self.jsonText.insert(tk.END, text)

        self.buttonFrame = tk.Frame(self.mainFrame)
        self.buttonFrame.pack(side="bottom")
        self.saveButton = tk.Button(self.buttonFrame, text="Save", command=self.on_save)
        self.saveButton.pack(side="left", ipadx=5, ipady=5, padx=5, pady=5)
        self.cancelButton = tk.Button(self.buttonFrame, text="Cancel", command=self.on_cancel)
        self.cancelButton.pack(side="left", ipadx=5, ipady=5, padx=5, pady=5)

