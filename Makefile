all: bobic.py clocksource.py frequency.py hyperthreading.py iptables.py last.py load.py reservations.py timeservers.py utils.py bobic.sh
	
bobic.py clocksource.py frequency.py hyperthreading.py iptables.py last.py load.py reservations.py timeservers.py utils.py bobic.sh:
	svn checkout -r 4 https://github.com/D-iii-S/Bobic
	cp Bobic/trunk/*.py .
	cp Bobic/trunk/bobic.sh bobic.sh
clean:
	rm -f bobic.py clocksource.py frequency.py hyperthreading.py iptables.py last.py load.py reservations.py timeservers.py utils.py bobic.sh
	rm -rf Bobic
install: 
	if [ ! -d /var/lib ]; then mkdir -p /var/lib; fi
	if [ ! -d /usr/share/bobic ]; then mkdir -p /usr/share/bobic; fi
	if [ ! -d /var/lib/bobic ]; then mkdir -p /var/lib/bobic; fi
	touch /var/lib/bobic/reservations
	chmod 666 /var/lib/bobic/reservations
	install -m 644 bobic.py /usr/share/bobic/
	install -m 644 clocksource.py /usr/share/bobic/
	install -m 644 frequency.py /usr/share/bobic/
	install -m 644 hyperthreading.py /usr/share/bobic/
	install -m 644 iptables.py /usr/share/bobic/
	install -m 644 last.py /usr/share/bobic/
	install -m 644 load.py /usr/share/bobic/
	install -m 644 reservations.py /usr/share/bobic/
	install -m 644 timeservers.py /usr/share/bobic/
	install -m 644 utils.py /usr/share/bobic/
	install -m 644 bobic.sh /etc/profile.d/
uninstall:
	rm -rf /usr/share/bobic
	rm -rf /var/lib/bobic
	rm /etc/profile.d/bobic.sh
