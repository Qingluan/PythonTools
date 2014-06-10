import re 

class xml:
	tag_pattern = r'(?P<%s><%s>.+?</%s>)'
	@staticmethod 
	def paraTag(content,tag):
		pattern = xml.tag_pattern %(tag,tag,tag)
		res = re.search(re.compile(pattern),content).group(tag)
		return  res
			

