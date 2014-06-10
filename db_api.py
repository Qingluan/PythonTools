import sqlite3





class SQLiteHelper:
	def __init__(self,db_file_path):
		self.command = {
			insert_co : "insert into %s values %s ",
			select_co : "select %s from %s where %s = %s"
			create_co : "craete table %s "

		}
		self.db_file = db_file_path
	def create_table(self,table_name,*table_keys):
	
		try:
			table_struct = "(" + " ".join(table_keys)+")"
			with sqlite3.connect(self.db_file) as cu:
				cx = cu.cursor()
				table_create = SQLiteHelper.command['create_co']+ table_struct
				cx.excute(table_create %table_name)

		except OperationalError:
			pass
		else:
			return True

			
	def inset_values(self,table_name,*values):
		content_values = "("+" ".join(values) +")"
		try:
			insert_co = self.command['insert_co']%(table_name,content_values)
			