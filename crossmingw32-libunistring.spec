Summary:	Unicode string library - MinGW32 cross version
Summary(pl.UTF-8):	Biblioteka do obsługi łańcuchów unikodowych - wersja skrośna dla MinGW32
%define		realname	libunistring
Name:		crossmingw32-%{realname}
Version:	0.9.3
Release:	1
License:	LGPL v3+
Group:		Libraries
Source0:	http://ftp.gnu.org/gnu/libunistring/%{realname}-%{version}.tar.gz
# Source0-md5:	db8eca3b64163abadf8c40e5cecc261f
URL:		http://gnu.org/software/libunistring/
BuildRequires:	crossmingw32-gcc
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld	-Wl,-z,.*

%description
This library provides functions for manipulating Unicode strings and
for manipulating C strings according to the Unicode standard.

This package contains the cross version for Win32.

%description -l pl.UTF-8
Ta biblioteka udostępnia funkcje do obsługi łańcuchów unikodowych oraz
do obsługi łańcuchów znaków C zgodnie ze standardem Unicode.

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static unistring library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka unistring (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static unistring library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka unistring (wersja skrośna MinGW32).

%package dll
Summary:	DLL unistring library for Windows
Summary(pl.UTF-8):	Biblioteka DLL unistring dla Windows
Group:		Applications/Emulators
Requires:	wine

%description dll
Header files for unistring library.

%description dll -l pl.UTF-8
Pliki nagłówkowe biblioteki unistring.

%prep
%setup -q -n %{realname}-%{version}

%build
%configure \
	--target=%{target} \
	--host=%{target}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%{__rm} -r $RPM_BUILD_ROOT%{_infodir} $RPM_BUILD_ROOT%{_prefix}/share/doc/libunistring

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README THANKS
%attr(755,root,root) %{_libdir}/libunistring.dll.a
%{_libdir}/libunistring.la
%{_includedir}/unistring
%{_includedir}/uni*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libunistring.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libunistring-*.dll
