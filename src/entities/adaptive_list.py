from .delete_button import DeleteButton
import tkinter as tk

class AdaptiveList:
    def __init__(self, master, frame = None, linked_list = None):
        self.__master = master
        if frame is not None:
            self.__frame = frame
        else:
            self.__frame = tk.Frame(self.__master)
        self.__items = []
        self.__buttons = []
        self.__linked_list = linked_list

    def add_item(self, item):
        self.__items.append(item)
        if self.__linked_list is not None:
            self.__buttons.append(DeleteButton(self.__frame, len(self.__buttons), self, self.__linked_list))

    def set_item(self, row, item):
        self.__items[row] = item
    
    def get_items(self):
        return self.__items
    
    def remove_item(self, index):
        self.__items[index].grid_forget()

    def pack(self):
        self.__frame.pack(side=tk.TOP)
        for i, item in enumerate(self.__items):
            item.grid(column = 0, row = i, sticky = tk.W)
            if self.__buttons:
                self.__buttons[i].grid(column = 1, row = i, sticky = tk.W)

    @property
    def frame(self):
        return self.__frame

    def __len__(self):
        count = 0
        for item in self.__items:
            if item is None:
                continue
            if item.winfo_ismapped():
                count+=1
        return count
