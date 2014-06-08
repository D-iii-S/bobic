Summary: Performance settings suite for measurement computers
Name: bobic
URL: https://github.com/D-iii-S/Bobic
Version: 1.1
Release: 1
License: ASL 2.0
BuildArch: noarch

%description
Performance settings suite for measurement computers

%prep

%build

%install
svn checkout -r 8 https://github.com/D-iii-S/Bobic
mkdir -p $RPM_BUILD_ROOT/var/lib
mkdir -p $RPM_BUILD_ROOT/usr/share/bobic
mkdir -p $RPM_BUILD_ROOT/etc/profile.d
mkdir -p $RPM_BUILD_ROOT/var/lib/bobic
touch $RPM_BUILD_ROOT/var/lib/bobic/reservations
chmod 666 $RPM_BUILD_ROOT/var/lib/bobic/reservations
install -m 644 Bobic/trunk/bobic.py $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 Bobic/trunk/clocksource.py $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 Bobic/trunk/frequency.py $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 Bobic/trunk/hyperthreading.py $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 Bobic/trunk/iptables.py $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 Bobic/trunk/last.py $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 Bobic/trunk/load.py $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 Bobic/trunk/reservations.py $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 Bobic/trunk/timeservers.py $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 Bobic/trunk/utils.py $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 Bobic/trunk/bobic.sh $RPM_BUILD_ROOT/etc/profile.d/

%files
/var/lib/bobic/reservations
/usr/share/bobic/bobic.py
/usr/share/bobic/clocksource.py
/usr/share/bobic/frequency.py
/usr/share/bobic/hyperthreading.py
/usr/share/bobic/iptables.py
/usr/share/bobic/last.py
/usr/share/bobic/load.py
/usr/share/bobic/reservations.py
/usr/share/bobic/timeservers.py
/usr/share/bobic/utils.py
/usr/share/bobic/bobic.pyc
/usr/share/bobic/clocksource.pyc
/usr/share/bobic/frequency.pyc
/usr/share/bobic/hyperthreading.pyc
/usr/share/bobic/iptables.pyc
/usr/share/bobic/last.pyc
/usr/share/bobic/load.pyc
/usr/share/bobic/reservations.pyc
/usr/share/bobic/timeservers.pyc
/usr/share/bobic/utils.pyc
/usr/share/bobic/bobic.pyo
/usr/share/bobic/clocksource.pyo
/usr/share/bobic/frequency.pyo
/usr/share/bobic/hyperthreading.pyo
/usr/share/bobic/iptables.pyo
/usr/share/bobic/last.pyo
/usr/share/bobic/load.pyo
/usr/share/bobic/reservations.pyo
/usr/share/bobic/timeservers.pyo
/usr/share/bobic/utils.pyo
%config(noreplace) /etc/profile.d/bobic.sh

%changelog
* Fri Jun 6 2014 - x (at) 1.1-1
- cpuinfo invalid ht flag check bypassed
