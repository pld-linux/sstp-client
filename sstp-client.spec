#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	SSTP client for Linux
Summary(pl.UTF-8):	Klient SSTP dla Linuksa
Name:		sstp-client
Version:	1.0.17
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	https://downloads.sourceforge.net/sstp-client/%{name}-%{version}.tar.gz
# Source0-md5:	ca563f85badc4e4549e95aa42b2bf081
URL:		http://sstp-client.sourceforge.net/
BuildRequires:	libevent-devel >= 2.0.10
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	ppp-plugin-devel >= 2.4.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
sstp-client is an SSTP client for Linux. It can be used to establish a
SSTP connection to a Windows 2008 Server. This software has similar
commandline and configuration as the pptp-client software.

%description -l pl.UTF-8
sstp-clien to klient SSTP dla Linuksa. Może być używany do nawiązania
połączenia SSTP z serwerem Windows 2008. Wiersz poleceń i konfiguracja
są podobne do pakietu pptp-client.

%package devel
Summary:	Header files for sstp client library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki klienckiej sstp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for sstp client library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki klienckiej sstp.

%package static
Summary:	Static sstp-client library
Summary(pl.UTF-8):	Statyczna biblioteka kliencka sstp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static sstp client library.

%description static -l pl.UTF-8
Statyczna biblioteka kliencka sstp.

%package -n ppp-plugin-sstp
Summary:	Common files for %{name} library
Summary(pl.UTF-8):	Wspólne pliki biblioteki %{name}
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n ppp-plugin-sstp
Common files for %{name} library.

%description -n ppp-plugin-sstp -l pl.UTF-8
Wspólne pliki biblioteki %{name}.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-pppd-plugin-dir=%{_libdir}/pppd/plugins \
	--with-system-ca-path=/etc/certs
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/pppd/plugins/*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/pppd/plugins/*.a
%endif

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsstp_api.la

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/sstp-client

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog DEVELOPERS NEWS README TODO USING sstp-test*.example
%attr(755,root,root) %{_sbindir}/sstpc
%attr(755,root,root) %{_libdir}/libsstp_api-0.so
%{_mandir}/man8/sstpc.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsstp_api.so
%{_includedir}/sstp-client
%{_pkgconfigdir}/sstp-client-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsstp_api.a
%endif

%files -n ppp-plugin-sstp
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pppd/plugins/sstp-pppd-plugin.so
