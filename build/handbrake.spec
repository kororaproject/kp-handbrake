Name:           HandBrake
Version:        0.9.9
Release:        12%{?dist}
Summary:        An open-source multiplatform video transcoder

License:        GPLv2+
URL:            http://handbrake.fr/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch1:         %{name}-%{version}-use-unpatched-a52.patch
Patch2:         %{name}-%{version}-use-unpatched-libmkv.patch
Patch3:         %{name}-%{version}-use-gstreamer1.patch

ExclusiveArch:  %{ix86} x86_64

# The project fetches libraries to bundle in the executable at compile time; to
# have them available before building, proceed as follows. All files will be
# available in the "download" folder.
#
# ./configure
# cd build
# make contrib.fetch

Source11:       http://download.handbrake.fr/handbrake/contrib/faac-1.28.tar.gz
Source12:       http://download.handbrake.fr/handbrake/contrib/fdk-aac-v0.1.1-6-gbae4553.tar.bz2
Source13:       http://download.handbrake.fr/handbrake/contrib/mp4v2-trunk-r355.tar.bz2
Source14:       http://download.handbrake.fr/handbrake/contrib/libav-v9.6.tar.bz2

BuildRequires:  a52dec-devel >= 0.7.4
BuildRequires:  bzip2-devel
#BuildRequires:  faac-devel >= 1.28
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  fribidi-devel
BuildRequires:  intltool
BuildRequires:  lame-devel >= 3.98
BuildRequires:  libass-devel
BuildRequires:  libbluray-devel
#>= 0.2.3
BuildRequires:  libdvdnav-devel
BuildRequires:  libdvdread-devel
BuildRequires:  libmkv-devel >= 0.6.5
#BuildRequires:  libmp4v2-devel >= 1.9.0
BuildRequires:  libmpeg2-devel >= 0.5.1
BuildRequires:  libogg-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libtheora-devel
BuildRequires:  libtool
BuildRequires:  libvorbis-devel
BuildRequires:  libxml2-devel
BuildRequires:  m4
BuildRequires:  make
BuildRequires:  patch
BuildRequires:  python
BuildRequires:  subversion
BuildRequires:  tar
BuildRequires:  wget
BuildRequires:  x264-devel
BuildRequires:  yasm
BuildRequires:  zlib-devel

# ffmpeg 2.0 only on Fedora 20+
%if 0%{?fedora} > 19 || 0%{?rhel} > 6
BuildRequires:  ffmpeg-devel >= 2.0
%endif

# No gui on RHEL 6, GTK libraries too old. 
%if 0%{?fedora} || 0%{?rhel} > 6

BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  libgudev1-devel
BuildRequires:  libnotify-devel
BuildRequires:  webkitgtk3-devel
Requires:       hicolor-icon-theme

%endif

%description
%{name} is a general-purpose, free, open-source, cross-platform, multithreaded
video transcoder software application. It can process most common multimedia
files and any DVD or Bluray sources that do not contain any kind of copy
protection.

%if 0%{?fedora} || 0%{?rhel} > 6

%package gui
Summary:        An open-source multiplatform video transcoder (GUI)
Obsoletes:      HandBrake < %{version}-%{release}
Provides:       HandBrake = %{version}-%{release}
Requires:       hicolor-icon-theme
Requires:       libdvdcss%{_isa}

%description gui
%{name} is a general-purpose, free, open-source, cross-platform, multithreaded
video transcoder software application. It can process most common multimedia
files and any DVD or Bluray sources that do not contain any kind of copy
protection.

This package contains the main program with a graphical interface.

%endif

%package cli
Summary:        An open-source multiplatform video transcoder (CLI)
Requires:       libdvdcss%{_isa}

%description cli
%{name} is a general-purpose, free, open-source, cross-platform, multithreaded
video transcoder software application. It can process most common multimedia
files and any DVD or Bluray sources that do not contain any kind of copy
protection.

This package contains the command line version of the program.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1

mkdir -p download
cp %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} download

# Use system libraries in place of bundled ones
for module in a52dec lame libdvdnav libdvdread libbluray libmkv mpeg2dec x264; do
    sed -i -e "/MODULES += contrib\/$module/d" make/include/main.defs
