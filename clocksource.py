import os
import utils

class clocksource:
	def __init__(self):
		self.dne = "Directory {0} does't exist!"
		self.ncs = "No clocksource in {0} found."
		self.ncap = "The CPU has not {0} capability!"
		self.clist = "The CPU has {0} capabilities."
		self.csrc = "Clock source number {0} is {1}!"
		self.tscsrc = "Clock source number {0} is tsc."

		self.clocksourcepath = "/devices/system/clocksource"
		self.syspath = utils.getfspath("sysfs")
		self.procpath = utils.getfspath("proc")
		self.cspath = self.syspath + self.clocksourcepath
		if not os.path.isdir(self.cspath):
			raise RuntimeError(self.dne.format(self.cspath))

		self.cscount = -1
		index = 0
		while True:
			strindex = str(index)
			if os.path.isdir(self.cspath+"/clocksource"+strindex):
				index = index + 1
				self.cscount = index
			else:
				break
		if self.cscount == -1:
			raise RuntimeError(self.ncs.format(self.cspath))

	def tsc_check(self):
		basic = False
		available = False
		nonstop = False
		deadline = False
		atomic = False
		fd = open(self.procpath + "/cpuinfo", "r")
		for line in fd:
			if len(line) > 5 and line[0:5] == "flags":
				pieces = line.split(" ")
				for p in pieces:
					if p == "tsc":
						basic = True
					if p == "constant_tsc":
						available = True
					elif p == "tsc_deadline_timer":
						deadline = True
					elif p == "nonstop_tsc":
						nonstop = True
					elif p == "rdtscp":
						atomic = True
		fd.close()
		capabilities = ""
		if not available:
			utils.printalert(self.ncap.format("tsc"))
		else:
			capabilities += ", tsc"

		if not available:
			utils.printalert(self.ncap.format("constant_tsc"))
		else:
			capabilities += ", constant_tsc"

		if not nonstop:
			utils.printwarning(self.ncap.format("nonstop_tsc"))
		else:
			capabilities += ", nonstop_tsc"

		if not deadline:
			utils.printwarning(self.ncap.format("tsc_deadline_timer"))
		else:
			capabilities += ", tsc_deadline_timer"

		if not available:
			utils.printwarning(self.ncap.format("rdtscp"))
		else:
			capabilities += ", rdtscp"

		if capabilities != "":
			print(self.clist.format(capabilities[2:]))

	def checkclocksource(self):
		self.tsc_check()
		for i in range(0, self.cscount):
			stri = str(i)
			val = utils.readstrfromfile(self.cspath + "/clocksource" + stri + "/current_clocksource")
			if val != "tsc":
				utils.printalert(self.csrc.format(stri, val))
			else:
				print(self.tscsrc.format(stri))
