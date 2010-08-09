from Tkinter import *
from math import floor
from Tix import *

stat = { 0:'str', 1:'agi', 2:'vit', 3:'int', 4:'dex', 5:'luk' }

type = {
	'normal': {
		'maxJob':50,
		'baseStats':48,
		'jobs': {
			'Assassin':[6,10,2,4,8,0],
			'Priest':[5,4,5,5,4,7]

		},
	},
	'transcend': {
		'maxJob':70,
		'baseStats':100,
		'jobs': {
			'Assassin Cross':[12,12,12,12,12,12],
			'High Priest':[11,11,11,11,11,14]
		}
	}
}

class Calc(object):	
	
	def __init__(self, root):
		
		# WIDGETS PLACEMENT
		statPos= (0,0)
		typePos= (0,4)
		classPos= (1,4)
		basePos= (2,4)
		jobPos= (4,4)
		leftPos= (6,0)
		
		# INIT MAIN WINDOW
		frame = Frame(root)
		frame.grid()
		
		# INIT STATVARS, BONUSVARS
		self.statVars = {} # character's stats
		self.bonusVars = {} # character's job bonuses
		for i in stat.keys():
			self.statVars[stat[i]] = StringVar()
			self.statVars[stat[i]].set('1')
			self.bonusVars[stat[i]] = StringVar()
			self.bonusVars[stat[i]].set('0')

		# INIT OTHERVARS
		self.typeVar = StringVar() # character's type (normal/trans)
		self.classVar = StringVar() # character's class
		self.lvlVar = IntVar() # character's base level
		self.jobVar = IntVar() # character's job level
		self.leftVar = StringVar() # stat points left to use
		self.typeVar.set('normal')
		self.classVar.set('Assassin')
		self.lvlVar.set(1)
		self.jobVar.set(1)
		self.leftVar.set('48')
		self.maxJob = type['normal']['maxJob']
		self.baseStats = type['normal']['baseStats']
		self.lvlStats = 0
		self.usedStats = 0
		
		# STAT ENTRIES, STAT BONUS FIELDS
		for i in stat.keys():
			Label(frame, text=stat[i].upper()+':').grid(
				row=statPos[0]+i,column=statPos[1])
			temp = Entry(frame, width=2,
				textvariable=self.statVars[stat[i]])
			temp.grid(row=statPos[0]+i,column=statPos[1]+1)
			temp.bind("<KeyRelease>",self.switchStat)
			Label(frame, text='+').grid(
				row=statPos[0]+i,column=statPos[1]+2)
			Label(frame,textvariable=self.bonusVars[stat[i]]
			).grid(row=statPos[0]+i,column=statPos[1]+3)
		
		# TYPE CHOICE
		for i, item in enumerate(type.keys()):
			Radiobutton(frame, text=item.capitalize(),
				variable=self.typeVar, value=item, 
				command=self.switchType).grid(
				row=typePos[0],column=typePos[1]+i)
		
		# LEFT STATPOINTS
		Label(frame, text="Stat points:").grid(columnspan=3,
			row=leftPos[0], column=leftPos[1])
		self.left = Label(frame, textvariable=self.leftVar, width=3)
		self.left.grid(row=leftPos[0], column=leftPos[1]+3)
			
		# CLASS COMBOBOX
		self.classes = ComboBox(frame,label="Class: ",
			command=self.switchClass, editable=0, 
			variable=self.classVar)
		self.classes.grid(row=classPos[0],column=classPos[1],
			columnspan=2)

		# JOB LEVEL SCALEBAR
		Label(frame,text="Job level:").grid(rowspan=2,
			row=jobPos[0], column=jobPos[1])
		self.jobScale = Scale(frame, from_=1, to=self.maxJob,
			orient=HORIZONTAL, variable=self.jobVar, 
			command=self.switchJob)
		self.jobScale.grid(
			row=jobPos[0], column=jobPos[1]+1,
			rowspan=2)
		
		# BASE LEVEL SCALEBAR
		Label(frame, text="Base level:").grid(rowspan=2,
			row=basePos[0], column=basePos[1])
		Scale(frame, from_=1, to=99, orient=HORIZONTAL,
			variable=self.lvlVar, command=self.switchBase).grid(
			row=basePos[0], column=basePos[1]+1,
			rowspan=2)



	def switchStat(self, event=None):
		# calculate used stats
		used = 0
		for i in self.statVars.values():
			s = int(i.get())
			if s > 1:
				for j in range(2,s+1):
					used += (j-1)/10 + 2
		self.usedStats = used
	
		#update left stat points
		self.updateLeft()


	def switchType(self, event=None):
		# change max joblvl
		self.maxJob = type[self.typeVar.get()]['maxJob']
		self.jobScale.config(to=self.maxJob)

		# change base stat points
		self.baseStats = type[self.typeVar.get()]['baseStats']

		# update left stat points
		self.updateLeft()

		# fill class list
		lb = self.classes.subwidget("listbox")
		lb.delete(0,END)
		classList = type[self.typeVar.get()]['jobs']
		for item in classList:
			self.classes.insert(END,item)
		self.classVar.set(classList.keys()[0])


	def switchClass(self, event=None):
		# update job bonuses
		self.updateBonuses()


	def switchBase(self, event=None):
		# calculate lvl stats
		lvl = self.lvlVar.get()
		stats = 0
		if lvl > 1:
			for i in range(2,lvl+1):
				stats += floor((i-1)/5+3)
		self.lvlStats = stats

		# update left stat points
		self.updateLeft()


	def switchJob(self, event=None):
		# update job bonuses
		self.updateBonuses()


	def updateLeft(self):
		left = int(self.baseStats+self.lvlStats-self.usedStats)
		self.leftVar.set(str(left))
		if left < 0:
			self.left.config(fg="#ff0000")
		else:
			self.left.config(fg="#000000")

	
	def updateBonuses(self):
		# temporarily only for max job level
		if self.jobVar.get() == self.maxJob:
			cls = self.classVar.get()
			typ = self.typeVar.get()
			bonuses = type[typ]['jobs'][cls]
			for i in stat.keys():
				self.bonusVars[stat[i]].set(bonuses[i])
		else:
			for i in self.bonusVars.values():
				i.set(0)

		
def main():
	root = Tk()
	calc = Calc(root)
	root.mainloop()
	
if __name__ == '__main__':
	main()
