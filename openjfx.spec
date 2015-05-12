%global openjfx_version 8u45-b13

Name:		openjfx
Version:	8u45_b13
Release:	1%{?dist}
Summary:	OpenJFX runtime libraries and documentation
Group:		Development/Languages
License:	GPL with the class path exception
URL:		https://wiki.openjdk.java.net/dashboard.action

# hg clone http://hg.openjdk.java.net/openjfx/8u-dev/rt openjfx-%{version} -r %{openjfx_version}
## find openjfx -name .hg* -exec rm -rf '{}' \;
# tar cJf --exclude ".hg*" openjfx-%{version}.tar.xz openjfx
Source0: openjfx-%{version}.tar.xz
Source1: http://services.gradle.org/distributions/gradle-1.8-bin.zip

BuildRequires:	java-1.8.0-openjdk java-1.8.0-openjdk-devel mercurial bison flex gperf ksh pkgconfig libpng12-devel libjpeg-devel libxml2-devel libxslt-devel systemd-devel glib2-devel gtk2-devel libXtst-devel pango-devel freetype-devel
Requires:	java-1.8.0-openjdk

%description
OpenJFX is an open source, next generation client application platform for desktop and embedded systems based on JavaSE. It is a collaborative effort by many individuals and companies with the goal of producing a modern, efficient, and fully featured toolkit for developing rich client applications. This is the open source project where we develop JavaFX.

%global openjdk8_version %(rpm -q java-1.8.0-openjdk --queryformat '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}')
%global openjdk8_dir %{buildroot}/usr/lib/jvm/%{openjdk8_version}
%global sdkdir %{_builddir}/%{name}-%{version}/build/sdk
# There is no need for a debug package (for now)
%define debug_packages  %{nil}

%prep
chmod -R +x %{_builddir}
[ -d %{buildroot} ] && chmod -R +x %{buildroot}
%setup -T -q -n gradle-1.8 -b 1
%setup -q

%build
%{_builddir}/gradle-1.8/bin/gradle

%install
chmod -R +x %{sdkdir}
mkdir -p %{openjdk8_dir}/{lib,bin,man/man1,jre/lib/ext,jre/lib/amd64}
# JDK libraries
install -m644 %{sdkdir}/lib/* %{openjdk8_dir}/lib/
install -m755 %{sdkdir}/bin/* %{openjdk8_dir}/bin/
install -m644 %{sdkdir}/man/man1/* %{openjdk8_dir}/man/man1/
# JRE libraries
install -m644 %{sdkdir}/rt/lib/ext/* %{openjdk8_dir}/jre/lib/ext/
install -m644 %{sdkdir}/rt/lib/amd64/* %{openjdk8_dir}/jre/lib/amd64/

%files
%doc
/usr/lib/jvm/%{openjdk8_version}/lib/*
/usr/lib/jvm/%{openjdk8_version}/bin/*
/usr/lib/jvm/%{openjdk8_version}/man/man1/*
/usr/lib/jvm/%{openjdk8_version}/jre/lib/*
