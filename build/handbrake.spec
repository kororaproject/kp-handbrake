Name:           HandBrake
Version:        0.9.9
Release:        3%{?dist}
Summary:        An open-source multiplatform video transcoder
Group:          Applications/Multimedia

License:        GPLv2+
URL:            http://handbrake.fr/
Source0:        %{name}-%{version}.tar.bz2

# The project fetches libraries to bundle in the executable at compile time; to
# have them available before building, proceed as follows. All files will be
# available in the "download" folder.
#
# ./configure
# cd build
# make contrib.fetch

Source10:       a52dec-0.7.4.tar.gz
Source11:       faac-1.28.tar.gz
Source12:       lame-3.98.tar.gz
Source13:       libav-v9.6.tar.bz2
Source14:       libbluray-0.2.3.tar.bz2
Source15:       libdvdnav-svn1168.tar.gz
Source16:       libdvdread-svn1168.tar.gz
Source17:       libmkv-0.6.5-0-g82075ae.tar.gz
Source18:       mp4v2-trunk-r355.tar.bz2
Source19:       mpeg2dec-0.5.1.tar.gz
Source20:       x264-r2273-b3065e6.tar.gz

BuildRequires:  bzip2-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  fribidi-devel
BuildRequires:  gstreamer-devel
BuildRequires:  gstreamer-plugins-base-devel
BuildRequires:  intltool
BuildRequires:  libass-devel
BuildRequires:  libgudev1-devel
BuildRequires:  libnotify-devel
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
BuildRequires:  webkitgtk-devel
BuildRequires:  wget
BuildRequires:  yasm
BuildRequires:  zlib-devel
Requires:       hicolor-icon-theme

%description
%{name} is a general-purpose, free, open-source, cross-platform, multithreaded
video transcoder software application. It can process most common multimedia
files and any DVD or Bluray sources that do not contain any kind of copy
protection.

%package gui
Summary:        An open-source multiplatform video transcoder (GUI)
Obsoletes:      HandBrake <= %{version}
Provides:       HandBrake = %{version}-%{release}
Group:    	Applications/Multimedia

%description gui
%{name} is a general-purpose, free, open-source, cross-platform, multithreaded
video transcoder software application. It can process most common multimedia
files and any DVD or Bluray sources that do not contain any kind of copy
protection.

This package contains the main program with a graphical interface.

%package cli
Summary:        An open-source multiplatform video transcoder (CLI)
Group:    	Applications/Multimedia

%description cli
%{name} is a general-purpose, free, open-source, cross-platform, multithreaded
video transcoder software application. It can process most common multimedia
files and any DVD or Bluray sources that do not contain any kind of copy
protection.

This package contains the command line version of the program.

%prep
%setup -q
mkdir -p download
cp %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} \
    %{SOURCE16} %{SOURCE17} %{SOURCE18} %{SOURCE19} %{SOURCE20} \
    download

%build
# By default the project is built with optimizations for speed and no debug.
# Override configure settings by passing RPM_OPT_FLAGS where needed.
echo "GCC.args.O.speed = ${RPM_OPT_FLAGS}" > custom.defs
echo "GCC.args.g.none = -g" >> custom.defs

./configure --prefix=%{_prefix} --verbose
make -C build %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make -C build DESTDIR=%{buildroot} install
desktop-file-validate %{buildroot}/%{_datadir}/applications/ghb.desktop

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
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

%files cli
%doc AUTHORS COPYING CREDITS NEWS THANKS TRANSLATIONS
%{_bindir}/HandBrakeCLI

%changelog
* Mon May 20 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-3
- Update to 0.9.9.
- Separate GUI and CLI packages.

* Sat May 11 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-2.5449svn
- Updated.

* Wed May 01 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-1.5433svn
- First build.
