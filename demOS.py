from os.path import *
from os import *
import glob

fName = "sample.txt"
print(abspath(fName))
print(basename(r"c:\work\text.txt"))

if (exists(r"c:\python310\python.exe")):
    print(getsize(r"c:\python310\python.exe"))
else:
    print("파일이 존재하지 않습니다.")

print("운영체제명:", name)
print("환경변수:", environ)
system("notepad.exe")

print(glob.glob("*.py"))

for item in glob.glob("*.py"):
    print(item)

