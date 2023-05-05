import tkinter as tk
class EntryRow:
    def __init__(self, master):
        self.__title = []
        self.__timecodes = []
        self.__row = []
        self.__master = master
        self.__frame = tk.Frame(self.__master)

    def add_timecode(self, timecode):
        self.__timecodes.append(timecode)
        self.construct()

    def set_title(self, title):
        self.__title = [title]
        self.construct()
    
    def get(self):
        return self.__title[0].str_var.get()

    def construct(self):
        for i, item in enumerate(self.__timecodes + self.__title):
            str_var = item.str_var
            if i == len(self):
                self.__row.append(
                    tk.Entry(
                        self.__frame,
                        width = len(str_var.get())+1,
                        textvariable=str_var,
                        state="readonly"
                    )
                )
            else:
                self.__row[i].config(
                    width = len(str_var.get())+1,
                    textvariable=str_var,
                    state="readonly"
                )

    def grid(self,column,row,sticky):
        self.__frame.grid(column=column, row=row, sticky=sticky)
        for item in self.__row:
            item.pack(side = tk.LEFT)
    
    def lift(self):
        for item in self.__row:
            item.lift()

    def __getattr__(self, method_name: str):
        def method(*args, **kwargs):
            return getattr(self.__frame, method_name)(*args, **kwargs)
        return method

    @property
    def frame(self):
        return self.__frame

    def __len__(self):
        return len(self.__row)
