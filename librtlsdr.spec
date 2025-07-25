Summary:	Realtek RTL2832U Software Defined Radio driver library
Summary(pl.UTF-8):	Biblioteka sterownika Realtek RTL2832U Software Defined Radio
Name:		librtlsdr
Version:	2.0.2
Release:	1
License:	GPL v2+
Group:		Libraries
#Source0Download: https://github.com/steve-m/librtlsdr/tags
Source0:	https://github.com/steve-m/librtlsdr/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	632f03d41e2b2f9c2dd94ef2b51be5bf
Patch0:		%{name}-pc.patch
URL:		https://osmocom.org/projects/rtl-sdr/wiki/Rtl-sdr
BuildRequires:	cmake >= 3.7.2
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
Obsoletes:	rtl-sdr < 0.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DVB-T dongles based on the Realtek RTL2832U can be used as a cheap
SDR, since the chip allows transferring the raw I/Q samples to the
host, which is officially used for DAB/DAB+/FM demodulation.

%description -l pl.UTF-8
Moduły (dongle) DVB-T oparte na układzie Realtek RTL2832U mogą służyć
jako tanie radio programowalne (SDR), ponieważ układ pozwala na
przesyłanie surowych próbek I/Q do hosta, który odpowiada za
demodulację DAB/DAB+/FM.

%package devel
Summary:	Header files for rtlsdr library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki rtlsdr
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	rtl-sdr-devel < 0.5
Requires:	libusb-devel >= 1.0

%description devel
Header files for rtlsdr library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki rtlsdr.

%package static
Summary:	Static rtlsdr library
Summary(pl.UTF-8):	Statyczna biblioteka rtlsdr
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static rtlsdr library.

%description static -l pl.UTF-8
Statyczna biblioteka rtlsdr.

%prep
%setup -q
%patch -P0 -p1

%{__sed} -i -e 's,/etc/udev/rules\.d,/lib/udev/rules.d,' CMakeLists.txt

%build
%cmake -B build \
	-DINSTALL_UDEV_RULES=ON \
	-DDETACH_KERNEL_DRIVER=OFF \
	-DLIB_INSTALL_DIR:PATH=%{_lib}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/rtl_adsb
%attr(755,root,root) %{_bindir}/rtl_biast
%attr(755,root,root) %{_bindir}/rtl_eeprom
%attr(755,root,root) %{_bindir}/rtl_fm
%attr(755,root,root) %{_bindir}/rtl_power
%attr(755,root,root) %{_bindir}/rtl_sdr
%attr(755,root,root) %{_bindir}/rtl_tcp
%attr(755,root,root) %{_bindir}/rtl_test
%attr(755,root,root) %{_libdir}/librtlsdr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librtlsdr.so.0
/lib/udev/rules.d/rtl-sdr.rules

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librtlsdr.so
%{_includedir}/rtl-sdr*.h
%{_libdir}/cmake/rtlsdr
%{_pkgconfigdir}/librtlsdr.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/librtlsdr.a
