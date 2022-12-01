class Title:
    def __init__(self, string_var):
        self.__string_var = string_var
        setattr(self, 'str_var', string_var.get())

    @property
    def str_var(self):
        return self.__string_var

    @str_var.setter
    def str_var(self, new_string):
        self.__string_var.set(new_string)

    def __len__(self):
        return len(self.str_var.get())
