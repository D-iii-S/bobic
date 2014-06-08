# Maintainer: Vojtech Horky <horky@d3s.mff.cuni.cz>
pkgname=bobic
pkgver=1.1
pkgrel=1
pkgdesc="Performance settings suite for measurement computers"
arch=('any')
url="https://github.com/D-iii-S/Bobic"
license=('ASL 2.0')
groups=()
depends=('python>=2.6')
makedepends=('svn')
optdepends=()
provides=()
conflicts=()
replaces=()
backup=()
options=()
install=
changelog=
source=()
noextract=()
sha256sums=() #autofill using updpkgsums

package() {
  svn checkout -r 8 https://github.com/D-iii-S/Bobic
  mkdir -p $pkgdir/var/lib
  mkdir -p $pkgdir/usr/share/bobic
  mkdir -p $pkgdir/etc/profile.d
  mkdir -p $pkgdir/var/lib/bobic
  touch $pkgdir/var/lib/bobic/reservations
  chmod 666 $pkgdir/var/lib/bobic/reservations
  install -m 644 Bobic/trunk/bobic.py $pkgdir/usr/share/bobic/
  install -m 644 Bobic/trunk/clocksource.py $pkgdir/usr/share/bobic/
  install -m 644 Bobic/trunk/frequency.py $pkgdir/usr/share/bobic/
  install -m 644 Bobic/trunk/hyperthreading.py $pkgdir/usr/share/bobic/
  install -m 644 Bobic/trunk/iptables.py $pkgdir/usr/share/bobic/
  install -m 644 Bobic/trunk/last.py $pkgdir/usr/share/bobic/
  install -m 644 Bobic/trunk/load.py $pkgdir/usr/share/bobic/
  install -m 644 Bobic/trunk/reservations.py $pkgdir/usr/share/bobic/
  install -m 644 Bobic/trunk/timeservers.py $pkgdir/usr/share/bobic/
  install -m 644 Bobic/trunk/utils.py $pkgdir/usr/share/bobic/
  install -m 644 Bobic/trunk/bobic.sh $pkgdir/etc/profile.d/
}
