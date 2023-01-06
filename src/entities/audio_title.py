import tkinter as tk

class Title:
    def __init__(self, master, string_var):
        self.__string_var = string_var
        setattr(self, 'str_var', string_var.get())
        self.widget = tk.Entry(master, textvariable=string_var, width=len(string_var.get()))

    def add_child(self):
        pass

    def __getattr__(self, method_name: str):
        def method(*args, **kwargs):
            return getattr(self.widget, method_name)(*args, **kwargs)
        return method

    @property
    def str_var(self):
        return self.__string_var

    @str_var.setter
    def str_var(self, new_string):
        self.__string_var.set(new_string)

    def __len__(self):
        return len(self.str_var.get())
