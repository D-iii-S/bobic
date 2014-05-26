import utils

class load:

	def __init__(self):
		self.loadavgfile = utils.getfspath("proc") + "/loadavg"
		self.lm = "AVG Load for the last {0} minutes is {1}"

	def avgload(self):
		fd = open(self.loadavgfile, "r")
		content = fd.read()
		pieces = content.split(" ")
		if float(pieces[0]) > 0.15:
			utils.printalert(self.lm.format(1, pieces[0]))
		elif float(pieces[0]) > 0.05:
			utils.printwarning(self.lm.format(1, pieces[0]))
		else:
			print(self.lm.format(1, pieces[0]))

		if float(pieces[1]) > 0.15:
			utils.printalert(self.lm.format(5, pieces[1]))
		elif float(pieces[1]) > 0.05:
			utils.printwarning(self.lm.format(5, pieces[1]))
		else:
			print(self.lm.format(5, pieces[1]))

		if float(pieces[2]) > 0.15:
			utils.printalert(self.lm.format(15, pieces[2]))
		elif float(pieces[2]) > 0.05:
			utils.printwarning(self.lm.format(15, pieces[2]))
		else:
			print(self.lm.format(15, pieces[2]))
		fd.close()
