# Maintainer: Vojtech Horky <vhotspur@github.com>
pkgname=bobic-git
pkgver=0.0.0
pkgrel=1
pkgdesc="Performance settings suite for measurement computers"
arch=('any')
url="https://github.com/D-iii-S/Bobic"
license=('ASL 2.0')
depends=('python>=2.6')
makedepends=('git')
source=("$pkgname"::'git://github.com/D-iii-S/Bobic.git')
sha256sums=('SKIP')

pkgver() {
	cd "$srcdir/$pkgname"
	# Use the tag of the last commit
	git describe --long --always | sed -E 's/([^-]*-g)/r\1/;s/-/./g'
}

package() {
	cd "$srcdir/$pkgname"
	make PREFIX=/usr DESTDIR="$pkgdir" install
}
