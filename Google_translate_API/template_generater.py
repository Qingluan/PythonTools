from record import setting
from record import utils_check
from paraXml import xml

class H:
	template = {
		'h1' :	"<h1>%s</h1>",
		'h2' :	"<h2>%s</h2>",
		'h3' :	"<h3>%s</h3>",
		'h4' :	"<h4>%s</h4>",
	}


	@staticmethod
	def output(Content,type='h1'):
		return H.template[type] % Content

class  Code:
	template = {
		'code' :  "<pre><code>%s</code></pre>",
	}

	@staticmethod
	def output(Content ,type='code'):
		return Code.template[type] % Content

class Symtanc:
	template = {
		'line' : '<hr>',
	}

	@staticmethod
	def output(type='line'):
		return Symtanc.template[type]



############################
############################
############################
# test class  
class  Factory:
	
	def __init__(self,*arguments):
		self.values = arguments
		

	def generater(self):
		files = utils_check.ls_dir()
		t_info = utils_check.get_today_time()
		file_name = setting['dir_path'] + t_info +'.html'
		tem = ""

		if file_name in files:
			name = t_info + ".html"		
			with  open(setting['dir_path']+name) as File:
				file_content = File.read()
				tem = xml.paraTag(file_content,"body")
			tem = tem [len('<body>'):-len('</body>')]
		else :
			tem = ""
		time  , content = self.values[0] , self.values[1]
		tem += H.output(time,type='h2')
		tem += Symtanc.output()
		tem += Code.output(content)
		
		return tem 
