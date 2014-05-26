import sys
from frequency import frequency
from hyperthreading import hyperthreading
from load import load
from clocksource import clocksource
from last import last
from reservations import reservations
from iptables import iptables
from timeservers import timeservers

def manual():
	print("Valid commands are:")
	print("bobic help - list of available commands")
	print("bobic rc - logon script")
	print("bobic setmax - set frequency scaling to maximum profile")
	print("bobic setstable - set frequency scaling to stable profile")
	print("bobic setsaving - set frequency scaling to saving profile")
	print("bobic enableht - enable hyperthreading")
	print("bobic disableht - disable hyperthreading")
	print("bobic reserve [-n name] YYYYMMDD YYYYMMDD - reserve the computer since ... till ... including")
	print("bobic reserve [-n name] YYYYMMDD - reserve the computer for ...")
	print("bobic reserve [-n name] - reserve the computer for today")
	print("bobic unreserve [-n name] YYYYMMDD YYYYMMDD - cancel concrete reservation")
	print("bobic unreserve all - cancel all reservations of all users and names")
	print("bobic unreserve [-n name] - cancel all reservations of current user (name)")
	print("bobic firewall - turn on the firewall")
	print("bobic unfirewall - turn off the firewall")

if len(sys.argv) == 1:
	print("Incorrect BOBIC invocation - to list available command type `bobic help`")
elif sys.argv[1] == "help":
	manual()
elif sys.argv[1] == "rc":
	print("")
	print("BOBIC logon script")
	frequency().getfrequencyscaling()
	hyperthreading().gethyperthreading()
	load().avgload()
	clocksource().checkclocksource()
	last().lastlog()
	timeservers().detect()
	reservations().checkreserve()
	print("To list all available BOBIC commands type `bobic help`")
	print("")
elif sys.argv[1] == "setmax":
	frequency().setfrequencyscaling("maximum")
elif sys.argv[1] == "setstable":
	frequency().setfrequencyscaling("stable")
elif sys.argv[1] == "setsaving":
	frequency().setfrequencyscaling("saving")
elif sys.argv[1] == "enableht":
	hyperthreading().enablehyperthreading()
elif sys.argv[1] == "disableht":
	hyperthreading().disablehyperthreading()
elif sys.argv[1] == "firewall":
	iptables().firewall(True)
elif sys.argv[1] == "unfirewall":
	iptables().firewall(False)
elif sys.argv[1] == "reserve":
	if len(sys.argv) > 3 and sys.argv[2] == "-n":
		if len(sys.argv) == 6:
			reservations().setreserve(sys.argv[3], sys.argv[4], sys.argv[5])
		elif len(sys.argv) == 5:
			reservations().setreserve(sys.argv[3], sys.argv[4])
		elif len(sys.argv) == 4:
			reservations().setreserve(sys.argv[3])
		else:
			print("Incorrect number of parameters")
	else:
		if len(sys.argv) == 4:
			reservations().setreserve("", sys.argv[2], sys.argv[3])
		elif len(sys.argv) == 3:
			reservations().setreserve("", sys.argv[2])
		elif len(sys.argv) == 2:
			reservations().setreserve("")
		else:
			print("Incorrect number of parameters")
elif sys.argv[1] == "unreserve":
	if len(sys.argv) > 3 and sys.argv[2] == "-n":
		if len(sys.argv) == 6:
			reservations().unreserve(sys.argv[3], sys.argv[4], sys.argv[5])
		elif len(sys.argv) == 4:
			reservations().unreserve(sys.argv[3])
		else:
			print("Incorrect number of paramters")
	else:
		if len(sys.argv) == 4:
			reservations().unreserve("", sys.argv[2], sys.argv[3])
		elif len(sys.argv) == 3:
			if sys.argv[2] != "all":
				print("Incorrect parameter for unreserve")
			else:
				reservations().unreserve("", "all")
		elif len(sys.argv) == 2:
			reservations().unreserve("")
		else:
			print("Incorrect number of paramters")
else:
	print("Incorrect BOBIC invocation - to list available command type `bobic help`")
