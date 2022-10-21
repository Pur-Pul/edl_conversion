class TimeCode():
    def __init__(self, data, rate):
        self.__origin = data
        self.__framerate = rate
        self.__current_offset = 0
        self.__timecode = [None, None, None, None]
        self.read_origin()
    
    def __str__(self):
        s = ""
        for i in self.__timecode:
            part = str(i)
            if len(part) == 1:
                part = "0"+part
            s+=part+":"
        s = s[:-1]
        return s
    
    def __len__(self):
        return 11

    def change_framerate(self, rate):
        self.__framerate = rate

    def read_origin(self):
        self.__timecode[0] = self.__origin[0] #hour
        self.__timecode[1] = self.__origin[1] #minute
        self.__timecode[2] = self.__origin[2] #second
        self.__timecode[3] = self.__origin[3] #frame

    def push(self, offset):
        self.read_origin()
        cycles=0
        max_vals = [None, 60, 60, self.__framerate]
        for i in reversed(range(0, len(self.__timecode))):
            self.__timecode[i], cycles = self.addition(self.__timecode[i], offset[i]+cycles, max_vals[i])

    def addition(self, value_1, value_2, max_val):
        ret = value_1 + value_2
        cycles=0
        if max_val:
            while ret >= max_val:
                ret -= max_val
                cycles += 1
            while ret < 0:
                ret += max_val
                cycles -= 1
        return (ret, cycles)

if __name__ == "__main__":
    new = TimeCode([10, 45, 55, 23], 24)
    new.push([0, 0, 5, 0])
    