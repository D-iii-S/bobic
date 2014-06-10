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
	echo "alias bobic='python "$(PREFIX)"/share/bobic/bobic.py'" > bobic.sh
	echo "python "$(PREFIX)"/share/bobic/bobic.py rc" >> bobic.sh
	install -m 644 bobic.sh $(DESTDIR)/etc/profile.d/bobic.sh
	
uninstall:
	rm -rf $(DESTDIR)$(PREFIX)/share/bobic
	rm -rf $(DESTDIR)$(PREFIX)/lib/bobic
	rm $(DESTDIR)/etc/profile.d/bobic.sh
