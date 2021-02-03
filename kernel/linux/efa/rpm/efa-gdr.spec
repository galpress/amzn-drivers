# Copyright 2019-2020 Amazon.com, Inc. or its affiliates. All rights reserved

%define name			efa-gdr
%define driver_name		efa
%define debug_package		%{nil}

Name:		%{name}
Version:	%{driver_version}
Release:	1%{?dist}
Summary:	%{name} kernel module

Group:		System/Kernel
License:	Dual BSD/GPL
URL:		https://github.com/amzn/amzn-drivers/
Source0:	%{name}-%{version}.tar

Requires:	dkms %kernel_module_package_buildreqs autoconf automake
Conflicts:	efa

%define install_path /usr/src/%{driver_name}-%{version}

%description
%{name} kernel module source and DKMS scripts to build the kernel module.

%prep
%setup -n %{name}-%{version} -q

%post
cd %{install_path}
./autogen.sh
dkms add -m %{driver_name} -v %{driver_version}
for kernel in $(/bin/ls /lib/modules); do
	dkms build -m %{driver_name} -v %{driver_version} -k $kernel
	dkms install --force -m %{driver_name} -v %{driver_version} -k $kernel
done

%preun
dkms remove -m %{driver_name} -v %{driver_version} --all

%build

%install
cd kernel/linux/efa
mkdir -p %{buildroot}%{install_path}
mkdir -p %{buildroot}%{install_path}/config
mkdir -p %{buildroot}%{install_path}/src
install -D -m 644 conf/efa-gdr.conf	%{buildroot}/etc/modules-load.d/efa.conf
install -D -m 644 conf/efa-modprobe-gdr.conf	%{buildroot}/etc/modprobe.d/efa.conf
install -m 644 conf/dkms-gdr.conf	%{buildroot}%{install_path}/dkms.conf
install -m 744 conf/configure-dkms-gdr.sh	%{buildroot}%{install_path}
install -m 644 README			%{buildroot}%{install_path}
install -m 644 RELEASENOTES.md		%{buildroot}%{install_path}
install -m 644 Makefile.am		%{buildroot}%{install_path}
install -m 644 Makefile.common		%{buildroot}%{install_path}
install -m 644 Makefile.kernel		%{buildroot}%{install_path}
install -m 744 autogen.sh		%{buildroot}%{install_path}
install -m 644 configure.ac		%{buildroot}%{install_path}
install -m 644 config/Makefile		%{buildroot}%{install_path}/config
install -m 644 config/efa.m4		%{buildroot}%{install_path}/config
install -m 644 config/build-linux.m4	%{buildroot}%{install_path}/config
cd src
install -m 644 efa_com.c		%{buildroot}%{install_path}/src
install -m 644 efa_com_cmd.c		%{buildroot}%{install_path}/src
install -m 644 efa_main.c		%{buildroot}%{install_path}/src
install -m 644 efa_sysfs.c		%{buildroot}%{install_path}/src
install -m 644 efa_verbs.c		%{buildroot}%{install_path}/src
install -m 644 efa_gdr.c		%{buildroot}%{install_path}/src
install -m 644 efa_gdr.h		%{buildroot}%{install_path}/src
install -m 644 efa-abi.h 		%{buildroot}%{install_path}/src
install -m 644 efa_admin_cmds_defs.h 	%{buildroot}%{install_path}/src
install -m 644 efa_admin_defs.h 	%{buildroot}%{install_path}/src
install -m 644 efa_com_cmd.h		%{buildroot}%{install_path}/src
install -m 644 efa_com.h		%{buildroot}%{install_path}/src
install -m 644 efa_common_defs.h	%{buildroot}%{install_path}/src
install -m 644 efa.h			%{buildroot}%{install_path}/src
install -m 644 efa_regs_defs.h		%{buildroot}%{install_path}/src
install -m 644 efa_sysfs.h		%{buildroot}%{install_path}/src
install -m 644 kcompat.h		%{buildroot}%{install_path}/src
install -m 644 Makefile.am		%{buildroot}%{install_path}/src

%files
%{install_path}
/etc/modules-load.d/efa.conf
/etc/modprobe.d/efa.conf

%changelog
* Thu Jan 28 2021 Gal Pressman <galpress@amazon.com> - 1.11.1
- Fix GDR driver packaging issues

* Sun Dec 06 2020 Gal Pressman <galpress@amazon.com> - 1.11.0
- Fix wrong modify QP parameters
- Align to upstream kernel changes

* Sun Oct 11 2020 Gal Pressman <galpress@amazon.com> - 1.10.2
- Fix possible use of uninitialized variable in GDR error flow

* Wed Sep 30 2020 Gal Pressman <galpress@amazon.com> - 1.10.1
- Misc fixes to GDR package installation
- Expose messages and RDMA read statistics
- Fix an error when registering MR on older kernels

* Wed Sep 09 2020 Gal Pressman <galpress@amazon.com> - 1.10.0
- SRD RNR retry support
- Remove a wrong warning triggered by GDR cleanup
- Fix GDR driver compilation on Ubuntu 16.04
- Add GDR driver packaging (rpm/deb)

* Mon Aug 03 2020 Gal Pressman <galpress@amazon.com> - 1.9.0
- Adapt to upstream kernel
- Refactor locking scheme in GDR flows
- Report create CQ error counter
- Report mmap error counter
- Report admin commands error counter
- Add a sysfs indication to GDR drivers
- Add 0xefa1 device support

* Wed Feb 26 2020 Gal Pressman <galpress@amazon.com> - 1.6.0
- Add NVIDIA GPUDirect RDMA support
- Add a configure script to the compilation process and use it to test for kernel funcionality
- Change directory structure, the source files are now located under src/
- Fix compilation on certain kernels of SuSE15.1
- Backport changes from upstream kernel

* Thu Jan 02 2020 Gal Pressman <galpress@amazon.com> - 1.5.1
- Fix SuSE ioctl flow backport

* Wed Dec 11 2019 Gal Pressman <galpress@amazon.com> - 1.5.0
- RDMA read support
- Make ib_uverbs a soft dependency
- Fix ioctl flows on older kernels
- SuSE 15.1 support

* Fri Sep 20 2019 Gal Pressman <galpress@amazon.com> - 1.4.1
- Fix Incorrect error print
- Add support for CentOS 7.7

* Thu Sep 5 2019 Gal Pressman <galpress@amazon.com> - 1.4.0
- Expose device statistics
- Rate limit admin queue error prints
- Properly assign err variable on everbs device creation failure

* Thu Aug 8 2019 Gal Pressman <galpress@amazon.com> - 1.3.1
- Fix build issue in debian/rules file
- Fix kcompat issue (usage before include)

* Sun Jul 7 2019 Gal Pressman <galpress@amazon.com> - 1.3.0
- Align to the driver that was merged upstream
- Fix a bug where failed functions would return success return value
- Fix modify QP udata check backport
- Fix locking issues in mmap flow
- Add Debian packaging files

* Tue May 7 2019 Jie Zhang <zhngaj@amazon.com> - 0.9.2
- Add a separate configuration file to load ib_uverbs as a soft dependency module
  on non-systemd based systems

* Tue Apr 2 2019 Robert Wespetal <wesper@amazon.com> - 0.9.1
- Update EFA post install script to install module for all kernels

* Fri Mar 8 2019 Robert Wespetal <wesper@amazon.com> - 0.9.0
- initial build for RHEL
