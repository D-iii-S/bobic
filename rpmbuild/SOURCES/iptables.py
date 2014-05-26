import os
import utils

class iptables:
	def __init__(self):
		self.sshenvndef = "SSH_CONNECTION environment variable is not properly set"
		self.ifnotfound = "Interface matching to SSH connection not found"

		try:
			pieces = os.environ["SSH_CONNECTION"].split(" ")
			if len(pieces) != 4:
				raise RuntimeError(self.sshenvndef)
			self.localip = pieces[2]
		except KeyError:
			raise RuntimeError(self.sshenvndef)

	def firewall(self, on):
		fd = os.popen("ip addr")
		found = False
		for line in fd:
			line = line.strip()
			if len(line) > 5 and line[0:5] == "inet ":
				line = line.split(" ")[1]
				pieces = line.split("/")
				if pieces[0] == self.localip:
					found = True
					ipt = os.popen("iptables -F")
					ipt.close()
					if on:
						ipt = os.popen("iptables -A INPUT -s " + line + " -j ACCEPT")
					ipt.close()
		if not found:
			utils.printalert(self.ifnotfound)
		else:
			if on:
				ipt = os.popen("iptables -P INPUT DROP")
			else:
				ipt = os.popen("iptables -P INPUT ACCEPT")
			ipt.close()
		fd.close()
