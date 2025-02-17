# Distributed under the terms of the GNU General Public License v2

EAPI=7

DESCRIPTION="LLVMgold plugin symlink for autoloading"
HOMEPAGE="https://llvm.org/"
SRC_URI=""

LICENSE="public-domain"
SLOT="0"
KEYWORDS="*"

RDEPEND="sys-devel/llvm:${PV}[gold]
	!sys-devel/llvm:0"

S=${WORKDIR}

src_install() {
	dodir "/usr/${CHOST}/binutils-bin/lib/bfd-plugins"
	dosym "../../../../lib/llvm/${PV}/$(get_libdir)/LLVMgold.so" \
		"/usr/${CHOST}/binutils-bin/lib/bfd-plugins/LLVMgold.so"
}
