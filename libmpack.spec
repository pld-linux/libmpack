Summary:	Simple implementation of msgpack in C
Name:		libmpack
Version:	1.0.2
Release:	0.1
License:	MIT
Group:		Development/Libraries
Source0:	https://github.com/tarruda/libmpack/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a6320e37991bb56520d4670419edb43c
URL:		https://github.com/tarruda/libmpack/
BuildRequires:	libtool
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

%prep
%setup -q

%build
%{__make} config=release \
	CC="%{__cc}" \
	PREFIX=%{_prefix} \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags} -fPIC -shared" \
	LIBDIR=%{_libdir} \
	VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}

libtool --mode=install install -p build/release/*.la $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE-MIT
