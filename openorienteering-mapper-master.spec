#
# spec file for package openorienteering-mapper-master
#
# Copyright (c) 2014-2020 Kai Pastor
#
# OpenOrienteering is free software.
# https://www.openorienteering.org
#
# This file is geared towards Open Build Service usage.
# - The version is set from obs_service-set_version.
# - Build features are enabled depending on the "branch".
# - Dependency names for Fedora packages are substituted via OBS project config.
# Unless using OBS/osc for building, the resulting spec file in the SRPMS
# provides the best starting point for individual RPM builds.

%global branch master
%global nativename openorienteering-mapper%{?branch:-%{branch}}

%if 0%{?sle_version} && ! 0%{?is_opensuse}
  %bcond_with gdal
%else
  %bcond_without gdal
%endif

# Cf. https://fedoraproject.org/wiki/Changes/CMake_to_do_out-of-source_builds
%global _vpath_builddir .

Name:           openorienteering-mapper%{?branch:-%{branch}}
Version:        git-HEAD
Release:        0
Summary:        Orienteering map drawing software
License:        GPL-3.0
Group:          Productivity/Graphics/Vector Editors
Url:            https://openorienteering.org/apps/mapper

Source0:        %{name}-%{version}.tar.gz
%if 0%{?suse_version}
Source1:        clipper_ver6.4.2.zip
%endif
Source99:       %{name}-rpmlintrc

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  fdupes
BuildRequires:  unzip

BuildRequires:  cups-devel
BuildRequires:  proj
BuildRequires:  zlib-devel

# Substitution for distribution particularities via OBS project configuration
BuildRequires:  distribution-release
%if %{with gdal}
BuildRequires:  gdal
BuildRequires:  libgdal-devel
%endif
BuildRequires:  libproj-devel
BuildRequires:  libqt5-qtbase-devel
BuildRequires:  libqt5-qtimageformats
BuildRequires:  libqt5-qtlocation-devel
BuildRequires:  libqt5-qtsensors-devel
BuildRequires:  libqt5-qtserialport-devel
BuildRequires:  libqt5-qttools-devel
BuildRequires:  libqt5-qttools
BuildRequires:  sqlite3
%if 0%{?suse_version}
BuildRequires:  libqt5-qtbase-private-headers-devel
BuildRequires:  update-desktop-files
%endif
%if 0%{?fedora_version}
BuildRequires:  polyclipping-devel
%if 0%{?fedora_version} > 30
BuildRequires:  qt5-qtbase-private-devel
%if 0%{?fedora_version} > 33
BuildRequires:  libcurl-devel
BuildRequires:  libtiff-devel
BuildRequires:  sqlite-devel
%else
BuildRequires:  proj-datumgrid
%endif
%else
BuildRequires:  proj-epsg
BuildRequires:  proj-nad
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%endif

%if %{with gdal}
Requires:       gdal
%endif
Requires:       libqt5-qtimageformats
Requires:       libqt5-qttools
Requires:       libqt5-qttranslations

%description
OpenOrienteering Mapper is an orienteering map drawing software.
It comes with predefined symbol sets implementing the IOF norms
ISOM (1:15000, 1:10000), ISSOM (1:5000, 1:4000), ISMTBOM (1:20000, 1:15000,
1:10000, 1:7500, 1:5000) and ISSkiOM (1:15000, 1:10000, 1:5000).
But it is easy to implement other symbol sets.


%prep
export LANG=C.UTF-8
%setup -n %{name}-%{version}
%if 0%{?suse_version}
mkdir clipper
cd clipper
unzip "%SOURCE1"
cd ..
%endif

%if 0%{?branch:1}
  # Inject Mapper_VERSION_PATCH
  sed -i -e "s/Mapper VERSION [0-9]*[.][0-9]*[.][0-9]*/Mapper VERSION ${RPM_PACKAGE_VERSION}/" \
    CMakeLists.txt
%endif


%build
export LANG=C.UTF-8
%if 0%{?branch:1}
  if [ -z "${SOURCE_DATE_EPOCH}" ] ; then
      export SOURCE_DATE_EPOCH=$(date +%s --date "${RPM_PACKAGE_VERSION##*.} 0000Z")
  fi
