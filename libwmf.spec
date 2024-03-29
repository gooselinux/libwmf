Summary: Windows MetaFile Library
Name: libwmf
Version: 0.2.8.4
Release: 22%{?dist}
Group: System Environment/Libraries
#libwmf is under the LGPLv2+, however...
#1. The tarball contains an old version of the urw-fonts under GPL+.
#   Those fonts are not installed
#2. The header of the command-line wmf2plot utility places it under the GPLv2+.
#   wmf2plot is neither built or install
License: LGPLv2+ and GPLv2+ and GPL+
Source: http://downloads.sourceforge.net/wvware/%{name}-%{version}.tar.gz
URL: http://wvware.sourceforge.net/libwmf.html
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0: libwmf-0.2.8.3-nodocs.patch
Patch1: libwmf-0.2.8.3-relocatablefonts.patch
Patch2: libwmf-0.2.8.4-fallbackfont.patch
Patch3: libwmf-0.2.8.4-deps.patch
Patch4: libwmf-0.2.8.4-multiarchdevel.patch
Patch5: libwmf-0.2.8.4-intoverflow.patch
Patch6: libwmf-0.2.8.4-reducesymbols.patch
Patch7: libwmf-0.2.8.4-useafterfree.patch
Requires: urw-fonts
Requires: %{name}-lite = %{version}-%{release}
Requires(post): %{_bindir}/update-gdk-pixbuf-loaders
Requires(postun): %{_bindir}/update-gdk-pixbuf-loaders
BuildRequires: gtk2-devel, libtool, libxml2-devel, gd-devel, libpng-devel
BuildRequires: libjpeg-devel, libXt-devel, libX11-devel, dos2unix, libtool

%description
A library for reading and converting Windows MetaFile vector graphics (WMF).

%package lite
Summary: Windows Metafile parser library
Group: System Environment/Libraries

%description lite
A library for parsing Windows MetaFile vector graphics (WMF).

%package devel
Summary: Support files necessary to compile applications with libwmf
Group: Development/Libraries
Requires: libwmf = %{version}-%{release}
Requires: gtk2-devel, libxml2-devel, gd-devel, libjpeg-devel, pkgconfig

%description devel
Libraries, headers, and support files necessary to compile applications 
using libwmf.

%prep
%setup -q
%patch0 -p1 -b .nodocs
%patch1 -p1 -b .relocatablefonts
%patch2 -p1 -b .fallbackfont
%patch3 -p1 -b .deps
%patch4 -p1 -b .multiarchdevel
%patch5 -p1 -b .intoverflow
%patch6 -p1 -b .reducesymbols.patch
%patch7 -p1 -b .useafterfree.patch
f=README ; iconv -f iso-8859-2 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f

