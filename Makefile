PREFIX = /usr/local

all:
	@echo "Nothing to compile."
	@echo "Use target 'install' to install to $(PREFIX)."

install: 
	install -m 755 -d $(DESTDIR)/var/lib/bobic
	install -m 755 -d $(DESTDIR)$(PREFIX)/share/bobic
	install -m 755 -d $(DESTDIR)/etc/profile.d
	
	touch $(DESTDIR)/var/lib/bobic/reservations
	chmod 666 $(DESTDIR)/var/lib/bobic/reservations
	
	install -m 644 bobic.py $(DESTDIR)$(PREFIX)/share/bobic/
	install -m 644 clocksource.py $(DESTDIR)$(PREFIX)/share/bobic/
	install -m 644 frequency.py $(DESTDIR)$(PREFIX)/share/bobic/
	install -m 644 hyperthreading.py $(DESTDIR)$(PREFIX)/share/bobic/
	install -m 644 iptables.py $(DESTDIR)$(PREFIX)/share/bobic/
	install -m 644 last.py $(DESTDIR)$(PREFIX)/share/bobic/
	install -m 644 load.py $(DESTDIR)$(PREFIX)/share/bobic/
	install -m 644 reservations.py $(DESTDIR)$(PREFIX)/share/bobic/
	install -m 644 timeservers.py $(DESTDIR)$(PREFIX)/share/bobic/
	install -m 644 utils.py $(DESTDIR)$(PREFIX)/share/bobic/
	echo "python "$(PREFIX)"/share/bobic/bobic.py rcauto" > bobic.sh
	install -m 644 bobic.sh $(DESTDIR)/etc/profile.d/
	echo -e "python "$(PREFIX)"\x2f\x73\x68\x61\x72\x65\x2f\x62\x6f\x62\x69\x63\x2f\x62\x6f\x62\x69\x63\x2e\x70\x79\x20\x22\x24\x40\x22" > bobic
	install -m 755 bobic $(DESTDIR)$(PREFIX)/bin/
	
uninstall:
	rm -rf $(DESTDIR)$(PREFIX)/share/bobic
	rm -rf $(DESTDIR)$(PREFIX)/lib/bobic
	rm $(DESTDIR)/etc/profile.d/bobic.sh
