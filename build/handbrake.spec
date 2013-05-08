%define name HandBrake
%define lowername handbrake
%define version 0.9.8
%define release 1
%global git 7b2805e

Name:           %{name}
Version:        %{version}
Release:        %{release}.git%{git}%{?dist}
Summary:        A program to transcode DVDs and other sources to MPEG-4

Group:          Applications/Multimedia
License:        GPLv2
URL:            http://handbrake.fr/
Source0:        %{lowername}-%{version}.tar.gz
Prefix:         %{_prefix}
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  glib2-devel, gtk2-devel, webkitgtk-devel
BuildRequires:  gstreamer-devel, gstreamer-plugins-base-devel, libgudev1-devel
BuildRequires:  bzip2-devel, intltool, libnotify-devel, libtool, yasm
BuildRequires:  fribidi-devel gstreamer-devel gstreamer-plugins-base-devel libnotify-devel libgudev1-devel webkitgtk-devel webkitgtk3-devel
BuildRequires:  libass-devel libsamplerate-devel libtheora-devel enca-devel libvorbis-devel

Requires:       gtk2, coreutils

%define debug_package %{nil}

%description
HandBrake is an open-source, GPL-licensed, multi-platform, multi-threaded
transcoder, available for MacOS X, Linux and Windows.

%package gui
Summary:  A program to transcode DVDs and other sources to MPEG-4
Group:    Applications/Multimedia

%package cli
Summary:  A program to transcode DVDs and other sources to MPEG-4
Group:    Applications/Multimedia

%description gui
HandBrake is an open-source, GPL-licensed, multi-platform, multi-threaded
transcoder, available for MacOS X, Linux and Windows.

%description cli
HandBrake is an open-source, GPL-licensed, multi-platform, multi-threaded
transcoder, available for MacOS X, Linux and Windows.

%prep
%setup -q -n %{lowername}-%{version}

%build
./configure --debug=std --prefix=%{_prefix}
make %{?_smp_mflags} -C build


%install
make -C build DESTDIR=$RPM_BUILD_ROOT install-strip

## blow away stuff we don't want
/bin/rm -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/icon-theme.cache

%clean
rm -rf %{buildroot}

%post gui
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%postun gui
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%files gui
%defattr(-,root,root,-)
%doc NEWS AUTHORS CREDITS THANKS COPYING
%{_datadir}/icons/hicolor
%{_datadir}/applications
%{_bindir}/ghb

%files cli
%defattr(-,root,root,-)
%doc NEWS AUTHORS CREDITS THANKS COPYING
%{_bindir}/HandBrakeCLI

%changelog
* Sun Apr 11 2010 John Stebbins <jstebbins@jetheaddev.com> - svn
- Snapshot release


