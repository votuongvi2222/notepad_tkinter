import tkinter
import os	
from tkinter import *
from tkinter import font
from tkinter.messagebox import *
from tkinter.filedialog import *

class MyNotepad:

	__root = Tk()
	# defaul format
	DEFAULT_FONT_SIZE = 11
	DEFAULT_FONT_FAMILY = 'Arial'
	DEFAULT_BG_COLOR = '#ededed'
	DEFAULT_FONT_COLOR = '#6b9dc2'

	# default window width and height
	DEFAULT_WINDOW_WIDTH = 300
	DEFAULT_WINDOW_HEIGHT = 300
	__thisWidth = DEFAULT_WINDOW_WIDTH
	__thisHeight = DEFAULT_WINDOW_HEIGHT
	__thisTextArea = Text(__root, selectbackground='gray', 
								selectforeground='black', 
								undo=True)
	__thisMenuBar = Menu(__root)
	__thisToolBar = Frame(__root, bg='white')
	__thisInfoBox = Frame(__root, bg='#e1e1e1')
	__thisFileMenu = Menu(__thisMenuBar, tearoff=0)
	__thisEditMenu = Menu(__thisMenuBar, tearoff=0)
	__thisHelpMenu = Menu(__thisMenuBar, tearoff=0)
	
	# To add scrollbar
	__thisScrollBar = Scrollbar(__thisTextArea)	
	__file = ''
	__lenCurrentText = 1
	__isSavedFlag = False


	def __init__(self,**kwargs):

		"""
		===================================================
		==				 CONFIG WINDOW					 ==
		===================================================
		"""
		# Set icon
		try:
				self.__root.wm_iconbitmap("icon_img/notepad_pencil.ico")
		except:
				pass

		# Set window size (the default is 300x300)

		try:
			self.__thisWidth = kwargs['width']
		except KeyError:
			pass

		try:
			self.__thisHeight = kwargs['height']
		except KeyError:
			pass

		# Set the window text
		self.__root.title("* Untitled - My Notepad")

		# Center the window
		screenWidth = self.__root.winfo_screenwidth()
		screenHeight = self.__root.winfo_screenheight()
	
		# For left-alling
		left = (screenWidth / 2) - (self.__thisWidth / 2)
		
		# For right-allign
		top = (screenHeight / 2) - (self.__thisHeight /2)
		
		# For top and bottom
		self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth,
											self.__thisHeight,
											left, top))

		# To make the textarea auto resizable
		self.__root.grid_rowconfigure(0, weight=1)
		self.__root.grid_columnconfigure(0, weight=1)

		# Add controls (widget)
		# self.__thisTextArea.grid(sticky = N + E + S + W)
		
		"""
		===================================================
		==				 CONFIG MAIN MENU				 ==
		===================================================
		"""

		################## FILE TAB 
		# To open new file
		self.__thisFileMenu.add_command(label="New",
										command=self.__newFile,
										accelerator='Ctrl+N')	
		self.__root.bind('<Control-n>', self.__newFile)
		
		# To open a already existing file
		self.__thisFileMenu.add_command(label="Open",
										command=self.__openFile,
										accelerator='Ctrl+O')
		self.__root.bind('<Control-o>', self.__openFile)

		self.__thisFileMenu.add_command(label="Save As",
										command=self.__saveAsFile,
										accelerator='Ctrl+Shift+S')
		self.__root.bind('<Control-Shift-s>', self.__saveAsFile)	
		
		# To save current file
		self.__thisFileMenu.add_command(label="Save",
										command=self.__saveFile,
										accelerator='Ctrl+S')
		self.__root.bind('<Control-s>', self.__saveFile)

		# To create a line in the dialog		
		self.__thisFileMenu.add_separator()										
		self.__thisFileMenu.add_command(label="Exit",
										command=self.__quitApplication,
										accelerator ='Ctrl+Q',)
		self.__thisMenuBar.add_cascade(label="File",
									menu=self.__thisFileMenu)	
		

		################## EDIT TAB 
		# To give a feature of cut
		self.__thisEditMenu.add_command(label="Cut",
										command=self.__cut,
										accelerator='Ctrl+X')		
	
		# to give a feature of copy	
		self.__thisEditMenu.add_command(label="Copy",
										command=self.__copy,
										accelerator='Ctrl+C')		
		
		# To give a feature of paste
		self.__thisEditMenu.add_command(label="Paste",
										command=self.__paste,
										accelerator='Ctrl+V')		
		
		# To give a feature of editing
		self.__thisMenuBar.add_cascade(label="Edit",
									menu=self.__thisEditMenu)	

		
		################## HELP/ABOUT TAB 
		# To create a feature of description of the notepad
		self.__thisHelpMenu.add_command(label="About Notepad",
										command=self.__showAbout)
		self.__thisMenuBar.add_cascade(label="Help",
									menu=self.__thisHelpMenu)


		"""
		===================================================
		==				 CONFIG TOOL BAR				 ==
		===================================================
		"""	
		## NEW
		self.__newIcon = PhotoImage(file='icon_img/new.png')
		self.__newBtn = Button(self.__thisToolBar, 
								image=self.__newIcon,
								relief=FLAT, 
								command=self.__newFile, 
								bg='white')
		self.__newBtn.pack(side=LEFT, 
							padx=1, 
							pady=1)
		## OPEN
		self.__openIcon = PhotoImage(file='icon_img/open.png')
		self.__openBtn = Button(self.__thisToolBar, 
								image=self.__openIcon,
								relief=FLAT, 
								command=self.__openFile, 
								bg='white')
		self.__openBtn.pack(side=LEFT, 
							padx=1, 
							pady=1)
		## SAVE
		self.__saveIcon = PhotoImage(file='icon_img/save.png')
		self.__saveBtn = Button(self.__thisToolBar, 
								image=self.__saveIcon,
								relief=FLAT, 
								command=self.__saveFile, 
								bg='white')
		self.__saveBtn.pack(side=LEFT, 
							padx=1, 
							pady=1)
		## EXIT 
		self.__exitIcon = PhotoImage(file='icon_img/exit.png')
		self.__exitBtn = Button(self.__thisToolBar, 
								image=self.__exitIcon,
								relief=FLAT, 
								command=self.__quitApplication, 
								bg='white')
		self.__exitBtn.pack(side=LEFT, 
							padx=1, 
							pady=1)
		self.__thisToolBar.pack(fill='both')
		
		"""
		===================================================
		==			 		TEXTEARE					 ==
		===================================================
		"""	
		self.__root.config(menu=self.__thisMenuBar)

		self.__thisScrollBar.pack(side=RIGHT,
								fill=Y)					
		
		# Scrollbar will adjust automatically according to the content		
		self.__thisTextArea.pack(fill=BOTH, 
								expand=True)

		self.__thisScrollBar.config(command=self.__thisTextArea.yview)	
		self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set,
									background=self.DEFAULT_BG_COLOR,
									foreground=self.DEFAULT_FONT_COLOR,
									font=(self.DEFAULT_FONT_FAMILY, self.DEFAULT_FONT_SIZE))
		
		"""
		===================================================
		==				 CONFIG INFO BOX				 ==
		===================================================
		"""	
		self.__thisTextArea.bindtags(('Text','post-class-bindings', '.', 'all'))
		self.__thisTextArea.bind_class("post-class-bindings", "<KeyPress>", self.__highlight)
		self.__thisTextArea.bind_class("post-class-bindings", "<Button-1>", self.__highlight)
		self.__thisTextArea.tag_configure('current_line',
											background=self.DEFAULT_FONT_COLOR, 
											foreground=self.DEFAULT_BG_COLOR,
											selectbackground=self.DEFAULT_BG_COLOR, 
											selectforeground='black')

		self.__colLabel = Label(self.__thisInfoBox, text='Col: 0', bg='#e1e1e1')
		self.__colLabel.pack(side=RIGHT, padx=1, pady=1)

		self.__rowLabel = Label(self.__thisInfoBox, text='Row: 1', bg='#e1e1e1')
		self.__rowLabel.pack(side=RIGHT, padx=1, pady=1)
		
		self.__thisInfoBox.pack(side=BOTTOM, fill=X)

		# Closing Window Protocol Linking it to our exit Function.
		self.__root.protocol('WM_DELETE_WINDOW', self.__quitApplication)
	
	def __highlight(self, event):
		self.__thisTextArea.tag_remove("current_line", 1.0, "end")
		self.__thisTextArea.tag_add("current_line", "insert linestart", "insert lineend+1c")

		indeces = str(self.__thisTextArea.index(INSERT)).split('.')
		self.__rowLabel.config(text='Row: '+ indeces[0])
		self.__colLabel.config(text='Col: '+ indeces[1])
		self.__thisInfoBox.pack(side=BOTTOM, fill=X)

	def __quitApplication(self):
		lenCheckedText = len(self.__thisTextArea.get('1.0', END))
		choice = None
		# Check whether it has saved if yes then exit else prompt to save it.
		if lenCheckedText == 1 or (self.__isSavedFlag and self.__lenCurrentText == lenCheckedText):
			exit()
			# if file is not existed and something was written
		elif self.__isExisted() and lenCheckedText > 0:
			choice = askyesnocancel("My Notepad's warning", 'Your work is not saved !!\nDo you want to save it ?')
		else:
			print(self.__isExisted())
			print(lenCheckedText, self.__lenCurrentText)
			choice = askyesnocancel("My Notepad's warning", 'Do you want to save your changes to ' + \
				self.__file)
		if choice:
			self.__saveFile()
			self.__root.destroy()
			exit()
		elif choice == None:
			pass
		else:
			self.__root.destroy()
			exit()

	def __showAbout(self):
		showinfo("My Notepad","This is a demo for Notepad using tkinter")

	def __openFile(self, event='o'):
		
		self.__file = askopenfilename(defaultextension=".txt",
									filetypes=[("All Files","*.*"),
										("Text Documents","*.txt")])

		if self.__isExisted():
			
			# no file to open
			self.__file = ''
		else:
			# Try to open the file
			# set the window title
			self.__root.title(os.path.basename(self.__file) + " - Notepad")
			self.__thisTextArea.delete(1.0,END)

			file = open(self.__file,"r")

			self.__thisTextArea.insert(1.0,file.read())

			file.close()
		self.__lenCurrentText = len(self.__thisTextArea.get('1.0', END))
		self.__isSavedFlag = True
		
	def __newFile(self, event='n'):
		self.__root.title("* Untitled - Notepad")
		self.__file = ''
		self.__thisTextArea.delete(1.0,END)

	def __saveFile(self, event='s'):
		self.__isSavedFlag = True
		if self.__isExisted():
			self.__saveAsFile()

		else:
			file = open(self.__file,"w")
			file.write(self.__thisTextArea.get(1.0,END))
			file.close()
		self.lenCurrenText = len(self.__thisTextArea.get('1.0', END))
		
	
	def __isExisted(self):
		return self.__file == ''
	
	def __saveAsFile(self):

		# Save as new file
		self.__file = asksaveasfilename(initialfile='* Untitled.txt',
										defaultextension=".txt",
										filetypes=[("All Files","*.*"),
											("Text Documents","*.txt")])

		if self.__file == "":
			self.__file = ''
		else:
			
			# Try to save the file
			file = open(self.__file,"w")
			file.write(self.__thisTextArea.get(1.0,END))
			file.close()
			
			# Change the window title
			self.__root.title(os.path.basename(self.__file) + " - Notepad")

	def __cut(self, event):
		self.__thisTextArea.event_generate("<<Cut>>")

	def __copy(self, event):
		self.__thisTextArea.event_generate("<<Copy>>")

	def __paste(self, event):
		self.__thisTextArea.event_generate("<<Paste>>")

	def run(self):

		# Run main application
		self.__root.mainloop()

if __name__ == '__main__':
	# Run main application
	notepad = MyNotepad(width=600,height=400)
	notepad.run()
