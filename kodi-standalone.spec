%global _missing_build_ids_terminate_build  0

%define source_date_epoch_from_changelog    0
%define __os_install_post                   %{nil}
%define debug_package                       %{nil}

Name:           kodi-standalone
Version:        1.0
Release:        1%{?dist}
License:        MIT
Summary:        Install Kodi as a standalone application

Requires:       flatpak

Source0:        kodi-sysusers.cs9.conf
Source1:        99-kodi.rules
Source2:        kodi-wayland.service
Source3:        kodi-standalone.env
Source4:        kodi-standalone.tmpfiles

BuildRequires:  systemd-rpm-macros

%description
Install Kodi as a standalone application on different RPM based distros.
Centos Stream 9 is the first target.

%prep
%setup -c -T

%build

# Create a preset file to start opens.
cat > kodi-standalone.preset << STOP
enable kodi-standalone.service
STOP


%install
echo rm -rf %{buildroot}

# install kodi flatpak
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub tv.kodi.Kodi

%{__install} -d %{buildroot}%{_sysconfdir}/kodi

%{__install} -Dp %{SOURCE0}             %{buildroot}%{_sysusersdir}/kodi-sysusers.conf
%{__install} -Dp %{SOURCE1}             %{buildroot}%{_udevrulesdir}/99-kodi.rules
%{__install} -Dp %{SOURCE2}             %{buildroot}%{_unitdir}/kodi-wayland.service
%{__install} -Dp %{SOURCE3}             %{buildroot}%{_sysconfdir}/kodi/kodi-standalone
%{__install} -Dp %{SOURCE4}             %{buildroot}%{_tmpfilesdir}/kodi-standalone.conf

# The standard display mangers are enabled via:
# /usr/lib/systemd/system-preset/85-display-manager.preset
#
# We need to enable kodi before them.
%{__install} -Dp kodi-standalone.preset %{buildroot}%{_presetdir}/84-kodi-standalone.preset

%files
%defattr(644, root, root, 755)

%dir %{_sysconfdir}/kodi

%{_sysusersdir}/kodi-sysusers.conf
%{_udevrulesdir}/99-kodi.rules
%{_unitdir}/kodi-wayland.service

%config %{_sysconfdir}/kodi/kodi-standalone


%pre
%systemd_pre kodi-wayland.service

%post
%systemd_post kodi-wayland.service

%preun
%systemd_preun kodi-wayland.service

%postun
%systemd_postun kodi-wayland.service

%changelog