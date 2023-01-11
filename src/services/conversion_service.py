from src import AdaptiveList, EntryRow, TimeCode, Title
import tkinter as tk

class ConversionService:
    def __init__(self, frame):
        self._frame = frame
        self._timecodes=[[],[]]
        self._table = AdaptiveList(self._frame)
        self._title_list = AdaptiveList(self._frame, linked_list=self._table)
        self._clip_num_var = tk.StringVar(self._table.frame)
        self._clip_num = 0

    def convert_file_to_table(self, lines):
        # Filters out relevant data from the strings in 'lines' and adds them to specific cells in the n*5 matrix 'table' where n is the amount of clips.
        # The amount of clips are then stored in the variable clip_num.
        # Unique source file titles are stored as strings in the list 'titles'
        self._table.clear()
        self._title_list.clear()
        self._table.add_item(None)
        row = EntryRow(self._table.frame)
        for index, line in enumerate(lines):
            words = line.split()
            if len(words) == 0:
                continue
            if (line.count(':') == 12 and not "*" in words[0]) and (index != len(lines) and "FROM" in lines[index+1]):
                time_strings = words[-4:]
                for time_index, time_string in enumerate(time_strings):
                    parts = time_string.split(":")
                    time_type = int(time_index/2)
                    self._timecodes[time_type].append((len(self._table), len(row), TimeCode([int(parts[0]),int(parts[1]),int(parts[2]),int(parts[3])], 24, tk.StringVar(self._frame))))
                    row.add_timecode(self._timecodes[time_type][-1][2])
            elif "*" in words[0] and "FROM" in words[1]:
                title = ""
                for word_index, word in enumerate(words[4:]):
                    if word_index != 0:
                        title += "_"
                    title += word

                if title not in self._title_list.get_items():
                    self._title_list.add_item(Title(self._title_list.frame,tk.StringVar(row.frame, value = title)), title)

                row.set_title(self._title_list.get_items()[title])
                self._table.add_item(row)
                self._clip_num += 1
                row = EntryRow(self._table.frame)
    
    def get_timecodes(self) -> list:
        return self._timecodes
    
    def get_table(self) -> AdaptiveList:
        return self._table
    
    def get_title_list(self) -> AdaptiveList:
        return self._title_list

    def get_clip_num(self) -> tk.StringVar:
        self._clip_num_var.set(self._clip_num)
        return self._clip_num_var
