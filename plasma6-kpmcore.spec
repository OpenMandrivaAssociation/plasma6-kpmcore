#define git 20240218
%define gitbranch release/24.02
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")
%define major 13
%define libname %mklibname %{name}-kf6
%define devname %mklibname %{name}-kf6 -d
%define stable %([ "$(echo %{version} |cut -d. -f3)" -ge 70 ] && echo -n un; echo -n stable)

Summary:	Library for managing partitions
Name:		plasma6-kpmcore
Version:	25.04.0
Release:	%{?git:%{?git:0.%{git}.}0.%{git}.}2
License:	GPLv3
Group:		System/Libraries
Url:		https://www.kde.org/
%if 0%{?git:1}
%if 0%{?git:1}
Source0:	https://invent.kde.org/system/kpmcore/-/archive/%{gitbranch}/kpmcore-%{gitbranchd}.tar.bz2#/kpmcore-%{git}.tar.bz2
%else
Source0:	https://invent.kde.org/system/kpmcore/-/archive/master/kpmcore-master.tar.bz2#/kpmcore-%{git}.tar.bz2
%endif
%else
%if 0%{?git:1}
Source0:	https://invent.kde.org/system/kpmcore/-/archive/%{gitbranch}/kpmcore-%{gitbranchd}.tar.bz2#/kpmcore-%{git}.tar.bz2
%else
Source0:	http://download.kde.org/%{stable}/release-service/%{version}/src/kpmcore-%{version}.tar.xz
%endif
%endif
BuildRequires:	cmake(ECM)
BuildRequires:	pkgconfig(blkid) >= 2.33.2
BuildRequires:	qt6-qtbase-tools
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(KF6I18n)
BuildRequires:	cmake(KF6CoreAddons)
BuildRequires:	cmake(KF6WidgetsAddons)
BuildRequires:	cmake(PolkitQt6-1)
Requires:	%{libname} = %{EVRD}
Requires:	e2fsprogs
Requires:	dosfstools
Requires:	fatresize
Requires:	xfsprogs
Suggests:	jfsutils
Suggests:	reiserfsprogs
Suggests:	ntfs-3g
Requires:	btrfs-progs
Requires:	f2fs-tools
Requires:	gptfdisk
Requires:	exfatprogs
Requires:	lvm2
Requires:	util-linux
Requires:	systemd
Requires:	coreutils
Requires:	smartmontools
Requires:	mdadm
Requires:	udftools

%patchlist
# Make calamares Great Again
# Without this, calamares crashes on startup with an unpartitioned disk
revert-8b4b5c8.patch

%description
Library for managing partitions.
Common code for KDE Partition Manager and other projects.

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries

%description -n %{libname}
Main library for %{name}.

%package -n %{devname}
Summary:	Development library for %{name}
Group:		Development/KDE and Qt
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Development library for %{name}.

%prep
%autosetup -p1 -n kpmcore-%{?git:%{gitbranchd}}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DQT_MAJOR_VERSION=6 \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja -C build

%install
%ninja_install -C build

%find_lang %{name} --all-name

%files -f %{name}.lang
%{_qtdir}/plugins/kpmcore
%{_libdir}/libexec/kpmcore_externalcommand
%{_datadir}/dbus-1/system-services/org.kde.kpmcore.helperinterface.service
%{_datadir}/dbus-1/system.d/org.kde.kpmcore.helperinterface.conf
%{_datadir}/polkit-1/actions/org.kde.kpmcore.externalcommand.policy

%files -n %{libname}
%{_libdir}/libkpmcore.so.%{major}*
%{_libdir}/libkpmcore.so.%(echo %{version}|cut -d. -f1).*

%files -n %{devname}
%{_includedir}/kpmcore
%{_libdir}/libkpmcore.so
%{_libdir}/cmake/KPMcore
