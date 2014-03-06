import termcolor

class Say(object):
	"""make up a words"""
	say = " say :"
	@staticmethod
	def construct(name,message,time):
		return time +" "+ termcolor.colored( name ,"green" ,attrs=['blink'])+ termcolor.colored(Say.say,"yellow")  + termcolor.colored(message,"magenta") 