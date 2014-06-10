import os

class BaseFrame:

	@staticmethod
	def get_command():
		while True:
			try:
				commands = input(">").split()
				if commands[0] == "q":
					print ("bye")
					exit(0)
				print (commands)
				commands = list(map(lambda x: int(x),commands))

				return commands
			except ValueError:
				print("Must be int !!")
				pass
			else :
				break

	def exc(self,call_back,commands):
		return  call_back(commands)


	def interface(self,call_back):
		while True:
			
			flag = self.exc(call_back,BaseFrame.get_command())
			if flag == False:
				break
		

class Cal(BaseFrame):

	def check(self,commands):
		if len(commands) == 1:

			print (commands)
			self.year(commands[0])

		elif len(commands) == 2:
			self.month_search(commands)

		elif len(commands) ==3:
			print ("You will find in follow ")
			tem = list(map((lambda x: str(x) + " "),commands[:2]))
			co = "cal " + " ".join(tem)
			os.system(co)
		else :
			print ("this is a fool argv")

	def year(self,year):
		flag = False
		if year % 100 == 0:
			if year % 400 == 0:
				flag =True
		else  :
			if year %  4 == 0:
				flag = True
		if flag :
			print ("This is 'ruen' year")
		else :
			print ("this is ping year")
		co = "cal " + str(year)
		os.system(co)

	def month_search(self,date):
		year,month = date
		co = "cal "+str(month) + " "+ str(year)
		os.system(co)

	def run (self):
		self.interface(self.check)

if __name__ == "__main__":
	calendar = Cal()
	calendar.run()