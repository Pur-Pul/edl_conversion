import tkFileDialog
import Tkinter as tk
import ttk

def on_configure(event):
	canvas.configure(scrollregion=canvas.bbox('all'))

#initializing the rootwindow
root = tk.Tk()
root.minsize(600,400)
root.title("edl_table")

#defining the canvas as a child of root
canvas = tk.Canvas(root)

#defining the scrollbar as a child of root and giving it control of the yview of canvas
scrollbar = tk.Scrollbar(root,command = canvas.yview)

#center the scrollbar to the left of the rootwindow and expanding the y of the scrollbar to fit with the size of the window
scrollbar.pack(side=tk.RIGHT, fill='y')

#configuring the yscrollcommand of the canvas
canvas.configure(yscrollcommand = scrollbar.set)

#defining the frame
frame = tk.Frame(canvas)

#the function on_configure will run when event Configure happens, which is after mainloop is initiated.
canvas.bind('<Configure>', on_configure)

#creates a window for the frame in the canvas and anchors it to the topleft of the window
canvas.create_window((0,0), window=frame, anchor='nw')

#opens the filebrowser and assgines selected file as a string to variable 'file_path_string'
file_path_string = tkFileDialog.askopenfilename()

#read the file and stores indivudal lines as strings in the list 'lines'
lines=[]
f = open(file_path_string, "r")
for x in f:
	lines.append(x)
f.close()
A=[]
B=[]

#Filters out relevant data from the strings in 'lines' and adds them to specific cells in the nx5 matrix 'A' where n is the amount of clips. 
#The amount of clips are then stored in the variable clipNum as an integer.
#Unique source file names are stored as strings in the list 'names'
names=[""]
clipNum=0
index=0
for x in lines:
	y = x.split()
	if x.count(':')>=12 and not "*" in y[0] and len(lines) > index+1 and len(lines[index+1].split()) > 0 and '*' in lines[index+1].split()[0] and 'FROM' in lines[index+1].split()[1]:
		B.append(y[len(y)-4])
		B.append(y[len(y)-3])
		B.append(y[len(y)-2])
		B.append(y[len(y)-1])
	elif len(y) > 0 and "*" in y[0] and "FROM" in y[1]:
		t=0
		name=""
		while t < len(y)-4:
			if t==0 or t==len(y)-1:
				name+=y[4+t]
			else:
				name+="_"
				name+=y[4+t]
			t+=1
		for i in names:
			if i==name:
				break;
			if i==names[len(names)-1]:
				names.append(name)
		B.append(name)
		A.append(B)
		B=[]
		clipNum+=1
	index+=1
		
#Initializes the grid of entry widgets, which displays the matrix 'A', as a child of 'frame'
mRow=0
data=[]
for x in A:
	data.append([])
	mCol=0
	for y in x:
		data[mRow].append(tk.StringVar())
		dataEntered = ttk.Entry(frame, width = 15, textvariable = data[mRow][mCol], state = "readonly")
		dataEntered.grid(column = mCol, row = mRow+1)
		data[mRow][mCol].set(y)
		mCol += 1
	mRow += 1


#nameBox=[]
#nName=0
#for x in names:
#	if x != "":
#		nameBox.append(tk.StringVar())
#		nameBoxEntered = ttk.Entry(root, width = 15, textvariable = nameBox[nName], state = "readonly")
#		nameBoxEntered.grid(column = 2+nName, row = mRow+1)
#		nameBox[nName].set(x)
#		nName+=1
#


#initializes the entry widget, which displays the amount of clips, as a child of 'frame'
clipNumBox=tk.StringVar()
clipNumEntered = ttk.Entry(frame, width = 15, textvariable = clipNumBox, state = "readonly")
clipNumEntered.grid(column = 0, row = 0)
clipNumBox.set(clipNum)


#print(A)
#print(names)
#print(clipNum)

#packs the canvas and expands it so all widgets are visible
canvas.pack(side=tk.LEFT, fill='both',expand=True)

#starts the mainloop
root.mainloop()
