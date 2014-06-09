PREFIX = /usr/local

all:
	@echo "Nothing to compile."
	@echo "Use target 'install' to install to $(PREFIX)."

install: 
	install -d $(DESTDIR)/var/lib/bobic
	install -d $(DESTDIR)$(PREFIX)/share/bobic
	install -d $(DESTDIR)/etc/profile.d
	
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
	install -m 644 bobic.sh $(DESTDIR)/etc/profile.d/
	
uninstall:
	rm -rf /usr/share/bobic
	rm -rf /var/lib/bobic
	rm /etc/profile.d/bobic.sh
