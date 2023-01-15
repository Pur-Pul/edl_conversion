import tkinter as tk
import tkinter.messagebox
import re
from tkinter import filedialog
from .conversion_service import ConversionService

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
        self.locked = True
        
        conversion_service = ConversionService(self.frame)
        conversion_service.convert_file_to_table(self.open_file())
        self.title_list = conversion_service.get_title_list()
        self.clip_num = conversion_service.get_clip_num()
        self.table = conversion_service.get_table()
        self.timecodes = conversion_service.get_timecodes()
        self.table.bind('<<row_removed>>', self.on_row_removal)
        
        self.init_table_ui()
        # starts the mainloop
        self.window.mainloop()

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    
    def on_row_removal(self, event):
        self.clip_num.set(int(self.clip_num.get())-1)

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
    
    def validate(self, var, regex):
        return re.search(regex, var)

    def apply_offset(self, off_vars, fps_var):
        if self.validate(fps_var.get(), "^\d+$") is None:
            tkinter.messagebox.showwarning(title="Alert", message="Given FPS not valid.")
            return
        if self.validate(off_vars[0].get(), "^-?[0-9][0-9]:[0-5][0-9]:[0-5][0-9]:[0-9][0-9]$") is None:
            tkinter.messagebox.showwarning(title="Alert", message="Given source timecode not valid.")
            return
        if self.validate(off_vars[1].get(), "^-?[0-9][0-9]:[0-5][0-9]:[0-5][0-9]:[0-9][0-9]$") is None:
            tkinter.messagebox.showwarning(title="Alert", message="Given destination timecode not valid.")
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

    def init_table_ui(self):
        lower_frame = tk.Frame(self.root)
        lower_frame.pack(side=tk.BOTTOM)

        source_offset_variable = tk.StringVar(lower_frame, value="00:00:00:00")
        dest_offset_variable = tk.StringVar(lower_frame, value="00:00:00:00")
        fps_variable = tk.StringVar(lower_frame, value=24)

        # initializes the entry widget, which displays the amount of clips, as a child of 'frame'
        #self.title_list.lift()
        #self.table.lift()

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

        tk.Button(
            lower_frame,
            text="Apply",
            command = lambda : self.apply_offset((source_offset_variable, dest_offset_variable), fps_variable)
        ).pack(
            side=tk.LEFT
        )

        self.title_list.pack()
        # Initializes the grid of entry widgets, which displays the matrix 'A', as a child of 'frame'
        self.table.pack()
                

if __name__ == "__main__":
    new_ui = UI()
