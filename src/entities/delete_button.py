import tkinter as tk

class DeleteButton:
    def __init__(self, master, row_idx, master_list, linked_list):
        self.__master = master
        self.__idx = row_idx
        self.__linked_list = linked_list
        self.__master_list = master_list
        self.widget = tk.Button(
            self.__master,
            text="X",
            command = lambda : self.remove()
        )

    def remove(self):
        print(self.__master_list.get_items())
        to_remove = self.__master_list.get_items()[self.__idx].get()
        print("remove: ", to_remove)
        for i, item in self.__linked_list.get_items().items():
            if item.get() == to_remove:
                print(item)
                self.__linked_list.remove_item(i)
        self.__master_list.remove_item(self.__idx)
        self.widget.grid_forget()

    def grid(self, **kwargs):
        self.widget.grid(**kwargs)