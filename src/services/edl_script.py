import tkinter as tk
import re
from tkinter import filedialog
from entities import TimeCode, Title, EntryRow, AdaptiveList

class UI:
    def __init__(self):
        # initializing the rootwindow
        self.window = tk.Tk()
        self.window.minsize(600, 400)
        self.window.title("edl_table")
        
        self.root = tk.Frame(self.window)
        self.root.pack(side=tk.LEFT, fill = tk.BOTH, expand= True)

        # defining the canvas as a child of root
        self.canvas = tk.Canvas(self.root)
        # packs the canvas and expands it so all widgets are visible
        self.canvas.pack(side=tk.TOP, fill='both', expand=True)

        # defining the scrollbar as a child of root and giving it control of the yview of canvas
        self.scrollbar = tk.Scrollbar(self.window, command=self.canvas.yview)

        # center the scrollbar to the right of the rootwindow and expanding the y of the scrollbar to fit with the size of the window
        self.scrollbar.pack(side=tk.RIGHT, fill='y')

        # configuring the yscrollcommand of the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # defining the frame
        self.frame = tk.Frame(self.canvas)

        # the function on_configure will run when event Configure happens, which is after mainloop is initiated.
        self.frame.bind('<Configure>', self.on_configure)

        # creates a window for the frame in the canvas and anchors it to the topleft of the window
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        #self.entries = []
        self.table = None
        self.title_list = None
        self.locked = True
        self.clipNum = 0
        self.timecodes=[[],[]]
        self.convert_file_to_table(self.open_file())
        self.init_table_ui()
        # starts the mainloop
        self.window.mainloop()

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def open_file(self):
        # opens the filebrowser and assgines selected file as a string to variable 'file_path_string'
        self.root.update_idletasks()
        file_path_string = filedialog.askopenfilename()

        # read the file and stores indivudal lines as strings in the list 'lines'
        lines = []
        f = open(file_path_string, "r")
        for x in f:
            lines.append(x)
        f.close()
        return lines

    def convert_file_to_table(self, lines):
        # Filters out relevant data from the strings in 'lines' and adds them to specific cells in the n*5 matrix 'table' where n is the amount of clips.
        # The amount of clips are then stored in the variable clipNum as an integer.
        # Unique source file titles are stored as strings in the list 'titles'
        table = AdaptiveList(self.frame)
        title_list = AdaptiveList(self.frame, linked_list=table)
        table.add_item(None)
        titles = {}
        row = EntryRow(table.frame)
        for index, x in enumerate(lines):
            y = x.split()
            if len(y) == 0:
                continue
            if (x.count(':') == 12 and not "*" in y[0]) and (index != len(lines) and "FROM" in lines[index+1]):
                s = y[len(y)-4:len(y)]
                for t_i, t in enumerate(s):
                    parts = t.split(":")
                    self.timecodes[int(t_i/2)].append((len(table), len(row), TimeCode([int(parts[0]),int(parts[1]),int(parts[2]),int(parts[3])], 24, tk.StringVar(self.frame))))
                    row.add_timecode(self.timecodes[int(t_i/2)][-1][2])
            elif "*" in y[0] and "FROM" in y[1]:
                t=0
                title = ""
                for t in range(4, len(y)):
                    if t != 4:
                        title += "_"
                    title += y[t]

                if title not in titles:
                    titles[title] = Title(tk.StringVar(row.frame, value = title))
                    title_list.add_item(tk.Entry(title_list.frame, textvariable=titles[title].str_var, width=len(titles[title])))

                row.set_title(titles[title])
                table.add_item(row)
                self.clipNum += 1
                row = EntryRow(table.frame)

        self.table = table
        self.title_list = title_list
    
    def validate(self, var, regex):
        return re.search(regex, var)

    def apply_offset(self, off_vars, fps_var):
        if self.validate(fps_var.get(), "^\d+$") is None:
            tk.messagebox.showwarning(title="Alert", message="Given FPS not valid.")
            return
        if self.validate(off_vars[0].get(), "^-?[0-9][0-9]:[0-5][0-9]:[0-5][0-9]:[0-9][0-9]$") is None:
            tk.messagebox.showwarning(title="Alert", message="Given source timecode not valid.")
            return
        if self.validate(off_vars[1].get(), "^-?[0-9][0-9]:[0-5][0-9]:[0-5][0-9]:[0-9][0-9]$") is None:
            tk.messagebox.showwarning(title="Alert", message="Given destination timecode not valid.")
            return
        parts=[[],[]]
        for i, var in enumerate(off_vars):
            parts[i] = var.get().split(":")
            sign = 1
            if parts[i][0][0] == "-":
                parts[i][0]=parts[i][0][1:]
                sign = -1

            for j in range(len(parts[i])):
                parts[i][j] = int(parts[i][j])*sign

            for row, col, timecode in self.timecodes[i]:
                timecode.change_framerate(int(fps_var.get()))
                timecode.push(parts[i])
                timecode.str_var
    '''
    def toggle_lock(self, button):
        state = ""
        if self.locked:
            self.locked = False
            button.configure(text="Lock entries")
            state = "normal"
        else:
            self.locked = True
            button.configure(text="Unlock entries")
            state = "readonly"
        for entry in self.entries:
            entry.configure(state=state)'''
        

    def init_table_ui(self):
        lower_frame = tk.Frame(self.root)
        lower_frame.pack(side=tk.BOTTOM)

        source_offset_variable = tk.StringVar(lower_frame)
        dest_offset_variable = tk.StringVar(lower_frame)
        fps_variable = tk.StringVar(lower_frame)

        tk.Label(
            lower_frame,
            text="Source offset:",
            padx=2
        ).pack(
            side=tk.LEFT
        )

        tk.Entry(
            lower_frame,
            textvariable=source_offset_variable,
            width=12
        ).pack(
            side=tk.LEFT
        )
        source_offset_variable.set("00:00:00:00")

        tk.Label(
            lower_frame,
            text="Destination offset:",
            padx=2
        ).pack(
            side=tk.LEFT
        )

        tk.Entry(
            lower_frame,
            textvariable=dest_offset_variable,
            width=12
        ).pack(
            side=tk.LEFT
        )
        dest_offset_variable.set("00:00:00:00")
        
        tk.Label(
            lower_frame,
            text="FPS:",
            padx=2
        ).pack(
            side=tk.LEFT
        )

        tk.Entry(
            lower_frame,
            textvariable=fps_variable,
            width=2
        ).pack(
            side=tk.LEFT
        )

        fps_variable.set(24)

        tk.Button(
            lower_frame,
            text="Apply",
            command = lambda : self.apply_offset((source_offset_variable, dest_offset_variable), fps_variable)
        ).pack(
            side=tk.LEFT
        )
        
        # initializes the entry widget, which displays the amount of clips, as a child of 'frame'
        clip_text_var = tk.StringVar(self.table.frame)
        clipNumEntered = tk.Entry(self.table.frame, width = 12, textvariable=clip_text_var, state="readonly")
        self.table.set_item(0, clipNumEntered)
        clip_text_var.set(self.clipNum)

        # This button locks/unlocks the entry widgets for editing.
        lock_button = tk.Button(
            lower_frame,
            text="Unlock entries"
        )
        '''
        lock_button.configure(
            command = lambda : self.toggle_lock(lock_button)
        )
        lock_button.pack(
            side=tk.LEFT
        )'''
        self.title_list.pack()
        # Initializes the grid of entry widgets, which displays the matrix 'A', as a child of 'frame'
        self.table.pack()
                

if __name__ == "__main__":
    new_ui = UI()
