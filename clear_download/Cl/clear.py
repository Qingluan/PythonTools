#!/usr/local/bin/python3


"""
    if you want to load this  ,you should  re-write "tool_re's pattern , ToPATH'
"""
from os import popen 
from os import system
import re,time

class Clear:
    """
        it can auto mv some file type to special file-index 
        ,but if you want to re-load in a new py-file ,you should re-write 
        value of "self.pattern "
    """
    def __init__(self,toPath,filetype):
        self.PATH = "~/Downloads/"
        self.commandDisItems = "ls " + self.PATH
        self.commandMvItem = "mv " + self.PATH 
        self.filetype = filetype
        self.ToPATH = toPath
        self.item_list = popen(self.commandDisItems)

#### this should re-write ######
        self.pattern = re.compile(r'\.tar\.gz$|\.tar\.bz2$')
##### this is some error char maybe in file name #####
        self.error_char = [" ","'","(",")"]
    def check(self,file_name):
        dealed_file_name = file_name
        Ju = True

        replace_list = []
        for i in self.error_char:
            if i in file_name:
                Ju = False
                replace_list.append(i)

        if len(replace_list) != 0:
            for i in replace_list :
                dealed_file_name = self.string_deal(i,dealed_file_name)
        #print(dealed_file_name)
        if self.tool_re(dealed_file_name) :
            return dealed_file_name
        else :
            return False

    def string_deal(self,error,item):
        if error in item:
            tem1 = item.split(error)
            tem2 = list(map((lambda x : x+"\\"+error),tem1))
            tem3 = ""
            for i in tem2 :
                tem3 += i
            file_name = tem3[:-2]
            return file_name


    def tool_re(self,text):
        pattern = self.pattern
        try:
            re.search(pattern,text).group()
            return True
        except AttributeError:
            return False


    def mv_file(self,file_name):
        COMMA = self.commandMvItem + file_name[:-1] + self.ToPATH
        #print(file_name[:-1])  #test
        system (COMMA)
        #print(COMMA) #test
        return True

    def main(self):
        for File in self.item_list:
            if self.check(File) != False:
                Deal_File = self.check(File)
                self.mv_file(Deal_File)
            else:
                pass
        self.finish_check()
    def finish_check(self):
        check_command = "ls " + self.PATH +" |grep " +self.filetype
        check_res = list(popen(check_command))
        if len(check_res) == 0:
            print(self.filetype+"--------- clear ok ")
        else :
            for item in check_res:
                print("error :",item)

if __name__ == "__main__":
    ToPATH = " ~/Downloads/GZ-BZ2/"
    filetype = "tar"
    clear_gz_bz2 = Clear(ToPATH,filetype)
    clear_gz_bz2.main()

