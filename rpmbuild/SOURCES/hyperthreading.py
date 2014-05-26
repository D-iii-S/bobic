import os
import utils
from frequency import frequency

class hyperthreading:

	def __init__(self):
		self.notonline = "CPU {0} is not on-line"
		self.htna = "Hyper Threading not available"
		self.thna = "Thread can't be enabled"
		self.thnd = "Thread can't be disabled"
		self.nofile = "Online file for the thread doesn't exist"
		self.hta = "Hyperthreading is available"
		self.hte = "Hyperthreading is enabled, all {0} CPUs are online"
		self.htn = "Hyperthreading may not be enabled, {0} of {1} available CPUs are offline"

		freqobj = frequency()
		self.cpucount = freqobj.cpucount
		self.cpucontrolpath = freqobj.cpucontrolpath
		self.procpath = utils.getfspath("proc")
		self.syspath = utils.getfspath("sysfs")
		self.cpusyspath = self.syspath + self.cpucontrolpath
		self.htavailable = False
		fd = open(self.procpath + "/cpuinfo", "r")
		for line in fd:
			if len(line) > 5 and line[0:5] == "flags":
				pieces = line.split(" ")
				for p in pieces:
					if p == "ht":
						self.htavailable = True
		fd.close()

	def allthreadsonline(self):
		if self.htavailable:
			htenabled = 0
		else:
			return 0
		for i in range(0, self.cpucount):
			stri = str(i)
			onlinefile = self.cpusyspath + "/cpu" + stri + "/online"
			if os.path.isfile(onlinefile):
				val = utils.readintfromfile(onlinefile)
				if val == 0:
					utils.printalert(self.notonline.format(stri))
					htenabled += 1
		return htenabled

	def enablehyperthreading(self):
		if not self.htavailable:
			utils.printalert(self.htna)
			return
		for i in range(0, self.cpucount):
			stri = str(i)
			onlinefile = self.cpusyspath + "/cpu" + stri + "/online"
			if os.path.isfile(onlinefile) and utils.readintfromfile(onlinefile) == 0:
				utils.writetofile(onlinefile, 1)
				val = utils.readintfromfile(onlinefile)
				if val != 1:
					utils.printalert(self.thna)
					return

	def disablecpu(self, number):
		stri = str(number)
		onlinefile = self.cpusyspath + "/cpu" + stri + "/online"
		if os.path.isfile(onlinefile):
			utils.writetofile(onlinefile, 0)
			val = utils.readintfromfile(onlinefile)
			if val != 0:
				utils.printalert(self.thnd)
				return
		else:
			utils.printalert(self.nofile)
			return

	def disablehyperthreading(self):
		if not self.htavailable:
			utils.printalert(self.htna)
			return
		corelist = []
		fd = open(self.procpath + "/cpuinfo", "r")
		for line in fd:
			if len(line) > 9 and line[0:9] == "processor":
				pieces = line.split(":")
				cpunumber = pieces[1].strip()
			if len(line) > 7 and line[0:7] == "core id":
				pieces = line.split(":")
				coreid = pieces[1].strip()
				found = False
				for i in corelist:
					if i == coreid:
						found = True
				if not found:
					corelist.append(coreid)
				else:
					self.disablecpu(cpunumber)
		fd.close()

	def gethyperthreading(self):
		if self.htavailable:
			print(self.hta)
			offlines = self.allthreadsonline()
			if offlines == 0:
				print(self.hte.format(self.cpucount))
			else:
				utils.printalert(self.htn.format(offlines, self.cpucount))
		else:
			utils.printwarning(self.htna)