%else
  if [ -z "${SOURCE_DATE_EPOCH}" ] ; then
      export SOURCE_DATE_EPOCH=$(date +%s --reference "%SOURCE0")
  fi
%endif

%cmake \
  -Wno-dev \
  -DCMAKE_BUILD_TYPE=Release \
  -DMapper_PACKAGE_NAME=%{name} \
  -DMapper_VERSION_DISPLAY="%{?branch:%{branch} }%{version}" \
%if 0%{?suse_version}
  -DMapper_BUILD_CLIPPER:BOOL=ON \
  -DCLIPPER_SOURCE_DIR=@Mapper_SOURCE_DIR@/clipper \
  -DCMAKE_INSTALL_DOCDIR=%{_docdir}/openorienteering-mapper%{?branch:-%{branch}} \
%endif
%if 0%{?fedora_version}
  -DLICENSING_PROVIDER=fedora \
%endif
%if ! %{with gdal}
  -DMapper_USE_GDAL:BOOL=OFF \
%endif
  # end

make %{?_smp_mflags}


%install
export LANG=C.UTF-8
%if 0%{?suse_version}
make -C build 'DESTDIR=%{buildroot}' install
%else
make 'DESTDIR=%{buildroot}' install
%endif

%if 0%{?branch:1}
  for I in %{buildroot}/usr/bin/Mapper \
           %{buildroot}%{_datadir}/applications/Mapper.desktop \
           %{buildroot}%{_datadir}/icons/hicolor/*/apps/Mapper.png \
           %{buildroot}%{_datadir}/man/man1/Mapper.1 ; \
      do mv "${I}" "${I%%Mapper*}Mapper-%{branch}${I##*/Mapper}" ; \
  done
  mv %{buildroot}%{_datadir}/mime/packages/openorienteering-mapper.xml \
     %{buildroot}%{_datadir}/mime/packages/openorienteering-mapper-%{branch}.xml
  for I in %{buildroot}%{_datadir}/icons/hicolor/*/mimetypes/application-x-openorienteering*.png ; \
      do mv "${I}" "${I%%x-openorienteering*}x-openorienteering-%{branch}${I##*x-openorienteering}" ; \
  done
  sed -i -e 's/Mapper/Mapper-%{branch}/;/^Name=/s/-%{branch}/ (%{branch})/' \
    %{buildroot}%{_datadir}/applications/Mapper-%{branch}.desktop
  sed -i -e 's/\(application\/x-openorienteering\)-\([a-z]*\)/\1-\2;\1-%{branch}-\2/g' \
    %{buildroot}%{_datadir}/applications/Mapper-%{branch}.desktop
  sed -i -e 's/x-openorienteering/x-openorienteering-%{branch}/g;s/glob pattern/glob weight="49" pattern/g' \
    %{buildroot}%{_datadir}/mime/packages/openorienteering-mapper-%{branch}.xml
  sed -i -e 's/^.B Mapper$/.B Mapper-%{branch}/' \
    %{buildroot}%{_datadir}/man/man1/Mapper-%{branch}.1
%endif
find "%{buildroot}%{_datadir}/%{name}/symbol sets" -name 'COPY_OF*' -delete
%fdupes -s %{buildroot}%{_datadir}

%if 0%{?suse_version}
%suse_update_desktop_file -r -n -G "Map drawing software" Mapper%{?branch:-%{branch}} Graphics VectorGraphics
%endif


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%check
export LANG=C.UTF-8
%if 0%{?suse_version}
cd build
%endif
make test ARGS=-V
%if %{with gdal}
src/gdal/mapper-gdal-info
%endif


%files
%defattr(-,root,root)
%docdir %{_docdir}/%{name}
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/*.qch
%{_docdir}/%{name}/*.qhc
%{_docdir}/%{name}/licensing.html
%{_docdir}/%{name}/3rd-party
%{_docdir}/%{name}/common-licenses
%{_bindir}/Mapper%{?branch:-%{branch}}
%{_datadir}/applications/Mapper%{?branch:-%{branch}}.desktop
%{_datadir}/mime/packages/openorienteering-mapper%{?branch:-%{branch}}.xml
%{_datadir}/icons/hicolor/
%{_datadir}/%{name}/
%doc %{_mandir}/man1/Mapper%{?branch:-%{branch}}.1*


%changelog
