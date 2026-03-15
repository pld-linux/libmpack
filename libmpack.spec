#
# Conditional build:
%bcond_without	tests		# unit tests
#
Summary:	Simple implementation of msgpack in C
Name:		libmpack
Version:	1.0.5
Release:	1
License:	MIT
Group:		Development/Libraries
Source0:	https://github.com/libmpack/libmpack/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ac4b25bfd0a07003ed8dac9c6dc851a6
URL:		https://github.com/libmpack/libmpack/
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libmpack is a small binary serialization/RPC library that implements
both the msgpack and msgpack-rpc specifications.

Differences from mspack-c:
 - Callback-based API to simplify (de)serialization directly to/from
   application-specific objects.
 - C89 compatible code
 - No allocation performed by the library, but helpers to simplify
   dynamic allocation if the application needs it.
 - Non-backtracking, incremental/iterative parse/serialization API

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%prep
%setup -q

%build
%{__make} config=release \
	CC="%{__cc}" \
	PREFIX=%{_prefix} \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	LIBDIR=%{_libdir} \
	VERBOSE=1 \
	PATCH=5

%if %{with tests}
%{__make} test \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	VERBOSE=1 \
	PATCH=5
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT \
	PATCH=5

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmpack.a
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmpack.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md LICENSE-MIT
%attr(755,root,root) %{_libdir}/libmpack.so.*.*.*
%ghost %{_libdir}/libmpack.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmpack.so
%{_includedir}/mpack.h
%{_pkgconfigdir}/mpack.pc
