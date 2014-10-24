%define origname ch-server
%define name ch-server
%define version 0.002
%define release 1

Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
Summary: small, simple web server for when that's what's needed

Group: Server Platform
License: MIT ( http://opensource.org/licenses/mit-license.html )
URL: https://duck.cpanel.net/c-stith-s-repos/ch-server
Source: https://duck.cpanel.net/c-stith-s-repos/ch-server/blobs/master/ch-server.tar.gz
Source1: ch-server.tar.gz

Packager: Christopher E. Stith <chris.stith@cpanel.net>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
BuildArch: noarch
Requires: /usr/sbin/useradd, /usr/sbin/groupadd, /sbin/chkconfig
Requires: perl-Net-Server
Requires: perl-JSON
Provides: %{origname} = %{version}-%{release}, %{name} = %{version}-%{release}

%description
ch-server is a small, simple web server.

It supports CGI programs each at an individually configured URI and serving of static files from a single document root with no virtual hosts.

It is intended to be suitable for web-accessible service health check scripts and other quite targeted cases on systems which would not otherwise have a web server installed.

%prep
%setup -q

%build

%install
%{__rm} -rf %{buildroot}
install -d 0755 %{buildroot}
install -d 0755 %{buildroot}/%{_bindir}
install -d 0755 %{buildroot}/%{_mandir}
install -d 0755 %{buildroot}/%{_mandir}/man1
install -d 0755 %{buildroot}/%{_sysconfdir}
install -d 0755 %{buildroot}/%{_sysconfdir}/init.d
install -d 0755 %{buildroot}/%{_sysconfdir}/%{name}
install -d 0755 %{_builddir}/%{name}-%{version}
install -m 0755 %{_builddir}/%{name}-%{version}/ch-server			%{buildroot}/%{_bindir}/ch-server
install -m 0755 %{_builddir}/%{name}-%{version}/etc/init.d/ch-server       	%{buildroot}/%{_sysconfdir}/init.d/ch-server
install -m 0644 %{_builddir}/%{name}-%{version}/etc/%{name}/mime           	%{buildroot}/%{_sysconfdir}/%{name}/mime
install -m 0644 %{_builddir}/%{name}-%{version}/etc/%{name}/conf           	%{buildroot}/%{_sysconfdir}/%{name}/conf
install -m 0644 %{_builddir}/%{name}-%{version}/man/ch-server.1.gz		%{buildroot}/%{_mandir}/man1/ch-server.1.gz

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS CHANGES COPYING README
%{_bindir}/ch-server
%{_sysconfdir}/init.d/ch-server
%config(noreplace) %{_sysconfdir}/%{name}/mime
%config(noreplace) %{_sysconfdir}/%{name}/conf
%{_mandir}/man1/ch-server.1.gz

%pre
if [ "$1" = "1" ]; then #If this is a fresh install . . .
  /usr/sbin/groupadd -r ch-server    2> /dev/null || :
  /usr/sbin/useradd -c "ch-server user" \
    -s /sbin/nologin -r -d /home/ch-server -g ch-server ch-server 2> /dev/null || :
else
  if [ "$1" = "0" ]; then #If this is the last RPM removed . . .
    service ch-server stop
    /sbin/chkconfig --del ch-server
  fi
fi

%post
if [ "$1" = "1" ]; then #if this is a fresh install . . .
  #Configure new services
  /sbin/chkconfig --add ch-server
  /sbin/chkconfig --level 345 on
fi

%changelog
* Wed Oct 29 2014 Christopher E. Stith <chris.stith@cpanel.net> - 0.002
- Removed Data::Dumper used during development
- Changed the unshift in the config file processing to push

* Fri Oct 24 2014 Christopher E. Stith <chris.stith@cpanel.net> - 0.001
- Initial build

