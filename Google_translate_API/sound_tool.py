from os import system
#from threading import Thread
#from time import asctime
class Sound:
	def __init__(self,text):
		self.words = text
	def say(self):
		command = "say "+self.words
		system(command)

####################### follow  is for test ###########
"""

class b(Sound):
	def __init__(self,text):
		Sound.__init__(self,text)
		print("ok  this second inherce")
		self.text = text
	def i_print(self):
		print("start reading a words")
		Sound.start(self)
if __name__ == "__main__":
	text  = input(">> ")
	th1 = b(text)
	th1.i_print()
	print(asctime(),text)
	print(asctime(),text)
	print(asctime(),text)
	print(asctime(),text)
	print(asctime(),text)
	print(asctime(),text)

	print(asctime(),text)
	print(asctime(),text)
	print(asctime(),text)
	print(asctime(),text)
	print(asctime(),text)
	print(asctime(),text)
	print(asctime(),text)
	print(asctime(),text)
	print(asctime(),text)
"""