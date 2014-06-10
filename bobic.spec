%global commit 7ec26668710de48cd11db491b6a6ecd79b9c8e6d 
%global zipurl https://github.com/D-iii-S/Bobic/archive/%{commit}.zip

Summary: Performance settings suite for measurement computers
Name: bobic
URL: https://github.com/D-iii-S/Bobic
Version: 1.1
Release: 1
License: ASL 2.0
BuildArch: noarch
Source0: %{zipurl}

%description
Performance settings suite for measurement computers

%prep
#Necessary for automatic downloading
cd %{_sourcedir}
wget %{zipurl}
unzip %{SOURCE0}
mv Bobic-%{commit}/* %{_builddir}
cd %{_builddir}

%build

%install
make DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr install

%files
%{_sharedstatedir}/%{name}/reservations
%{_datarootdir}/%{name}/
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.sh

%changelog
* Fri Jun 6 2014 - x (at) 1.1-1
- cpuinfo invalid ht flag check bypassed
