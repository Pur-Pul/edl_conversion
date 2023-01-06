from .delete_button import DeleteButton
import tkinter as tk

class AdaptiveList:
    def __init__(self, master, frame = None, linked_list = None):
        self.__master = master
        if frame is not None:
            self.__frame = frame
        else:
            self.__frame = tk.Frame(self.__master)
        self.__items = {}
        self.__list_end = 0
        self.__buttons = {}
        self.__linked_list = linked_list

    def add_item(self, item, key = None):
        if key is None:
            key = self.__list_end
        self.__items[key] = item
        if self.__linked_list is not None:
            self.__buttons[key] = DeleteButton(self.__frame, key, self, self.__linked_list)
        self.__list_end += 1

    def set_item(self, key, item):
        self.__items[key] = item
    
    def get_items(self):
        return self.__items
    
    def remove_item(self, key):
        self.__items[key].grid_forget()
        self.frame.event_generate("<<row_removed>>", when="tail")
    
    def clear(self):
        for key in self.__items:
            self.remove_item(key)
        self.__items = {}

    def pack(self):
        self.__frame.pack(side=tk.TOP)
        for i, item in enumerate(self.__items.values()):
            item.grid(column = 0, row = i, sticky = tk.W)
            if self.__buttons.values():
                list(self.__buttons.values())[i].grid(column = 1, row = i, sticky = tk.W)
    
    def __getattr__(self, method_name: str):
        def method(*args, **kwargs):
            return getattr(self.frame, method_name)(*args, **kwargs)
        return method

    @property
    def frame(self):
        return self.__frame

    def __len__(self):
        count = 0
        for item in self.__items.values():
            if item is None:
                continue
            if item.winfo_ismapped():
                count+=1
        return count
