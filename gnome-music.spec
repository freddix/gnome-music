Summary:	Default audio player application for GNOME 3
Name:		gnome-music
Version:	3.12.1
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-music/3.12/%{name}-%{version}.tar.xz
# Source0-md5:	1e08459389d9d627025b31a2229e042a
URL:		https://live.gnome.org/Design/Apps/Documents
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkg-config
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	glib-gio-gsettings
Requires:	gobject-introspection
Requires:	gstreamer-plugins-good
Requires:	hicolor-icon-theme
Requires:	python3-dbus
Requires:	python3-modules
Requires:	python3-pygobject3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/gnome-music

%description
Music provides a clean and focused interface for browsing your music
collection according to Artist, Album or Track.

%prep
%setup -q

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac
%{__sed} -i 's|#!/usr/bin/env.*|#!/usr/bin/python3|g' gnome-music.in

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4 -I libgd
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-compile	\
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*/*.la

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%update_icon_cache hicolor
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_bindir}/gnome-music
%dir %{_libdir}/gnome-music
%attr(755,root,root) %{_libdir}/gnome-music/libgd.so
%{_libdir}/gnome-music/girepository-1.0
%{py3_sitescriptdir}/gnomemusic
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/gnome-music
%{_desktopdir}/gnome-music.desktop
%{_iconsdir}/hicolor/*/*/*.png

