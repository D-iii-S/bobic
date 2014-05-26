Summary: Performance settings suite for benchmarking computers
Name: bobic
Version: 1.0
Release: 1.0
License: Proprietary
BuildArch: noarch
Source0: bobic.py
Source1: clocksource.py
Source2: frequency.py
Source3: hyperthreading.py
Source4: iptables.py
Source5: last.py
Source6: load.py
Source7: reservations.py
Source8: timeservers.py
Source9: utils.py
Source10: bobic.sh

%description
Performance settings suite for benchmarking computers

%prep

%build

%install
mkdir -p $RPM_BUILD_ROOT/var/lib
mkdir -p $RPM_BUILD_ROOT/usr/share/bobic
mkdir -p $RPM_BUILD_ROOT/etc/profile.d
touch $RPM_BUILD_ROOT/var/lib/reservations
chmod 666 $RPM_BUILD_ROOT/var/lib/reservations
install -m 644 %{SOURCE0} $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT/usr/share/bobic/
install -m 644 %{SOURCE9} $RPM_BUILD_ROOT/usr/share/bobic/
install -m 755 %{SOURCE10} $RPM_BUILD_ROOT/etc/profile.d/

%files
/var/lib/reservations
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
/etc/profile.d/bobic.sh
