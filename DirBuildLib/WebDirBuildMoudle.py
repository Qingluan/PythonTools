#!/usr/local/bin/python3
from sys import argv
from os import getcwd ,system
from time import asctime
TreePath = getcwd()

class BuildDir:
	def __init__(self):
		self.ProjectName = None
		self.WebName_list =  None
		self.TreePath = getcwd()
		self.argv_list = argv
		print("Creating Web project....")
	def check_argv(self):
		if len(self.argv_list) < 2 :
			raise ValueError("you  should at least input 'one' word to rename project name")
		elif len(self.argv_list) == 2:
			self.ProjectName = self.argv_list[1]
			self.WebName_list = [self.ProjectName]
		else:
			self.ProjectName = self.argv_list[1]
			self.WebName_list = self.argv_list[2:]

	def ProjectBuild(self):
		if self.ProjectName :
			Command = "mkdir " + self.TreePath + "/" +self.ProjectName
			print(Command)
			system(Command)
			
	def WebDirBuild(self,WebName,Path):
		path = Path + "/" + WebName
		Command_1  = "mkdir " + path
		print(Command_1) #test
		system(Command_1)
		webDir = path+"/"
		Command_2 = "mkdir " + webDir + "js"
		system(Command_2)
		print(Command_2) #test
		Command_3 = "mkdir " + webDir + "css"
		system(Command_3)
		print(Command_3) #test
		Command_4 = "mkdir " + webDir + "Less"
		system(Command_4)
		print(Command_4) #test
		Command_5 = "mkdir " + webDir + "html"
		system(Command_5)
		print(Command_5) #test
		Command_7 = 'mkdir ' + webDir + "Res"
		system(Command_7)
		print(Command_7)
		####### for  default index directory ####
		Command_6  = "mkdir " + webDir + "html/index"
		system(Command_6)	
		print(Command_6) #test

		return True

	def Control(self,WebName_list):
		if self.ProjectName  and self.WebName_list :
			self.ProjectBuild()
			for  eachWeb in self.WebName_list :
				sub_path = self.TreePath+"/"+self.ProjectName
				self.WebDirBuild(eachWeb,sub_path)

		else :
			ValueError("you should at least input a 'ProjectName' ")

	def Main(self):
		self.check_argv()
		print("Project Name :",self.ProjectName,"\nWeb list >\t",self.WebName_list)
		self.Control(self.WebName_list)	
		print(asctime())
	
if __name__ == 	"__main__":
	building  =  BuildDir()
	building.Main()



