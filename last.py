import os
import time
import utils

class last:

	def __init__(self):
		self.nolast = "No foreign lastlog"

	def lastlog(self):
		fd = os.popen("last -10 -w -F")
		users = [utils.get_username()]
		nolastlog = True
		for line in fd:
			line = line.strip()
			backup = line
			if line == "":
				break
			pieces = line.split(" ")
			if pieces[0] == "reboot":
				continue
			found = False
			for user in users:
				if user == pieces[0]:
					found = True
					break
			if found:
				continue
			else:
				users.append(pieces[0])
			if line.find("still logged in") > 0:
				nolastlog = False
				utils.printalert(backup)
			else:
				pieces = line.split(" - ")
				line = pieces[len(pieces) - 1]
				pieces = line.split("(")
				line = pieces[0].strip()
				if line == "down" or line == "crash":
					utils.printwarning(backup)
					nolastlog = False
					continue
				logout = time.mktime(time.strptime(line, "%a %b %d %H:%M:%S %Y"))
				actual = time.time()
				delta = actual -logout
				if delta < 86400:
					utils.printwarning(backup)
					nolastlog = False
				else:
					print(backup)
					nolastlog = False
		if nolastlog:
			print(self.nolast)
