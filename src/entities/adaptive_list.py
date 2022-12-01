import tkinter as tk

class AdaptiveList:
    def __init__(self, master, frame = tk.Frame()):
        self.__master = master
        self.__frame = frame
        self.__frame.configure(master=self.__master)
        self.__items = []

    def add_item(self, item):
        self.__items.append(item)

    def set_item(self, row, item):
        self.__items[row] = item
    
    def get_items(self):
        return self.__items
    
    def remove_item(self, index):
        self.__items[index].grid_forget()
        self.__items.pop(index)

    def pack(self):
        self.__frame.pack(side=tk.TOP)
        for i, item in enumerate(self.__items):
            item.grid(column=0, row = i, sticky = tk.W)

    @property
    def frame(self):
        return self.__frame

    def __len__(self):
        return len(self.__items)