%build
rm configure.ac
ln -s patches/acconfig.h acconfig.h
autoreconf -i -f
%configure --with-libxml2 --disable-static --disable-dependency-tracking
export tagname=CC
make LIBTOOL=/usr/bin/libtool %{?_smp_mflags}
dos2unix doc/caolan/*.html

%install
rm -rf $RPM_BUILD_ROOT
export tagname=CC
make DESTDIR=$RPM_BUILD_ROOT LIBTOOL=/usr/bin/libtool install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/loaders/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/loaders/*.la
rm -rf $RPM_BUILD_ROOT%{_includedir}/libwmf/gd
find doc -name "Makefile*" -exec rm {} \;
#we're carrying around duplicate fonts
rm -rf $RPM_BUILD_ROOT%{_datadir}/libwmf/fonts/*afm
rm -rf $RPM_BUILD_ROOT%{_datadir}/libwmf/fonts/*pfb
sed -i $RPM_BUILD_ROOT%{_datadir}/libwmf/fonts/fontmap -e 's#libwmf/fonts#fonts/default/Type1#g'

%post
/sbin/ldconfig
%{_bindir}/update-gdk-pixbuf-loaders %{_host} &>/dev/null || :

%post lite -p /sbin/ldconfig

%postun 
/sbin/ldconfig
%{_bindir}/update-gdk-pixbuf-loaders %{_host} &>/dev/null || :

%postun lite -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/libwmf-*.so.*
%{_libdir}/gtk-2.0/*/loaders/*.so
%{_bindir}/wmf2svg
%{_bindir}/wmf2gd
%{_bindir}/wmf2eps
%{_bindir}/wmf2fig
%{_bindir}/wmf2x
%{_bindir}/libwmf-fontmap
%{_datadir}/libwmf/

%files lite
%defattr(-,root,root,-)
%{_libdir}/libwmflite-*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/*.html
%doc doc/*.png
%doc doc/*.gif
%doc doc/html
%doc doc/caolan
%{_libdir}/*.so
%{_libdir}/pkgconfig/libwmf.pc
%{_includedir}/libwmf
%{_bindir}/libwmf-config

%clean
rm -r $RPM_BUILD_ROOT

%changelog
* Fri Apr 16 2010 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-22
- Resolves: rhbz#583029 clarify licences

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.2.8.4-21.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 26 2009 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-20
- Resolves: CVE-2009-1364

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 13 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.2.8.4-18
- Split libwmflite (WMF parser) into -lite subpackage (#432651).
- Build with dependency tracking disabled.
- Convert docs to UTF-8.

* Wed Aug 29 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-17
- rebuild

* Thu Aug 02 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-16
- I wrote it and still had to check the headers to see if I had
  cut and pasted "and later" into then

* Thu May 24 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-15
- drop duplicate font metrics

* Thu Feb 15 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-14
- remove use of archaic autotools

* Fri Feb 09 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-13
- Resolves: rhbz#222734 no need for Makefiles in doc dirs

* Tue Jan 16 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-12
- Resolves: rhbz#222734 no need for Makefiles in doc dirs

* Thu Nov 16 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-11
- Resolves: rhbz#215925 reduce exported symbols

* Fri Jul 14 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-10
- retweak for 64bit

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.2.8.4-9.1
- rebuild

* Wed Jul 12 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-9
- CVE-2006-3376 libwmf integer overflow

* Tue May 16 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-8
- rh#191971# BuildRequires

* Fri May  5 2006 Matthias Clasen <mclasen@redhat.com> 0.2.8.4-7
- Rebuild against the new GTK+
- Require GTK+ 2.9.0

* Tue May 02 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-6
- add a .pc and base libwmf-devel on pkg-config output

* Tue Feb 28 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-5
- rh#143096# extra deps according to libwmf-config

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.2.8.4-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.2.8.4-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 19 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-4
- rh#178275# match srvg gtk2 _host usage for pixbuf loaders

* Tue Jan 03 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-3
- add libwmf-0.2.8.4-fallbackfont.patch for rh#176620#

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> 0.2.8.4-2.1
- rebuilt

* Wed Nov 23 2005 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-2
- rh#173299# modify pre/post requires

* Thu Jul 28 2005 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-1
- get patches merged upstream
- drop integrated libwmf-0.2.8.3-warnings.patch
- drop integrated libwmf-0.2.8.3-noextras.patch
- drop integrated libwmf-0.2.8.3-rh154813.patch

* Tue Jul 26 2005 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-9
- rh#154813# wmf upsidedown, spec (what of is there is) says that
  this shouldn't happen, but...

* Wed Mar  2 2005 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-8
- rebuild with gcc4

* Thu Dec 16 2004 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-7
- RH#143096# No need for extra X libs to be linked against

* Tue Nov  2 2004 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-6
- #rh137878# Extra BuildRequires

* Thu Oct  7 2004 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-5
- #rh134945# Extra BuildRequires

* Wed Sep  1 2004 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-4
- #131373# cleanup compiletime warnings

* Thu Jul  8 2004 Matthias Clasen <mclasen@redhat.com> - 0.2.8.3-3
- Update to use the new update-gdk-pixbuf-loaders script in gtk2-2.4.1-2

* Thu May 20 2004 Caolan McNamara <caolanm@redhat.com>
- Initial version
