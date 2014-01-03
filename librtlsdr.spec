Summary:	Realtek RTL2832U Software Defined Radio driver library
Name:		librtlsdr
Version:	0.5.2
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	https://github.com/steve-m/librtlsdr/archive/v%{version}.tar.gz
# Source0-md5:	1fc260a86976e06caf905f726d0c9b9b
URL:		http://sdr.osmocom.org/trac/wiki/rtl-sdr
BuildRequires:	cmake
BuildRequires:	libusb-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DVB-T dongles based on the Realtek RTL2832U can be used as a cheap
SDR, since the chip allows transferring the raw I/Q samples to the
host, which is officially used for DAB/DAB+/FM demodulation.

%package devel
Summary:	Header files for rtl-sdr
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for rtl-sdr.

%package static
Summary:	Static %{name} library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static %{name} library.

%prep
%setup -q

%build
%cmake . \
	-DINSTALL_UDEV_RULES=ON \
	-DDETACH_KERNEL_DRIVER=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/rtl_*
%attr(755,root,root) %{_libdir}/%{name}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}.so.0
/etc/udev/rules.d/rtl-sdr.rules

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}.so
%{_includedir}/rtl-sdr*.h
%{_pkgconfigdir}/%{name}.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/%{name}.a
