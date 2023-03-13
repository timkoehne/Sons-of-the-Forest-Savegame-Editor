from tkinter import ttk
import itertools as it

class TkSearchableCombobox(ttk.Combobox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.popdown = self.tk.call('ttk::combobox::PopdownWindow', self) #get popdownWindow reference 
        self.listbox = self.popdown + '.f.l' #get popdown listbox
        self._bind(('bind', self.listbox), "<KeyPress>", self.popup_key_pressed, None)

    def popup_key_pressed(self, evt):
        values = self.cget("values")
        
        if evt.state == 0: #lowercase
            newval = self.current() + 1
        else: #uppercase
            newval = self.current() - 1
        
        for i in it.chain(range(newval, len(values)), range(0, self.current())):
            if evt.char.lower() == values[i][0].lower():
                self.current(i)
                self.icursor(i)
                if str(evt.widget) == self.listbox:
                    self.tk.eval(evt.widget + ' selection clear 0 end')
                    self.tk.eval(evt.widget + ' selection set ' + str(i))
                    self.tk.eval(evt.widget + ' see ' + str(i))
                return
