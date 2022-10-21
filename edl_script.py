import tkinter as tk
import re
from tkinter import filedialog
from time_code import TimeCode


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

        self.data = None
        self.clipNum = 0
        self.timecodes=[]
        self.init_table_ui(self.convert_file_to_table(self.open_file()))
        # starts the mainloop
        self.window.mainloop()

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.frame.bbox('all'))

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
        # Unique source file names are stored as strings in the list 'names'
        table = []
        names = [""]
        row = []
        for x in lines:
            y = x.split()
            if len(y) == 0:
                continue
            if x.count(':') == 12 and not "*" in y[0]:
                s = y[len(y)-4:len(y)]
                for t in s:
                    parts = t.split(":")
                    self.timecodes.append((len(table), len(row), TimeCode([int(parts[0]),int(parts[1]),int(parts[2]),int(parts[3])], 24)))
                    row.append(self.timecodes[-1][2])
            elif "*" in y[0] and "FROM" in y[1]:
                t=0
                name=""
                for t in range(4, len(y)):
                    if t!=4:
                        name+="_"
                    name+=y[t]

                if name not in names:
                    names.append(name)
                row.append(name)
                table.append(row)
                self.clipNum+=1
                row=[]
        return table
    
    def validate(self, var, regex):
        return re.search(regex, var)

    def apply_offset(self, off_var, fps_var):
        if self.validate(fps_var.get(), "^\d+$") is None:
            tk.messagebox.showwarning(title="Alert", message="Given FPS not valid.")
            return
        if self.validate(off_var.get(), "^-?[0-9][0-9]:[0-5][0-9]:[0-5][0-9]:[0-9][0-9]$") is None:
            tk.messagebox.showwarning(title="Alert", message="Given timecode not valid.")
            return
        parts = off_var.get().split(":")
        sign = 1
        if parts[0][0] == "-":
            parts[0]=parts[0][1:]
            sign = -1
        for i in range(len(parts)):
            parts[i] = int(parts[i])*sign

        for row, col, timecode in self.timecodes:
            timecode.change_framerate(int(fps_var.get()))
            timecode.push(parts)
            self.data[row][col].set(timecode)
    
    def init_table_ui(self, table):
        lower_frame = tk.Frame(self.root)
        lower_frame.pack(side=tk.BOTTOM)

        offset_variable = tk.StringVar(lower_frame)
        fps_variable = tk.StringVar(lower_frame)

        tk.Label(
            lower_frame,
            text="Offset:",
            padx=2
        ).pack(
            side=tk.LEFT
        )

        tk.Entry(
            lower_frame,
            textvariable=offset_variable,
            width=12
        ).pack(
            side=tk.LEFT
        )
        offset_variable.set("00:00:00:00")
        
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
            command = lambda : self.apply_offset(offset_variable, fps_variable)
        ).pack(
            side=tk.LEFT
        )
        
        # initializes the entry widget, which displays the amount of clips, as a child of 'frame'
        clip_text_var = tk.StringVar(self.frame)
        clipNumEntered = tk.Entry(self.frame, width = 12, textvariable=clip_text_var, state="readonly")
        clipNumEntered.grid(column = 0, row = 1,sticky=tk.W)
        clip_text_var.set(self.clipNum)

        # Initializes the grid of entry widgets, which displays the matrix 'A', as a child of 'frame'
        self.data=[None]*len(table)
        for mRow, x in enumerate(table):
            self.data[mRow]=[None]*len(x)
            for mCol, y in enumerate(x):
                self.data[mRow][mCol] = tk.StringVar(self.frame)
                tk.Entry(self.frame, width = len(y)+1, textvariable=self.data[mRow][mCol], state="readonly").grid(column = mCol, row = mRow+2,sticky=tk.W)
                
                self.data[mRow][mCol].set(y)

if __name__ == "__main__":
    new_ui = UI()
