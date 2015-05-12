%global openjfx_version 8u45-b13

Name:		java-1.8.0-openjfx
Version:	8u45_b13
Release:	1%{?dist}
Summary:	OpenJFX runtime libraries and documentation
Group:		Development/Languages
License:	GPL with the class path exception
URL:		https://wiki.openjdk.java.net/dashboard.action

# hg clone http://hg.openjdk.java.net/openjfx/8u-dev/rt %{name}-%{version} -r %{openjfx_version}
## find openjfx -name .hg* -exec rm -rf '{}' \;
# tar --exclude ".hg*" -cJf %{name}-%{version}.tar.xz %{name}-%{version}
Source0: %{name}-%{version}.tar.xz
Source1: http://services.gradle.org/distributions/gradle-1.8-bin.zip

BuildRequires:	java-1.8.0-openjdk java-1.8.0-openjdk-devel mercurial bison flex gperf ksh pkgconfig libpng12-devel libjpeg-devel libxml2-devel libxslt-devel systemd-devel glib2-devel gtk2-devel libXtst-devel pango-devel freetype-devel
Requires:	java-1.8.0-openjdk

%description
OpenJFX is an open source, next generation client application platform for desktop and embedded systems based on JavaSE. It is a collaborative effort by many individuals and companies with the goal of producing a modern, efficient, and fully featured toolkit for developing rich client applications. This is the open source project where we develop JavaFX.

%global openjdk8_version %(rpm -q java-1.8.0-openjdk)
%global openjdk8_install_dir %{buildroot}/usr/lib/jvm/%{openjdk8_version}

# There is no need for a debug package (for now)
%define debug_packages  %{nil}

%prep
rpm -q %{name} && echo "You need to uninstall the previously built openjfx package before proceeding (this sounds stupid, but it actually makes sense!)"
chmod -R +x %{_builddir}
[ -d %{buildroot} ] && chmod -R +x %{buildroot}
%setup -T -q -n gradle-1.8 -b 1
%setup -q
cp %{openjfx_srcdir}/gradle.properties.template %{openjfx_srcdir}/gradle.properties
sed -i "s|#BUILD_JAVADOC = true|BUILD_JAVADOC = true|" %{openjfx_srcdir}/gradle.properties
sed -i "s|#NUM_COMPILE_THREADS = 12|NUM_COMPILE_THREADS = 8|" %{openjfx_srcdir}/gradle.properties

%build
%{_builddir}/gradle-1.8/bin/gradle

%install
%global sdkdir build/sdk
chmod -R +x %{sdkdir}
mkdir -p %{openjdk8_install_dir}/{lib,bin,man/man1,jre/lib/ext,jre/lib/amd64}

# JDK libraries
install -m644 %{sdkdir}/lib/* %{openjdk8_install_dir}/lib/
install -m755 %{sdkdir}/bin/* %{openjdk8_install_dir}/bin/
install -m644 %{sdkdir}/man/man1/* %{openjdk8_install_dir}/man/man1/

# JRE libraries
install -m644 %{sdkdir}/rt/lib/ext/* %{openjdk8_install_dir}/jre/lib/ext/
install -m644 %{sdkdir}/rt/lib/amd64/* %{openjdk8_install_dir}/jre/lib/amd64/

%files
%defattr(-,root,root,-)
%doc build/javadoc
/usr/lib/jvm/%{openjdk8_version}/lib/*
/usr/lib/jvm/%{openjdk8_version}/bin/*
/usr/lib/jvm/%{openjdk8_version}/man/man1/*
/usr/lib/jvm/%{openjdk8_version}/jre/lib/*
