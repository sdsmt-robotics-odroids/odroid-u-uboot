%global commit 33e05ffb159141b640571e91470172d83a2a1273

Name:           odroid-u-uboot
Version:        2014.08.29
Release:        2%{?dist}
Summary:        U-boot for ODROID-U2/U3/X2

Group:          System Environment/Base
License:        GPLv2
URL:            http://odroid.com/dokuwiki/doku.php?id=en:odroid-u3
Source0:        https://github.com/hardkernel/u-boot/archive/%{commit}/u-boot-%{commit}.tar.gz
Source1:        boot.ini
Source2:        grubby
Patch0:         od-uboot-gcc47.patch

# We always need to use a cross compiler because we can't use hardfloat static
# libraries. This means that we'll always produce an ARM package, even when
# built on x86 machines. The code compiled here is also indifferent of the
# architecture used on the ODROID's OS.
BuildArch:      noarch

BuildRequires:  arm-none-eabi-gcc-cs
BuildRequires:  dos2unix
Requires:       grubby

%description
U-boot for Hardkernel's ODROID-U2/U3/X2. This package installs u-boot.bin and a
default boot.ini, and also configures grubby.

%prep
%setup -qn u-boot-%{commit}
%patch0 -p1
rm -f mkbl2
dos2unix COPYING.txt
chmod 644 COPYING.txt

%build
make %{?_smp_mflags} smdk4412_config
make %{?_smp_mflags} CROSS_COMPILE=arm-none-eabi-

%install
install -p -m0644 -D %{SOURCE2} %{buildroot}%{_datadir}/%{name}/grubby-%{version}-%{release}
install -p -m0644 -D %{SOURCE1} %{buildroot}/boot/uboot/boot.ini
install -p -m0755 -D sd_fuse/u-boot.bin.HardKernel %{buildroot}/boot/uboot/u-boot.bin

ln -s grubby-%{version}-%{release} %{buildroot}%{_datadir}/%{name}/grubby

%post
cat %{_datadir}/%{name}/grubby-%{version}-%{release} >> %{_sysconfdir}/sysconfig/uboot

%preun
while read l; do
  sed -i "0,/^`echo "$l" | sed 's/\//\\\\\//g'`/{//d}" %{_sysconfdir}/sysconfig/uboot
done < %{_datadir}/%{name}/grubby-%{version}-%{release}

%files
%doc COPYING COPYING.txt CREDITS MAINTAINERS README
%{_datadir}/%{name}/grubby
%{_datadir}/%{name}/grubby-%{version}-%{release}
%config(noreplace) /boot/uboot/boot.ini
/boot/uboot/u-boot.bin

%changelog
* Mon Aug 03 2015 Scott K Logan <logans@cottsay.net> - 2014.08.29-2
- Temporarily switch to the prebuilt u-boot.bin (see https://github.com/hardkernel/u-boot/issues/16)

* Sun Jul 19 2015 Scott K Logan <logans@cottsay.net> - 2014.08.29-1
- Initial package