done

%if 0%{?fedora} > 19 || 0%{?rhel} > 6
sed -i -e "/MODULES += contrib\/ffmpeg/d" make/include/main.defs
%endif

%build
# This makes build stop if any download is attempted
export http_proxy=http://127.0.0.1

# Disable Fedora 21 GCC error as it breaks mp4v build.
%if 0%{?fedora} >= 21
export RPM_OPT_FLAGS="${RPM_OPT_FLAGS} -Wno-error=format-security"
%endif

# By default the project is built with optimizations for speed and no debug.
# Override configure settings by passing RPM_OPT_FLAGS and disabling preset
# debug options.
echo "GCC.args.O.speed = ${RPM_OPT_FLAGS} -I%{_includedir}/ffmpeg" > custom.defs
echo "GCC.args.g.none = " >> custom.defs

# Not an autotools configure script.
./configure \
    --prefix=%{_prefix} \
    --verbose \
    --disable-gtk-update-checks \
    --enable-fdk-aac \
    --build build \
%if 0%{?rhel} == 6
    --disable-gtk
%endif

make -C build %{?_smp_mflags}

%install
rm -rf %{buildroot}
make -C build DESTDIR=%{buildroot} install

%if 0%{?fedora} || 0%{?rhel} > 6

desktop-file-validate %{buildroot}/%{_datadir}/applications/ghb.desktop

%post gui
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun gui
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans gui
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files gui
%doc AUTHORS COPYING CREDITS NEWS THANKS TRANSLATIONS
%{_bindir}/ghb
%{_datadir}/applications/ghb.desktop
%{_datadir}/icons/hicolor/16x16/apps/hb-icon.png
%{_datadir}/icons/hicolor/22x22/apps/hb-icon.png
%{_datadir}/icons/hicolor/24x24/apps/hb-icon.png
%{_datadir}/icons/hicolor/32x32/apps/hb-icon.png
%{_datadir}/icons/hicolor/48x48/apps/hb-icon.png
%{_datadir}/icons/hicolor/64x64/apps/hb-icon.png
%{_datadir}/icons/hicolor/128x128/apps/hb-icon.png
%{_datadir}/icons/hicolor/256x256/apps/hb-icon.png

%endif

%files cli
%doc AUTHORS COPYING CREDITS NEWS THANKS TRANSLATIONS
%{_bindir}/HandBrakeCLI

%changelog
* Tue Mar 25 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-12
- Remove libdvdnav patch from the build and use libdvdnav with a patch from
  trunk.
- Use system ffpmeg 2 libraries in place of bundled libav for Fedora 20+.
- Use GTK3 interface.

* Mon Mar 17 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-11
- Fix crash on Fedora.

* Fri Mar 14 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-10
- Use system libdvdnav/libdvdread.

* Mon Dec 23 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-9
- Use system libraries for libbluray, lame, mpeg2dec, a52dec (patch), libmkv
  (patch), x264 (faac, fdk-aac, libav, libdvdnav, libdvdread and mp4v2 are still
  bundled).
- Use Fedora compiler options.
- Use GStreamer 1.x on Fedora and RHEL/CentOS 7.
- Add fdk-aac support.

* Mon Dec 23 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-8
- Scriptlets need to run for gui subpackage and not base package. Thanks to
  Peter Oliver.

* Mon Sep 09 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-7
- Add requirement on libdvdcss, fix hicolor-icon-theme requirement.

* Fri Jul 26 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-6
- Enable building CLI only on CentOS/RHEL 6.
- Disable GTK update checks (updates come only packaged).

* Tue Jul 23 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-5
- Enable command line interface only for CentOS/RHEL 6.

* Thu May 30 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-4
- Updated x264 to r2282-1db4621 (stable branch) to fix Fedora 19 crash issues.

* Mon May 20 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-3
- Update to 0.9.9.
- Separate GUI and CLI packages.

* Sat May 11 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-2.5449svn
- Updated.

* Wed May 01 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-1.5433svn
- First build.
