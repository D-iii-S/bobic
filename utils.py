import pwd
import os

def get_username():
	return pwd.getpwuid(os.getuid())[0]

def printwarning(*string):
	res = "\033[94m"
	for s in string:
		res += str(s)
	res += "\033[0m"
	print(res)

def printalert(*string):
	res = "\033[91m"
	for s in string:
		res += str(s)
	res += "\033[0m"
	print(res)

def writetofile(file, value):
	fd = open(file, "w")
	fd.write(str(value))
	fd.close()

def readstrfromfile(file):
	fd = open(file, "r")
	value = fd.read().strip()
	fd.close()
	return value

def readintfromfile(file):
	val = readstrfromfile(file)
	return int(val)

def getfspath(fs):
	fd = open("/etc/mtab", "r")
	for line in fd:
		if len(line) > len(fs) and line[0:len(fs)] == fs:
			pieces = line.split(" ")
			fd.close()
			return pieces[1]
	raise RuntimeError("No "+fs+" mounted.")
