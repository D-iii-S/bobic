import os
import utils

class timeservers:

	def __init__(self):
		self.srvrun = "{0} service running!"
		self.notrunning = "Services {0} are not running"

	def detect(self):
		ntpd = False
		ptpd = False
		chronyd = False
		fd = os.popen("ps -A")
		for line in fd:
			if line.find("ntpd") != -1:
				ntpd = True
			if line.find("ptpd") != -1:
				ptpd = True
			if line.find("chronyd") != -1:
				chronyd = True

		notrunning = ""

		if ntpd:
			utils.printalert(self.srvrun.format("NTPD"))
		else:
			notrunning += ", ntpd"

		if ptpd:
			utils.printalert(self.srvrun.format("PTPD"))
		else:
			notrunning += ", ptpd"

		if chronyd:
			utils.printalert(self.srvrun.format("Chronyd"))
		else:
			notrunning += ", chronyd"

		if notrunning != "":
			print(self.notrunning.format(notrunning[2:]))
