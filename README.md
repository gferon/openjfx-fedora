# README

## Test without Mock

### Clone repo

```
git clone git@github.com:gferon/openjfx-fedora.git rpmbuild
```

### Install dependencies

```
dnf install @development-tools fedora-packager rpmdevtools
rpmdev-setuptree
dnf builddep SPECS/openjfx.spec
```

### Download sources

```
spectool -g -R SPECS/openjfx.spec
```

### Launch the build

```
rpmbuild -ba SPECS/openjfx.spec
```
