pkgname=openorienteering-mapper
pkgver=git-HEAD
pkgrel=0
pkgdesc="Orienteering map drawing software"
arch=('i686' 'x86_64')
url="http://www.openorienteering.org/apps/mapper/"
license=('GPL3')
depends=('qt5-imageformats' 'qt5-tools' 'proj' 'gdal')
makedepends=('gcc' 'cmake' 'ninja' 'qt5-tools' 'doxygen' 'libcups' 'sqlite' 'qt5-location' 'qt5-sensors' 'qt5-serialport')
install=arch.${pkgname}.install
source=("${pkgname}-${pkgver}.tar.gz"
        'clipper_ver6.4.2.zip')
# Indent to workaround https://github.com/openSUSE/obs-service-set_version/issues/47
   sha256sums=('SKIP'
               'a14320d82194807c4480ce59c98aa71cd4175a5156645c4e2b3edd330b930627')

BRANCH_SUFFIX=${pkgname#openorienteering-mapper}
BRANCH=${BRANCH_SUFFIX#-}

export LANG=C.UTF-8

build()
{
  cd ${srcdir}/${pkgname}-${pkgver}

  rm -rf ${srcdir}/${pkgname}-${pkgver}/build
  mkdir -p ${srcdir}/${pkgname}-${pkgver}/build
  cd ${srcdir}/${pkgname}-${pkgver}/build

  cmake .. \
    -GNinja \
    -DCMAKE_VERBOSE_MAKEFILE=1 \
    -DCMAKE_BUILD_TYPE=Release \
    -DMapper_PACKAGE_NAME=${pkgname} \
    -DMapper_VERSION_DISPLAY="${BRANCH:+${BRANCH} }${pkgver}" \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DMapper_BUILD_CLIPPER=1 \
    -DCLIPPER_SOURCE_DIR=${srcdir} \
    #end
  cmake --build .
}

package()
{
  cd ${srcdir}/${pkgname}-${pkgver}/build
  
  DESTDIR=${pkgdir}/ cmake --build . --target install
  find "${pkgdir}/usr/share/${pkgname}/symbol sets" -name 'COPY_OF*' -delete
  
  if test -n "${BRANCH}" ; then
    echo "Adjusting filenames for ${BRANCH}"
    set -x
    for I in ${pkgdir}/usr/bin/Mapper \
             ${pkgdir}/usr/share/applications/Mapper.desktop \
             ${pkgdir}/usr/share/icons/hicolor/*/apps/Mapper.png \
             ${pkgdir}/usr/share/man/man1/Mapper.1 ; \
      do mv "${I}" "${I%%Mapper*}Mapper${BRANCH_SUFFIX}${I##*/Mapper}" ; \
    done
    mv ${pkgdir}/usr/share/mime/packages/openorienteering-mapper.xml \
       ${pkgdir}/usr/share/mime/packages/${pkgname}.xml
    for I in ${pkgdir}/usr/share/icons/hicolor/*/mimetypes/application-x-openorienteering*.png ; \
      do mv "${I}" "${I%%x-openorienteering*}x-openorienteering${BRANCH_SUFFIX}${I##*x-openorienteering}" ; \
    done
    sed -i -e "s/Mapper/Mapper${BRANCH_SUFFIX}/;/^Name=/s/${BRANCH_SUFFIX}/ (${BRANCH})/" ${pkgdir}/usr/share/applications/Mapper${BRANCH_SUFFIX}.desktop
    sed -i -e "s/\(application\/x-openorienteering\)-\([a-z]*\)/\1-\2;\1${BRANCH_SUFFIX}-\2/g" ${pkgdir}/usr/share/applications/Mapper${BRANCH_SUFFIX}.desktop
    sed -i -e "s/x-openorienteering/x-openorienteering${BRANCH_SUFFIX}/g;s/glob pattern/glob weight=\"49\" pattern/g" ${pkgdir}/usr/share/mime/packages/${pkgname}.xml
    sed -i -e "s/^.B Mapper\$$/.B Mapper${BRANCH_SUFFIX}/" ${pkgdir}/usr/share/man/man1/Mapper${BRANCH_SUFFIX}.1
    set +x
  fi
}
