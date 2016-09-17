#
# Conditional build:
%bcond_without	lua		# build without tests

%define	__lua	/usr/bin/lua5.1
#define	luaver %(%{__lua} -e "print(string.sub(_VERSION, 5))")
%define	luaver 5.1
%define	lualibdir %{_libdir}/lua/%{luaver}
%define	luapkgdir %{_datadir}/lua/%{luaver}

Summary:	Simple implementation of msgpack in C
Name:		libmpack
Version:	1.0.2
Release:	0.1
License:	MIT
Group:		Development/Libraries
Source0:	https://github.com/tarruda/libmpack/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a6320e37991bb56520d4670419edb43c
Patch0:		https://github.com/tarruda/libmpack/pull/8.diff
# Patch0-md5:	91f4f18a5b74713465b392b3fe20d07a
Patch1:		https://github.com/tarruda/libmpack/commit/0cc47f7e859b7124cf46483a6e59ed973bbe5e42.diff
# Patch1-md5:	af5612df21a914fe0d06944196cfd274
Patch2:		lua.patch
URL:		https://github.com/tarruda/libmpack/
BuildRequires:	libtool
%if %{with lua}
BuildRequires:	lua-devel >= %{luaver}
%endif
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

%package -n lua-mpack
Summary:	Lua binding to libmpack
Group:		Development/Languages
# does not link with libmpack.so
#Requires:	%{name} = %{version}-%{release}

%description -n lua-mpack
Lua binding to libmpack.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} config=release \
	CC="%{__cc}" \
	PREFIX=%{_prefix} \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	LIBDIR=%{_libdir} \
	VERBOSE=1

%if %{with lua}
%{__make} -C binding/lua \
	CC="%{__cc}" \
	USE_SYSTEM_LUA=yes
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with lua}
%{__make} -C binding/lua install \
	USE_SYSTEM_LUA=yes \
	DESTDIR=$RPM_BUILD_ROOT
%endif

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

%files -n lua-mpack
%defattr(644,root,root,755)
%attr(755,root,root) %{lualibdir}/mpack.so
