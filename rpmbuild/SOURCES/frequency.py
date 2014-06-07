import utils
import os

class frequency:

	def __init__(self):
		self.nodir = "Directory {0} does't exist!"
		self.nocpu = "No cpu in {0} found!"
		self.freqdriver = "Frequency scaling driver is {0}."
		self.cpudetail = "CPUs numbers {0}: {1}"
		self.nocpufreq = "Cpufreq configuration is not available at all!"
		self.udriver = "Unknown cpufreq driver {0}."
		self.tbavail = " Turbo boost available."
		self.tbnavail = " Turbo boost not available."
		self.tbon = " Turbo boost is turned on."
		self.tboff = " Turbo boost is turned off."
		self.allmax = "All {0} online CPUs set to maximum profile."
		self.alluser = "All {0} online CPUs set to userspace governor with maximal speed."
		self.allstable = "All {0} online CPUs set to stable profile. Frequency governor is {1}."
		self.allsaving = "All {0} online CPUs set to saving profile. Frequency governor is {1}."
		self.nstandard = "Non-standard CPU frequency settings."
		self.pcts = " min_perf_pct is {0}, max_perf_pct is {1}."
		self.maxpct100 = "Cannot set max_perf_pct to 100, operation failed!"
		self.minpct100 = "Cannot set min_perf_pct to 100, operation failed!"
		self.minpct0 = "Cannot set min_perf_pct to 0, operation failed!"
		self.nbwrite = "Cannot write {0} to no_turbo file, operation failed!"
		self.bwrite = "Cannot write {0} to boost file, operation failed!"
		self.chgfail = "Can't change {0} to {1}, operation failed!"
		self.unknprof = "Unknown CPU frequency profile!"
		self.userfall = "Performance governor not available, emulating it with userspace."
		self.nperfuser = "No performance nor userspace governor available, operation failed!"
		self.ngovern = "No suitable governor available, operation failed!"

		self.cpucontrolpath = "/devices/system/cpu"
		self.syspath = utils.getfspath("sysfs")
		self.cpusyspath = self.syspath + self.cpucontrolpath
		if not os.path.isdir(self.cpusyspath):
			raise RuntimeError(self.nodir.format(self.cpusyspath))

		self.cpucount = -1
		index = 0
		while True:
			strindex = str(index)
			if os.path.isdir(self.cpusyspath+"/cpu"+strindex):
				index = index + 1
				self.cpucount = index
			else:
				break
		if self.cpucount == -1:
			raise RuntimeError(self.nocpu.format(self.cpusyspath))

	def checkboost(self, scaling_driver):
		''' returns (Boost available, Boost on, max_pct, min_pct) '''
		print(self.freqdriver.format(scaling_driver))

		if scaling_driver == "acpi-cpufreq" or scaling_driver == "powernow-k8" or scaling_driver == "p4-clockmod":
			boostpath = self.cpusyspath + "/cpufreq/boost"
			if os.path.isfile(boostpath):
				boost = utils.readintfromfile(boostpath)
				if boost:
					return (True, True, -1, -1)
				else:
					return (True, False, -1, -1)
			else:
				return (False, False, -1, -1)

		elif scaling_driver == "intel_pstate":
			boostpath = self.cpusyspath + "/intel_pstate"
			if os.path.isdir(boostpath):
				noboost = utils.readintfromfile(boostpath + "/no_turbo")
				max_perf = utils.readintfromfile(boostpath + "/max_perf_pct")
				min_perf = utils.readintfromfile(boostpath + "/min_perf_pct")
				if noboost:
					return (True, False, min_perf, max_perf)
				else:
					return (True, True, min_perf, max_perf)
			else:
				return (False, False, -1, -1)

	def detailed_output(self, summary):
		trimmedlist = []
		newdict = {}
		for item in summary:
			tmphash = ""
			for i in item:
				if i == "scaling_setspeed" and item[i] == -1:
					continue
				elif i != "cpu_number":
					tmphash += ", " + i + " is " + str(item[i])
			trimmedlist.append(tmphash[2:])
			newdict[item["cpu_number"]] = tmphash[2:]
		contingent = set(trimmedlist)

		for ahash in contingent:
			numbers = ""
			for number in newdict:
				if newdict[number] == ahash:
					numbers += ", " + number
			print(self.cpudetail.format(numbers[2:], ahash))

	def getfrequencyscaling(self):
		if not os.path.isdir(self.cpusyspath + "/cpu0/cpufreq"):
			utils.printalert(self.nocpufreq)
			return

		nowarn = True
		summary = []
		overall = ""
		scaling_driver = ""
		governor = ""
		effcpucount = self.cpucount

		for i in range(0, self.cpucount):

			stri = str(i)
			cpupath = self.cpusyspath + "/cpu" + stri + "/cpufreq/"
			onlinefile = self.cpusyspath + "/cpu" + stri + "/online"
			if os.path.isfile(onlinefile):
				online = utils.readintfromfile(onlinefile)
				if online != 1:
					effcpucount -= 1
					continue
			scaling_driver = utils.readstrfromfile(cpupath + "scaling_driver")
			if scaling_driver != "intel_pstate" and scaling_driver != "acpi-cpufreq" and scaling_driver != "powernow-k8" and scaling_driver != "p4-clockmod":
				utils.printalert(self.udriver.format(scaling_driver))
				return
			scaling_governor = utils.readstrfromfile(cpupath + "scaling_governor")
			cpuinfo_max_freq = utils.readintfromfile(cpupath + "cpuinfo_max_freq")
			cpuinfo_min_freq = utils.readintfromfile(cpupath + "cpuinfo_min_freq")
			scaling_max_freq = utils.readintfromfile(cpupath + "scaling_max_freq")
			scaling_min_freq = utils.readintfromfile(cpupath + "scaling_min_freq")
			if scaling_governor == "userspace":
				scaling_setspeed = utils.readintfromfile(cpupath + "scaling_setspeed")
			else:
				scaling_setspeed = -1

			bioslimit = "not set"
			if os.path.exists(cpupath + "bios_limit"):
				if utils.readintfromfile(cpupath + "bios_limit") < utils.readintfromfile(cpupath + "cpuinfo_max_freq"):
					bioslimit = "set"
					nowarn = False

			summary.append({"cpu_number": stri, "scaling_driver": scaling_driver, "scaling_governor": scaling_governor, "cpuinfo_max_freq": cpuinfo_max_freq, "cpuinfo_min_freq": cpuinfo_min_freq, "scaling_max_freq": scaling_max_freq, "scaling_min_freq": scaling_min_freq, "scaling_setspeed": scaling_setspeed, "bioslimit": bioslimit})

			#Maximum settings
			if scaling_governor == "performance" and scaling_max_freq == cpuinfo_max_freq:
				if overall == "maximum" or overall == "":
					overall = "maximum"
				else:
					nowarn = False

			#Userspace maximum settings
			elif scaling_governor == "userspace" and scaling_setspeed == cpuinfo_max_freq:
				if overall == "usermax" or overall == "":
					overall = "usermax"
				else:
					nowarn = False

			#Stable settings
			elif scaling_governor != "performance" and scaling_min_freq == cpuinfo_max_freq:
				if overall == "stable" or overall == "":
					overall = "stable"
				else:
					nowarn = False

				if governor == "" or governor == scaling_governor:
					governor = scaling_governor
				else:
					nowarn = False

			#Saving settings
			elif scaling_governor != "performance" and scaling_min_freq == cpuinfo_min_freq and scaling_max_freq == cpuinfo_max_freq:
				if overall == "saving" or overall == "":
					overall = "saving"
				else:
					nowarn = False

				if governor == "" or governor == scaling_governor:
					governor = scaling_governor
				else:
					nowarn = False

			else:
				nowarn = False

		boostconfig = self.checkboost(scaling_driver)

		#Final evaluation
		if not boostconfig[0]:
			if nowarn:
				if overall == "maximum":
					print(self.allmax.format(effcpucount) + self.tbnavail)
				elif overall == "usermax":
					utils.printwarning(self.alluser.format(effcpucount) + self.tbnavail)
				elif overall == "stable":
					print(self.allstable.format(effcpucount, governor) + self.tbnavail)
				elif overall == "saving":
					print(self.allsaving.format(effcpucount, governor) + self.tbnavail)
				else:
					utils.printalert(self.nstandard + self.tbnavail)
					self.detailed_output(summary)
			else:
				utils.printalert(self.nstandard + self.tbnavail)
				self.detailed_output(summary)
		else:
			if boostconfig[1] and (boostconfig[3] == 100 or boostconfig[3] == -1) and nowarn and overall == "maximum":
				print(self.allmax.format(effcpucount) + self.tbon)
			elif boostconfig[1] and (boostconfig[3] == 100 or boostconfig[3] == -1) and nowarn and overall == "usermax":
				utils.printwarning(self.alluser.format(effcpucount) + self.tbon)
			elif not boostconfig[1] and (boostconfig[3] == 100 or boostconfig[3] == -1) and nowarn and overall == "usermax":
				utils.printwarning(self.alluser.format(effcpucount) + self.tboff)
			elif not boostconfig[1] and ((boostconfig[2] == -1 and boostconfig[3] == -1) or (boostconfig[2] == 100 and boostconfig[3] == 100)) and nowarn and overall == "stable":
				print(self.allstable.format(effcpucount, governor) + self.tboff)
			elif boostconfig[1] and ((boostconfig[2] == -1 and boostconfig[3] == -1) or (boostconfig[2] == 0 and boostconfig[3] == 100)) and nowarn and overall == "saving":
				print(self.allsaving.format(effcpucount, governor) + self.tbon)
			else:
				if boostconfig[1]:
					if boostconfig[2] == -1 and boostconfig[2] == -1:
						utils.printalert(self.nstandard + self.tbon)
					else:
						utils.printalert(self.nstandard + self.tbon + self.pcts.format(boostconfig[2], boostconfig[3]))
				else:
					if boostconfig[2] == -1 and boostconfig[2] == -1:
						utils.printalert(self.nstandard + self.tboff)
					else:
						utils.printalert(self.nstandard + self.tboff + self.pcts.format(boostconfig[2], boostconfig[3]))
				self.detailed_output(summary)

	def setboost(self, driver, mode):

		if driver == "intel_pstate":
			boostdir = self.cpusyspath + "/intel_pstate"
			if not os.path.isdir(boostdir):
				return

			if mode != 1:
				nbvalue = 0
			else:
				nbvalue = 1

			utils.writetofile(boostdir + "/no_turbo", nbvalue)
			if utils.readintfromfile(boostdir + "/no_turbo") != nbvalue:
				utils.printalert(self.nbwrite.format(nbvalue))

			if mode == 2 or mode == 1:
				utils.writetofile(boostdir + "/min_perf_pct", 100)
				if utils.readintfromfile(boostdir + "/min_perf_pct") != 100:
					utils.printalert(self.minpct100)
			else:
				utils.writetofile(boostdir + "/min_perf_pct", 0)
				if utils.readintfromfile(boostdir + "/min_perf_pct") != 0:
					utils.printalert(self.minpct0)

			utils.writetofile(boostdir + "/max_perf_pct", 100)
			if utils.readintfromfile(boostdir + "/max_perf_pct") != 100:
				utils.printalert(self.maxpct100)

		elif driver == "acpi-cpufreq" or driver == "powernow-k8" or driver == "p4-clockmod":
			boostpath = self.cpusyspath + "/cpufreq/boost"
			if not os.path.isfile(boostpath):
				return

			if mode != 1:
				bvalue = 1
			else:
				bvalue = 0

			utils.writetofile(boostpath, bvalue)
			if utils.readintfromfile(boostpath) != bvalue:
				utils.printalert(self.bwrite.format(bvalue))

	def setcpus(self, profile):
		if not os.path.isdir(self.cpusyspath + "/cpu0/cpufreq"):
			utils.printalert(self.nocpufreq)
			return ""

		scaling_driver = ""
		governor = ""

		for i in range(0, self.cpucount):
			stri = str(i)
			cpupath = self.cpusyspath + "/cpu" + stri + "/cpufreq/"
			onlinefile = self.cpusyspath + "/cpu" + stri + "/online"
			if os.path.isfile(onlinefile):
				online = utils.readintfromfile(onlinefile)
				if online != 1:
					continue
			scaling_driver = utils.readstrfromfile(cpupath + "scaling_driver")
			if scaling_driver == "intel_pstate":

				if profile == "maximum":

					utils.writetofile(cpupath + "scaling_governor", "performance")
					if utils.readstrfromfile(cpupath + "scaling_governor") != "performance":
						utils.printalert(self.chgfail.format("scaling_governor", "performance"))
					utils.writetofile(cpupath + "scaling_max_freq", utils.readstrfromfile(cpupath + "cpuinfo_max_freq"))
					if utils.readintfromfile(cpupath + "scaling_max_freq") != utils.readintfromfile(cpupath + "cpuinfo_max_freq"):
						utils.printalert(self.chgfail.format("scaling_max_freq", "cpuinfo_max_freq"))

				elif profile == "stable":

					utils.writetofile(cpupath + "scaling_governor", "powersave")
					if utils.readstrfromfile(cpupath + "scaling_governor") != "powersave":
						utils.printalert(self.chgfail.format("scaling_governor", "powersave"))
					utils.writetofile(cpupath + "scaling_max_freq", utils.readstrfromfile(cpupath + "cpuinfo_max_freq"))
					if utils.readintfromfile(cpupath + "scaling_max_freq") != utils.readintfromfile(cpupath + "cpuinfo_max_freq"):
						utils.printalert(self.chgfail.format("scaling_max_freq", "cpuinfo_max_freq"))
					utils.writetofile(cpupath + "scaling_min_freq", utils.readstrfromfile(cpupath + "cpuinfo_max_freq"))
					if utils.readintfromfile(cpupath + "scaling_min_freq") != utils.readintfromfile(cpupath + "cpuinfo_max_freq"):
						utils.printalert(self.chgfail.format("scaling_min_freq", "cpuinfo_max_freq"))

				elif profile == "saving":

					utils.writetofile(cpupath + "scaling_governor", "powersave")
					if utils.readstrfromfile(cpupath + "scaling_governor") != "powersave":
						utils.printalert(self.chgfail.format("scaling_governor", "powersave"))
					utils.writetofile(cpupath + "scaling_max_freq", utils.readstrfromfile(cpupath + "cpuinfo_max_freq"))
					if utils.readintfromfile(cpupath + "scaling_max_freq") != utils.readintfromfile(cpupath + "cpuinfo_max_freq"):
						utils.printalert(self.chgfail.format("scaling_max_freq", "cpuinfo_max_freq"))
					utils.writetofile(cpupath + "scaling_min_freq", utils.readstrfromfile(cpupath + "cpuinfo_min_freq"))
					if utils.readintfromfile(cpupath + "scaling_min_freq") != utils.readintfromfile(cpupath + "cpuinfo_min_freq"):
						utils.printalert(self.chgfail.format("scaling_min_freq", "cpuinfo_min_freq"))

				else:
					utils.printalert(self.unknprof)

			elif scaling_driver == "acpi-cpufreq" or scaling_driver == "powernow-k8" or scaling_driver == "p4-clockmod":

				governors = utils.readstrfromfile(cpupath + "scaling_available_governors")
				if profile == "maximum":

					if governors.find("performance") != -1:
						utils.writetofile(cpupath + "scaling_governor", "performance")
						if utils.readstrfromfile(cpupath + "scaling_governor") != "performance":
							utils.printalert(self.chgfail.format("scaling_governor", "performance"))

						utils.writetofile(cpupath + "scaling_max_freq", utils.readstrfromfile(cpupath + "cpuinfo_max_freq"))
						if utils.readintfromfile(cpupath + "scaling_max_freq") != utils.readintfromfile(cpupath + "cpuinfo_max_freq"):
							utils.printalert(self.chgfail.format("scaling_max_freq", "cpuinfo_max_freq"))
					elif governors.find("userspace") != -1:
						utils.printwarning(self.userfall)

						utils.writetofile(cpupath + "scaling_governor", "userspace")
						if utils.readstrfromfile(cpupath + "scaling_governor") != "userspace":
							utils.printalert(self.chgfail.format("scaling_governor", "userspace"))

						utils.writetofile(cpupath + "scaling_max_freq", utils.readstrfromfile(cpupath + "cpuinfo_max_freq"))
						if utils.readintfromfile(cpupath + "scaling_max_freq") != utils.readintfromfile(cpupath + "cpuinfo_max_freq"):
							utils.printalert(self.chgfail.format("scaling_max_freq", "cpuinfo_max_freq"))

						utils.writetofile(cpupath + "scaling_setspeed", utils.readstrfromfile(cpupath + "cpuinfo_max_freq"))
						if utils.readintfromfile(cpupath + "scaling_setspeed") != utils.readintfromfile(cpupath + "cpuinfo_max_freq"):
							utils.printalert(self.chgfail.format("scaling_setspeed", "cpuinfo_max_freq"))
					else:
						utils.printalert(self.nperfuser)

				elif profile == "stable":

					matched = False
					for governor in ("powersave", "conservative", "ondemand", "userspace"):
						if governors.find(governor) != -1:
							matched = True
							utils.writetofile(cpupath + "scaling_governor", governor)
							if utils.readstrfromfile(cpupath + "scaling_governor") != governor:
								utils.printalert(self.chgfail.format("scaling_governor", governor))

							utils.writetofile(cpupath + "scaling_max_freq", utils.readstrfromfile(cpupath + "cpuinfo_max_freq"))
							if utils.readintfromfile(cpupath + "scaling_max_freq") != utils.readintfromfile(cpupath + "cpuinfo_max_freq"):
								utils.printalert(self.chgfail.format("scaling_max_freq", "cpuinfo_max_freq"))
							utils.writetofile(cpupath + "scaling_min_freq", utils.readstrfromfile(cpupath + "cpuinfo_max_freq"))
							if utils.readintfromfile(cpupath + "scaling_min_freq") != utils.readintfromfile(cpupath + "cpuinfo_max_freq"):
								utils.printalert(self.chgfail.format("scaling_min_freq", "cpuinfo_max_freq"))

							if governor == "userspace":
								utils.writetofile(cpupath + "scaling_setspeed", utils.readstrfromfile(cpupath + "cpuinfo_max_freq"))
								if utils.readintfromfile(cpupath + "scaling_setspeed") != utils.readintfromfile(cpupath + "cpuinfo_max_freq"):
									utils.printalert(self.chgfail.format("scaling_setspeed", "cpuinfo_max_freq"))
							break
					if not matched:
						utils.printalert(self.ngovern)

				elif profile == "saving":

					matched = False
					for governor in ("powersave", "conservative", "ondemand", "userspace"):
						if governors.find(governor) != -1:
							matched = True
							utils.writetofile(cpupath + "scaling_governor", governor)
							if utils.readstrfromfile(cpupath + "scaling_governor") != governor:
								utils.printalert(self.chgfail.format("scaling_governor", governor))

							utils.writetofile(cpupath + "scaling_max_freq", utils.readstrfromfile(cpupath + "cpuinfo_max_freq"))
							if utils.readintfromfile(cpupath + "scaling_max_freq") != utils.readintfromfile(cpupath + "cpuinfo_max_freq"):
								utils.printalert(self.chgfail.format("scaling_max_freq", "cpuinfo_max_freq"))
							utils.writetofile(cpupath + "scaling_min_freq", utils.readstrfromfile(cpupath + "cpuinfo_min_freq"))
							if utils.readintfromfile(cpupath + "scaling_min_freq") != utils.readintfromfile(cpupath + "cpuinfo_min_freq"):
								utils.printalert(self.chgfail.format("scaling_min_freq", "cpuinfo_min_freq"))

							if governor == "userspace":
								utils.writetofile(cpupath + "scaling_setspeed", utils.readstrfromfile(cpupath + "cpuinfo_min_freq"))
								if utils.readintfromfile(cpupath + "scaling_setspeed") != utils.readintfromfile(cpupath + "cpuinfo_min_freq"):
									utils.printalert(self.chgfail.format("scaling_setspeed", "cpuinfo_min_freq"))
							break
					if not matched:
						utils.printalert(self.ngovern)

				else:
					utils.printalert(self.unknprof)
			else:
				utils.printalert(self.udriver.format(scaling_driver))

		return scaling_driver

	def setfrequencyscaling(self, mode):
		if mode == "maximum":
			self.setboost(self.setcpus(mode), 2)
		elif mode == "stable":
			self.setboost(self.setcpus(mode), 1)
		elif mode == "saving":
			self.setboost(self.setcpus(mode), 0)
		else:
			utils.printalert(self.unknprof)
