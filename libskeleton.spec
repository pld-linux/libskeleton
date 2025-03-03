#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	A library for reading and writing Ogg Skeleton data
Summary(pl.UTF-8):	Biblioteka do odczytu i zapisu danych Ogg Skeleton
Name:		libskeleton
Version:	0.1.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://gitlab.xiph.org/xiph/libskeleton/-/tags
Source0:	https://gitlab.xiph.org/xiph/libskeleton/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
# Source0-md5:	42ea2b16a1af330078f5f9b49ae1a50e
URL:		https://wiki.xiph.org/Ogg_Skeleton
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	libogg-devel >= 2:1.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
Requires:	libogg >= 2:1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A library for reading and writing Ogg Skeleton data.

Ogg Skeleton provides structuring information for multitrack Ogg
files. It is compatible with Ogg Theora and provides extra clues for
synchronization and content negotiation such as language selection.

%description -l pl.UTF-8
Biblioteka do odczytu i zapisu danych Ogg Skeleton.

Ogg Skeleton zapewnia informacje strukturalne dla wielościeżkowych
plików Ogg. Jest zgodny z Ogg Theora i zapewnia dodatkowe podpowiedzi
do synchronizacji i negocjacji treści, np. wyboru języka.

%package devel
Summary:	Header files for libskeleton library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libskeleton
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libogg-devel >= 2:1.0

%description devel
Header files for libskeleton library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libskeleton.

%package static
Summary:	Static libskeleton library
Summary(pl.UTF-8):	Statyczna biblioteka libskeleton
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libskeleton library.

%description static -l pl.UTF-8
Statyczna biblioteka libskeleton.

%package apidocs
Summary:	API documentation for libskeleton library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libskeleton
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libskeleton library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libskeleton.

%prep
%setup -q -n %{name}-v%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# headers expect subdir
install -d $RPM_BUILD_ROOT%{_includedir}/skeleton
%{__mv} $RPM_BUILD_ROOT%{_includedir}/*.h $RPM_BUILD_ROOT%{_includedir}/skeleton

install -d $RPM_BUILD_ROOT%{_bindir}
install examples/.libs/skeleton-* $RPM_BUILD_ROOT%{_bindir}

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libskeleton.la

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libskeleton

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README
%attr(755,root,root) %{_bindir}/skeleton-apply
%attr(755,root,root) %{_bindir}/skeleton-info
%attr(755,root,root) %{_libdir}/libskeleton.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libskeleton.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libskeleton.so
%{_includedir}/skeleton
%{_pkgconfigdir}/skeleton.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libskeleton.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc doc/libskeleton/html/*
