%global commit 9e94ddb9f5ff3e437c0d3793bae3d4cdd4ff8ca1
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
