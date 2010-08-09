from Tkinter import *
from math import floor

stat = { 0:'str', 1:'agi', 2:'vit', 3:'int', 4:'dex', 5:'luk' }
type = {'normal':48,'transcend':100}

jobsN = {
	'assassin':[6,10,2,4,8,0],
	'priest':[5,4,5,5,4,7]
}

jobsT = {}

class Calc(object):
	
	statVars = {}
	bonusVars = {}
	entries = []
	
	def __init__(self, root):
		frame = Frame(root)
		frame.grid()
		
		for i in stat.keys():
			self.statVars[stat[i]] = StringVar()
			self.statVars[stat[i]].set('1')
			self.bonusVars[stat[i]] = StringVar()
			self.bonusVars[stat[i]].set('0')	
		
		for i in stat.keys():
			Label(frame, text=stat[i].upper()+':').grid(row=i,column=0)
			temp = Entry(frame, width=2,
				textvariable=self.statVars[stat[i]])
			temp.grid(row=i,column=1)
			temp.bind("<KeyRelease>",self.update)
			Label(frame, text='+').grid(row=i,column=2)
			Label(frame,textvariable=self.bonusVars[stat[i]]).grid(
				row=i,column=3)
		
		typePosition = [0,4]
		self.typeVar = IntVar()
		self.typeVar.set(type['normal'])
		for i, item in enumerate(type.keys()):
			Radiobutton(frame, text=item.capitalize(),
				variable=self.typeVar, value=type[item], 
				command=self.update).grid(
				row=typePosition[0],column=typePosition[1]+i)
		
		leftPosition = [7,0]
		Label(frame, text="Stat points:").grid(columnspan=2,
			row=leftPosition[0], column=leftPosition[1])
		self.leftVar = StringVar()
		self.leftVar.set('48')
		Label(frame, textvariable=self.leftVar).grid(
			row=leftPosition[0], column=leftPosition[1]+2,
			columnspan=2)
			
		levelPosition=[4,4]
		Label(frame, text="Base level:").grid(rowspan=2,
			row=levelPosition[0], column=levelPosition[1])
		self.lvlVar = IntVar()
		self.lvlVar.set(1)
		Scale(frame, from_=1, to=99, orient=HORIZONTAL,
			variable=self.lvlVar, command=self.update).grid(
			row=levelPosition[0], column=levelPosition[1]+1,
			rowspan=2)

		jobPosition=[2,4]
		Label(frame,text="Job level:").grid(rowspan=2,
			row=jobPosition[0], column=jobPosition[1])
		self.jobVar = IntVar()
		self.jobVar.set(1)
		Scale(frame, from_=1, to=50, orient=HORIZONTAL,
			variable=self.jobVar, command=self.update).grid(
			row=jobPosition[0], column=jobPosition[1]+1,
			rowspan=2)

	def update(self, event=None):
		self.updateLeft()
		self.updateBonus()
		
	def updateBonus(self):
		for i in stat.keys():
			self.bonusVars[stat[i]].set(jobsN['assassin'][i])

	def updateLeft(self):
		start = self.typeVar.get()
		start += self.baseStatPoints()
		for i in self.statVars.values():
			temp = i.get()
			if temp > '1':
				start -= self.spentStatPoints(int(i.get()))
		self.leftVar.set(str(start))
	
	def spentStatPoints(self, points):
		ret = 0
		for i in range(2,points+1):
			ret += (i-1)/10 + 2
		return ret
		
	def baseStatPoints(self):
		ret = 0
		for i in range(2,self.lvlVar.get()+1):
			ret += floor((i-1)/5)+3
		return int(ret)
		
def main():
	root = Tk()
	calc = Calc(root)
	root.mainloop()
	
if __name__ == '__main__':
	main()
