import time
import fcntl
import utils

class reservations:

	def __init__(self):
		self.reservations = "/var/lib/bobic/reservations"
		self.rsvnow = "Computer is reserved RIGHT NOW - since {0} till {1} by {2}"
		self.rsvforever = "Computer is reserver RIGHT NOW - since {0} forever by {1}"
		self.rsvfut = "Computer is reserved since {0} till {1} by {2}"
		self.norsv = "No reservations"
		self.rsvd = "Computer is already reserved - since {0} till {1} by {2}"

	def checkreserve(self):
		today = int(time.strftime("%Y%m%d", time.localtime()))
		fd = open(self.reservations, "r+")
		fcntl.lockf(fd, fcntl.LOCK_EX)
		events = []
		noreservations = True
		for line in fd:
			pieces = line.strip().split(" ")
			if int(pieces[0]) < today and int(pieces[1]) < today:
				continue
			elif int(pieces[0]) <= today:
				if pieces[1] != "99999999":
					utils.printalert(self.rsvnow.format(pieces[0], pieces[1], pieces[2]))
				else:
					utils.printalert(self.rsvforever.format(pieces[0], pieces[2]))
				noreservations = False
				events.append(pieces)
			else:
				utils.printwarning(self.rsvfut.format(pieces[0], pieces[1], pieces[2]))
				noreservations = False
				events.append(pieces)
		fd.seek(0)
		for ev in events:
			fd.write(ev[0]+" "+ev[1]+" "+ev[2]+"\n")
		fd.truncate()
		fcntl.lockf(fd, fcntl.LOCK_UN)
		fd.close()
		if noreservations:
			print(self.norsv)

	def setreserve(self, username, since="", till=""):
		if since == "":
			since = time.strftime("%Y%m%d", time.localtime())
		if till == "":
			till = "99999999"
		fd = open(self.reservations, "r+")
		fcntl.lockf(fd, fcntl.LOCK_EX)
		for line in fd:
			pieces = line.strip().split(" ")
			if int(pieces[0]) <= int(till) and int(pieces[1]) >= int(since):
				utils.printalert(self.rsvd.format(pieces[0], pieces[1], pieces[2]))
				return
		if username == "":
			username = utils.get_username()
		fd.write(since+" "+till+" "+username+"\n")
		fcntl.lockf(fd, fcntl.LOCK_UN)
		fd.close()

	def unreserve(self, username, since="", till=""):
		if username == "":
			username = utils.get_username()
		fd = open(self.reservations, "r+")
		fcntl.lockf(fd, fcntl.LOCK_EX)
		events = []
		for line in fd:
			pieces = line.strip().split(" ")
			if pieces[0] == since and pieces[1] == till:
				continue
			elif since == "all" and till == "":
				continue
			elif since == "" and till == "" and pieces[2] == username:
				continue
			else:
				events.append(pieces)
		fd.seek(0)
		for ev in events:
			fd.write(ev[0]+" "+ev[1]+" "+ev[2]+"\n")
		fd.truncate()
		fcntl.lockf(fd, fcntl.LOCK_UN)
		fd.close()
