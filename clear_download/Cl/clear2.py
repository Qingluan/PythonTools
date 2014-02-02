#!/usr/local/bin/python3

from clear import Clear 
from re import compile

"""
    in clear.py self.pattern is 'self.pattern = re.compile(r'\.tar\.gz$|\.tar\.bz2$')'
"""
class clear_zip(Clear):
    def __init__(self,toPath,filetype):
        Clear.__init__(self,toPath,filetype)
        self.pattern = compile(r'\.dmg$')

if __name__ == "__main__":
    ToPATH = " ~/Downloads/Dmg/"
    filetype = "dmg"
    clear_zip_rar = clear_zip(ToPATH,filetype)
    clear_zip_rar.main()
